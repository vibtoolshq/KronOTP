"""KronOTP release artifact and public registry contract. No publishing or credentials."""
import argparse
import base64
import csv
import email
import hashlib
import gzip
import importlib.metadata
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import subprocess
import tarfile
import tempfile
import tomllib
import urllib.error
import urllib.parse
import urllib.request
import zipfile

LIMIT = 2_000_000
META_LIMIT = 1_000_000
PACKAGE = "kron-otp"
VERSION = r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"

def require(condition, message):
    if not condition:
        raise ValueError(message)

def names(v):
    require(isinstance(v,str) and re.fullmatch(VERSION,v), "stable version required")
    return (f"kron-otp-{v}.tgz", f"kron_otp-{v}-py3-none-any.whl", f"kron_otp-{v}.tar.gz")

def digest(data):
    return {"sha256":hashlib.sha256(data).hexdigest(),
            "sha512":base64.b64encode(hashlib.sha512(data).digest()).decode(),
            "size":len(data)}

def source_version(root=Path(".")):
    js=json.loads((root/"javascript/package.json").read_text())
    py=tomllib.loads((root/"python/pyproject.toml").read_text())["project"]
    require(js["name"]==py["name"]==PACKAGE and js["version"]==py["version"] and not js.get("private"),"package identity")
    names(js["version"])
    return js["version"]

def binding(v, env=os.environ):
    names(v)
    sha, ref, run, attempt = (env[k] for k in ("GITHUB_SHA","GITHUB_REF","GITHUB_RUN_ID","GITHUB_RUN_ATTEMPT"))
    require(re.fullmatch("[a-f0-9]{40}",sha) and run.isdecimal() and attempt.isdecimal(),"run identity")
    require(ref.startswith(("refs/heads/","refs/tags/","refs/pull/")),"ref identity")
    if ref.startswith("refs/tags/"):
        require(ref=="refs/tags/v"+v,"tag/version mismatch")
    return {"version":v,"sha":sha,"ref":ref,"run_id":run,"attempt":attempt}

def publish_allowed(b, event, main_sha):
    return (event=="push" and b["ref"]=="refs/tags/v"+b["version"]
            and b["attempt"]=="1" and b["sha"]==main_sha)

def read_file(p):
    require(p.is_file() and not p.is_symlink() and 0<p.stat().st_size<=LIMIT,"artifact file")
    return p.read_bytes()

def tar_files(data, root, allowed, required):
    out={}; seen=set()
    dirs={root}
    for p in allowed:
        dirs.update(str(x) for x in PurePosixPath(root,p).parents if str(x)!=".")
    with tarfile.open(fileobj=io.BytesIO(data),mode="r:gz") as t:
        for m in t:
            p=PurePosixPath(m.name)
            require(len(seen)<80 and m.name not in seen and not p.is_absolute()
                    and ".." not in p.parts and "\\" not in m.name,"unsafe tar path")
            seen.add(m.name)
            if m.isdir():
                require(m.name in dirs,"unexpected directory")
                continue
            require(m.isfile() and 0<=m.size<=100_000 and p.parts[0]==root,"unsafe tar member")
            rel=str(PurePosixPath(*p.parts[1:]))
            require(rel in allowed and rel not in out,"unexpected archive file")
            out[rel]=t.extractfile(m).read()
            require(sum(map(len,out.values()))<=500_000,"archive size")
    require(required<=set(out)<=allowed,"archive file set")
    return out

def metadata(data,v):
    m=email.message_from_bytes(data)
    require(m["Name"]==PACKAGE and m["Version"]==v and m["Requires-Python"]==">=3.10","Python metadata")

def inspect_sdist(data,v,source):
    tracked={"LICENSE","README.md","pyproject.toml","MANIFEST.in","src/kron_otp.py",
             "tests/test_kron_otp.py","tests/totp_vectors.json"}
    optional={"src/__init__.py","tests/__init__.py"}
    egg="src/kron_otp.egg-info/"
    generated={"PKG-INFO","setup.cfg"}|{egg+x for x in ("PKG-INFO","SOURCES.txt","dependency_links.txt","requires.txt","top_level.txt")}
    f=tar_files(data,"kron_otp-"+v,tracked|optional|generated,tracked|generated)
    for p in tracked|(optional&f.keys()):
        require(f[p]==(source/p).read_bytes(),"sdist source mismatch: "+p)
    metadata(f["PKG-INFO"],v); metadata(f[egg+"PKG-INFO"],v)
    vectors=json.loads(f["tests/totp_vectors.json"])
    require(len(vectors["rfc6238_sha1_6digits"])==6 and len(vectors["cross_language"])==80,"vector count")
    return f

