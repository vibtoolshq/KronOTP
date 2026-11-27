"""Bounded synthetic benchmark; observation only, not production SLA."""
import concurrent.futures
import importlib.metadata as metadata
import json
import os
import pathlib
import platform
import resource
import subprocess
import sys
import time
from unittest.mock import patch

import kron_otp
from kron_otp import KronOTP

KEY = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"
EXPECTED = "287082"
ORIGIN = pathlib.Path(kron_otp.__file__).resolve()
assert ORIGIN.is_relative_to(pathlib.Path(sys.prefix).resolve())
assert metadata.version("kron-otp") == "2.0.0"
clock = time.perf_counter_ns

def generate():
    start = clock()
    with patch("pyotp.totp.time.time", return_value=59):
        value = KronOTP.generate(KEY)
    elapsed = (clock()-start)/1e6
    assert value == EXPECTED, "generate mismatch"
    return elapsed

def verify():
    start = clock()
    with patch("pyotp.totp.time.time", return_value=59):
        ok = KronOTP.verify(KEY, EXPECTED)
    elapsed = (clock()-start)/1e6
    assert ok is True, "verify mismatch"
    return elapsed

def pair():
    generate()
    verify()

def stats(values):
    import math
    assert values and all(math.isfinite(x) and x >= 0 for x in values)
    v = sorted(values)
    return {"n":len(v), **{f"p{p}_ms":v[math.ceil(p*len(v)/100)-1] for p in (50,95,99)}}

def mem():
    rss = int(pathlib.Path("/proc/self/statm").read_text().split()[1])*os.sysconf("SC_PAGE_SIZE")
    return {"rss_bytes":rss, "peak_rss_bytes":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024}

def emit(kind, data):
    print(json.dumps({"kind":kind, **data}), flush=True)

def measured(n):
    start, cpu = clock(), time.process_time()
    g, v = [], []
    for _ in range(n):
        g.append(generate())
        v.append(verify())
    sec = (clock()-start)/1e9
    return {"pairs":n,"operations":n*2,"seconds":sec,"ops_per_sec":n*2/sec,
            "generate":stats(g),"verify":stats(v),"cpu_seconds":time.process_time()-cpu,
            **mem(),"errors":0,"mismatches":0}

def child(mode):
    p = subprocess.run([sys.executable,"-I",__file__,mode],capture_output=True,text=True,timeout=60,check=True)
    return p.stdout.strip()

def sustained():
    start, cpu = clock(), time.process_time()
    end = start+600_000_000_000
    baseline = mem()
    samples = [{"elapsed_s":0,**baseline}]
    next_sample = start+10_000_000_000
    last, n, min_gap = None, 0, float("inf")
    g, v = [], []
    while clock()<end:
        now = clock()
        if now>=next_sample:
            sample = {"elapsed_s":(now-start)/1e9,**mem()}
            samples.append(sample)
            emit("rss_sample",sample)
            next_sample += 10_000_000_000
        if last is not None and now-last<5_000_000:
            time.sleep((5_000_000-(now-last))/1e9)
            continue
        begin = clock()
        if begin>=end:
            break
        if last is not None:
            min_gap = min(min_gap,(begin-last)/1e6)
        last = begin
        a,b = generate(),verify()
        n += 1
        if n%20==0:
            g.append(a)
            v.append(b)
    elapsed = (clock()-start)/1e9
    final = mem()
    samples.append({"elapsed_s":elapsed,**final})
    assert elapsed>=600 and 0<n<=120000 and min_gap>=5, "sustained workload"
    assert len(samples)>=61 and all(b["elapsed_s"]-a["elapsed_s"]<=12 for a,b in zip(samples,samples[1:])), "RSS sampling gap"
    emit("sustained",{"seconds":elapsed,"pairs":n,"operations":2*n,"pairs_per_sec":n/elapsed,
        "min_start_gap_ms":min_gap,"sample_interval_s":10,"samples":len(samples),
        "baseline_rss_bytes":baseline["rss_bytes"],"final_rss_bytes":final["rss_bytes"],
        "rss_delta_bytes":final["rss_bytes"]-baseline["rss_bytes"],**final,
        "cpu_seconds":time.process_time()-cpu,"generate_sample":stats(g),"verify_sample":stats(v),
        "errors":0,"mismatches":0})

def main():
    model=next((x.split(":",1)[1].strip() for x in pathlib.Path("/proc/cpuinfo").read_text().splitlines() if x.startswith("model name")),"unknown")
    emit("environment",{"runtime":platform.python_version(),"platform":platform.platform(),"arch":platform.machine(),
         "cpu":model,"logical_cpus":os.cpu_count(),"total_memory_bytes":os.sysconf("SC_PHYS_PAGES")*os.sysconf("SC_PAGE_SIZE"),
         "image":os.getenv("ImageVersion"),"version":"2.0.0","origin":str(ORIGIN)})
    cold=[]
    for _ in range(20):
        t=clock()
        assert child("cold")=="OK"
        cold.append((clock()-t)/1e6)
    emit("cold",stats(cold))
    for _ in range(500):
        pair()
    emit("warmup",{"operations":1000})
    emit("serial",measured(10000))
    for workers in (1,4,8):
        start=clock()
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            results=[json.loads(x) for x in pool.map(child,["worker"]*workers)]
        sec=(clock()-start)/1e9
        assert all(x["operations"]==2000 and x["errors"]==0 and x["mismatches"]==0 for x in results)
        emit("parallel",{"workers":workers,"operations":workers*2000,"seconds":sec,
             "ops_per_sec":workers*2000/sec,"worker_cpu_seconds":sum(x["cpu_seconds"] for x in results),
             "max_worker_peak_rss_bytes":max(x["peak_rss_bytes"] for x in results),
             "worker_results":results,"errors":0,"mismatches":0})
    sustained()
    emit("complete",{"status":"PASS","errors":0,"mismatches":0})

if __name__=="__main__":
    mode=sys.argv[1] if len(sys.argv)>1 else ""
    if mode=="cold":
        pair()
        print("OK")
    elif mode=="worker":
        print(json.dumps(measured(1000)))
    else:
        main()
