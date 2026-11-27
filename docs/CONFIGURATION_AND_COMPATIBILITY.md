---
title: "Configuration, Dependencies and Compatibility"
description: "Actual fixed TOTP settings, supported runtimes, package dependencies and v1 to v2 migration guidance."
order: 50
draft: false
---

## P04 consolidated qualification — 2026-11-28

**Current status (2026-11-28):** P01–P03 closed; P04 qualification evidence verified and consolidation acceptance pending this documentation PR and final closeout. P05 final production/release acceptance has not started. Older dated statements below about deferred governance, unexecuted P04 tests or offline clone are historical, not current status. No new package release or application change.

| Hosted environment | Node.js tested versions | Python tested versions |
| --- | --- | --- |
| Ubuntu 24.04 x64 | 20.19.0, 22.23.5, 24.22.3, 26.13.1 | 3.10.22, 3.11.18, 3.12.16, 3.13.18, 3.14.10, 3.15.2 |
| Windows Server 2025 x64 | 20.19.0, 24.22.3 | 3.10.0, 3.10.11, 3.12.10 |
| macOS 15 ARM64 | 20.19.0, 24.22.3 | 3.10.11, 3.12.10 |

19 selected targets, 38 source/installed v2.0.0 suites passed in [46058729635](https://github.com/vibtoolshq/KronOTP/actions/runs/46058729635). Exact Python 3.10.0 on Ubuntu 24.04 was not tested; its lower-bound target was explicitly relocated to Windows. These are observed combinations, not an exhaustive Cartesian product or guarantee of every future patch, platform or dependency resolution. Declared floors remain Node >=20.19.0 and Python >=3.10.

Production use should choose current security-patched upstream-supported runtimes, not merely the declared minimum. At 2026-11-28, the Node release information lists 22/24/26 LTS and 20 EOL; Python 3.10 reached its scheduled October 2026 EOL, while 3.11–3.15 are within their upstream support windows. Prefer a maintained Node LTS and maintained stable Python (e.g. 3.14 with current patches); verify the current lifecycle and OS/vendor patch availability before deployment. See [Node release status](https://nodejs.org/en/about/previous-releases) and [Python version status](https://devguide.python.org/versions/). The historical minimum-version tests do not recommend obsolete or unpatched runtime binaries.

Installed public packages are exact v2.0.0; source dependency lock and consumer resolution are distinct. Python has no full committed runtime dependency lock. No fresh GUI platform qualification.

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
