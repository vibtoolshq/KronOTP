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
| `.vibtools/logo.webp` | BRAND-01 transparent, 96 × 96 optimized derivative of approved KronOTP blue K/timer/security icon; root README and Vib Docs Engine branding asset |
| `.vibtools/docs.config.json` | Frozen Vib Docs Engine schema v1 configuration; `docsType: developer`, `docsPath: docs`, explicit valid `logoPath: .vibtools/logo.webp`, and v2.0.0 metadata |
| `docs/MANIFEST.md` | Canonical Vib Docs Engine source inventory (15 entries); automatically excluded from portal builds |
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
| `project/BASELINE_2026-11-28.md` | Read-first dated source/phase forensic baseline, release/CI truth, unresolved gates and resume requirements |
| `project/BASELINE_FILE_INVENTORY_2026-11-28.md` | Exact blob SHA/size inventory of 51 source-snapshot files, for future Git drift analysis |
| `notes/` | Private local-only working folder; **never included in Git or published archives** |

The above is a map, not a claim that engine-level APIs, pages, buttons or databases exist beyond their documented paths. Update this file in the same commit as any future file move/add/remove.

## DEVDOCS-01 forensic documentation inventory (2026-11-19)

The Git-tracked `docs/` folder now includes a **flat developer documentation suite**, not product UI implementation. `docs/index.md` is the portal root; `docs/MANIFEST.md` is the exact canonical inventory, stripped by Vib Docs Engine. The legacy `docs/MINIFEST.md` typo and duplicate root `docs/README.md` were removed to avoid orphaned portal routes. Public engine interfaces remain solely the two static `KronOTP` operations per language. No application-source, package or workflow change is made by this documentation phase.


## P04-S02-A01 runtime qualification — 2026-11-28

P04-S02/A01 adds `.github/workflows/p04-s02-compatibility.yml`, a PR-only compatibility qualification workflow. Eight Node and eleven Python targets (19 total) on Ubuntu 24.04 x64, Windows Server 2025 x64 and macOS 15 ARM64. Exact Python 3.10.0 is tested on Windows only; Ubuntu 3.10.x remains. Pinned actions, read-only contents permission, unchanged source tests and isolated npm/PyPI 2.0.0 consumer regressions; record runtime, dependencies, package origins and R-04 observations. Qualification acceptance is PENDING until actual dedicated CI and Required CI pass. No existing engine, dependency, workflow, governance or publishing changes.


## P04-S03 dependency and distribution qualification — 2026-11-28

P04-S03 adds `.github/workflows/p04-s03-security.yml`: PR-only, read-only, pinned actions on Ubuntu 24.04. Checks locked npm and isolated public v2 consumer graphs, independent Python source/consumer dependency audits using pip-audit 2.10.1, and official npm/PyPI v2 archives against registry digests, safe payload paths and pinned release source. Registry signatures/provenance metadata are observations, not verified publisher attestations; independent publish jobs are non-atomic. No engine/dependency/UI/publisher changes. Qualification acceptance PENDING until dedicated CI and mandatory Required CI PASS; final evidence in acceptance handoff.


## P04-S04 synthetic consumer qualification — 2026-11-28

P04-S04 adds `.github/workflows/p04-s04-consumer.yml`, `qualification/p04-s04/node-consumer.cjs` and `qualification/p04-s04/python_consumer.py`. PR-only isolated public v2.0.0 consumers exercise 12 named scenarios per engine: RFC current, adjacent, expiry, malformed, wrong account, stateless repeat, replay rollover/recovery, isolation, throttling/reset, rollback denial, concurrent duplicate and concurrent attempt budget. Synthetic caller transaction serializes check/verify/reserve using Node owner event loop and Python thread lock; 8 concurrent requests per case. 120s conservative token reservation, rolling 3/60s attempts, no matched counter inference. Collision tradeoff, single-process state and distributed atomic storage requirement remain; not production authentication, no external accounts. Qualification PENDING until dedicated and mandatory CI PASS. No public API, engine, GUI, dependency, existing workflow or release change.


## P04-S05 bounded performance qualification — 2026-11-28

P04-S05 adds `.github/workflows/p04-s05-performance.yml`, `qualification/p04-s05/benchmark.cjs` and `qualification/p04-s05/benchmark.py`. PR-only Ubuntu24 Node24/Python3.12 isolated public v2 consumers; fixed RFC correctness, monotonic measurement, 20 cold starts, 1000 warm-up operations, 10000 generate and 10000 verify, 1/4/8 independent process workers (2000 operations each), 600s sustained with >=5ms between pair starts, 10s RSS sampling, 20min job timeout. Reports nearest-rank p50/p95/p99, throughput, CPU and RSS, worker results, runtime/dependencies/hardware. Observation only; no numeric SLA. Zero unexpected errors/mismatches/OOM/timeout required. Timing includes deterministic clock shim and process startup where identified. No production load or engine/API/GUI/dependency/existing workflow changes. Acceptance PENDING until actual qualification and mandatory CI PASS.


