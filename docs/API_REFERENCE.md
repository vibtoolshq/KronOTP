# KronOTP API Reference — v1.0.0

This lists **all existing public API methods** of the current `KronOTP` class in each language. There are no instance settings, public constructor, asynchronous requests, stored accounts or extra features.

## Shared defaults

| Property | Value |
| --- | --- |
| TOTP algorithm | SHA-1 HMAC |
| Token length | 6 ASCII decimal digits, always a **string** (leading zeroes retained) |
| Time step | 30 seconds |
| Verification time tolerance | Current step and one previous/next step (±30-second step) |
| Secret input | Base32-encoded provisioning secret, spaces/whitespace removed, case normalized to uppercase |
| Provisioning | External; caller must already have lawful access to shared secret |
| State storage / replay block | **Not implemented** in these libraries |

## JavaScript (Node.js, CommonJS)

Install: `npm install kron-otp@1.0.0`. Module source: `javascript/src/kron-otp.js`.

```js
const KronOTP = require('kron-otp');
// Also valid: const { KronOTP } = require('kron-otp');

const secret = process.env.TOTP_SECRET;
if (!secret) throw new Error('Missing TOTP_SECRET');

const token = KronOTP.generate(secret);      // string: exactly 6 digits
const accepted = KronOTP.verify(secret, token); // boolean
```

### `KronOTP.generate(secret)`

- Argument: `secret` must be a string containing canonical Base32 characters A–Z/2–7, optional supported Base32 trailing `=` padding and whitespace/case variations.
- Returns: exactly 6 digits as a string, derived from current system time.
- Throws: `TypeError` if secret is missing, has wrong type, invalid alphabet/length/padding or non-canonical Base32 encoding.
- Validation is performed by private `#createTOTP`, then `OTPAuth.Secret.fromBase32`.
- **Current behavior:** the Node wrapper does not require 14 decoded bytes; an 80-bit valid Base32 key can be accepted (unlike the Python version).

### `KronOTP.verify(secret, token)`

- Arguments: Base32 string `secret`; exactly six-character ASCII decimal string `token`.
- Returns: `true` if the token matches within ±one time step; otherwise `false`.
- Throws: `TypeError` for an invalid secret **even when the token is invalid**, because secret validation runs before token-format checking.
- Other token input types (e.g. numeric `123456`) return `false` when the secret is valid.

## Python

Install: `python -m pip install kron-otp==1.0.0`. Source: `python/src/kron_otp.py`.

```python
from kron_otp import KronOTP

secret = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"  # Public test fixture only
token: str = KronOTP.generate(secret)
accepted: bool = KronOTP.verify(secret, token)
```

### `KronOTP.generate(secret: str) -> str`

- Argument: string Base32 secret; removes whitespace and uppercases, rejects invalid/non-canonical encodings.
- Calls internal `_normalize_secret` then `_totp`, then `pyotp.TOTP.now()`.
- Returns: exactly six-digit string.
- Raises `ValueError` on bad secret, including non-string inputs; PyOTP >=2.12 requires at least **14 decoded bytes**.

### `KronOTP.verify(secret: str, token: str) -> bool`

- Returns `True` for a matching six-digit token within `valid_window=1`.
- Returns `False` for mismatched token, wrong token format, invalid or too-short secret.
- It checks token format first, then builds the generator. It **does not raise ValueError** for the handled invalid-secret cases, unlike JS.

## Public API differences and design limitations

| Input scenario | JavaScript `KronOTP` | Python `KronOTP` |
| --- | --- | --- |
| Good canonical >=160-bit Base32 | Generate/verify | Generate/verify |
| 80-bit Base32 example | Accepted | Rejected |
| Invalid secret at generate | Throws `TypeError` | Raises `ValueError` |
| Invalid secret at verify | Throws `TypeError` | Returns `False` |
| Invalid token (valid secret) | `false` | `False` |
| Custom digits, algorithm, time-step | Not exposed | Not exposed |
| Single-use OTP tracking | Not implemented | Not implemented |

Use secure, canonical 160-bit or longer keys where possible for cross-language compatibility. Differences above reflect actual source; they are **not** repaired by documentation updates.

## Integration responsibility

The library's `verify()` is a local cryptographic comparison. It does not authenticate a user identity or enforce rate limiting, login sessions, OTP replay prevention, account locks or token attempt counters. Those protections belong to the application/server implementing the login flow.

See [Installation](./INSTALLATION.md), [Usage & troubleshooting](./USAGE_AND_TROUBLESHOOTING.md) and [Automation](./AUTOMATION_AND_PUBLISHING.md).
