# kron-otp (Node.js)

A small CommonJS TOTP engine for Node.js, maintained in the [KronOTP monorepo](https://github.com/vibtoolshq/KronOTP).

## Install

```sh
npm install kron-otp@2.0.0
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
- **v2.0.0 breaking change:** `verify(secret, token)` returns `true`/`false`, including `false` for expected invalid secrets. Previous v1.0.0 threw `TypeError` on invalid secrets. Update any consumer error-handling logic before upgrading.
- Configuration remains SHA-1, 6 digits and 30 seconds. **v2.0.0:** canonical ASCII Base32, >=14 decoded bytes (112 bits), <=4096 raw chars and <=1024 cleaned chars, only ASCII space/tab/CR/LF/FF/VT removed; `generate` rejects invalid keys with sanitized `TypeError`. Recommend cryptographically random >=20-byte secrets for provisioning.
- Supported Node.js: 20.19+ (dependency requirement).

## Local tests

```sh
npm ci
npm test
```

Only use provisioning secrets for accounts you own or are authorized to automate. Keep secrets in a secret manager, do not log them, and enforce replay prevention and rate limits on the server.

See the [integration and publishing guide](../docs/AUTOMATION_AND_PUBLISHING.md).

Licensed under the [MIT License](./LICENSE).

**Migration from v1.0.0:** Short legacy keys with fewer than 14 decoded bytes now fail validation; re-provision weak credentials securely. The legacy v1.0.0 version is not overwritten. v2.0.0 includes the P01 input/contract updates. This library has no built-in rate limits or replay protection.
