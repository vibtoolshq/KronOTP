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
- `verify(secret, token)` returns `true` or `false` for a six-digit string, with ±one 30-second step tolerated. Invalid secrets throw `TypeError`.
- Configuration: SHA-1, 6 digits, 30-second period. Secrets are normalized by removing whitespace and uppercasing.
- Supported Node.js: 20.19+ (dependency requirement).

## Local tests

```sh
npm ci
npm test
```

Only use provisioning secrets for accounts you own or are authorized to automate. Keep secrets in a secret manager, do not log them, and enforce replay prevention and rate limits on the server.

See the [integration and publishing guide](../docs/AUTOMATION_AND_PUBLISHING.md).

Licensed under the [MIT License](./LICENSE).