def inspect_wheel(data,v,source):
    prefix="kron_otp-"+v+".dist-info/"
    allowed={"kron_otp.py",prefix+"licenses/LICENSE"}|{prefix+x for x in ("METADATA","WHEEL","RECORD","top_level.txt")}
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        infos=z.infolist()
        require(len(infos)==len(allowed) and {x.filename for x in infos}==allowed,"wheel file set")
        require(all(not x.is_dir() and stat.S_IFMT(x.external_attr>>16) in (0,stat.S_IFREG) and x.file_size<=100_000 for x in infos),"wheel member")
        f={x.filename:z.read(x) for x in infos}
    metadata(f[prefix+"METADATA"],v)
    require(f["kron_otp.py"]==(source/"src/kron_otp.py").read_bytes() and f[prefix+"licenses/LICENSE"]==(source/"LICENSE").read_bytes(),"wheel source mismatch")
    rows=list(csv.reader(io.StringIO(f[prefix+"RECORD"].decode())))
    require(len(rows)==len(f) and {r[0] for r in rows}==allowed,"RECORD set")
    for name,d,s in rows:
        if name==prefix+"RECORD":
            require(not d and not s,"RECORD self")
        else:
            require(d=="sha256="+base64.urlsafe_b64encode(hashlib.sha256(f[name]).digest()).decode().rstrip("=") and int(s)==len(f[name]),"RECORD mismatch")

def verify_toolchain():
    require(sys.version_info[:3]==(3,12,16),"controlled Python version")
    require(sys.platform=="linux" and os.uname().machine=="x86_64","controlled platform")
    expected={}
    for line in Path("scripts/release/requirements-build.lock").read_text().splitlines():
        if line and not line.startswith("#"):
            name,version=line.split()[0].split("==")
            expected[name]=version
    actual={re.sub(r"[-_.]+","-",d.metadata["Name"].lower()):d.version
            for d in importlib.metadata.distributions()}
    require(len(expected)==50 and actual==expected,"locked tool graph mismatch")
    subprocess.run([sys.executable,"-m","pip","check"],check=True)
    print(json.dumps({"LOCKED_TOOLCHAIN":actual},sort_keys=True))

def canonical_sdist(path,root,files,epoch):
    """Normalize archive headers/order, preserving every validated member byte."""
    dirs={root}
    for name in files:
        dirs.update(str(p) for p in PurePosixPath(root,name).parents if str(p)!=".")
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="",mode="wb",fileobj=raw,mtime=epoch,compresslevel=9) as compressed:
            with tarfile.open(fileobj=compressed,mode="w",format=tarfile.PAX_FORMAT) as t:
                for name in sorted(dirs):
                    info=tarfile.TarInfo(name); info.type=tarfile.DIRTYPE
                    info.mode=0o755; info.mtime=epoch
                    t.addfile(info)
                for name,body in sorted(files.items()):
                    info=tarfile.TarInfo(root+"/"+name)
                    info.mode=0o644; info.mtime=epoch; info.size=len(body)
                    t.addfile(info,io.BytesIO(body))

def build(bundle):
    verify_toolchain()
    require(subprocess.check_output(["node","--version"],text=True).strip()=="v24.22.3","controlled Node version")
    require(subprocess.check_output(["npm","--version"],text=True).strip()=="11.19.1","controlled npm version")
    epoch=int(subprocess.check_output(["git","show","-s","--format=%ct","HEAD"],text=True).strip())
    require(315532800<=epoch<4354819200,"archive timestamp range")
    env={**os.environ,"SOURCE_DATE_EPOCH":str(epoch),"PYTHONHASHSEED":"0","TZ":"UTC","LC_ALL":"C.UTF-8","PIP_NO_INDEX":"1"}
    os.umask(0o022)
    print("SOURCE_DATE_EPOCH="+str(epoch))
    v=source_version()
    b=binding(v)
    require(subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()==b["sha"],"checkout SHA")
    bundle=bundle.resolve(); bundle.mkdir()
    npm,wheel,sdist=names(v)
    with tempfile.TemporaryDirectory(prefix="kronotp-build-") as tmp:
        src=Path(tmp)/"input"; src.mkdir()
        archive=subprocess.check_output(["git","archive","HEAD","javascript","python"])
        with tarfile.open(fileobj=io.BytesIO(archive)) as t:
            t.extractall(src,filter="data")
        subprocess.run(["npm","pack","--ignore-scripts","--pack-destination",str(bundle)],cwd=src/"javascript",check=True,env=env)
        allowed={"src/kron-otp.js","README.md","LICENSE","package.json"}
        f=tar_files(read_file(bundle/npm),"package",allowed,allowed)
        require(all(f[p]==(src/"javascript"/p).read_bytes() for p in allowed),"npm source mismatch")
        js=json.loads(f["package.json"])
        require(js["name"]==PACKAGE and js["version"]==v,"npm identity")
        subprocess.run([sys.executable,"-m","build","--no-isolation","--sdist","--outdir",str(bundle),str(src/"python")],check=True,env=env)
        f=inspect_sdist(read_file(bundle/sdist),v,src/"python")
        canonical_sdist(bundle/sdist,"kron_otp-"+v,f,epoch)
        require(inspect_sdist(read_file(bundle/sdist),v,src/"python")==f,"canonical sdist content drift")
        extracted=Path(tmp)/"sdist"; extracted.mkdir()
        for p,data in f.items():
            dest=extracted/p; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(data); os.chmod(dest,0o644); os.utime(dest,(epoch,epoch))
        subprocess.run([sys.executable,"-m","build","--no-isolation","--wheel","--outdir",str(bundle),str(extracted)],check=True,env=env)
        inspect_wheel(read_file(bundle/wheel),v,src/"python")
        subprocess.run([sys.executable,"-m","twine","check","--strict",str(bundle/wheel),str(bundle/sdist)],check=True,env=env)
    require({p.name for p in bundle.iterdir()}==set(names(v)),"bundle file set")
    m={"schema":1,"binding":b,"files":{n:digest(read_file(bundle/n)) for n in names(v)}}
    raw=json.dumps(m,sort_keys=True,separators=(",",":")).encode()
    (bundle/"manifest.json").write_bytes(raw)
    sha=hashlib.sha256(raw).hexdigest()
    print(json.dumps({"BUILD_ONCE":m,"manifest_sha256":sha},sort_keys=True))
    output=os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output,"a") as f:
            f.write(f"version={v}\nmanifest_sha={sha}\n")
    return sha

