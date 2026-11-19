# Quickstart — Node.js and Python

Install a **published v2.0.0** library in your own consumer project. Both examples use the **public RFC sample secret** only; do **not** use this fixed secret to secure a real account.

## Node.js (CommonJS)

Requirements: Node.js **20.19.0 or newer**, npm. In your consumer directory:

```sh
npm install kron-otp@2.0.0
```

```js
const KronOTP = require('kron-otp');
// Equivalent: const { KronOTP } = require('kron-otp');

const secret = 'GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ'; // public test fixture
const code = KronOTP.generate(secret);
if (!/^[0-9]{6}$/.test(code)) throw new Error('Invalid code shape');
if (!KronOTP.verify(secret, code)) throw new Error('Local check failed');
console.log('Local OTP generation and verification succeeded');
```

Expected: one six-digit **string** (not printed above), and a successful local verification. `KronOTP.generate` is synchronous; no constructor, `await`, API token or network call is required after dependencies are installed.

## Python

Requirements: Python **3.10+**, pip; a virtual environment is recommended.

```sh
python -m pip install kron-otp==2.0.0
```

```python
from kron_otp import KronOTP

secret = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"  # public test fixture
code: str = KronOTP.generate(secret)
assert len(code) == 6 and code.isascii() and code.isdigit()
assert KronOTP.verify(secret, code) is True
print("Local OTP generation and verification succeeded")
```

Python import uses **underscore** (`kron_otp`); pip distribution uses **hyphen** (`kron-otp`). The real shared secret must come from an account or service whose TOTP setup you control; never print or commit it.

## Take the next step

1. Replace the public example key with a securely provisioned **random ≥20-byte** Base32 secret, supplied to your code through your application's secret-management system. The engine rejects secrets shorter than **14 decoded bytes**.
2. Generate a code immediately before use; each time step is **30 seconds**. Codes can contain leading zeros; never convert them to integers.
3. Treat `verify` as **local comparison only**. A production server must add account binding, attempt limits, replay protection and controlled login sessions.

Explore [exact API contracts](./API_REFERENCE.md), [integration patterns](./INTEGRATION_GUIDE.md), [installation and development setup](./INSTALLATION.md), or [the optional source-only GUI](../python/tests/gui/README.md).
