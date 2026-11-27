---
title: "Integration Engineering"
description: "Integrate the synchronous KronOTP API into authorized applications while implementing account binding and replay protection."
order: 60
draft: false
---

## P04 consolidated qualification — 2026-11-28

**Current status (2026-11-28):** P01–P03 closed; P04 qualification evidence verified and consolidation acceptance pending this documentation PR and final closeout. P05 final production/release acceptance has not started. Older dated statements below about deferred governance, unexecuted P04 tests or offline clone are historical, not current status. No new package release or application change.

Both engines remain stateless synchronous six-digit SHA-1/30-second libraries, with a ±1-step verification window and boolean verify result. A successful verify does not identify the matched counter. Never infer the matched counter from the server's current counter. The relying party must bind the secret to an authenticated account/enrollment, protect it, synchronize trusted time, fail closed on clock anomalies, throttle per account and relevant abuse dimensions, atomically reserve an accepted code before granting authentication, and maintain replay state across replicas/restarts for the full acceptance horizon. Use appropriately protected replay storage; do not log secrets or OTPs. A conservative per-account code reservation spanning the full acceptance window plus boundary margin can reject coincidental equal codes from different counters. The synthetic fixtures use 120 seconds retention, 3 attempts/60 seconds and 8 concurrent requests; these are test parameters, not universal policy. They demonstrate single-process serialization, not distributed atomicity, durable storage or session issuance.

[46060701345](https://github.com/vibtoolshq/KronOTP/actions/runs/46060701345) passed 12 named scenarios per engine, including replay/rollover, throttling, account isolation and concurrent single winner. No real accounts, external authentication, distributed persistence or production rate-limit service were tested. R-04 negative-clock error classification remains OPEN: treat clock faults as operational failures, not a reason to replace a valid secret.

## Design principles

KronOTP generates and locally compares TOTP values; **your application** still needs an already-provisioned secret tied to the intended account. It does not fetch third-party 2FA secrets, perform user login, issue sessions, prevent code replay, cap attempts, or synchronize clocks. A matching local token is not sufficient proof of identity without an authenticated, rate-limited server flow.

## Node.js: synchronous library call

```js
const KronOTP = require('kron-otp');
const secret = process.env.TOTP_SECRET; // injected by your application's secret store
if (!secret) throw new Error('TOTP_SECRET must be provided by the caller');

const token = KronOTP.generate(secret);  // returns a six-digit string
const matchesLocally = KronOTP.verify(secret, token); // true/false
// Use token only in an authorized integration; do not log actual secrets.
```

Both `require('kron-otp')` and `require('kron-otp').KronOTP` resolve to the exported class. No callback, event, promise, or client initialization is necessary.

## Python: synchronous library call

```python
import os
from kron_otp import KronOTP

secret = os.environ["TOTP_SECRET"]  # caller-defined, not a built-in engine variable
code = KronOTP.generate(secret)     # str, including leading zeros
valid_locally = KronOTP.verify(secret, code)  # bool
```

Use the same Python interpreter/virtual environment that installed `kron-otp==2.0.0`. Both engines generate a code for the **current** system clock; neither method accepts an explicit timestamp. For deterministic tests, the repository's tests mock the time dependency internally; do not rely on this as a public method argument.

## Server-side 2FA verification contract (application responsibility)

A real server that uses `verify` should, independently of this package:

1. Bind a securely provisioned, high-entropy secret to a known account under authenticated enrollment.
2. Keep secrets in a protected server-side store, not in application source code or CI logs.
3. Throttle attempts by account/client and enforce account lockout/risk policies where appropriate.
4. After a matching code, atomically reject reuse for that account over the full acceptance horizon before granting authentication. KronOTP returns only a boolean; do not infer the matched counter from the current time. Use protected, durable replay state across replicas and restarts.
5. Protect sessions, enrollment/recovery and administrative recovery codes.
6. Monitor clock synchronization and consider the ±one-step acceptance window's security tradeoff.

KronOTP provides only the local TOTP check; it does not implement or export the server mechanisms described here. The library's `verify` is stateless and can return true again for a reused valid token.

## Browser automation is optional and external

The existing [automation guide](./AUTOMATION_AND_PUBLISHING.md) includes consumer examples for Playwright, Puppeteer and Selenium. **None** of those frameworks is a KronOTP runtime dependency; the samples must be installed/configured separately and selectors adapted to the user's own authorized site. KronOTP neither creates a browser nor bypasses an account's authentication.

## Optional source-only desktop integration

The [Tkinter Authenticator source app](https://github.com/vibtoolshq/KronOTP/blob/main/python/tests/gui/README.md) consumes **installed PyPI 2.0.0**, adds account selection, supported `otpauth://totp` parsing, live codes, clipboard tools and optional **Windows CurrentUser DPAPI-encrypted** saved accounts. The GUI lives under `python/tests/gui/`; `pip install kron-otp` does **not** install it. GUI methods and vault types are implementation details of this example, **not supported public APIs** of the Python package.

Only SHA1/6 digits/30 seconds are accepted by the GUI importer, matching the engine. HOTP, 8-digit TOTP, SHA256/SHA512, variable periods and QR image capture are not implemented.

## Error boundaries

- Invalid key for `generate`: JS `TypeError` / Python `ValueError`; display a generic validation error, never echo the key.
- Invalid/expired token for `verify`: `false`/`False`; distinguish this from a server authorization decision.
- Leading zeros: keep OTP as a **string**. If remote form rejects otherwise valid codes, check its enrolled secret, supported algorithm/period, server skew, expiration and account linkage.
- GUI vault unlock errors: Windows DPAPI current user/profile may not match the encrypted vault; do not overwrite or silently reset a corrupt file.

[Quickstart](./QUICKSTART.md) · [API reference](./API_REFERENCE.md) · [Debugging](./DEBUGGING.md)
