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
- P01 development source explicitly requires >=14 decoded bytes (112 bits), <=4096 raw/<=1024 cleaned Base32 chars and ASCII space/tab/CR/LF/FF/VT normalization; Unicode-only whitespace is rejected. Use a cryptographically random 160-bit or longer Base32 secret for provisioning.
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

**Release distinction:** Source-tree P01 strict normalization/bounds are not yet published in the PyPI `1.0.0` package. No version or dependency metadata was changed in P01.
