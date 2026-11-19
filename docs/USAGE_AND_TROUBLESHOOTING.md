---
title: "Usage and Troubleshooting — KronOTP v2.0.0"
description: "Practical TOTP usage, input and clock errors, version migration and source-only GUI limitations."
order: 70
draft: false
---

KronOTP's **published packages** are synchronous TOTP libraries; they have **no bundled application UI, CLI or server**. The **GitHub source repository**, separately, includes an optional Tkinter Authenticator application with account management. Distinguish the public library contract from example-app functionality.

## Integration workflow

1. Provision a random, high-entropy Base32 TOTP secret as part of an **authorized account enrollment**; the libraries do not retrieve it. Recommend ≥20 random decoded bytes, though acceptance minimum is 14.
2. Install the matching npm/PyPI v2.0.0 package; use its actual import entry and current system clock.
3. Generate a code with `KronOTP.generate(secret)`; preserve all six characters including leading zeros.
4. Use that code in a properly authorized login flow, or call `KronOTP.verify(secret, token)` for a **local** comparison.
5. For a real authentication server implement account binding, replay prevention, attempt throttling and session lifecycle yourself. Local verification is not remote account acceptance.

### Working snippets

```js
const KronOTP = require('kron-otp');
const secret = 'GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ'; // PUBLIC test vector
const code = KronOTP.generate(secret);
console.log(KronOTP.verify(secret, code)); // true (same current time step)
```

```python
from kron_otp import KronOTP

secret = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"  # PUBLIC test vector
code = KronOTP.generate(secret)
print(KronOTP.verify(secret, code))  # True (same current time step)
```

These fixed keys are for documentation/tests **only**, never real account credentials. See [Quickstart](./QUICKSTART.md) for installation and exact error contracts in [API reference](./API_REFERENCE.md).

## Troubleshooting

| Problem | Diagnosis/action |
| --- | --- |
| `Cannot find module 'kron-otp'` | Use Node >=20.19.0 and install npm dependency in the application directory; check `npm ls kron-otp` |
| `ModuleNotFoundError: kron_otp` | Install `kron-otp==2.0.0` in the **same Python interpreter** and import using underscore |
| `generate` reports invalid secret | Expected nonempty canonical Base32, ASCII-only normalized spaces, ≥14 decoded bytes, ≤4096 raw/≤1024 cleaned chars; do not log the input |
| `verify` returns false unexpectedly | Preserve token as six ASCII decimal characters, check correct enrolled secret, expiry, SHA1/6/30 configuration and clock skew |
| Remote login rejects locally generated code | Check account linkage, service parameters, expiration and remote verification policies; library cannot bypass site rules |
| Old key accepted by JavaScript 1.0.0 now fails | v2 rejects short/noncanonical inputs; securely re-enroll with adequate entropy |
| Code starts with zero and becomes shorter | Your application converted it to an integer; keep `string`/`str` |
| Time-based tests fail near Unix epoch | PyPI v2 includes Python first-step boundary fix; ensure the installed package really is v2.0.0 |
| GUI import error | Obtain `python/tests/gui/` source and install real PyPI 2.0.0 in the same interpreter; GUI checks installed module origin |
| GUI vault unreadable | Windows CurrentUser DPAPI requires original OS account/profile; preserve encrypted file and use independent recovery codes |
| Want 8 digits, SHA256/512, QR scanner or a web dashboard | Not implemented as KronOTP public package options |

## Source-only Authenticator app

[GUI guide](https://github.com/vibtoolshq/KronOTP/blob/main/python/tests/gui/README.md) describes the source-only Tkinter app: multi-account list/search/add/edit/delete, compatible `otpauth://totp` paste, temporary unsaved key, live code, 30-second countdown, OTP copy, local check and Windows DPAPI opt-in encrypted saved accounts. It is not bundled in PyPI. Windows app Lock is not a separate password barrier, DPAPI files are not portable backups, and the clipboard may expose copied OTPs briefly.

## Security and compatibility

- Preserve a separate trusted recovery mechanism for enrolled services. Never commit actual provisioning secrets or print them in CI logs.
- `verify` accepts the adjacent previous/next step and is **stateless**; it does not reject reused valid codes.
- JavaScript `generate` invalid secret → `TypeError`; Python → `ValueError`. Both `verify` implementations ordinarily return boolean false for malformed input.
- v2 is a breaking migration from v1 for previously accepted short keys and JavaScript invalid-secret exception behavior.
- CI and published package checks are not a full independent security/operating-system certification. Branch/tag repository governance and P04 assurance remain deferred.

More detail: [Integration](./INTEGRATION_GUIDE.md), [Debugging](./DEBUGGING.md), [Compatibility](./CONFIGURATION_AND_COMPATIBILITY.md).
