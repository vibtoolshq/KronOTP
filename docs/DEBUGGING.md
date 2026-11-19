---
title: "Testing, Debugging and Failure Diagnosis"
description: "Debug KronOTP imports, invalid Base32 secrets, clock drift, GUI vault failures and CI checks."
order: 110
draft: false
---

## First isolate package/runtime issues

| Observation | Where to check | Code-grounded explanation |
| --- | --- | --- |
| Node `Cannot find module 'kron-otp'` | `npm ls kron-otp` from consumer working directory | npm module must be installed in the consumer; source module is under `javascript/src/` |
| Node unexpected runtime error | `node --version` | Declared Node requirement `>=20.19.0` |
| Python `ModuleNotFoundError: kron_otp` | `python -m pip show kron-otp` in **same** interpreter | Distribution name has hyphen, import name underscore |
| Python `ImportError` or wrong version in GUI | GUI's `load_pypi_engine` | GUI explicitly requires installed PyPI version 2.0.0 and exact module origin |
| `generate` rejects secret | Input length/Base32/padding/entropy | JavaScript `TypeError` or Python `ValueError` for bad secret; never log key contents |
| `verify` returns false | Token format, enrollment key, clock | Token must be a **six ASCII decimal-digit string**; invalid tokens/expected bad keys are ordinary nonmatches |
| Different TOTP between services | Clock / algorithm / selected account | Engine fixed SHA1, 6 digits, 30s; remote service may use other settings or an incorrect enrolled key |
| Expected leading zero lost | Caller int conversion | Never convert the six-digit **string** to a number |
| Windows vault cannot decrypt | Windows user/profile / corruption | DPAPI CurrentUser binds vault to the Windows identity; app does not recover/export secrets |
| GUI `Save` unavailable on macOS/Linux | OS boundary | GUI persistent DPAPI vault is intentionally Windows-only; temporary use does not save |

## Minimal safe checks

**Node source tests** (from `javascript/`):

```sh
npm ci --ignore-scripts --no-audit --no-fund
npm test
```

**Python source tests** (from `python/`; install in isolated environment first):

```sh
python -m pip install -e .
python -m unittest discover -s tests -v
```

**GUI integration tests** (repo root, installed PyPI v2.0.0, Windows Tkinter/DPAPI):

```powershell
python -m unittest discover -s python/tests/gui -p test_app.py -v
```

The Node/Python core suites use **six fixed-time RFC SHA1 six-digit values and 80 synthetic test vectors** stored in `python/tests/totp_vectors.json`. Source tests patch/mock the clocks; these are **internal test techniques**, not public timestamp parameters. Published registry smoke installs from npm/PyPI and is a separate check.

## Safe Python failure handling

```python
from kron_otp import KronOTP

def try_generate(secret: str) -> str | None:
    try:
        return KronOTP.generate(secret)
    except ValueError:
        # Never include the shared key in error text or logs.
        return None
```

`str | None` syntax requires Python 3.10+, matching the declared runtime. JavaScript consumers can catch `TypeError` from `generate`; JavaScript `verify` normally returns `false` on malformed secrets/tokens.

## GUI-specific diagnosis

- The app and test files under `python/tests/gui/` are GitHub-only, not installed via pip. Run `python python/tests/gui/app.py` from repo root, using the interpreter into which PyPI 2.0.0 was installed.
- On Windows saved account data resides at `%LOCALAPPDATA%\KronOTP\vault.dat` encrypted by DPAPI. It is not a portable backup. **Do not delete or overwrite** unreadable encrypted vaults as a troubleshooting shortcut; preserve them and independently recover the original Windows profile if possible.
- Unlock uses Windows user decryption rather than a separate PIN or password. App Lock and inactivity lock hide loaded records; same-user malware may access process or DPAPI material.
- GUI only imports supported `otpauth://totp` with SHA1/6 digits/30s; camera/QR imaging, HOTP and SHA256/512 are outside scope.
- Clipboard clearing after 15 seconds is conditional: the app clears only if it believes the clipboard still contains its previously copied OTP. Other software may copy it before clearing.

## CI/release investigation

Read the three workflow files under `.github/workflows/`. A docs-only push may produce **no new CI run** because main push triggers are path-filtered; PRs still run the stable `Required CI`. A successful branch validation with both publish jobs **SKIPPED** is expected; publication occurs only on an authorized version-tag push. Check actual job conclusions before claiming success.

Never paste live TOTP secrets, registry tokens or usernames/passwords into issue comments, screenshots, log attachments or docs.

[API failure contracts](./API_REFERENCE.md) · [Runtime settings](./CONFIGURATION_AND_COMPATIBILITY.md) · [Testing & releases](./TESTING_AND_RELEASES.md)
