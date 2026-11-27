# Architecture & Design Decisions

## P04 consolidated qualification — 2026-11-28

**Current status (2026-11-28):** P01–P03 closed; P04 qualification evidence verified and consolidation acceptance pending this documentation PR and final closeout. P05 final production/release acceptance has not started. Older dated statements below about deferred governance, unexecuted P04 tests or offline clone are historical, not current status. No new package release or application change.

Current package metadata: Node CommonJS kron-otp 2.0.0, Python kron-otp 2.0.0. Both engines remain stateless synchronous six-digit SHA-1/30-second libraries, with a ±1-step verification window and boolean verify result. A successful verify does not identify the matched counter. Never infer the matched counter from the server's current counter. The relying party must bind the secret to an authenticated account/enrollment, protect it, synchronize trusted time, fail closed on clock anomalies, throttle per account and relevant abuse dimensions, atomically reserve an accepted code before granting authentication, and maintain replay state across replicas/restarts for the full acceptance horizon. Use appropriately protected replay storage; do not log secrets or OTPs. A conservative per-account code reservation spanning the full acceptance window plus boundary margin can reject coincidental equal codes from different counters. The synthetic fixtures use 120 seconds retention, 3 attempts/60 seconds and 8 concurrent requests; these are test parameters, not universal policy. They demonstrate single-process serialization, not distributed atomicity, durable storage or session issuance.

The source-only GUI/DPAPI app is not a published library API. P04 adds only PR-triggered qualification workflows and test fixtures under qualification/, not application components. | Hosted environment | Node.js tested versions | Python tested versions |
| --- | --- | --- |
| Ubuntu 24.04 x64 | 20.19.0, 22.23.5, 24.22.3, 26.13.1 | 3.10.22, 3.11.18, 3.12.16, 3.13.18, 3.14.10, 3.15.2 |
| Windows Server 2025 x64 | 20.19.0, 24.22.3 | 3.10.0, 3.10.11, 3.12.10 |
| macOS 15 ARM64 | 20.19.0, 24.22.3 | 3.10.11, 3.12.10 |

