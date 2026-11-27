"""Synthetic single-process caller fixture only; not production auth code."""
import hashlib
import importlib.metadata as metadata
import json
import pathlib
import platform
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch

import kron_otp
from kron_otp import KronOTP

A = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"  # public RFC test key
B = "JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP"  # synthetic only
RETENTION, WINDOW = 120, 60

def code(key, t):
    with patch("pyotp.totp.time.time", return_value=t):
        return KronOTP.generate(key)

def match(key, token, t):
    with patch("pyotp.totp.time.time", return_value=t):
        return KronOTP.verify(key, token)

class Caller:
    def __init__(self, limit=3):
        self.limit, self.last = limit, -1
        self.accounts = {"a": A, "b": B}
        self.attempts, self.used = {}, {}
        self.checks = 0
        self.lock = threading.Lock()

    def submit(self, account, token, t):
        # Serialize the entire check/verify/reserve operation, including test clock.
        # Timestamp is trusted synthetic server input, not a client field.
        with self.lock:
            if type(t) is not int or t < 0 or t < self.last:
                return False
            self.last = t
            if account not in self.accounts:
                return False
            attempts = [x for x in self.attempts.get(account, []) if t-x < WINDOW]
            self.attempts[account] = attempts
            if len(attempts) >= self.limit:
                return False
            attempts.append(t)
            self.checks += 1
            if not match(self.accounts[account], token, t):
                return False
            used = self.used.setdefault(account, {})
            for key in [k for k, expiry in used.items() if expiry <= t]:
                del used[key]
            # No matched counter from boolean verify; conservative full horizon.
            fingerprint = hashlib.sha256(token.encode("ascii")).hexdigest()
            if fingerprint in used:
                return False
            used[fingerprint] = t + RETENTION
            return True

def concurrent(caller, token, t):
    gate = threading.Barrier(8, timeout=15)
    def request():
        gate.wait()
        return caller.submit("a", token, t)
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(request) for _ in range(8)]
        return [f.result(timeout=20) for f in futures]

def main():
    origin = pathlib.Path(kron_otp.__file__).resolve()
    assert origin.is_relative_to(pathlib.Path(sys.prefix).resolve()), "package origin"
    assert metadata.version("kron-otp") == "2.0.0"
    report = json.loads(pathlib.Path("install.json").read_text())
    items = [x for x in report["install"] if x["metadata"]["name"].lower().replace("_","-") == "kron-otp"]
    assert len(items) == 1 and items[0]["download_info"]["archive_info"]["hashes"]["sha256"]
    print(json.dumps({"version": metadata.version("kron-otp"), "origin": str(origin),
                      "artifact": items[0]["download_info"], "python": platform.python_version()}))
    count = 0
    def passed(name):
        nonlocal count
        count += 1
        print("PASS " + name)
    current, nxt, other = code(A,59), code(A,89), code(B,59)
    assert current == "287082", "RFC reference mismatch"
    assert nxt != current and other != current, "fixture collision"
    assert match(A,current,59)
    passed("current_rfc")
    assert match(A,nxt,59) and match(A,nxt,119)
    passed("adjacent_window")
    assert not match(A,nxt,120)
    passed("expired")
    assert all(not match(A,bad,59) for bad in (None,123456,"12345","１２３４５６","abcdef"))
    passed("malformed")
    assert not match(B,current,59)
    passed("wrong_account")
    assert match(A,current,59) and match(A,current,59)
    passed("stateless_repeat")
    c = Caller(16)
    assert c.submit("a",nxt,59)
    assert all(not c.submit("a",nxt,t) for t in (60,89,119,120))
    assert c.submit("a",code(A,180),180)
    passed("replay_rollover_recovery")
    c = Caller()
    assert c.submit("a",current,59) and not c.submit("b",current,59)
    assert c.submit("b",other,59) and not c.submit("unknown",current,59)
    passed("account_isolation")
    c = Caller()
    assert all(not c.submit("a","invalid",59) for _ in range(3))
    assert not c.submit("a",current,59) and c.checks == 3
    assert c.submit("b",other,59) and c.submit("a",code(A,119),119)
    passed("throttle_reset_isolation")
    c = Caller()
    assert c.submit("a",current,59) and not c.submit("a",current,58)
    passed("clock_rollback_denied")
    c = Caller(16)
    results = concurrent(c,current,59)
    assert sum(results) == 1 and c.checks == 8
    passed("concurrent_duplicate_single_winner")
    c = Caller(3)
    results = concurrent(c,"invalid",59)
    assert not any(results) and c.checks == 3 and not c.submit("a",current,59)
    passed("concurrent_attempt_budget")
    assert count == 12
    print("P04_S04_PYTHON_PASS cases=" + str(count))

if __name__ == "__main__":
    main()