## P05-A02 — source distribution completeness (2026-11-28)

`python/MANIFEST.in` explicitly includes `tests/totp_vectors.json` in future Python source distributions. `.github/workflows/p05-sdist.yml` qualifies candidate sdist and wheel built from that sdist, strict archive paths/source bytes/metadata/RECORD, twine check, and separate 13-method source and installed-wheel regressions with all 86 shared vectors. The wheel consumer adapts only import/mock paths in a disposable copy. No runtime fixture or GUI in the wheel; no engine, dependency, version, existing workflow or publishing change. Build tools are resolved in an isolated CI environment and recorded, not a reproducibility lock. Qualification acceptance pending actual CI and verified closeout. Historical published v2.0.0 sdist remains incomplete and published v2 does not contain the R-04 source fix; no new release.


## P05-A04 — immutable release and recovery contract (2026-11-28)

New paths: `scripts/release/registry_contract.py`, `qualification/p05-a04/test_release_contract.py`, `.github/workflows/p05-a04-release-contract.yml`. P05-A04 adds a stdlib release contract helper and offline qualification tests. A release builds exactly one npm tarball and one Python sdist plus a wheel from that sdist, with strict payload, metadata, fixture and RECORD checks. Run-owned artifacts and manifest SHA-256 bind bytes to version, commit, ref, run and attempt; publisher jobs verify the same bundle. Only an initial stable tag push at current main can publish, using existing organization secrets. Public GET preflight requires all three artifacts absent; after terminal publisher outcomes the registry contract classifies all absent, exact full, partial, conflicting or unknown. Only full byte-exact results and successful publishers enable secret-free automatic exact-version registry smoke; manual/main smoke retained. No automatic partial recovery, overwrites, skip-existing or blind reruns. For recovery preserve run URL, bundle, manifest and per-file hashes/status before artifact expiry (14 days requested, subject to repository limits); separately authorize only missing exact artifacts or a new version after reconciliation. Never move/delete a tag or unpublish automatically. Registry publication is still non-atomic. Token validity/permission and policy preflight, build tool reproducibility and actual publisher provenance remain separate gates. Qualification pending actual CI and verified closeout; no live publishing in this change.


## P05-A05 — controlled release tooling (2026-11-28)

New paths: `scripts/release/requirements-build.lock` and `.github/workflows/p05-a05-toolchain.yml`. Release builds and Python publishing use isolated hash-locked tooling (50 exact package versions including build, setuptools, wheel, Twine, pip and pip-audit). Controlled Ubuntu 24.04 x64, Node 24.22.3/npm 11.19.1 and CPython 3.12.16. Build subprocesses use the locked interpreter without backend isolation/downloads. The sdist preserves verified member bytes while canonicalizing tar/gzip headers and ordering with commit-derived SOURCE_DATE_EPOCH; wheel built from that sdist. Dedicated PR qualification compares two independent fresh venv/build roots for byte-identical artifacts and checks source/installed-candidate npm/Python runtime and tooling advisory graphs. Runtime dependency ranges, engine and publishing credentials unchanged. Scope is controlled same-commit Linux rebuild, not universal reproducibility or permanent vulnerability guarantee. Production use maintained security-patched runtimes; historical compatibility is not lifecycle support. Qualification pending CI; no live publication. Token validity and registry policy remain mandatory release-preflight.


## BASELINE-FREEZE-02 — post-v2.0.1 (2026-11-28)

**[Current post-v2.0.1 baseline](./BASELINE_POST_V2_0_1.md)** and **[68-file exact pre-freeze inventory](./BASELINE_FILE_INVENTORY_POST_V2_0_1.md)** are the continuation references. The historical v2.0.0 baseline and inventory remain immutable evidence, not current status. Incoming GitHub/local/origin parity verified clean; published v2.0.1 npm/PyPI exact bytes verified; G12 accepted via recovery. Resolve the final protected documentation-freeze merge before beginning the next phase.

Six documentation paths only; exact incoming SHA `f23a9739efdeadde17a8562ab49f8506a5eba7bc`, tree `94328f842bb6a6308b1b293db12993d4ce05e6e9`; no code, tests, build, version or release change. Final freeze acceptance requires protected PR Required CI and final clean parity.
