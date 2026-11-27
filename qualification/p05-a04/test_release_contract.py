"""Offline synthetic contracts; never contact or publish to registries."""
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"scripts/release"))
import registry_contract as c

V="2.0.1"
N,W,S=c.names(V)
BODY={n:n.encode() for n in (N,W,S)}
D={n:c.digest(b) for n,b in BODY.items()}
ENV={"GITHUB_SHA":"a"*40,"GITHUB_REF":"refs/tags/v"+V,"GITHUB_RUN_ID":"123","GITHUB_RUN_ATTEMPT":"1"}
NURL=f"https://registry.npmjs.org/kron-otp/-/{N}"
PURL={n:f"https://files.pythonhosted.org/packages/test/{n}" for n in (W,S)}

def fake(npm=True, py=(W,S), *, npm_status=None, py_status=None, corrupt=None, extra=None, wrong=False, malformed=False):
    def fetch(url,limit=c.META_LIMIT):
        if url==f"https://registry.npmjs.org/kron-otp/{V}":
            if npm_status is not None: return npm_status,b""
            if not npm: return 404,b""
            return 200,json.dumps({"name":"kron-otp","version":"9.9.9" if wrong else V,"dist":{"tarball":NURL,"integrity":"sha512-"+D[N]["sha512"]}}).encode()
        if url==f"https://pypi.org/pypi/kron-otp/{V}/json":
            if py_status is not None: return py_status,b""
            if not py: return 404,b""
            if malformed: return 200,b"{"
            rows=[{"filename":n,"url":PURL[n],"digests":{"sha256":D[n]["sha256"]},"yanked":False,"packagetype":"bdist_wheel" if n==W else "sdist"} for n in py]
            if extra: rows.append({"filename":extra})
            return 200,json.dumps({"info":{"name":"kron-otp","version":V},"urls":rows}).encode()
        for n,u in {N:NURL,**PURL}.items():
            if url==u: return 200,b"bad" if corrupt==n else BODY[n]
        raise AssertionError("unexpected URL")
    return fetch