def verify_bundle(bundle, expected_sha, expected_binding):
    raw=read_file(bundle/"manifest.json")
    require(re.fullmatch("[a-f0-9]{64}",expected_sha or "") and hashlib.sha256(raw).hexdigest()==expected_sha,"manifest digest")
    m=json.loads(raw)
    require(m["schema"]==1 and m["binding"]==expected_binding,"manifest binding")
    expected=set(names(expected_binding["version"]))
    require(set(m["files"])==expected and {p.name for p in bundle.iterdir()}==expected|{"manifest.json"},"manifest file set")
    for n in expected:
        require(digest(read_file(bundle/n))==m["files"][n],"artifact digest: "+n)
    return m

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):
        return None

def get(url, limit=META_LIMIT):
    """Only explicit public GET; no credentials, redirects or retries."""
    u=urllib.parse.urlsplit(url)
    require(u.scheme=="https" and u.netloc in {"registry.npmjs.org","pypi.org","files.pythonhosted.org"}
            and not u.query and not u.fragment,"registry URL")
    req=urllib.request.Request(url,headers={"User-Agent":"KronOTP-release-contract/1","Accept":"*/*","Cache-Control":"no-cache"})
    try:
        with urllib.request.build_opener(NoRedirect()).open(req,timeout=15) as resp:
            require(resp.status==200,"unexpected HTTP status")
            data=resp.read(limit+1)
            require(0<len(data)<=limit,"response size")
            return 200,data
    except urllib.error.HTTPError as exc:
        return exc.code,b""

