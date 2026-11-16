# Engine Function-Level Technical Reference

Verified against `javascript/src/kron-otp.js` and `python/src/kron_otp.py`, published version `1.0.0` (baseline `50df7c4`). Methods listed are **existing** methods, not planned APIs.

## JavaScript: `javascript/src/kron-otp.js`

| Function / element | Visibility | Inputs → output | Exact purpose |
| --- | --- | --- | --- |
| `const OTPAuth = require('otpauth')` | Module import | Package → object | Uses third-party Secret/TOTP primitives to compute HMAC SHA-1 OTP values |
| `class KronOTP` | Public export | Class | Stateless static-method facade |
| `static #createTOTP(secret)` | Private | Base32 string → configured `OTPAuth.TOTP` | Rejects non-strings, removes all JS-regex whitespace, uppercases, validates alphabet/length/padding, decodes and checks canonical Base32; configures SHA1/6/30 |
| `static generate(secret)` | Public | Base32 string → six-character string | Builds TOTP and invokes library `.generate()` at the current system time |
| `static verify(secret, token)` | Public | Base32 string, six-digit string → boolean | First creates configured TOTP (therefore validates secret); rejects non-string or non-six-digit tokens; `.validate({token, window:1}) !== null` |
| `module.exports = KronOTP` | Public export | CommonJS import → class | Enables `const KronOTP = require('kron-otp')` |
| `module.exports.KronOTP = KronOTP` | Public export | Named CommonJS property | Enables `const {KronOTP} = require('kron-otp')` |

Errors: non-string/malformed/non-canonical Base32 yields **TypeError**; invalid token format yields **false** if secret is valid. Empty input is invalid. The JavaScript wrapper does **not** enforce a minimum decoded length of 14 bytes; an 80-bit Base32 demo key can pass here.

## Python: `python/src/kron_otp.py`

| Function / element | Visibility | Inputs → output | Exact purpose |
| --- | --- | --- | --- |
| `import base64, binascii, hashlib, re, pyotp` | Imports | Dependencies | Base32 canonicalization, SHA-1 digest selection, token regex, TOTP library |
| `class KronOTP` | Public import | Class | Stateless static-method facade |
| `@staticmethod _normalize_secret(secret: str) -> str` | Internal | Base32 string → normalized unpadded Base32 | Rejects non-string/invalid characters, normalizes via Python `split()`/uppercase, validates canonical encoding by Base32 decode/re-encode |
| `@staticmethod _totp(secret: str) -> pyotp.TOTP` | Internal | Base32 string → configured TOTP | Calls normalization, configures digits=6, interval=30, digest=SHA1; PyOTP itself enforces decoded minimum length |
| `@staticmethod generate(secret: str) -> str` | Public | Base32 string → six-character string | Invokes `.now()`; translates expected invalid-secret exceptions to `ValueError` |
| `@staticmethod verify(secret: str, token: str) -> bool` | Public | Base32 string, token → boolean | Returns false on invalid token, normalized/decoded invalid secret, or OTP mismatch; calls `.verify(valid_window=1)` |

`python/src/__init__.py` is empty and is not the exposed PyPI module; `pyproject.toml` uses `py-modules = ["kron_otp"]` with package dir `src`.

## Cross-language behavior table

| Contract | JavaScript | Python |
| --- | --- | --- |
| Format | Six ASCII digits (string) | Six ASCII digits (string) |
| Algorithm | SHA-1 | SHA-1 |
| Period | 30 seconds | 30 seconds |
| Verification tolerance | ±one time step | ±one time step |
| Secret case/whitespace | Removes JS regex whitespace, uppercases | Removes Python `split()` whitespace, uppercases |
| Bad generated secret | Throws `TypeError` | Throws `ValueError` |
| Bad verify secret | Throws `TypeError` | Returns `False` |
| Bad verify token | Returns `false` when secret valid | Returns `False` |
| 80-bit canonical Base32 | Accepted in current JS runtime | Rejected by PyOTP >=2.12 |
| 160-bit canonical Base32 | Supported | Supported |

**Important:** This mismatch is documented, not fixed by the documentation phase. Upgrading/downgrading dependencies or unifying contracts needs a separate scoped implementation and regression test.

## Consumer inputs and usage

A provided TOTP *shared secret* (not a generated code) is required. Typical examples:
- JS: `const KronOTP = require('kron-otp'); const token = KronOTP.generate(secret);`
- Python: `from kron_otp import KronOTP; token = KronOTP.generate(secret)`.

Neither wrapper accepts a configurable timestamp, issuer, algorithm, digits, period, secret storage, replay ledger or server-side rate limiter through its public API.
