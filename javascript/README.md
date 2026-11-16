# kron-otp (Node.js)

A small CommonJS TOTP engine for Node.js, maintained in the [KronOTP monorepo](https://github.com/vibtoolshq/KronOTP).

## Install

```sh
npm install kron-otp
```

## Usage

```js
const KronOTP = require('kron-otp');

const secret = process.env.TOTP_SECRET; // Base32 provisioning secret, not an OTP
if (!secret) throw new Error('TOTP_SECRET is required');

const token = KronOTP.generate(secret); // six-digit string
const valid = KronOTP.verify(secret, token);
console.log('Verification:', valid);
```

- `generate(secret)` returns a six-digit string, or throws `TypeError` for a malformed Base32 secret.
- On development `main` after P01, `verify(secret, token)` returns `true`/`false`, including `false` for an invalid secret. Previously published `1.0.0` throws `TypeError` for invalid secrets (a breaking migration consideration).
- Configuration remains SHA-1, 6 digits and 30 seconds. P01 `main`: canonical ASCII Base32, >=14 decoded bytes (112 bits), <=4096 raw chars and <=1024 cleaned chars, only ASCII space/tab/CR/LF/FF/VT removed; `generate` rejects invalid keys with sanitized `TypeError`. Recommend cryptographically random >=20-byte secrets for provisioning.
- Supported Node.js: 20.19+ (dependency requirement).

## Local tests

```sh
npm ci
npm test
```

Only use provisioning secrets for accounts you own or are authorized to automate. Keep secrets in a secret manager, do not log them, and enforce replay prevention and rate limits on the server.

See the [integration and publishing guide](../docs/AUTOMATION_AND_PUBLISHING.md).

Licensed under the [MIT License](./LICENSE).

**Release distinction:** Source-tree P01 input fixes are not yet published. `npm install kron-otp@1.0.0` still uses its original validation and error contract until a separately authorized release.
