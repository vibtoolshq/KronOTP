---
title: "Installation and Environment Requirements"
description: "Supported runtime versions, npm and PyPI installs, editable developer setup and source-only Authenticator installation."
order: 20
draft: false
---

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
