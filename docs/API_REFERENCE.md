# KronOTP API Reference — Development `main` (P01)

**Version boundary:** This page describes source on `main` after Phase P01. The previously published npm/PyPI `1.0.0` artifacts are unchanged, and their earlier invalid-secret behavior can differ. Do not assume `npm install kron-otp@1.0.0` contains P01 fixes.

This lists **all existing public API methods** of the current `KronOTP` class in each language. There are no instance settings, public constructor, asynchronous requests, stored accounts or extra features.

## Shared defaults

| Property | Value |
| --- | --- |
| TOTP algorithm | SHA-1 HMAC |
| Token length | 6 ASCII decimal digits, always a **string** (leading zeroes retained) |
| Time step | 30 seconds |
| Verification time tolerance | Current step and one previous/next step (±30-second step) |
| Secret input | Canonical ASCII Base32, case-insensitive, only ASCII space/tab/CR/LF/FF/VT ignored; >=14 decoded bytes, <=4096 raw characters and <=1024 cleaned characters |
| Provisioning | External; caller must already have lawful access to shared secret |
| State storage / replay block | **Not implemented** in these libraries |

## JavaScript (Node.js, CommonJS)

Published `1.0.0`: `npm install kron-otp@1.0.0` (**does not include P01**). Current development source: `javascript/src/kron-otp.js`.

```js
const KronOTP = require('kron-otp');
// Also valid: const { KronOTP } = require('kron-otp');

const secret = process.env.TOTP_SECRET;
if (!secret) throw new Error('Missing TOTP_SECRET');

const token = KronOTP.generate(secret);      // string: exactly 6 digits
const accepted = KronOTP.verify(secret, token); // boolean
```

### `KronOTP.generate(secret)`

- Argument: `secret` must be a string containing ASCII Base32 characters A–Z/2–7 (case-insensitive), legal trailing `=` padding and optionally ASCII space/tab/CR/LF/FF/VT.
- Returns: exactly 6 digits as a string, derived from current system time.
- Throws: sanitized `TypeError` if secret is missing/wrong type, noncanonical, <14 decoded bytes, >4096 raw characters or >1024 cleaned Base32 characters.
- Validation is performed by private `#createTOTP`, then `OTPAuth.Secret.fromBase32`.
- **P01 `main` behavior:** JavaScript now enforces the same 14-decoded-byte minimum as Python. A cryptographically random >=20-byte secret is recommended for new provisioning; length alone is not entropy.

### `KronOTP.verify(secret, token)`

- Arguments: Base32 string `secret`; exactly six-character ASCII decimal string `token`.
- Returns: `true` if the token matches within ±one time step; otherwise `false`.
- Returns `false` for an invalid secret or token; token shape is checked before secret decoding. This is a **breaking change** from previously published JS `1.0.0` which threw `TypeError` for a bad secret.
- Other token input types (e.g. numeric `123456`) return `false` irrespective of secret validity.

## Python

Published `1.0.0`: `python -m pip install kron-otp==1.0.0` (**does not include P01**). Current development source: `python/src/kron_otp.py`.

```python
from kron_otp import KronOTP

secret = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"  # Public test fixture only
token: str = KronOTP.generate(secret)
accepted: bool = KronOTP.verify(secret, token)
```

### `KronOTP.generate(secret: str) -> str`

- Argument: string ASCII Base32 secret; removes only ASCII whitespace (space/tab/CR/LF/FF/VT), uppercases after rejecting non-ASCII, rejects invalid/noncanonical encodings, <14 decoded bytes, >4096 raw or >1024 cleaned characters.
- Calls internal `_normalize_secret` then `_totp`, then `pyotp.TOTP.now()`.
- Returns: exactly six-digit string.
- Raises sanitized `ValueError` on bad secret including non-string/oversized/short keys; both wrapper and PyOTP >=2.12 require **14 decoded bytes**.

### `KronOTP.verify(secret: str, token: str) -> bool`

- Returns `True` for a matching six-digit token within `valid_window=1`.
- Returns `False` for mismatched token, wrong token format, invalid or too-short secret.
- It checks token format first, then builds the generator. It returns `False` for expected invalid-secret input, as now does JavaScript on `main`.

## Public API differences and design limitations

| Input scenario | JavaScript `KronOTP` | Python `KronOTP` |
| --- | --- | --- |
| Good canonical >=160-bit Base32 | Generate/verify | Generate/verify |
| 80-bit Base32 example | Rejected on `main` | Rejected on `main` |
| Invalid secret at generate | Throws `TypeError` | Raises `ValueError` |
| Invalid secret at verify | Returns `false` on `main` | Returns `False` on `main` |
| Invalid token (valid secret) | `false` | `False` |
| Custom digits, algorithm, time-step | Not exposed | Not exposed |
| Single-use OTP tracking | Not implemented | Not implemented |

**P01 migration:** Choose randomly generated >=160-bit keys for newly provisioned accounts, although the implementation minimum remains 112 bits for compatibility with existing Python keys. Consumers who depended on short JS keys, JS verify exceptions or broad Unicode whitespace acceptance must adapt before a future release. Python epoch-start verification bug remains scheduled for P02; it is not fixed by P01.

## Integration responsibility

The library's `verify()` is a local cryptographic comparison. It does not authenticate a user identity or enforce rate limiting, login sessions, OTP replay prevention, account locks or token attempt counters. Those protections belong to the application/server implementing the login flow.

See [Installation](./INSTALLATION.md), [Usage & troubleshooting](./USAGE_AND_TROUBLESHOOTING.md) and [Automation](./AUTOMATION_AND_PUBLISHING.md).