def registry(v, expected=None, fetch=get):
    """Map each exact expected file to absent/match/conflict/unknown; actual bytes only on verified match."""
    npm,wheel,sdist=names(v)
    states={n:"unknown" for n in names(v)}; data={}; provenance={"observed_digests":{}}
    def compare(n,url,algo,wanted):
        try:
            status,body=fetch(url,LIMIT)
            require(status==200 and 0<len(body)<=LIMIT,"artifact unavailable")
            actual=digest(body)
            provenance["observed_digests"][n]=actual
            if actual[algo]!=wanted or (expected is not None and actual!=expected[n]):
                states[n]="conflict"
            else:
                states[n]="match"; data[n]=body
        except (OSError,ValueError,TypeError,KeyError):
            states[n]="unknown"
    try:
        status,raw=fetch(f"https://registry.npmjs.org/{PACKAGE}/{v}")
        if status==404:
            states[npm]="absent"
        elif status==200:
            j=json.loads(raw); d=j["dist"]
            require(j["name"]==PACKAGE and j["version"]==v,"npm metadata identity")
            require(d["tarball"]==f"https://registry.npmjs.org/{PACKAGE}/-/{npm}","npm tarball URL")
            integrity=d["integrity"]
            require(isinstance(integrity,str) and integrity.startswith("sha512-") and len(base64.b64decode(integrity[7:],validate=True))==64,"npm integrity")
            provenance["npm_metadata_sha512"]=integrity[7:]
            provenance["npm_attestations_present"]=bool(d.get("attestations"))
            if expected is not None and integrity[7:]!=expected[npm]["sha512"]:
                states[npm]="conflict"
            else:
                compare(npm,d["tarball"],"sha512",integrity[7:])
    except (OSError,ValueError,TypeError,KeyError):
        states[npm]="unknown"
    try:
        status,raw=fetch(f"https://pypi.org/pypi/{PACKAGE}/{v}/json")
        if status==404:
            states[wheel]=states[sdist]="absent"
        elif status==200:
            j=json.loads(raw)
            require(j["info"]["name"]==PACKAGE and j["info"]["version"]==v,"PyPI metadata identity")
            files=j["urls"]
            require(isinstance(files,list) and len(files)>0,"empty PyPI release")
            filenames=[x["filename"] for x in files]
            if len(filenames)!=len(set(filenames)) or not set(filenames)<={wheel,sdist}:
                states[wheel]=states[sdist]="conflict"
            else:
                for n in (wheel,sdist):
                    if n not in filenames:
                        states[n]="absent"; continue
                    f=files[filenames.index(n)]
                    u=urllib.parse.urlsplit(f["url"])
                    require(u.scheme=="https" and u.netloc=="files.pythonhosted.org" and not u.query and not u.fragment and PurePosixPath(u.path).name==n,"PyPI file URL")
                    h=f["digests"]["sha256"]
                    require(isinstance(h,str) and re.fullmatch("[a-f0-9]{64}",h) and isinstance(f["yanked"],bool),"PyPI file metadata")
                    require(f["packagetype"]==("bdist_wheel" if n==wheel else "sdist"),"PyPI package type")
                    provenance.setdefault("pypi_metadata_sha256",{})[n]=h
                    if f["yanked"] or (expected is not None and h!=expected[n]["sha256"]):
                        states[n]="conflict"
                    else:
                        compare(n,f["url"],"sha256",h)
    except (OSError,ValueError,TypeError,KeyError):
        states[wheel]=states[sdist]="unknown"
        data.pop(wheel,None); data.pop(sdist,None)
    return states,data,provenance

def classify(states):
    values=set(states.values())
    if "unknown" in values: return "UNKNOWN"
    if "conflict" in values: return "CONFLICT"
    if values=={"absent"}: return "ALL_ABSENT"
    if values=={"match"}: return "FULL_EXACT"
    return "PARTIAL"

def smoke_allowed(state,preflight,npm,pypi):
    return state=="FULL_EXACT" and preflight==npm==pypi=="success"

def main():
    p=argparse.ArgumentParser()
    p.add_argument("command",choices=["build","verify","publish-verify","preflight","reconcile","smoke"])
    p.add_argument("--bundle",type=Path)
    p.add_argument("--manifest-sha")
    p.add_argument("--version")
    p.add_argument("--main-sha")
    p.add_argument("--destination",type=Path)
    p.add_argument("--preflight-result")
    p.add_argument("--npm-result")
    p.add_argument("--pypi-result")
    a=p.parse_args()
    if a.command=="build":
        build(a.bundle); return
    v=a.version or source_version()
    names(v)
    m=None
    if a.bundle is not None:
        require(source_version()==v,"source version mismatch")
        b=binding(v)
        require(subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()==b["sha"],"checkout SHA")
        m=verify_bundle(a.bundle,a.manifest_sha,b)
    if a.command in ("verify","publish-verify"):
        require(m is not None,"bundle required")
        if a.command=="publish-verify":
            require(publish_allowed(m["binding"],os.environ["GITHUB_EVENT_NAME"],a.main_sha),"publication guard")
        print("BUNDLE_VERIFIED"); return
    if a.command in ("preflight","reconcile"):
        require(m is not None,"bundle required")
    states, data, provenance=registry(v,m["files"] if m else None)
    state=classify(states)
    print(json.dumps({"REGISTRY_STATE":state,"version":v,"files":states,"provenance":provenance},sort_keys=True))
    if a.command=="preflight":
        require(state=="ALL_ABSENT","existing or uncertain registry state: stop; no publish")
    elif a.command=="reconcile":
        require(smoke_allowed(state,a.preflight_result,a.npm_result,a.pypi_result),"publication incomplete or publisher gate failed; preserve artifacts and obtain operator approval")
    elif a.command=="smoke":
        require(state=="FULL_EXACT","registry smoke requires all exact artifacts")
        a.destination.mkdir()
        for n,body in data.items():
            (a.destination/n).write_bytes(body)
        for n in names(v)[1:]:
            try:
                status,_=get(f"https://pypi.org/integrity/{PACKAGE}/{v}/{n}/provenance")
                print(f"PyPI provenance {n}: HTTP {status}; not cryptographically verified")
            except (OSError,ValueError):
                print(f"PyPI provenance {n}: unavailable; not verified")
        print("REGISTRY_BYTES_VERIFIED")

if __name__=="__main__":
    main()
