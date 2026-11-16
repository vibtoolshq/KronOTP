# KronOTP

**KronOTP** is a small, open-source monorepo containing independent Node.js and Python TOTP generators/verifiers for authorized two-factor authentication integrations and automation.

| Module | Install | Import | Status |
| --- | --- | --- | --- |
| [JavaScript](./javascript/README.md) | `npm install kron-otp` (after first release) | `require('kron-otp')` | Implemented and tested |
| [Python](./python/README.md) | `pip install kron-otp` (after first release) | `from kron_otp import KronOTP` | Implemented and tested |

Both implementations generate six-digit SHA-1 TOTP codes with 30-second periods. Verification accepts a ±one-step clock tolerance. Use at least a 160-bit secret for cross-language interoperability; keep real shared secrets out of source control.

## Example

Node.js (from `javascript/` during development):

```js
const KronOTP = require('./src/kron-otp');
const secret = process.env.TOTP_SECRET;
if (!secret) throw new Error('TOTP_SECRET is required');
const code = KronOTP.generate(secret);
console.log('Valid code:', KronOTP.verify(secret, code));
```

Python (from `python/` during development):

```python
import os
from src.kron_otp import KronOTP

secret = os.environ["TOTP_SECRET"]
code = KronOTP.generate(secret)
print("Valid code:", KronOTP.verify(secret, code))
```

## Repository layout

```text
KronOTP/
├── .github/workflows/
│   ├── ci.yml              # Change-filtered tests
│   └── release.yml         # Validation on main, tag-triggered publishing
├── javascript/
│   ├── package.json
│   ├── package-lock.json
│   ├── LICENSE
│   ├── README.md
│   ├── src/kron-otp.js
│   └── tests/test.js
├── python/
│   ├── pyproject.toml
│   ├── LICENSE
│   ├── README.md
│   ├── src/kron_otp.py
│   └── tests/test_kron_otp.py
├── docs/AUTOMATION_AND_PUBLISHING.md
├── AI_INSTRUCTIONS.md
├── LICENSE
└── README.md
```

## Testing and releases

Run `npm ci && npm test` in `javascript/`. Run `python -m pip install -e .` then `python -m unittest discover -s tests -v` in `python/`.

GitHub Actions tests both packages. A version tag like `v1.0.0` triggers release validation and, **only after validation succeeds**, publishes to npm and PyPI using organization secrets `NPM_TOKEN` and `PYPI_API_TOKEN`. Do not push a release tag until both secrets are correctly scoped and rotated if exposed. The publishing jobs are skipped for ordinary branch pushes.

See [Automation & Publishing](./docs/AUTOMATION_AND_PUBLISHING.md) for setup, release requirements, and security notes. Publishing is not a transaction across registries: one package can be published even if the other registry rejects its upload.

## Security and license

Only use TOTP with accounts and environments you are authorized to access; protect provisioning secrets, ensure synchronized time, and apply replay prevention and throttling in the server-side authentication flow.

KronOTP is distributed under the [MIT License](./LICENSE).
