# Engine Function-Level Technical Reference

Verified against `javascript/src/kron-otp.js` and `python/src/kron_otp.py` on development `main` after P02 (frozen baseline `b4192dc`). Published `1.0.0` packages retain their historical input contracts. Methods listed are **existing** methods, not planned APIs.

## JavaScript: `javascript/src/kron-otp.js`

| Function / element | Visibility | Inputs → output | Exact purpose |
| --- | --- | --- | --- |
| `const OTPAuth = require('otpauth')` | Module import | Package → object | Uses third-party Secret/TOTP primitives to compute HMAC SHA-1 OTP values |
| `class KronOTP` | Public export | Class | Stateless static-method facade |
| `static #createTOTP(secret)` | Private | Base32 string → configured `OTPAuth.TOTP` | Rejects non-strings and raw >4096 chars, removes ASCII whitespace only, rejects non-ASCII characters before uppercasing, caps compact input at 1024 chars, validates canonical Base32 and decoded key >=14 bytes; configures SHA1/6/30 |
| `static generate(secret)` | Public | Base32 string → six-character string | Builds TOTP and invokes library `.generate()` at the current system time |
| `static verify(secret, token)` | Public | Base32 string, six-digit string → boolean | Checks token type/six-digit ASCII format first; returns false for expected invalid keys; `.validate({token, window:1}) !== null` |
| `module.exports = KronOTP` | Public export | CommonJS import → class | Enables `const KronOTP = require('kron-otp')` |
| `module.exports.KronOTP = KronOTP` | Public export | Named CommonJS property | Enables `const {KronOTP} = require('kron-otp')` |

Errors: `generate` rejects missing/non-string, malformed, <14-byte or oversized Base32 with sanitized **TypeError**. `verify` returns **false** for expected malformed inputs. Accepted whitespace is ASCII `space/tab/CR/LF/FF/VT` only. Raw length max 4096; compact length max 1024. This changes the old JavaScript `v1.0.0` behavior for invalid secrets.

## Python: `python/src/kron_otp.py`

| Function / element | Visibility | Inputs → output | Exact purpose |
| --- | --- | --- | --- |
| `import base64, binascii, hashlib, re, time, pyotp` | Imports | Dependencies | Base32 canonicalization, SHA-1 digest selection, token regex, single system clock snapshot and TOTP library |
| `class KronOTP` | Public import | Class | Stateless static-method facade |
| `@staticmethod _normalize_secret(secret: str) -> str` | Internal | Base32 string → normalized unpadded Base32 | Rejects non-string/invalid characters, normalizes ASCII whitespace via `re.sub`/uppercase, rejects non-ASCII before uppercasing; checks raw/compact limits and >=14 decoded bytes; validates canonical encoding by Base32 decode/re-encode |
| `@staticmethod _totp(secret: str) -> pyotp.TOTP` | Internal | Base32 string → configured TOTP | Calls normalization, configures digits=6, interval=30, digest=SHA1; both wrapper and PyOTP enforce >=14 decoded bytes |
| `@staticmethod generate(secret: str) -> str` | Public | Base32 string → six-character string | Invokes `.now()`; translates expected invalid-secret exceptions to `ValueError` |
| `@staticmethod verify(secret: str, token: str) -> bool` | Public | Base32 string, token → boolean | Returns false for expected invalid input/mismatch; samples clock once; at Unix counter 0 compares only valid counters 0/+1 using PyOTP `valid_window=0`; otherwise uses original PyOTP `valid_window=1` |

`python/src/__init__.py` is empty and is not the exposed PyPI module; `pyproject.toml` uses `py-modules = ["kron_otp"]` with package dir `src`.

## Cross-language behavior table

| Contract | JavaScript | Python |
| --- | --- | --- |
| Format | Six ASCII digits (string) | Six ASCII digits (string) |
| Algorithm | SHA-1 | SHA-1 |
| Period | 30 seconds | 30 seconds |
| Verification tolerance | ±one time step | ±one time step |
| Secret case/whitespace | Both ignore ASCII space, tab, CR, LF, FF, VT; reject U+FEFF and non-ASCII characters before uppercasing | Same |
| Bad generated secret | Throws `TypeError` | Throws `ValueError` |
| Bad verify secret | Returns `false` | Returns `False` |
| Bad verify token | Returns `false` | Returns `False` |
| 80-bit canonical Base32 | Rejected (P01) | Rejected |
| 160-bit canonical Base32 | Supported | Supported |

**P01 input contract:** Both enforce >=14 decoded bytes; <=4096 raw chars, <=1024 chars after ASCII-whitespace removal; malformed secrets rejected by `generate` and treated as nonmatches by `verify`. Use a cryptographically random >=20-byte secret for new account provisioning. **P02 correction:** Python now avoids counter -1 at Unix epoch time 0–29 and accepts valid counters 0/+1, retaining ordinary ±1 window elsewhere. This is the development `main` contract, NOT yet a published update to registry v1.0.0.

## Consumer inputs and usage

A provided TOTP *shared secret* (not a generated code) is required. Typical examples:
- JS: `const KronOTP = require('kron-otp'); const token = KronOTP.generate(secret);`
- Python: `from kron_otp import KronOTP; token = KronOTP.generate(secret)`.

Neither wrapper accepts a configurable timestamp, issuer, algorithm, digits, period, secret storage, replay ledger or server-side rate limiter through its public API.

## P02 deterministic cross-engine coverage

The new source-only `python/tests/totp_vectors.json` contains six RFC 6238 SHA-1 known 6-digit outputs (including leading zeroes) and 80 synthetic 160-bit secret/time/expected-OTP cases from an independent HMAC reference calculation. `javascript/tests/test.js` and `python/tests/test_kron_otp.py` assert matching generated results and verification against the same fixture, plus epoch/rollover/two-step-outside behaviors. No new public timestamp API or runtime dependency was introduced. Package versions on npm/PyPI remain 1.0.0 and do not contain P01/P02 source changes.

## GUI-02 optional application functions (not public engine API)

- `python/tests/gui/app.py::load_pypi_engine()` — verifies exact published package metadata and resolved module path (no source import fallback).
- `parse_auth_input()` — accepts a Base32 secret or SHA1/6/30 `otpauth://totp` URI, rejects unsupported modes; does not generate OTP.
- `Authenticator.add_account`, `.edit_account`, `.delete_account` — multi-account actions, engine-validating secret before opt-in encrypted storage; `Use once` remains memory-only.
- `Authenticator._show_current`, `.copy_otp`, `._clear_owned_clipboard`, `._tick`, `._privacy_lock` — engine-generation, current-step display, conditional copy-clear, idle timeout and privacy lock.
- `python/tests/gui/vault.py::AccountVault.load/save` — Windows DPAPI encrypted JSON envelope and validated schema/atomic replacement, not an independent authentication or backup service.
- **None of these methods are published KronOTP engine APIs**. The engine remains exclusively `KronOTP.generate(secret)` and `KronOTP.verify(secret, token)` with SHA1/6 digits/30 seconds.
