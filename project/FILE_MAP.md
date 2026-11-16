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
| `docs/README.md` | Public docs entry point and maintenance guidelines |
| `docs/MINIFEST.md` | All direct docs entries |
| `docs/INSTALLATION.md` | Public installation and runtime setup |
| `docs/API_REFERENCE.md` | Precise existing JavaScript/Python API and its limitations |
| `docs/USAGE_AND_TROUBLESHOOTING.md` | Supported use flow, non-existent UI clarification, troubleshooting |
| `docs/TESTING_AND_RELEASES.md` | End-user tests, published-package links and release instructions |
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
