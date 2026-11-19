# Configuration, Dependencies and Compatibility

## Engine configuration: fixed, not user-settable

Neither published `KronOTP` class exposes configuration options, a constructor contract, an environment configuration interface or public mutation hooks.

| Behavior | Actual fixed value | Exposed setter? |
| --- | --- | --- |
| TOTP algorithm | HMAC-SHA1 | No |
| Output | Six ASCII decimal digits as a `string` | No |
| Time step | 30 seconds from system clock | No |
| Verification tolerance | Current and adjacent time steps (one previous/next) | No |
| Secret | Canonical Base32, case-insensitive; only ASCII whitespace removed | Call input only |
| Minimum secret length | 14 decoded bytes; ≥20 random bytes recommended for new keys | No |
| Input bounds | At most 4096 raw characters, at most 1024 cleaned Base32 characters | No |
| Key persistence | None in published libraries | Caller responsibility |
| Replay limits / rate limits | None | Caller responsibility |

The published API does **not** accept a timestamp, issuer, label, digits, period, skew setting, custom hash algorithm, QR configuration, or storage path. Do not pass such arguments and assume they are used.

## Package compatibility (declared, not universally certified)

| | Node.js package | Python package |
| --- | --- | --- |
| Distribution | npm `kron-otp@2.0.0` | PyPI `kron-otp==2.0.0` |
| Declared runtime | Node `>=20.19.0` | Python `>=3.10` |
| Runtime dependency | `otpauth ^9.6.0` | `pyotp>=2.12,<3` |
| Locked source-dev transitive deps | `otpauth 9.6.0`, `@noble/hashes 2.4.0` in `javascript/package-lock.json` | Python has no equivalent committed full transitive lock |
| Module system | CommonJS (`require`) | Python module (`from kron_otp import KronOTP`) |
| Tests in workflows | Node 24 on Ubuntu | Python 3.12 on Ubuntu |
| Python GUI tested | N/A | Windows Python 3.12, installed PyPI 2.0.0 |

The Python package declares **OS Independent**, but the separate GUI's encrypted vault specifically requires Windows. No claim is made that every declared runtime, platform/architecture, high-DPI configuration or hosting environment has been exhaustively tested.

## Environment variables

**Published library:** no required or read-by-library environment variables. `TOTP_SECRET` in examples is an **application-defined** secret-storage convention, not a built-in KronOTP option.

**Browser integration examples:** may use consumer-defined `KRONOTP_SECRET`, `KRONOTP_LOGIN_URL`, `TEST_USERNAME` and `TEST_PASSWORD`. These belong to the sample automation script, not the library.

**GUI:** `LOCALAPPDATA` is inspected by `AccountVault` to locate its default Windows encrypted file; otherwise the usual Windows profile local app-data fallback is used. Do not treat this as a cross-platform vault interface. The GUI uses fixed `15_000 ms` conditional OTP clipboard clearing and `300 seconds` inactivity locking; these are source constants, not published engine options.

**Release Actions:** `NPM_TOKEN` and `PYPI_API_TOKEN` are GitHub **Secrets references** used by publish jobs only; never place their values in documentation or logs.

## Compatibility and migration from 1.0.0

- JavaScript v2 `verify(invalidSecret,token)` normally returns `false` where v1 could throw `TypeError`; adjust caller error handling.
- Both v2 engines reject secrets shorter than 14 decoded bytes and noncanonical/oversized Base32 or Unicode-only whitespace. Do not relax validation to preserve weak legacy credentials; reprovision keys securely.
- The Python epoch 0–29-second verification regression is fixed in v2 source/package.
- Historical published 1.0.0 remains unchanged; v2.0.0 is a major-version release.

See [exact API reference](./API_REFERENCE.md), [installation](./INSTALLATION.md) and [security/integration guide](./INTEGRATION_GUIDE.md).
