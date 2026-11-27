# KronOTP

## P04 consolidated qualification — 2026-11-28

**Current status (2026-11-28):** P01–P03 closed; P04 qualification evidence verified and consolidation acceptance pending this documentation PR and final closeout. P05 final production/release acceptance has not started. Older dated statements below about deferred governance, unexecuted P04 tests or offline clone are historical, not current status. No new package release or application change.

Published packages remain v2.0.0. | Hosted environment | Node.js tested versions | Python tested versions |
| --- | --- | --- |
| Ubuntu 24.04 x64 | 20.19.0, 22.23.5, 24.22.3, 26.13.1 | 3.10.22, 3.11.18, 3.12.16, 3.13.18, 3.14.10, 3.15.2 |
| Windows Server 2025 x64 | 20.19.0, 24.22.3 | 3.10.0, 3.10.11, 3.12.10 |
| macOS 15 ARM64 | 20.19.0, 24.22.3 | 3.10.11, 3.12.10 |

19 selected targets, 38 source/installed v2.0.0 suites passed in [46058729635](https://github.com/vibtoolshq/KronOTP/actions/runs/46058729635). Exact Python 3.10.0 on Ubuntu 24.04 was not tested; its lower-bound target was explicitly relocated to Windows. These are observed combinations, not an exhaustive Cartesian product or guarantee of every future patch, platform or dependency resolution. Declared floors remain Node >=20.19.0 and Python >=3.10.

Production use should choose current security-patched upstream-supported runtimes, not merely the declared minimum. At 2026-11-28, the Node release information lists 22/24/26 LTS and 20 EOL; Python 3.10 reached its scheduled October 2026 EOL, while 3.11–3.15 are within their upstream support windows. Prefer a maintained Node LTS and maintained stable Python (e.g. 3.14 with current patches); verify the current lifecycle and OS/vendor patch availability before deployment. See [Node release status](https://nodejs.org/en/about/previous-releases) and [Python version status](https://devguide.python.org/versions/). The historical minimum-version tests do not recommend obsolete or unpatched runtime binaries.

Both engines remain stateless synchronous six-digit SHA-1/30-second libraries, with a ±1-step verification window and boolean verify result. A successful verify does not identify the matched counter. Never infer the matched counter from the server's current counter. The relying party must bind the secret to an authenticated account/enrollment, protect it, synchronize trusted time, fail closed on clock anomalies, throttle per account and relevant abuse dimensions, atomically reserve an accepted code before granting authentication, and maintain replay state across replicas/restarts for the full acceptance horizon. Use appropriately protected replay storage; do not log secrets or OTPs. A conservative per-account code reservation spanning the full acceptance window plus boundary margin can reject coincidental equal codes from different counters. The synthetic fixtures use 120 seconds retention, 3 attempts/60 seconds and 8 concurrent requests; these are test parameters, not universal policy. They demonstrate single-process serialization, not distributed atomicity, durable storage or session issuance.

See [qualification evidence](./docs/COVERAGE_AND_QA.md) and [compatibility](./docs/CONFIGURATION_AND_COMPATIBILITY.md). Residual review items: R-04 (Python generate at a simulated negative system clock mislabels the error as invalid secret; 22/22 diagnostic observations), missing shared vector fixture in PyPI v2 sdist (direct sdist regression not run), unsigned historical tag, unverified publisher attestations/signature authenticity, independent non-atomic npm/PyPI publishing, Python range-based dependencies, publisher secret scope and automatic post-release smoke not established. The maintainer explicitly deferred R-04 remediation/final acceptance to P05 for scoped P04 closure only. R-04 stays OPEN, not fixed or permanently waived. No other risk is implicitly accepted. Final production/release acceptance remains NO-GO pending P05 and any separately authorized remediation.

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

## Current frozen baseline for maintainers and AI agents (2026-11-28)

Before another update, read the [source/phase forensic baseline](./project/BASELINE_2026-11-28.md) and [exact 51-file Git SHA inventory](./project/BASELINE_FILE_INVENTORY_2026-11-28.md). They identify the current authoritative GitHub source snapshot separately from historic release and CI evidence. **The local Windows clone was offline on 2026-11-28; do not assume local parity.** No source/API/GUI/package release is changed by the baseline documentation.


## P03-GOV-01 governance enforcement — 2026-11-28

On 2026-11-28 (Asia/Dhaka), P03-GOV-01 activated repository rulesets: main governance 28257893, v* tag creation 28257876 and v* tag immutability 28257888. API read-back verified active enforcement. Earlier statements that protection is unconfigured or blocked on administrator access describe the historical state, not the current settings.

Main requires a pull request and strict up-to-date Required CI from GitHub Actions (app 15368), with zero independent approvals as explicitly approved for this single-maintainer repository. Main force-push and deletion are blocked; no main bypass actors. The tag-creation ruleset permits only the authorized individual user technicelnurnobi (85743335) to bypass the creation restriction. Separate tag immutability blocks updates and deletion with no bypass. This does not prevent a sufficiently authorized settings administrator from later changing the rules themselves.

Development now uses a branch, pull request, required check, normal merge and local fast-forward. Configuration read-back passed; formal P03 acceptance remains conditional on this documentation PR passing Required CI and merging normally, final Git/local parity, unchanged historical tags, and recorded closeout evidence. No release tag, publish, deployment or destructive enforcement test is authorized by this phase. P04 and P05 remain outside scope; historical v2.0.0 publication is not full production acceptance.
