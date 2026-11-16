# Architecture & Design Decisions

Verified against tracked source at baseline `50df7c42c0d1d83d21fe68097e0d70e46b0ef064` (2026-11-16). This is an **npm/PyPI library monorepo**. There is **no UI, HTTP server, database, queue, background worker, persistent secret store, or application page** in the repository.

## Components and boundaries

```text
Consumer app (owns authentication and provisioned TOTP secret)
    ├── Node.js → npm kron-otp → javascript/src/kron-otp.js → otpauth (SHA-1 HMAC)
    └── Python  → PyPI kron-otp → python/src/kron_otp.py → pyotp (SHA-1 HMAC)

CI: .github/workflows/{ci,release,registry-smoke}.yml
```

The library does **not** discover or obtain shared secrets. The caller supplies a Base32 provisioning secret. Both engines normalize it, construct a local TOTP generator, compute six-digit codes from current system time (30-second steps), and optionally verify a supplied token against a ±one-step clock window.

## Node.js engine

- Package: `javascript/package.json` — `kron-otp` version `1.0.0`, CommonJS; entry `src/kron-otp.js`, Node >=20.19.
- Dependency: `otpauth@^9.6.0`; lockfile `javascript/package-lock.json` pins `otpauth@9.6.0` and `@noble/hashes@2.4.0` for repo installs.
- `KronOTP.#createTOTP` validates and normalizes Base32, calls `OTPAuth.Secret.fromBase32`, enforces canonical round-trip, creates `OTPAuth.TOTP` with SHA1, six digits and 30 seconds.
- Static `generate` and `verify` methods are exported both as `module.exports = KronOTP` and `module.exports.KronOTP`.

## Python engine

- Distribution: `python/pyproject.toml` — `kron-otp` version `1.0.0`, import `kron_otp`, Python >=3.10, setuptools single module under `python/src/`.
- Dependency: `pyotp>=2.12,<3` — performs SHA-1 HMAC/time-step OTP logic. This version requires a Base32-decoded secret of at least 14 bytes.
- `_normalize_secret` canonicalizes Base32 using standard-library `base64.b32decode/b32encode`. `_totp` creates `pyotp.TOTP` with SHA-1, six digits, interval 30.
- `generate` uses `.now()`; `verify` uses `.verify(valid_window=1)`.

## Secret and verification flow

1. The **consumer** provisions and protects a Base32 TOTP secret via its own secure account setup.
2. It injects the secret into code at runtime (e.g. a secret manager/environment variable), never hardcoding an active secret.
3. Generator normalizes case/whitespace and validates encoding (but each language has slightly different acceptance policy; see `FUNCTION_REFERENCE.md`).
4. The dependency computes the TOTP value derived from synchronized time and secret; KronOTP returns a string including any leading zeros.
5. Verification checks format and accepts the current or adjacent 30-second step. **No used-code record is stored**, so replay defense/rate limiting must be implemented by the authenticator server.

## What is *not* implemented

No built-in provisioning URI/QR UI, multi-account management, storage, issuer configuration, custom algorithm/digits/step public API, webhook, app dashboard, browser button, worker scheduler, CLI, secret recovery, replay ledger, or rate-limit service. Documentation must not imply otherwise.

## Key technical decisions

- Two independent language implementations with narrow static methods; no cross-language runtime bridge.
- Node CommonJS and Python module are published separately to npm and PyPI.
- Runtime 6-digit SHA-1 TOTP; verify allows ±one step. For shared compatibility prefer a 160-bit Base32 secret.
- Dependencies are external and versioned by manifests. Do not describe either wrapper as cryptographically independent from `otpauth`/`pyotp`.
- CI and publishing run via GitHub Actions. Source docs, private planning and user guides occupy separate zones governed by `AGENTS.md`.
