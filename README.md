# KronOTP

![KronOTP project logo](./.vibtools/logo.webp)

**KronOTP** is a small, open-source monorepo containing independent Node.js and Python TOTP generators/verifiers for authorized two-factor authentication integrations and automation.

| Module | Install | Import | Status |
| --- | --- | --- | --- |
| [JavaScript](./javascript/README.md) | `npm install kron-otp@2.0.0` | `require('kron-otp')` | Implemented and tested |
| [Python](./python/README.md) | `pip install kron-otp==2.0.0` | `from kron_otp import KronOTP` | Implemented and tested |

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
│   ├── release.yml         # Validation on main, tag-triggered publishing
│   └── registry-smoke.yml  # Exact-version npm/PyPI download/install checks
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
│   ├── tests/test_kron_otp.py
│   ├── tests/totp_vectors.json  # Shared RFC and synthetic tests
│   └── tests/gui/              # Source-only Tkinter Authenticator application
│       ├── app.py             # Multi-account interface using the PyPI engine
│       ├── vault.py           # Windows DPAPI current-user encrypted account store
│       ├── test_app.py        # GUI and vault integration checks (Windows)
│       └── README.md
├── docs/                    # Developer portal docs (index.md + MANIFEST.md)
├── project/                 # Developer technical maps, history, MINIFEST
├── AGENTS.md                # Pre-change documentation and privacy rules
├── AI_INSTRUCTIONS.md
├── LICENSE
└── README.md
```

## Documentation & development records

- **Developer documentation**: [docs/index.md](./docs/index.md) — installation, complete public API, safe usage, troubleshooting, automation and release guidance.
- **Maintainer reference**: [project/README.md](./project/README.md) — architecture, full file/function maps, dependency reasoning, CI internals, known gaps and phase log.
- **Repository agent rules**: [AGENTS.md](./AGENTS.md) and [AI_INSTRUCTIONS.md](./AI_INSTRUCTIONS.md).
- **Private local-only notes**: `notes/` is deliberately ignored by Git and never published. Its `README.md` and `MINIFEST.md` remain only on an authorized developer's machine.

## Testing and releases

Run `npm ci && npm test` in `javascript/`. Run `python -m pip install -e .` then `python -m unittest discover -s tests -v` in `python/`.

GitHub Actions tests both packages. A version tag like `v1.0.0` triggers release validation and, **only after validation succeeds**, publishes to npm and PyPI using organization secrets `NPM_TOKEN` and `PYPI_API_TOKEN`. Do not push a release tag until both secrets are correctly scoped and rotated if exposed. The publishing jobs are skipped for ordinary branch pushes.

See [Automation & Publishing](./docs/AUTOMATION_AND_PUBLISHING.md) for setup, release requirements, and security notes. Publishing is not a transaction across registries: one package can be published even if the other registry rejects its upload.

## Security and license

Only use TOTP with accounts and environments you are authorized to access; protect provisioning secrets, ensure synchronized time, and apply replay prevention and throttling in the server-side authentication flow.

KronOTP is distributed under the [MIT License](./LICENSE).

## v2.0.0 compatibility and expedited release note

v2.0.0 includes the P01/P02 changes on `main`: both engines reject Base32 secrets shorter than **14 decoded bytes**, enforce raw/cleaned input limits (4096/1024 chars), and accept only ASCII whitespace normalization. **JavaScript `verify` returns `false` instead of throwing `TypeError` for expected malformed secrets**; adapt code that caught that exception. Python fixes Unix-epoch 0–29-second valid-code verification. Existing algorithm (SHA-1/6 digits/30 seconds, ±one step) and public class/method names are unchanged.

**Expedited release exception (2026-11-16):** The maintainer directed this release before GitHub main/tag governance hardening and P04 production-acceptance work are complete. Branch/tag protection and cross-platform/long-running performance/security acceptance remain open. The passing focused CI/registry checks are not a security certification. Published v1.0.0 remains immutable; registry delivery of v2.0.0 is confirmed separately by release jobs.

## v2.0.0 verified release results (2026-11-16)

- **Annotated tag:** [v2.0.0](https://github.com/vibtoolshq/KronOTP/tree/v2.0.0), release commit `eefafd9934a44243879068d9b8081005e68aeade`. Historical tag v1.0.0 not moved.
- **GitHub Actions:** [Release workflow run 43867458691](https://github.com/vibtoolshq/KronOTP/actions/runs/43867458691) — validation, npm publish and PyPI publish **SUCCESS**.
- **Official registry artifacts:** [npm kron-otp@2.0.0](https://www.npmjs.com/package/kron-otp/v/2.0.0) and [PyPI kron-otp==2.0.0](https://pypi.org/project/kron-otp/2.0.0/).
- **Independent public consumer check:** downloaded npm `kron-otp-2.0.0.tgz`, installed into clean temporary Node consumer and validated version, generate/verify, bad-secret nonmatch and short-key rejection. Downloaded official PyPI `kron_otp-2.0.0-py3-none-any.whl`, installed in an isolated Python venv and verified metadata, generate/verify, invalid inputs and Unix-epoch second 29. Both passed. Default pip index initially lagged; specifying `--index-url https://pypi.org/simple` succeeded.
- **Risk/assurance boundary:** GitHub main/tag protection was explicitly deferred by owner instruction and P04 production acceptance remains untested. v2.0.0 is **published and install-tested**, not fully security-certified; consuming applications still require replay prevention, rate limiting and secure key management.

## Optional Python GUI demo (GUI-01)

The source repository includes a small Tkinter [Live TOTP Tester](./python/tests/gui/README.md) at `python/tests/gui/app.py`. It calls the **installed published PyPI kron-otp==2.0.0 module** and lets you paste a user-owned Base32 key, view live 6-digit codes and a 30-second countdown, and copy the code. The GUI is a **source-only test/demo application**; it is not included in the npm or PyPI packages, does not store secrets and does not verify remote logins.

## KronOTP Authenticator — local desktop app (GUI-02)

**Source-only Python/Tkinter application**, designed for real daily use with the **published PyPI KronOTP v2.0.0 engine**. It now supports multiple saved accounts, issuer/name search, add/edit/delete, `otpauth://totp` URI paste, a temporary unsaved secret, live 30-second OTPs, copy with conditional 15-second clipboard clear, privacy lock and 5-minute inactivity lock. A separate local check calls the engine's `verify` method; it does not log in to any remote service.

On Windows, explicit **Save encrypted** uses DPAPI CurrentUser to protect secrets in `%LOCALAPPDATA%\KronOTP\vault.dat`; on other OSs only unsaved sessions are available. DPAPI ties saved accounts to your Windows user/profile and does **not** provide independent master-password security. Back up account recovery codes separately. No secrets are saved in the repository. The GUI is **not** bundled with the PyPI wheel and is not separately packaged as an EXE.

```powershell
python -m pip install kron-otp==2.0.0
python python/tests/gui/app.py
```

See [Authenticator usage, protection and recovery limitations](./python/tests/gui/README.md). **This is a production-oriented application, not independently security-certified**; original P03 branch/tag governance and P04 broader security/platform assurance remain uncompleted.
