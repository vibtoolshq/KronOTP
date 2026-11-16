# kron-otp (Python)

A small Python TOTP engine backed by PyOTP, maintained in the [KronOTP monorepo](https://github.com/vibtoolshq/KronOTP).

## Install

```sh
python -m pip install kron-otp==2.0.0
```

## Usage

```python
import os
from kron_otp import KronOTP

secret = os.environ["TOTP_SECRET"]  # Base32 provisioning secret, not an OTP
token = KronOTP.generate(secret)   # six-digit string
verified = KronOTP.verify(secret, token)
print("Verification:", verified)
```

- `generate(secret: str) -> str` returns a six-digit string or raises `ValueError` for invalid secrets.
- `verify(secret: str, token: str) -> bool` returns `False` for invalid secrets or tokens.
- Configuration: SHA-1, 6 digits, 30-second period, ±one 30-second verification window.
- **v2.0.0** explicitly requires >=14 decoded bytes (112 bits), <=4096 raw/<=1024 cleaned Base32 chars and ASCII space/tab/CR/LF/FF/VT normalization; Unicode-only whitespace is rejected. Use a cryptographically random 160-bit or longer Base32 secret for provisioning.
- Supported Python: 3.10+.

## Local tests

From the `python/` directory:

```sh
python -m pip install -e .
python -m unittest discover -s tests -v
```

Keep TOTP provisioning secrets private. Use server-side rate limits and replay protection; successful local code generation is not proof of authentication.

See the [integration and publishing guide](../docs/AUTOMATION_AND_PUBLISHING.md).

Licensed under the [MIT License](./LICENSE).

**v2.0.0 changes:** stricter ASCII-only whitespace and size validation, plus a fix for verifying valid OTPs at Unix seconds 0–29. Older 1.0.0 is not overwritten. This library remains stateless; implement replay prevention and attempt throttling at the relying-party server.

## Optional Tkinter Live TOTP Tester (source-only)

A small Windows-friendly local example is in [tests/gui/app.py](./tests/gui/app.py); see [GUI instructions](./tests/gui/README.md). It uses the **installed PyPI kron-otp==2.0.0 package**, not this repository's editable source:

```powershell
python -m pip install kron-otp==2.0.0
python python/tests/gui/app.py
```

Run from the **repository root** or run `python app.py` while in `python/tests/gui/`. Requires Tkinter in the selected Python interpreter. This test window masks/show-hides a user-provided Base32 secret, generates six-digit codes, refreshes at the 30-second boundary and copies only the OTP. It neither stores secrets nor authenticates against a server. **The PyPI wheel does not bundle the GUI**, so installing `kron-otp` alone does not provide `app.py`.
