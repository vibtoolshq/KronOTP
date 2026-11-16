# kron-otp (Python)

A small Python TOTP engine backed by PyOTP, maintained in the [KronOTP monorepo](https://github.com/vibtoolshq/KronOTP).

## Install

```sh
python -m pip install kron-otp
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
- The `pyotp>=2.12` dependency requires at least 112 bits of decoded secret material; use a securely generated 160-bit or longer Base32 secret.
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
