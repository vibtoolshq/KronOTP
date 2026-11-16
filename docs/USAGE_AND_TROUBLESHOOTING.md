# Usage Guide & Troubleshooting — Development `main` P01 + P02

**Important:** The published npm and PyPI packages `1.0.0` have not been republished; this page documents P01/P02 behavior in `main`, not yet available through a new registry release.

## What kind of product is this?

KronOTP is a **library**, not an installable GUI. It has **no pages, buttons, toolbar, settings dialogs, account screens, API server, dashboard, timer animation or user click workflow**. Node.js and Python users call a class method from their own application. If you see browser fields in an automation example, they belong to the *consumer's target test application*, not KronOTP.

## Complete supported user workflow

1. **Choose a runtime**: Node.js or Python; install the published package using [Installation](./INSTALLATION.md).
2. **Provision your account normally** using an authenticator configuration that lawfully supplies a Base32 shared TOTP secret. KronOTP does not extract that value from other applications.
3. **Protect the secret** in a secret manager or injected environment variable (for example `TOTP_SECRET`). Use a securely generated **160-bit or longer** canonical Base32 value for cross-language use.
4. **Generate at time of use** with `KronOTP.generate(secret)`. A token is valid only around its 30-second step.
5. **Use the six-digit string** in your own authorized 2FA form, or call `KronOTP.verify(secret, token)` in local tests.
6. **Check the actual login result** in your application. A generated code is not proof of successful login.
7. **For server-side verification**, add your own rate limits, replay protection, attempt counters and account protection. The KronOTP wrapper contains none of these features.

## Node.js working example

```js
const KronOTP = require('kron-otp');
const secret = process.env.TOTP_SECRET;
if (!secret) throw new Error('TOTP_SECRET must be configured');

try {
  const code = KronOTP.generate(secret);
  const matches = KronOTP.verify(secret, code);
  console.log('Verification result:', matches);
} catch (error) {
  if (error instanceof TypeError) {
    console.error('The configured Base32 secret is invalid.');
  } else {
    throw error;
  }
}
```

## Python working example

```python
import os
from kron_otp import KronOTP

secret = os.environ["TOTP_SECRET"]
try:
    code = KronOTP.generate(secret)
except ValueError:
    print("The configured Base32 secret is invalid.")
else:
    print("Verification result:", KronOTP.verify(secret, code))
```

## Troubleshooting

| Problem | Why it happens / what to check |
| --- | --- |
| Cannot import `kron-otp` in JavaScript | The npm package must be installed in the **consumer project**; use `require('kron-otp')` and Node >=20.19. The hyphenated name is the npm package name |
| `ModuleNotFoundError: kron_otp` | Install the Python distribution in the **same interpreter/venv** running the code; import uses underscore `kron_otp`, not hyphen |
| OTP is six digits but remote login rejects it | Check shared secret, SHA-1/6-digit/30-second service compatibility, synchronized system clocks, user/account linkage, expired step and server-side policy. KronOTP cannot bypass a service's requirements |
| Missing/invalid Base32 secret | Use the provisioning **shared secret**, not a QR image URL, password or current six-digit code; the engine normalizes whitespace/case but rejects invalid Base32 |
| Legacy short key fails on both engines in development `main` | P01 now rejects keys below 14 decoded bytes in both languages; the published npm `1.0.0` previously accepted some short keys. Re-provision weak legacy credentials securely before upgrading; use random 20+ byte secrets for new accounts |
| `verify` returns false | Wrong token, wrong time, wrong secret or invalid format. Tokens must be **strings** with exactly six ASCII digits, including any leading zero |
| Invalid Base32 or too-long input on development `main` | Both engines reject >4096 raw chars, >1024 cleaned chars or <14 decoded bytes. `generate` throws TypeError (JS)/ValueError (Python), `verify` returns false/False. Only ASCII whitespace is ignored; Unicode BOM/NBSP is invalid |
| npm/PyPI install temporarily fails after a release | Public registry metadata/tarball distribution may propagate; inspect official registry version and download availability. Do not repeatedly publish an identical version |
| Want a QR scanner, UI button, web page or token store | Not provided by KronOTP. Add the UX/storage in your own authorized application; do not assume built-in support |
| Accidentally logged a secret | Treat it as compromised: remove from logs and rotate/regenerate the account's shared secret using its legitimate provisioning process |

## Automation

Use [Automation & Publishing](./AUTOMATION_AND_PUBLISHING.md) for Playwright, Puppeteer and Selenium code examples. The examples require your own application login URL, first-factor credentials and the already provisioned TOTP secret. Adapt selectors to your app and verify its authenticated state. KronOTP itself does not interact with browsers.

## Safe operation

Do not embed real secrets in screenshots, CI logs, code, tracked Markdown or error reports. Token generation/verification alone does not replace first-factor authentication, permission checks, replay prevention or account security controls.

## P01 development-source migration note

- The source on `main` changes JavaScript `verify(badSecret, token)` from a thrown `TypeError` to a nonmatch (`false`). Avoid relying on the old exception path when integrating a future release.
- Both engines reject short (<14 decoded bytes), oversized and non-ASCII-whitespace-containing secrets. 14–19 decoded-byte keys remain accepted for compatibility with existing PyOTP deployments; use random >=20 bytes for new provisioning.
- Input bounds: 4096 raw characters; 1024 compact Base32 characters including legal `=` padding. Normal SHA-1/6-digit/30-second verification is unchanged; P02 fixes Python's synthetic Unix-epoch 0–29s counter underflow by excluding negative drift counters while keeping normal ±1 semantics.
- The current public `1.0.0` registry packages are unchanged; do not claim P01 is already published.

## P02 clock-boundary clarification

When a deterministic test freezes the clock to Unix epoch seconds 0–29, the Python source on development `main` now verifies valid current and next-step TOTP values without raising on negative timecode −1. At normal timestamps, the existing ±one-step verification tolerance is unchanged. A real application's system clock should still be synchronized. The previously published `1.0.0` packages are unchanged; these P02 fixes are not yet published.
