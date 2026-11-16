# Installation & Environment Setup — KronOTP v2.0.0

This guide documents the **v2.0.0 release**. The library generates/verifies codes only for a shared Base32 secret **already owned/provisioned by the consumer**. Older v1.0.0 packages retain their historical validation/error behavior; do not mix them with v2.0.0 assumptions.

## Requirements

| Runtime | Requirements | Published package |
| --- | --- | --- |
| Node.js | Node >=20.19.0 and npm, internet for installation | [kron-otp 2.0.0 (npm)](https://www.npmjs.com/package/kron-otp/v/2.0.0) |
| Python | Python >=3.10 and pip, internet for installation | [kron-otp 2.0.0 (PyPI)](https://pypi.org/project/kron-otp/2.0.0/) |

Source repository: https://github.com/vibtoolshq/KronOTP. npm uses `otpauth`; Python uses `pyotp>=2.12,<3`. **Use 160-bit or longer canonical Base32 secrets for reliable cross-language operation** (Python dependency requires at least 112 decoded bits). Do not use the known sample key as an actual account credential.

## Node.js — install in a consumer application

From the application's own directory:

```sh
npm install kron-otp@2.0.0
```

CommonJS usage:

```js
const KronOTP = require('kron-otp');
const secret = process.env.TOTP_SECRET;
if (!secret) throw new Error('TOTP_SECRET is not configured');
const token = KronOTP.generate(secret);
const isValid = KronOTP.verify(secret, token);
console.log('Locally verified:', isValid);
```

The module exports the class as either `require('kron-otp')` or `require('kron-otp').KronOTP`. Do not confuse the Base32 shared secret with the six-digit token. Set `TOTP_SECRET` from a secure secret manager or other secure runtime configuration; never commit an active secret to Git.

## Python — install in a consumer environment

A virtual environment is recommended.

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install kron-otp==2.0.0
```

macOS / Linux shell:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install kron-otp==2.0.0
```

Python use:

```python
import os
from kron_otp import KronOTP

secret = os.environ["TOTP_SECRET"]
code = KronOTP.generate(secret)
print("Locally verified:", KronOTP.verify(secret, code))
```

The **distribution name** is `kron-otp`, but the **Python import name** is `kron_otp`.

## Working directly from source (without publishing)

```sh
git clone https://github.com/vibtoolshq/KronOTP.git
cd KronOTP
```

Node.js:

```sh
cd javascript
npm ci
npm test
```

Python (from `python/`, in an isolated Python environment):

```sh
python -m pip install -e .
python -m unittest discover -s tests -v
```

Node local source import: `require('./src/kron-otp')` when working in the `javascript/` folder. Python direct source import: `from src.kron_otp import KronOTP` from the `python/` folder; after editable/published package installation prefer `from kron_otp import KronOTP`.

## Security and compatibility notes

- KronOTP does **not** register accounts or retrieve your TOTP secret; provisioning is external.
- Generator and verifier use SHA-1, six digits, 30-second periods, and a ±one-step verification window.
- **Version 2.0.0 (P01 changes):** accepts only canonical ASCII Base32 with 14+ decoded bytes, <=4096 raw/<=1024 whitespace-compacted characters, and only ASCII space/tab/CR/LF/FF/VT removed. `generate` rejects expected invalid keys; `verify` returns false/False for expected malformed input. Historical `1.0.0` has different JS invalid-secret handling and short-key acceptance. **v2.0.0 is a breaking upgrade; migrate existing consumers carefully.**
- For newly provisioned accounts use cryptographically random 160-bit or longer secrets. A minimum length check does not prove key entropy.
- Time synchronization matters; an out-of-sync clock leads to invalid codes.
- Never print the shared secret or put it into code, test artifacts or GitHub Actions logs.
- There is no CLI command, dashboard, login page, browser extension or settings UI supplied by this repository.

Next: [API reference](./API_REFERENCE.md), [Usage & troubleshooting](./USAGE_AND_TROUBLESHOOTING.md).