19 selected targets, 38 source/installed v2.0.0 suites passed in [46058729635](https://github.com/vibtoolshq/KronOTP/actions/runs/46058729635). Exact Python 3.10.0 on Ubuntu 24.04 was not tested; its lower-bound target was explicitly relocated to Windows. These are observed combinations, not an exhaustive Cartesian product or guarantee of every future patch, platform or dependency resolution. Declared floors remain Node >=20.19.0 and Python >=3.10.

Verified against tracked source at baseline `50df7c42c0d1d83d21fe68097e0d70e46b0ef064` (2026-11-16). This is an **npm/PyPI library monorepo**. There is **no product UI, HTTP server, database, queue, background worker, persistent secret store, or application page** in the published libraries. GUI-02 extends the *source-only, standalone Tkinter Authenticator application* under `python/tests/gui/` with multi-account management and optional Windows DPAPI-encrypted storage; the app is NOT packaged in PyPI.

## Components and boundaries

```text
Consumer app (owns authentication and provisioned TOTP secret)
    ├── Node.js → npm kron-otp → javascript/src/kron-otp.js → otpauth (SHA-1 HMAC)
    └── Python  → PyPI kron-otp → python/src/kron_otp.py → pyotp (SHA-1 HMAC)

CI: .github/workflows/{ci,release,registry-smoke}.yml
```

The library does **not** discover or obtain shared secrets. The caller supplies a Base32 provisioning secret. Both engines normalize it, construct a local TOTP generator, compute six-digit codes from current system time (30-second steps), and optionally verify a supplied token against a ±one-step clock window.

## Node.js engine

- Package: `javascript/package.json` — `kron-otp` version `2.0.0`, CommonJS; entry `src/kron-otp.js`, Node >=20.19.0.
- Dependency: `otpauth@^9.6.0`; lockfile `javascript/package-lock.json` pins `otpauth@9.6.0` and `@noble/hashes@2.4.0` for repo installs.
- P01 `KronOTP.#createTOTP` enforces ASCII Base32 normalization, raw <=4096 and compact <=1024 characters, >=14 decoded bytes and canonical round-trip before constructing SHA1/6/30 `OTPAuth.TOTP`; `verify` returns false for expected invalid input.
- Static `generate` and `verify` methods are exported both as `module.exports = KronOTP` and `module.exports.KronOTP`.

## Python engine

- Distribution: `python/pyproject.toml` — `kron-otp` version `2.0.0`, import `kron_otp`, Python >=3.10, setuptools single module under `python/src/`. The GUI-01 demo under tests is not an installed module.
- Dependency: `pyotp>=2.12,<3` — performs SHA-1 HMAC/time-step OTP logic. This version requires a Base32-decoded secret of at least 14 bytes.
- P01 `_normalize_secret` validates ASCII-only Base32, raw <=4096/compact <=1024 characters and >=14 decoded bytes with canonical round-trip. `_totp` creates `pyotp.TOTP` with SHA-1, six digits, interval 30.
- `generate` uses `.now()`; `verify` uses `.verify(valid_window=1)`.

## Secret and verification flow

1. The **consumer** provisions and protects a Base32 TOTP secret via its own secure account setup.
2. It injects the secret into code at runtime (e.g. a secret manager/environment variable), never hardcoding an active secret.
3. Generator validates up to 4096 raw chars / 1024 cleaned Base32 chars, removes only ASCII whitespace, then enforces >=14 decoded bytes and canonical encoding. Language-native `generate` exceptions remain distinct; `verify` rejects malformed inputs as false/False.
4. The dependency computes the TOTP value derived from synchronized time and secret; KronOTP returns a string including any leading zeros.
5. Verification checks format and accepts the current or adjacent 30-second step. **No used-code record is stored**, so replay defense/rate limiting must be implemented by the authenticator server.

## What is *not* implemented

No built-in provisioning URI/QR UI, multi-account management, storage, issuer configuration, custom algorithm/digits/step public API, webhook, app dashboard, browser button, worker scheduler, CLI, secret recovery, replay ledger, or rate-limit service. The source-only GUI-01 test window is a local consumer example, not a package API or authentication service. Documentation must not imply otherwise.

## Key technical decisions

- Two independent language implementations with narrow static methods; no cross-language runtime bridge.
- Node CommonJS and Python module are published separately to npm and PyPI.
- Runtime 6-digit SHA-1 TOTP; verify allows ±one step. P01 accepts >=14 decoded-byte canonical Base32 in both wrappers; for provisioning prefer a cryptographically randomly generated >=160-bit secret.
- Dependencies are external and versioned by manifests. Do not describe either wrapper as cryptographically independent from `otpauth`/`pyotp`.
- CI and publishing run via GitHub Actions. Source docs, private planning and user guides occupy separate zones governed by `AGENTS.md`.

## P01 scope boundary

The development `main` input hardening is not yet included in public `v1.0.0` artifacts. Python epoch-start verification, CI pipelines, public versions and user-facing application layers remain unchanged; those belong to later approved phases.

## GUI-01 source-only PyPI integration boundary

The optional `python/tests/gui/app.py` uses Python standard-library Tkinter. On startup it requires installed distribution `kron-otp==2.0.0`, compares the resolved `kron_otp.py` module path to the distribution metadata and rejects importing the repository source or a different installed version. The GUI calls `KronOTP.generate(secret)`; it never implements its own TOTP HMAC. The user must press Generate first; a Tkinter `after()` callback updates time remaining and refreshes the OTP on period boundaries while the secret is unchanged. Editing the secret clears state. No filesystem or network persistence, no new runtime dependency, no PyPI GUI packaging and no engine/API modification.

## GUI-02 — local Authenticator architecture

```text
python/tests/gui/app.py (Tkinter/ttk user interface)
  ├── installed PyPI kron_otp.KronOTP.generate / verify (SHA1 / 6 / 30 only)
  ├── python/tests/gui/vault.py (Windows-only DPAPI CurrentUser encrypted vault)
  │     └── %LOCALAPPDATA%/KronOTP/vault.dat (encrypted JSON envelope)
  └── optional in-memory one-off account; clipboard conditional expiry / idle lock
```

- **Engine isolation:** `load_pypi_engine()` requires installed `kron-otp==2.0.0` and the exact installed module filesystem origin, blocking accidental source shadowing. No custom OTP implementation, algorithm change or new dependency.
- **Data flow:** account form accepts own Base32 secret or `otpauth://totp` (SHA1/6 digits/30s only), engine validates by generating a code, optional Windows saved record goes through DPAPI **before** live account state updates; temporary records stay in memory. Selecting an account calls the engine to generate a six-digit code; a timer updates countdown and refreshes at a step boundary. Local check delegates to engine `.verify` but does not authenticate any site.
- **Storage threat model:** Windows `%LOCALAPPDATA%/KronOTP/vault.dat` is encrypted by Microsoft CurrentUser DPAPI; no plaintext files/exports. Decryption requires the same Windows user profile, not a separate app password. Vault validates account count/schema, rejects symlinks/bounded malformed files and writes encrypted payload with atomic replace. Running malicious code in the same unlocked OS account can still access secrets. Python process memory and the OTP clipboard are not zeroizable secure enclaves.
- **Privacy controls:** secret entry masked, explicit Save or Use once, local-only search, App Lock clearing memory, five-minute inactivity timeout, clipboard conditional clearing after 15 seconds. The app has no server sessions, user verification, QR camera, cloud sync, portability, cross-device recovery, online backup, replay denial or throttling. Tests use public synthetic fixtures.
- **Packaging:** Tkinter app/vault are GitHub source examples outside `python/src/`, not installed by PyPI; the published engine, JS engine, CI workflows and package versions remain unchanged.
