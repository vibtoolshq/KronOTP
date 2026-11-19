# Public API Reference — KronOTP v2.0.0

**Complete supported public package API:** one `KronOTP` class per language, each exporting **two static methods**. No other supported public class methods, public constructor arguments, interfaces, enums, hooks, events, CLI commands, network operations or configuration setters are implemented.

## Shared data contract

| Property | Runtime behavior |
| --- | --- |
| Secret type | Nonempty Base32 **string**, ASCII alphabet A–Z/2–7 (case-insensitive) and correct optional trailing `=` padding |
| Whitespace normalization | Only ASCII space, tab, LF, CR, FF, VT are removed |
| Input length | ≤4096 raw characters; ≤1024 cleaned Base32 characters |
| Decoded secret length | ≥14 bytes required; ≥20 securely random bytes recommended for new provisioning |
| Algorithm | HMAC-SHA1 |
| Output | Exactly **6 ASCII digits as a string**, leading zeros retained |
| Time step | 30 seconds from system clock |
| `verify` window | Previous, current or next 30-second counter (±1 step) |
| State and replay tracking | None; `verify` is repeatable for the same valid token |

Base32 normalization also checks canonical unused padding bits and padding placement; valid-looking, noncanonical encodings can fail. No public arguments expose algorithm, number of digits, step, timestamp or allowed clock window.

## Node.js / CommonJS — `javascript/src/kron-otp.js`

**Distribution:** npm `kron-otp@2.0.0`, Node `>=20.19.0`, dependency `otpauth ^9.6.0`.

```js
const KronOTP = require('kron-otp');
// Named alias also refers to the SAME class:
// const { KronOTP } = require('kron-otp');
```

**Export identity:** `module.exports = KronOTP` and `module.exports.KronOTP = KronOTP`. The exported class is used via **static** methods, no instance needed.

### `KronOTP.generate(secret)`

| Parameter | Required | Type | Default | Meaning |
| --- | --- | --- | --- | --- |
| `secret` | Yes | `string` | None | Canonical Base32 shared secret already provisioned for caller |

**Return:** `string` of six ASCII decimal characters, computed from the system clock.

**Failure:** Throws `TypeError` if secret is not a string, is empty/malformed/noncanonical, exceeds limits, or decodes to fewer than 14 bytes. Input-dependent errors use sanitized messages and do not reveal the secret. Dependency/internal unexpected failures are not promised to be handled by this public contract.

```js
const KronOTP = require('kron-otp');
const key = 'GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ'; // RFC public fixture
const otp = KronOTP.generate(key);
console.log(/^[0-9]{6}$/.test(otp)); // true
```

### `KronOTP.verify(secret, token)`

| Parameter | Required | Type | Default | Meaning |
| --- | --- | --- | --- | --- |
| `secret` | Yes | `string` | None | Same Base32 shared secret (ordinary invalid input yields false) |
| `token` | Yes | `string` | None | Exactly six ASCII decimal digits; never a number |

**Return:** `boolean` — `true` only when OTPAuth validates the entered token at the current/adjacent step; `false` on ordinary mismatch, malformed token or invalid secret. **Does not throw for expected invalid secrets/tokens** in v2.0.0, a breaking difference from v1.0.0.

```js
const matches = KronOTP.verify(key, otp); // true when current token remains within window
const invalid = KronOTP.verify(key, 'oops'); // false
```

**Internal-only:** `KronOTP.#createTOTP(secret)`, `OTPAuth.Secret` and `OTPAuth.TOTP` are implementation details, not exported KronOTP extension points.

## Python — `python/src/kron_otp.py`

**Distribution:** PyPI `kron-otp==2.0.0`, Python `>=3.10`, dependency `pyotp>=2.12,<3`.

```python
from kron_otp import KronOTP
```

### `KronOTP.generate(secret: str) -> str`

| Parameter | Required | Type | Default | Meaning |
| --- | --- | --- | --- | --- |
| `secret` | Yes | `str` | None | Canonical Base32 secret; invalid values rejected |

**Return:** Six ASCII decimal characters as `str`. **Failure:** raises `ValueError` for expected malformed, non-string, weak, noncanonical or excessive secrets. This is a synchronous static method; do not instantiate the class.

```python
from kron_otp import KronOTP

secret = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"  # public fixture only
code: str = KronOTP.generate(secret)
assert len(code) == 6 and code.isascii() and code.isdigit()
```

### `KronOTP.verify(secret: str, token: str) -> bool`

| Parameter | Required | Type | Default | Meaning |
| --- | --- | --- | --- | --- |
| `secret` | Yes | `str` | None | Same Base32 secret; ordinary invalid values yield False |
| `token` | Yes | `str` | None | Exactly six ASCII decimal characters |

**Return:** `bool` — `True` for a matching current/adjacent counter; `False` for malformed token, invalid secret or mismatch. Python samples time once. At Unix epoch times 0–29 seconds it avoids PyOTP's negative counter evaluation by explicitly checking counters 0 and +1; otherwise it passes `valid_window=1`.

```python
assert KronOTP.verify(secret, code) is True  # locally valid current token
assert KronOTP.verify(secret, "12345") is False
```

**Internal-only:** `KronOTP._normalize_secret(secret)` and `KronOTP._totp(secret)` are ordinary Python attributes with underscore-prefixed names, **not supported public APIs**. Their signatures and return values may change without a public API version promise.

## Error and cross-language comparison

| Scenario | Node.js | Python |
| --- | --- | --- |
| Valid key, generate | `string` | `str` |
| Invalid key, generate | `TypeError` | `ValueError` |
| Valid current or adjacent token | `true` | `True` |
| Wrong token length/format | `false` | `False` |
| Invalid key, verify | `false` | `False` |
| Custom time/algorithm/digits | No exposed option | No exposed option |
| Account storage/issuer/QR data | Not included | Not included in library |
| OTP single-use/replay block | Not included | Not included |

**Upgrade warning:** v1.0.0 could throw `TypeError` on JavaScript verify of bad secret; v2 normally returns false. v2 also rejects short Base32 keys that legacy consumers may have used. Plan a major-version migration and reprovision weak keys.

## Not part of the public library

`python/tests/gui/app.py` defines a **source-only** `Authenticator` UI, `load_pypi_engine()`, `parse_auth_input()` and account management methods. `python/tests/gui/vault.py` defines `AccountVault`, `VaultError` and `validate_accounts()` for Windows DPAPI storage. **These modules ship in the Git repository, not inside the PyPI wheel**, and are implementation details of the optional application, not supported KronOTP package interfaces.

The libraries do **not** expose exceptions named `KronOTPError`, server middleware, an HTTP client, CLI, webhooks, TypeScript declarations, plugin registry or async APIs.

[Quickstart](./QUICKSTART.md) · [Architecture](./ARCHITECTURE.md) · [Compatibility](./CONFIGURATION_AND_COMPATIBILITY.md) · [Integration](./INTEGRATION_GUIDE.md)
