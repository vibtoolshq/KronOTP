# Repository File & Directory Map

Source-of-truth: initial architecture baseline `50df7c42c0d1d83d21fe68097e0d70e46b0ef064`, updated for production hardening phases P01–P03 on development `main`. This map covers **tracked files and key directories**; `notes/` is intentionally untracked.

| Path | Responsibility and how/when used |
| --- | --- |
| `AGENTS.md` | This repo's mandatory privacy, pre-change planning, docs and phase-log rules; read before edits |
| `AI_INSTRUCTIONS.md` | Existing global scope-lock, coding, safety, testing, Git and stop rules |
| `.gitignore` | Prevents dependency artifacts, environments and private `notes/` from being tracked |
| `LICENSE` | Root MIT license terms |
| `README.md` | Public monorepo overview and initial install links |
| `javascript/package.json` | Node package name/version/entry, runtime dependency, test command, publishing metadata |
| `javascript/package-lock.json` | Locked npm dependency graph used by `npm ci` |
| `javascript/LICENSE` | MIT license bundled with npm distribution |
| `javascript/README.md` | Public JavaScript package usage documentation bundled in npm tarball |
| `javascript/src/kron-otp.js` | Full Node.js runtime; `KronOTP` class, Base32 handling, TOTP generate/verify |
| `javascript/tests/test.js` | Node assert tests called by `npm test`/CI, including six fixed-time RFC and 80 shared synthetic parity cases since P02 |
| `python/pyproject.toml` | PyPI metadata, setuptools build configuration, Python version and PyOTP dependency |
| `python/LICENSE` | MIT license included with Python distributions |
| `python/README.md` | Public PyPI package README and examples |
| `python/src/__init__.py` | Empty placeholder file; **not** the package's published import entry |
| `python/src/kron_otp.py` | Full Python runtime; `KronOTP` class and Base32/TOTP adapters |
| `python/tests/__init__.py` | Empty test-directory initializer |
| `python/tests/test_kron_otp.py` | Python `unittest` existing P01 input tests plus P02 fixed-time RFC/epoch/window/80-case shared-fixture regression checks |
| `python/tests/totp_vectors.json` | P02 shared, **public synthetic** SHA-1 fixed-time fixture (6 RFC and 80 independently computed key/time/OTP cases); consumed by both source suites, not part of runtime exports |
| `python/tests/gui/app.py` | GUI-02 source-only Tkinter Authenticator: account UI, URI parsing, source provenance, live OTP from PyPI engine, clipboard expiry and privacy lock; not shipped in wheel |
| `python/tests/gui/vault.py` | Windows-only standard-library DPAPI CurrentUser encrypted account storage, bounded schema and atomic encrypted writes; no plaintext backup |
| `python/tests/gui/test_app.py` | Focused Windows/Tkinter integration/DPAPI/URI/account-lifecycle tests using public RFC synthetic secret (run separately, not standard CI) |
| `python/tests/gui/README.md` | GUI-02 instructions: install from PyPI, multi-account use, encrypted storage, OS threat model and recovery limitations |
| `.github/workflows/ci.yml` | Path-filtered source tests; P03 lockfile-safe `npm ci`, Python editable install from package metadata, SHA-pinned actions |
| `.github/workflows/release.yml` | P03 secure tag-push-only publisher gating, current-main-head tag check, least-privileged token permissions, SHA-pinned action versions |
| `.github/workflows/registry-smoke.yml` | P03 strict SemVer target resolver, dynamic npm/PyPI download, install and exact-version verification; manual input and manifest-derived push default |
| `docs/AUTOMATION_AND_PUBLISHING.md` | Public Playwright/Puppeteer/Selenium integration examples and publishing steps |
| `docs/README.md` | Public developer docs boundary, navigation and maintenance requirements |
| `docs/MINIFEST.md` | Canonical direct Markdown file inventory (mandatory repository spelling, currently 17 files) |
| `docs/MANIFEST.md` | Conventional manifest spelling; compatibility link to canonical MINIFEST |
| `docs/index.md` | Complete developer-docs homepage and structured navigation |
| `docs/QUICKSTART.md` | Executable, synthetic-secret Node/Python 2.0.0 quickstart |
| `docs/ARCHITECTURE.md` | Source implementation data flow, real module mapping, GUI/vault boundaries and CI diagrams |
| `docs/CONFIGURATION_AND_COMPATIBILITY.md` | Fixed engine options, actual dependency declarations, runtime requirements and v1→v2 migration |
| `docs/INTEGRATION_GUIDE.md` | Secure server/application integration patterns, tested sync calls, optional GUI/automation boundaries |
| `docs/DEVELOPMENT_AND_CONTRIBUTING.md` | Verified local dev setup, contribution rules, workflow checks and tag-publishing safety |
| `docs/DEBUGGING.md` | Diagnostic examples, sanitized errors, runtime import and vault troubleshooting |
| `docs/FAQ.md` | Focused developer frequently asked questions and unsupported feature boundaries |
| `docs/COVERAGE_AND_QA.md` | Forensic implementation/file/API/capability coverage matrix, corrected documentation mismatches and actual QA proof |
| `docs/INSTALLATION.md` | v2.0.0 npm/PyPI installations, source editable setup, GUI source-only instructions and uninstall |
| `docs/API_REFERENCE.md` | Exhaustive public Node/Python KronOTP class and 2-static-method signatures, types, errors and limitations |
| `docs/USAGE_AND_TROUBLESHOOTING.md` | Supported library usage, source-only GUI distinction, clock/import errors and migration |
| `docs/TESTING_AND_RELEASES.md` | Exact tests and CI triggers, tag-gated publishing, public v2.0.0 verification and no-release scope |
| `project/README.md` | Developer-facing reference index and purpose |
| `project/MINIFEST.md` | Inventory of all project-folder entries |
| `project/ARCHITECTURE.md` | Actual module/dependency design and TOTP data flow |
| `project/FILE_MAP.md` | This file-to-purpose map |
| `project/FUNCTION_REFERENCE.md` | Precise engine methods, locations and contracts |
| `project/CI_AND_RELEASE.md` | CI trigger/step/release pipeline internals |
| `project/QUALITY_AND_SECURITY.md` | Actual test coverage, known gaps, security boundaries |
| `project/DEVELOPMENT_LOG.md` | Phases/commits/change history and ongoing update log |
| `notes/` | Private local-only working folder; **never included in Git or published archives** |

The above is a map, not a claim that engine-level APIs, pages, buttons or databases exist beyond their documented paths. Update this file in the same commit as any future file move/add/remove.

## DEVDOCS-01 forensic documentation inventory (2026-11-19)

The Git-tracked `docs/` folder now includes a **flat developer documentation suite**, not product UI implementation. `docs/index.md` is the developer entry; `docs/MINIFEST.md` is the exact canonical inventory, with `docs/MANIFEST.md` an alias for readers expecting the conventional name. Public engine interfaces remain solely the two static `KronOTP` operations per language. No application-source, package or workflow change is made by this documentation phase.
