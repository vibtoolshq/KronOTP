---
title: "KronOTP Developer Documentation"
description: "KronOTP developer documentation for the Node.js and Python TOTP libraries, API reference, installation, integrations, architecture and security boundaries."
version: "2.0.0"
order: 0
draft: false
---

**Current distribution:** npm `kron-otp@2.0.0` (CommonJS) and PyPI `kron-otp==2.0.0` (`kron_otp` import). **Source baseline audited:** `7aaeb9703b42d4ea1d2c3b83233eb74be35707ce`, 2026-11-19.

KronOTP exposes **two operations in two languages**: generate a six-digit time-based one-time password from an already-provisioned Base32 secret, and verify an entered token locally with a one-step time tolerance. The library does not provision accounts, fetch secrets, validate remote logins, persist tokens, or enforce replay/rate limits. A separate, optional **source-only** Tkinter Authenticator lives in the GitHub repository; it is not bundled with either published library.

## Developer navigation

| Goal | Guide |
| --- | --- |
| First verified code in Node.js and Python | [Quickstart](./QUICKSTART.md) |
| Supported runtimes, install, editable checkout | [Installation](./INSTALLATION.md) |
| Exact exported class, signatures, errors, differences | [API reference](./API_REFERENCE.md) |
| Real module dependencies, data flow, GUI/vault architecture | [Architecture](./ARCHITECTURE.md) |
| Fixed algorithm settings, input bounds, compatibility | [Configuration & compatibility](./CONFIGURATION_AND_COMPATIBILITY.md) |
| Secure application integration, server obligations, example patterns | [Integration engineering](./INTEGRATION_GUIDE.md) |
| JavaScript/Python usage, common failures, migration | [Usage & troubleshooting](./USAGE_AND_TROUBLESHOOTING.md) |
| Optional browser-automation examples and publishing procedures | [Automation & publishing](./AUTOMATION_AND_PUBLISHING.md) |
| Tests, CI, registry smoke, release validation | [Testing & releases](./TESTING_AND_RELEASES.md) |
| Maintainer setup, contribution and release discipline | [Development & contribution](./DEVELOPMENT_AND_CONTRIBUTING.md) |
| Diagnosis without leaking secrets | [Debugging reference](./DEBUGGING.md) |
| Concise answers and supported limits | [FAQ](./FAQ.md) |
| Forensic inventory, public API coverage and evidence | [Coverage & QA report](./COVERAGE_AND_QA.md) |

Repository inventory is maintained in `docs/MANIFEST.md` (excluded from Vib Docs Engine publishing). The [documentation home](./index.md) is authoritative; `project/` contains maintainer technical maps and private local `notes/` remains outside Git.

## Version and responsibility boundary

- **v2.0.0:** JavaScript `generate` throws `TypeError` on invalid secret; Python `generate` raises `ValueError`. Both `verify` methods return boolean `false`/`False` for ordinary malformed secrets/tokens.
- Fixed **HMAC-SHA1, six decimal digits, 30-second step**; verification accepts adjacent steps. No public options for algorithm, interval, digits, timestamp, window width, issuer or persistence.
- A caller must maintain time sync, provision/store high-entropy secrets securely, prevent replay, throttle attempts and implement authentication/session policy. A locally matching OTP is not proof that a remote account accepted it.
- The source-only GUI can manage multiple accounts and optionally store secrets in a Windows CurrentUser DPAPI vault. That vault is not portable, not a master-password barrier and is not part of the PyPI wheel.
- GitHub branch/tag governance hardening (P03) and broader production-security/platform assurance (P04) remain deferred. Successful package publishing and targeted tests are not independent security certification.

[Repository](https://github.com/vibtoolshq/KronOTP) · [npm 2.0.0](https://www.npmjs.com/package/kron-otp/v/2.0.0) · [PyPI 2.0.0](https://pypi.org/project/kron-otp/2.0.0/)
