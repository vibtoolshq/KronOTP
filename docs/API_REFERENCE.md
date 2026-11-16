# KronOTP API Reference — v2.0.0 (P01 + P02)

**Version boundary:** This page documents **v2.0.0**, incorporating P01 and P02. Historical npm/PyPI `1.0.0` artifacts remain unchanged, and their invalid-secret handling differs. Upgrading from 1.0.0 to 2.0.0 can require consumer code changes.

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

For **v2.0.0**: `npm install kron-otp@2.0.0`. Source: `javascript/src/kron-otp.js`.

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
- **v2.0.0 behavior:** JavaScript now enforces the same 14-decoded-byte minimum as Python. A cryptographically random >=20-byte secret is recommended for new provisioning; length alone is not entropy.

### `KronOTP.verify(secret, token)`

- Arguments: Base32 string `secret`; exactly six-character ASCII decimal string `token`.
- Returns: `true` if the token matches within ±one time step; otherwise `false`.
- Returns `false` for an invalid secret or token; token shape is checked before secret decoding. This is a **breaking change** from previously published JS `1.0.0` which threw `TypeError` for a bad secret.
- Other token input types (e.g. numeric `123456`) return `false` irrespective of secret validity.

## Python

For **v2.0.0**: `python -m pip install kron-otp==2.0.0`. Source: `python/src/kron_otp.py`.

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

- Returns `True` for a matching six-digit token in the existing current/adjacent 30-second time steps. At Unix epoch seconds 0–29, explicitly checks valid counters 0 and +1 without evaluating negative counter −1; otherwise uses PyOTP `valid_window=1`.
- Returns `False` for mismatched token, wrong token format, invalid or too-short secret.
- It checks token format first, then builds the generator. It returns `False` for expected invalid-secret input, as now does JavaScript in v2.0.0.

## Public API differences and design limitations

| Input scenario | JavaScript `KronOTP` | Python `KronOTP` |
| --- | --- | --- |
| Good canonical >=160-bit Base32 | Generate/verify | Generate/verify |
| 80-bit Base32 example | Rejected in v2.0.0 | Rejected in v2.0.0 |
| Invalid secret at generate | Throws `TypeError` | Raises `ValueError` |
| Invalid secret at verify | Returns `false` in v2.0.0 | Returns `False` in v2.0.0 |
| Invalid token (valid secret) | `false` | `False` |
| Custom digits, algorithm, time-step | Not exposed | Not exposed |
| Single-use OTP tracking | Not implemented | Not implemented |

**P01 migration:** Choose randomly generated >=160-bit keys for newly provisioned accounts, although the implementation minimum remains 112 bits for compatibility with existing Python keys. Consumers who depended on short JS keys, JS verify exceptions or broad Unicode whitespace acceptance must adapt before a future release. Python epoch-start verification was fixed for v2.0.0 by P02; historical PyPI `1.0.0` remains unchanged.

## Integration responsibility

The library's `verify()` is a local cryptographic comparison. It does not authenticate a user identity or enforce rate limiting, login sessions, OTP replay prevention, account locks or token attempt counters. Those protections belong to the application/server implementing the login flow.

See [Installation](./INSTALLATION.md), [Usage & troubleshooting](./USAGE_AND_TROUBLESHOOTING.md) and [Automation](./AUTOMATION_AND_PUBLISHING.md).

### P02 deterministic verification evidence

The source suites now share six fixed-time RFC 6238 SHA-1 six-digit expected OTPs and 80 synthetic 160-bit Base32 secret/timestamp/OTP triples. Both engines must generate the same expected values and verify them at matching fixed timestamps. Python additionally guards negative drift counters at Unix epoch time 0–29. These are source regression tests, not a public timestamp parameter or change to 30-second/±1 configuration.