class Contract(unittest.TestCase):
    def state(self,fetch,expected=D):
        return c.classify(c.registry(V,expected,fetch)[0])
    def test_absent(self): self.assertEqual(self.state(fake(False,())),"ALL_ABSENT")
    def test_exact(self):
        states,data,_=c.registry(V,D,fake())
        self.assertEqual(c.classify(states),"FULL_EXACT")
        self.assertEqual(data,BODY)
    def test_npm_only(self): self.assertEqual(self.state(fake(True,())),"PARTIAL")
    def test_wheel_only(self): self.assertEqual(self.state(fake(False,(W,))),"PARTIAL")
    def test_sdist_only(self): self.assertEqual(self.state(fake(False,(S,))),"PARTIAL")
    def test_pypi_only(self): self.assertEqual(self.state(fake(False)),"PARTIAL")
    def test_bad_download(self):
        for n in BODY:
            with self.subTest(n=n): self.assertEqual(self.state(fake(corrupt=n)),"CONFLICT")
    def test_wrong_digest(self):
        other={**D,N:c.digest(b"other")}
        self.assertEqual(self.state(fake(),other),"CONFLICT")
    def test_extra_file(self): self.assertEqual(self.state(fake(extra="extra.whl")),"CONFLICT")
    def test_duplicate_file(self): self.assertEqual(self.state(fake(extra=W)),"CONFLICT")
    def test_wrong_version(self): self.assertEqual(self.state(fake(wrong=True)),"UNKNOWN")
    def test_malformed(self): self.assertEqual(self.state(fake(malformed=True)),"UNKNOWN")
    def test_non404(self):
        for status in (301,401,403,429,500,503):
            with self.subTest(status=status):
                self.assertEqual(self.state(fake(npm_status=status)),"UNKNOWN")
                self.assertEqual(self.state(fake(py_status=status)),"UNKNOWN")
    def test_timeout(self):
        def timeout(*a): raise TimeoutError()
        self.assertEqual(self.state(timeout),"UNKNOWN")
    def test_public_legacy(self): self.assertEqual(self.state(fake(),None),"FULL_EXACT")
    def test_url_guard(self):
        for url in ("http://registry.npmjs.org/x","https://evil.example/x","https://registry.npmjs.org@evil.example/x","https://pypi.org/x?q=secret"):
            with self.assertRaises(ValueError): c.get(url)
    def test_tag_guard(self):
        b=c.binding(V,ENV)
        self.assertTrue(c.publish_allowed(b,"push","a"*40))
        for event in ("pull_request","workflow_dispatch"):
            self.assertFalse(c.publish_allowed(b,event,"a"*40))
        self.assertFalse(c.publish_allowed(b,"push","b"*40))
        self.assertFalse(c.publish_allowed({**b,"attempt":"2"},"push","a"*40))
        self.assertFalse(c.publish_allowed({**b,"ref":"refs/heads/main"},"push","a"*40))
        with self.assertRaises(ValueError): c.binding(V,{**ENV,"GITHUB_REF":"refs/tags/v9.0.0"})
    def test_manifest(self):
        b=c.binding(V,ENV)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            for n,body in BODY.items(): (p/n).write_bytes(body)
            raw=json.dumps({"schema":1,"binding":b,"files":D}).encode()
            (p/"manifest.json").write_bytes(raw)
            h=hashlib.sha256(raw).hexdigest()
            self.assertEqual(c.verify_bundle(p,h,b)["files"],D)
            for key,val in (("sha","b"*40),("ref","refs/heads/main"),("run_id","999"),("attempt","2"),("version","9.9.9")):
                with self.subTest(key=key),self.assertRaises(ValueError): c.verify_bundle(p,h,{**b,key:val})
            with self.assertRaises(ValueError): c.verify_bundle(p,"0"*64,b)
            (p/N).write_bytes(b"tamper")
            with self.assertRaises(ValueError): c.verify_bundle(p,h,b)
            (p/N).write_bytes(BODY[N]); (p/"extra").write_text("x")
            with self.assertRaises(ValueError): c.verify_bundle(p,h,b)
    def test_smoke_gate(self):
        self.assertTrue(c.smoke_allowed("FULL_EXACT","success","success","success"))
        for state in ("PARTIAL","UNKNOWN","ALL_ABSENT","CONFLICT"):
            self.assertFalse(c.smoke_allowed(state,"success","success","success"))
        for i in range(3):
            results=["success"]*3
            for result in ("failure","skipped","cancelled"):
                results[i]=result
                self.assertFalse(c.smoke_allowed("FULL_EXACT",*results))
    def test_single_attempt_twine(self):
        import textwrap
        from types import SimpleNamespace
        from unittest.mock import Mock
        from twine.repository import Repository
        root=Path(__file__).resolve().parents[2]
        text=(root/".github/workflows/release.yml").read_text()
        code=textwrap.dedent(text.split("# BEGIN SINGLE_ATTEMPT_TWINE\n",1)[1].split("# END SINGLE_ATTEMPT_TWINE",1)[0].rstrip())
        package=object()
        response=SimpleNamespace(status_code=500,reason="synthetic server error")
        instance=SimpleNamespace(_upload=Mock(return_value=response),session=Mock())
        def dispatch(args):
            self.assertEqual(args,["upload","--non-interactive","--repository-url","https://upload.pypi.org/legacy/","fake.whl"])
            self.assertIs(Repository.upload(instance,package),response)
            instance._upload.assert_called_once_with(package)
            self.assertEqual(instance.session.mount.call_args.args[1].max_retries.total,0)
            return 0
        with patch("twine.cli.dispatch",side_effect=dispatch),patch.object(Repository,"upload",Repository.upload),patch.object(sys,"argv",["-","fake.whl"]):
            with self.assertRaises(SystemExit) as exc: exec(code,{})
            self.assertEqual(exc.exception.code,0)
    def test_workflow_wiring(self):
        root=Path(__file__).resolve().parents[2]
        release=(root/".github/workflows/release.yml").read_text()
        smoke=(root/".github/workflows/registry-smoke.yml").read_text()
        self.assertEqual(release.count("secrets.NPM_TOKEN"),1)
        self.assertEqual(release.count("secrets.PYPI_API_TOKEN"),1)
        self.assertNotIn("secrets.",smoke)
        self.assertNotIn("skip-existing",release)
        self.assertEqual(release.count("npm publish "),1)
        self.assertEqual(release.count('dispatch(["upload",'),1)
        self.assertIn("--fetch-retries=0",release)
        self.assertEqual(release.count("registry_contract.py publish-verify"),3)
        self.assertIn("needs: [validate, preflight, npm, pypi]",release)
        self.assertIn("always() &&",release)
        self.assertIn("needs: [validate, reconcile]",release)
        self.assertIn("uses: ./.github/workflows/registry-smoke.yml",release)
        self.assertIn("workflow_call:",smoke)
        self.assertIn("github.run_attempt == 1",release)
        self.assertIn("github.event_name == 'push' && github.ref_type == 'tag'",release)

if __name__=="__main__": unittest.main(verbosity=2)
