---
title: "Installation and Environment Requirements"
description: "Supported runtime versions, npm and PyPI installs, editable developer setup and source-only Authenticator installation."
order: 20
draft: false
---

## P04 consolidated qualification — 2026-11-28

**Current status (2026-11-28):** P01–P03 closed; P04 qualification evidence verified and consolidation acceptance pending this documentation PR and final closeout. P05 final production/release acceptance has not started. Older dated statements below about deferred governance, unexecuted P04 tests or offline clone are historical, not current status. No new package release or application change.

Production use should choose current security-patched upstream-supported runtimes, not merely the declared minimum. At 2026-11-28, the Node release information lists 22/24/26 LTS and 20 EOL; Python 3.10 reached its scheduled October 2026 EOL, while 3.11–3.15 are within their upstream support windows. Prefer a maintained Node LTS and maintained stable Python (e.g. 3.14 with current patches); verify the current lifecycle and OS/vendor patch availability before deployment. See [Node release status](https://nodejs.org/en/about/previous-releases) and [Python version status](https://devguide.python.org/versions/). The historical minimum-version tests do not recommend obsolete or unpatched runtime binaries.

For actual selected runtime combinations see [Compatibility](./CONFIGURATION_AND_COMPATIBILITY.md). The official v2.0.0 tarball/wheel/sdist passed scoped digest/payload checks; the sdist contains the test module but lacks the shared vector JSON, so use a full repository checkout for source regressions. Do not claim bundled sdist tests pass. Install with exact package version, review resolved dependencies, and use current upstream security patches. No GUI bundled.

## Published packages (both v2.0.0)

| Language | Runtime declaration | Package and dependency | Import |
| --- | --- | --- | --- |
| JavaScript | Node.js `>=20.19.0`; npm | npm `kron-otp@2.0.0`; runtime `otpauth ^9.6.0` | `require('kron-otp')` |
| Python | Python `>=3.10`; pip | PyPI `kron-otp==2.0.0`; runtime `pyotp>=2.12,<3` | `from kron_otp import KronOTP` |

The source repository tracks exact npm dependency versions in `javascript/package-lock.json` (currently `otpauth 9.6.0` and `@noble/hashes 2.4.0`). The Python project declares a bounded PyOTP requirement rather than a full committed version lock.

## Install into a Node.js consumer

```sh
npm install kron-otp@2.0.0
```

```js
const KronOTP = require('kron-otp');
const secret = process.env.TOTP_SECRET; // caller-provided through secure configuration
if (!secret) throw new Error('Missing caller-provided secret');
const code = KronOTP.generate(secret); // six-digit string
```

Use the exact package name with a hyphen. Node package is **CommonJS**, not a published ES module or a TypeScript declaration package.

## Install into a Python consumer

Create and activate a virtual environment when practical:

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install kron-otp==2.0.0
```

**Linux/macOS shell:**

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install kron-otp==2.0.0
```

```python
from kron_otp import KronOTP

# Retrieve a real key from your application's protected secret store.
# token = KronOTP.generate(secret)
```

For a directly executable synthetic example, see [Quickstart](./QUICKSTART.md). The **pip distribution** is named `kron-otp`, but the **importable module** is `kron_otp`. Multiple Python installations require using the interpreter in which the distribution was installed.

## Editable source development

```sh
git clone https://github.com/vibtoolshq/KronOTP.git
cd KronOTP
```

**JavaScript package checkout:**

```sh
cd javascript
npm ci --ignore-scripts --no-audit --no-fund
npm test
```

**Python package checkout:** from `python/` in an activated environment:

```sh
python -m pip install -e .
python -m unittest discover -s tests -v
```

Source tests use the repository's shared `python/tests/totp_vectors.json` fixture; do not assume it is included in the published npm tarball or wheel. Python source test imports `src.kron_otp`; installed consumer import is `kron_otp`.

## Optional Tkinter Authenticator source app

The source-only Windows-oriented app resides at `python/tests/gui/app.py`. You must **clone/download the repository**; installing PyPI alone does **not** install the application.

```powershell
python -m pip install kron-otp==2.0.0
python python/tests/gui/app.py
```

It supports multiple local accounts and a Windows CurrentUser DPAPI-encrypted vault on explicit Save; Windows storage needs a stable user profile and separate account recovery codes. Other OSs have unsaved session-only accounts. No separate EXE, QR camera or master-password layer is distributed.

## Uninstall

Remove libraries from the same environment in which you installed them:

```sh
npm uninstall kron-otp
python -m pip uninstall kron-otp
```

Uninstalling the Python **package** does not necessarily delete the separate GUI's Windows-encrypted `%LOCALAPPDATA%\KronOTP\vault.dat`. Do not delete that file unless you have independent recovery methods for all enrolled accounts. Neither library reads a built-in required environment variable.

## Version migration notes

The published v1.0.0 remains a historical artifact. v2.0.0 changes JavaScript `verify` behavior for expected invalid secrets from throwing to returning false, disallows weak short Base32 keys in both languages, and includes the Python epoch counter fix. Upgrade compatible applications deliberately; no implicit migration of account secrets occurs.

[API reference](./API_REFERENCE.md) · [Compatibility](./CONFIGURATION_AND_COMPATIBILITY.md) · [Testing](./TESTING_AND_RELEASES.md)


## P05-A02 — source distribution completeness (2026-11-28)

`python/MANIFEST.in` explicitly includes `tests/totp_vectors.json` in future Python source distributions. `.github/workflows/p05-sdist.yml` qualifies candidate sdist and wheel built from that sdist, strict archive paths/source bytes/metadata/RECORD, twine check, and separate 13-method source and installed-wheel regressions with all 86 shared vectors. The wheel consumer adapts only import/mock paths in a disposable copy. No runtime fixture or GUI in the wheel; no engine, dependency, version, existing workflow or publishing change. Build tools are resolved in an isolated CI environment and recorded, not a reproducibility lock. Qualification acceptance pending actual CI and verified closeout. Historical published v2.0.0 sdist remains incomplete and published v2 does not contain the R-04 source fix; no new release.
