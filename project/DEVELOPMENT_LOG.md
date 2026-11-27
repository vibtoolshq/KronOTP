# Verified Development & Phase Log

This **Git-tracked, sanitized** history records implementation locations, reasons, baselines and verification. Private scratch plans and investigation drafts stay in local ignored `notes/`. Historical phase dates not independently confirmed here are intentionally not fabricated.

| Phase / work | What was implemented and why | Tracked commit | Verification / status |
| --- | --- | --- | --- |
| 01 — scaffold | Monorepo folders, JS/Python placeholder files and LICENSE stub | `b5815ab3067b1e55980118d1511df6a159a33781` | GitHub–Local synced; complete |
| 02 — configuration | Root ignore/README, JS package metadata, Python build metadata | `7e99125fb937d616c6acc3a47ffa4a7cb76b563a` | Config checks; complete |
| 03 — JS engine | `KronOTP` JS generate/verify and basic tests | `d9264092cabc943f75f10d5f78f7ab91021c0878` | Node smoke pass; complete |
| 04 — Python engine | `KronOTP` Python generate/verify and tests | `2845714b97b1b7085e5c5181462c97e7335bb8ff` | Implemented; initial Python CI failure surfaced later |
| 4.5 — conditional CI | `.github/workflows/ci.yml` path-filtered jobs | `048d356647fa610b731da469957fdda8a2f43736` | Initial Python tests failed; hotfix followed |
| 4.5 — CI test fixture fix | Changed short Python test secret to 160-bit valid fixture | `ac8d273c29b1b72feede8a5b0fd99b84286659e3` | CI Python 4/4 PASS; complete |
| 05 — integration & publishing guide | `docs/AUTOMATION_AND_PUBLISHING.md` | `e12ff5fced095a31173a5e6802ea56d6ced0e72f` | Documentation synced |
| Release preparation | Added `release.yml`, version/metadata, lockfile, MIT licenses and module READMEs | `e77155eefd7d18d49fcde489b510f4fd8df5d797` | CI+release validation PASS |
| v1.0.0 release | Annotated tag on release-prep commit, npm and PyPI 1.0.0 publication | Tag `v1.0.0` → `e77155eefd7d18d49fcde489b510f4fd8df5d797` | GitHub Actions release run `43835128215` SUCCESS |
| Published-package checks | Added `.github/workflows/registry-smoke.yml`; npm/PyPI download-install tests | `50df7c42c0d1d83d21fe68097e0d70e46b0ef064` | Workflow run `43836244524` both PASS |
| 2026-11-16 — documentation infrastructure | Ignored private `notes/`, new `AGENTS.md`, technical maps and public user guides; per-folder README/MINIFEST requirements | `51ccd1fe9913faa385a2d802199279240a381333` (initial implementation) | `git check-ignore` confirmed private notes excluded, project/docs tracked, GitHub–Local synced, patch check PASS, no engine/workflow changes; **CLOSED** |

## Per-change log template (append for each future phase)

```text
Date (YYYY-MM-DD) | Phase or ticket | Scope lock | Reason/root cause
Paths and functions changed | Implementation details | Tests (PASS/FAIL/SKIPPED)
Commit SHA | GitHub/Local baseline | Release tag (if any) | Gaps | CLOSED / BLOCKED
```

### Maintenance and integrity

- Before an edit, write the planned scope to private local `notes/`, not here.
- Include **verified** changelog details in this file *alongside* each code/config update; do not defer until a future release.
- Keep `FILE_MAP.md`, `FUNCTION_REFERENCE.md` and CI guides synchronized with implementation.
- No source logic, package version, GitHub workflow or public release is modified by this documentation-only phase.

## 2026-11-16 — Documentation infrastructure verified close-out

- **Scope**: Documentation-only, with root `AGENTS.md`, `.gitignore`, private local `notes/`, tracked `project/` and tracked `docs/`.
- **Implementation commit**: `51ccd1fe9913faa385a2d802199279240a381333`.
- **Verification evidence**: three private notes ignored under `.gitignore:49:/notes/`; `git ls-files notes` returned no paths; root GitHub file tree contained no `notes/`; local `main` and `origin/main` matched and status was clean after the fast-forward pull; `git diff --check` passed.
- **Existing functionality**: JavaScript/Python engine sources, package manifests, tests, release workflows and published v1.0.0 tag were not modified. CI workflows' configured path filters did not trigger for this documentation-only commit.
- **Follow-up**: This row records the initial implementation SHA and tested state. The commit that adds this close-out record is discoverable from `git log -- project/DEVELOPMENT_LOG.md`; the commit cannot include its own SHA without changing that SHA.

## 2026-11-16 — Production Hardening P01: Secret input & error handling

- **Incoming baseline:** `b4192dc252b2a46b83bc053deea65c7b224f42b4`.
- **Scope lock:** KO-001, KO-003, KO-004, KO-008 only; JS/Python secret validation, input caps, ASCII whitespace and expected invalid-input contract.
- **Implementation:** JS+Python reject decoded Base32 keys <14 bytes; raw length >4096 or whitespace-compacted length >1024; normalize only ASCII space/tab/CR/LF/FF/VT, reject Unicode case-fold surprises and noncanonical padding; JS `verify` now returns false rather than TypeError for expected malformed secret. Normal SHA-1/6-digit/30-second ±1 step remains.
- **Compatibility:** JS callers using short keys or expecting verify to throw must migrate. Python's previously accepted exotic Unicode whitespace is now rejected. This is a development `main` change; npm/PyPI `1.0.0` unchanged. No new version/tag/publish.
- **Actual files:** `javascript/src/kron-otp.js`, `python/src/kron_otp.py`, both test files, affected `project/` and `docs/` reference and module READMEs.
- **Implementation commit:** `30e02b1456e59f383121bdb1e9be9210cf9f1d00` (GitHub `main`); Windows local fast-forward pulled. Follow-up documentation-only patch-audit closeout commit is visible in Git history.
- **Focused verification:** Node P01 test PASS; Python P01 unittest **6/6 PASS**. GitHub [CI run 43847176070](https://github.com/vibtoolshq/KronOTP/actions/runs/43847176070): detect, Node and Python jobs all SUCCESS. GitHub [release validation 43847175995](https://github.com/vibtoolshq/KronOTP/actions/runs/43847175995): validation SUCCESS, npm and PyPI publishing SKIPPED. Source patch whitespace/scope check PASS; GitHub/local HEAD matched after initial pull.
- **Patch audit:** No new P01 engine defect detected by targeted cases; corrected outdated `project/`/`docs/` descriptions without modifying runtime in closeout. All KO-001/003/004/008 addressed **on development main only**. P02 epoch bug and P03/P04 security/CI requirements remain OPEN.

## 2026-11-16 — Production Hardening P02: time correctness and deterministic source tests

- **Incoming baseline:** `3c14a1bd284f6ad91c758a6a7e566246d6a7a1b1`, P01 CLOSED.
- **Scope Lock:** KO-002 Python epoch-boundary bug, KO-005 deterministic regression gaps only; no public API, dependency, workflow or publishing change.
- **Root cause:** PyOTP 2.12 `TOTP.verify(valid_window=1)` evaluates negative counter −1 first when time is 0–29s since Unix epoch and raises `ValueError`; KronOTP previously returned `False` even for a correct token.
- **Implementation:** Python `verify` snapshots system time and at counter zero checks only current and next valid counters via PyOTP's zero-window verify; at all other times retains the original ±1 window. Original secret validation, SHA-1/6/30, boolean result semantics and stateless behavior remain unchanged.
- **Deterministic tests:** Shared public-only `python/tests/totp_vectors.json` with six RFC SHA-1 last-six-digit outputs and 80 independent synthetic vectors, consumed by both JS and Python source test suites; additional boundary tests 0,1,29,30,59,60,61, ±1, two-step-outside and leading zeros. No new dependency or runtime timestamp API.
- **Tracked files:** `python/src/kron_otp.py`, both engine test suites, `python/tests/totp_vectors.json`, relevant technical/public docs and file map.
- **Publishing boundary:** npm/PyPI 1.0.0 not updated; no tag/version or workflow changes. CI and patch audit closeout evidence: recorded in local private phase note and ensuing Git history after execution.

### P02 verified phase closure — 2026-11-16

- **Implementation commit:** `068e11dd5a9221bf3a5d1f42eea93d8a03adf602` (original incoming `3c14a1bd284f6ad91c758a6a7e566246d6a7a1b1`).
- **Observed focused tests:** local Node `npm test` PASS (6 fixed RFC + 80 independent cross-language reference vectors), local Python `unittest` **9/9 PASS** (including epoch 0,1,29,30,59,60,61, drift window, leading zeros and 80 reference comparisons).
- **GitHub Actions:** [KronOTP CI run 43851819951](https://github.com/vibtoolshq/KronOTP/actions/runs/43851819951) — detect changes, JavaScript tests and Python tests all SUCCESS.
- **Patch audit:** `git diff --check` PASS; 11 changed paths are only Python `verify`, source tests/shared fixture and affected project/docs; JS runtime blob unchanged; module versions, dependencies, CI/release workflows and npm/PyPI artifacts unchanged. No release workflow run was triggered for this phase; no tag or publication.
- **Result:** KO-002 and KO-005 resolved **on development main**. P02 CLOSED after source CI and Git sync; P03 pending separate approval. GitHub/local final HEAD is recorded in the local private phase note.

## 2026-11-16 — Production Hardening P03: CI & release workflow configuration

- **Incoming baseline:** `7f0a0cc34f7c6dabd4f43cde12963dc7c07083fe`; P01/P02 were closed.
- **Scope Lock:** KO-006 dependency consistency, KO-010 version-aware published smoke, KO-007 workflow security and actual GitHub main/tag protection, with exact listed three YAML files and relevant technical/public Markdown only.
- **Implemented in source:** Node `npm ci` instead of `npm install`; Python `pip install -e .` from `pyproject.toml`; verified SHA-pinned official/paths-filter Actions; tag **push only** publishers and current-main-HEAD tag requirement; unnecessarily broad npm id-token permission removed; smoke resolver validates requested SemVer, manifests fallback and exact installed artifact version in both registries.
- **Unchanged:** JS/Python engines/tests, package names, versions, dependencies, lockfile, README and `v1.0.0` public registries. No tag creation or publishing.
- **Governance blocked:** GitHub main `protected:false`, rulesets `[]`, protection API 403, no administrative ruleset writer in connected integration. Code changes cannot implement or confirm branch/tag restrictions; KO-007 remains OPEN. No owner risk acceptance given.
- **Verification, commit and final phase status:** See the later dated closeout entry and local ignored P03 note for actual test jobs/commit IDs. Do not mark full P03 CLOSED unless actual branch/tag protections have been verified.

### P03 workflow patch verification — partial completion, governance BLOCKED

- **Implementation commit:** `10107e53ab68afc83414c1cb0fd542963aa50852` from incoming `7f0a0cc34f7c6dabd4f43cde12963dc7c07083fe`.
- **CI** [43855173877](https://github.com/vibtoolshq/KronOTP/actions/runs/43855173877): Node & Python tests SUCCESS; **registry smoke** [43855173893](https://github.com/vibtoolshq/KronOTP/actions/runs/43855173893): resolver/npm/PyPI 1.0.0 exact-version install tests SUCCESS; **release validation** [43855173879](https://github.com/vibtoolshq/KronOTP/actions/runs/43855173879): SUCCESS, both publish jobs SKIPPED. Local resolver 7/7 allowed/rejected input cases passed without registry calls.
- **Patch audit:** 9 changed tracked paths only (3 workflows, related `project/`/`docs/` Markdown). `git diff --check` PASS, engine/manifest Git blob SHAs unchanged, local fast-forward pull completed, ignored private notes not in tracked tree.
- **Governance no-go:** `main` still `protected:false`, rulesets `[]`, protection API 403 by connector; no ruleset writer. **KO-006 and KO-010 config/test changes verified; KO-007 is NOT CLOSED. P03 is BLOCKED**, pending authorized GitHub admin configuration and verification, not P04-ready under documented roadmap. No tag or npm/PyPI publication.

### P03 scoped post-patch correction: compatible required CI check

- P03 patch audit found documentation-only pull requests would not receive an available required check with the original path-filtered PR trigger. Changed `.github/workflows/ci.yml` only to always run detection on PRs, run Node/Python selectively, and aggregate affected checks under a single `Required CI` job; CI workflow/release/smoke YAML changes trigger both engines.
- This does **not** configure repository protection. Full P03 remains BLOCKED on GitHub main/tag settings even if corrective CI is green. Final follow-up commit and CI run are recorded in local private notes/Git history.

## 2026-11-16 — Expedited v2.0.0 release preparation

- **Incoming baseline:** `e4ff4bc4a318f75829856db2716ee3cb57188f51`; published v1.0.0 historical tag preserved.
- **Owner authorization:** user explicitly requested to bypass/defer GitHub main/tag governance protection and release now. P03's KO-007 stays OPEN; P04 remains NOT TESTED. This is an exception to the five-phase sequence, not an assertion all phases are CLOSED.
- **Versioning:** bump npm `kron-otp` and PyPI `kron-otp` from 1.0.0 to **2.0.0** (major due to JS verify-error contract and weak-secret acceptance breaking changes); synchronize npm lockfile root version. Update user/technical docs and migration warnings in same source-controlled preparation commit.
- **Scope:** metadata and truthful documentation only; engine source and tests, dependencies, CI/release workflow files, v1.0.0 tag unchanged. Actual publishing and public-artifact check outcomes should be added only after jobs complete.

## 2026-11-16 — Expedited v2.0.0 release verified

- **Version preparation commit:** `eefafd9934a44243879068d9b8081005e68aeade`, including versioned npm/PyPI manifests, npm lockfile and accurate migration/user docs; no engine, tests, dependency or workflow source changes in that commit.
- **Published new annotated tag:** `v2.0.0` at `eefafd9934a44243879068d9b8081005e68aeade`. Historical `v1.0.0` unchanged. Git tag push succeeded without force.
- **GitHub Actions release** [43867458691](https://github.com/vibtoolshq/KronOTP/actions/runs/43867458691): validation SUCCESS, Publish npm SUCCESS, Publish PyPI SUCCESS; npm uploaded `kron-otp@2.0.0`, PyPI uploaded `kron_otp-2.0.0-py3-none-any.whl` and `kron_otp-2.0.0.tar.gz`.
- **Public artifact validation:** exact 2.0.0 npm tarball downloaded then installed into a temporary clean Node consumer; version, OTP functions and weak/invalid-secret cases PASS. Exact PyPI 2.0.0 wheel downloaded from `https://pypi.org/simple`, installed in isolated Python venv; version, OTP functions, invalid-secret cases and epoch-29 regression PASS. Default pip index initially showed only 1.0.0 (stale mirror/index), official PyPI retry succeeded. This is independent of CI source tests and confirms published installability in the tested environment.
- **Deferred security:** User authorized bypassing enforced GitHub main/tag rulesets for this release; KO-007 governance stays OPEN, P03 is **not fully CLOSED**. P04 minimum supported runtime matrix, independent dependency CVEs, target-app integration, replay/throttle controls and sustained load were **not tested**. Release is verified for the installed artifacts, **not comprehensively production/security certified**. No GitHub Release object/page was created (only tag and package uploads).

## 2026-11-16 — GUI-01: Optional Python PyPI Live TOTP Tester

- **Incoming baseline:** `3141ac891fe0db1fc7a269c02f4502a9fc8af4b1`, GitHub/local/origin synchronized and clean; pre-change Scope Lock documented in private ignored notes.
- **Authorized new scope:** add `python/tests/gui/app.py` and its README, plus related `python/README.md`, root README, technical file/architecture/security/development docs and public docs guidance. No modifications to JS/Python engine, existing tests, packaging/version, dependencies, CI/release workflows, tags or registry.
- **Implementation:** native Tkinter/ttk compact local demo. Requires the exact installed public PyPI version `kron-otp==2.0.0` and validates module origin to prevent developer source fallback; masked key entry, show/hide, Generate, real 30-second countdown and rollover refresh, current-code clipboard Copy and sanitized input error handling. No secret persistence or server authentication.
- **Package distribution boundary:** demo is a tracked GitHub example in `python/tests/gui/`, not bundled with the wheel because pyproject publishes `kron_otp.py` alone. Other product features/UI remain unchanged.
- **Verification and final commit:** record actual local Tkinter/real PyPI smoke, CI job results, scope audit and final commit in the GUI-01 closeout (do not predeclare PASS). P03 governance deferred and P04 assurance untested, unaffected.

### GUI-01 focused verification & patch audit — 2026-11-16

- **Implementation commit:** `9b86872300ec1e43d14b7e71d6bc0a69a2f4ae6d` (source/test-demo and documentation), from incoming `3141ac891fe0db1fc7a269c02f4502a9fc8af4b1`.
- **Actual published-package verification:** isolated Windows Python 3.12 virtual environment outside repository installed `kron-otp==2.0.0` and `pyotp==2.12.0` from the public official PyPI index. GUI provenance guard matched module path to installed PyPI distribution. Simulated version mismatch and source-shadow attempts were correctly rejected.
- **Actual Tkinter UI-focused verification:** real Tk root created and closed cleanly; tested masked input, Show/Hide, empty and weak secret errors, six-digit code generated by installed PyPI engine, current 30s countdown, OTP-only clipboard copy, rollover at 59→60 seconds, and clearing/disabling Copy when secret changed. All programmed checks **PASS**; no personal account data used. No manual multi-platform screenshot/visual review was performed.
- **GitHub CI:** [GUI-01 CI run 43900702231](https://github.com/vibtoolshq/KronOTP/actions/runs/43900702231) — changed modules, Python tests and Required CI **SUCCESS**; JavaScript tests **SKIPPED** correctly (no JS changes). [Release branch validation 43900702066](https://github.com/vibtoolshq/KronOTP/actions/runs/43900702066) **SUCCESS**, npm and PyPI publishing jobs **SKIPPED**.
- **Patch scope:** exactly `python/tests/gui/app.py`, `python/tests/gui/README.md`, `python/README.md`, root README, `project/FILE_MAP.md`, `project/ARCHITECTURE.md`, `project/DEVELOPMENT_LOG.md`, `project/QUALITY_AND_SECURITY.md`, `docs/README.md`, `docs/TESTING_AND_RELEASES.md` modified in implementation commit. `git diff --check` PASS, Python source blob `b9acc65300f796ca2b4cb79d7b7b83ad65d5c52c` and Node source blob `f7e17fda583d71f7ea2e5dfccc4b7463382b5240` unchanged.
- **Status:** GUI-01 tested and eligible for closure once docs-only verification commit and final GitHub/local sync succeed. No npm/PyPI package version change, tag, build or release. GUI is source-only and not bundled in `kron-otp==2.0.0`. P03 governance remains deferred and P04 assurance untested.

## 2026-11-16 — GUI-02: production-oriented Authenticator app (approved separate scope)

- **Incoming baseline:** GitHub/local `e87c91c578a01f8d300f27496ef915909534b229`, clean. Pre-change date/Scope Lock documented in private local `notes/2026-11-16-GUI-02-authenticator.md` before tracked source edits.
- **User goal:** replace minimal one-secret Tkinter tester with real-use local Auth OTP generator; retain only published KronOTP TOTP computation and the `python/tests/gui/` location. Scope includes multi-account functionality and secure opt-in Windows persistence.
- **Implementation paths:** update `python/tests/gui/app.py`, `python/tests/gui/README.md`; new `python/tests/gui/vault.py` (Windows DPAPI CurrentUser) and `python/tests/gui/test_app.py` (synthetic security/UI integration); related root/package README, technical project and public docs. No engine/runtime/public API, existing tests, package metadata, dependencies or workflows changed.
- **Features:** saved and temporary accounts; search/edit/delete; strict SHA1/6/30 `otpauth://totp` URI ingestion; automatic live code/countdown; copy with conditional 15s clear; privacy lock and five-minute inactivity timeout; pinned window, shortcuts, local `KronOTP.verify` tool.
- **Security decisions:** DPAPI ties vault to Windows user; non-Windows uses session-only mode rather than plaintext. No master password/portable backup/QR scan/server authentication; warn about memory/clipboard risks and separately retained recovery codes. App is production-oriented, not independently security-certified.
- **Verification & CI evidence:** See follow-up GUI-02 closeout entry with exact real Windows/PyPI tests, commit hash and GitHub/Local sync. No results are claimed before tests.

### GUI-02 focused QA, callback correction and verification (2026-11-16)
- **Base commit:** `e87c91c578a01f8d300f27496ef915909534b229`. New Authenticator/vault/tests/docs commit `fb4add5ee0cae0ae66826d6df1d9e9076cd25dc7`; scoped callback corrections `da4c2a7792b0e1b6810b1a243b71af583c68dd19` and `d6e19475e5a0d34cca25755ed503ccf6244ae8a3`.
- **Root cause and correction:** initial 8/8 Windows suite passed with Tcl `invalid command name ..._tick` shutdown warnings from test-invoked callbacks leaving old queued `after()` jobs. Explicitly cancel live timer/clipboard jobs at close, collapse duplicate `_tick()` scheduled jobs and cancel manually cleared clipboard callbacks. **Retest 8/8 PASS, exit 0, zero Tcl warnings.**
- **Local focused environment:** Windows Python 3.12 with isolated official PyPI `kron-otp==2.0.0`/PyOTP environment. `python -m unittest discover -s python/tests/gui -p test_app.py -v` 8 tests PASS: SHA1/6/30 URI accepted, unsupported mode/duplicate issuer rejected; DPAPI encryption with no plaintext synthetic secret in vault, readback and tamper rejection; bounded record validation; multi-account saved/temporary add/edit/delete/search/lock; no mutation after failed save; 59→60 rollover with live installed engine; 15-second clipboard ownership semantics and five-minute idle lock; Tk event-loop clean shutdown.
- **GitHub Actions** [CI 43906779325](https://github.com/vibtoolshq/KronOTP/actions/runs/43906779325): Detect changed modules, Python tests, Required CI **SUCCESS**; JavaScript tests **SKIPPED** (no JS change). The existing CI Python job tests the engine; the DPAPI/Tk GUI tests were executed locally on Windows and are **not** part of this CI workflow.
- **Scope/safety:** only `python/tests/gui/` additions/updates and related root/python README, `project/`/`docs/` Markdown; no change to Python/JS engine sources, existing engine tests, dependency/version, GitHub workflows, npm/PyPI public packages or tag. A Windows DPAPI vault is not a master-password vault; external user security audit/cross-platform QA not claimed.
- **Status:** GUI-02 verified locally and CI PASS; phase is ready to close after this docs-only verification commit and GitHub/local baseline matching.

## 2026-11-19 — DEVDOCS-01: Complete KronOTP developer documentation audit

- **Incoming verified baseline:** GitHub and Windows local `main`/`origin/main` SHA `7aaeb9703b42d4ea1d2c3b83233eb74be35707ce`; tree `bac53e0392dc8b35bb392da1d31e83d89f0c336e`, worktree clean and `notes/` Git-ignored.
- **Scope:** read the tracked repository implementation/metadata/tests/workflows and existing docs, create and reconcile only public `docs/*.md` and required developer-reference `project/FILE_MAP.md`/this log; no edits to JS/Python engines, Tkinter GUI/vault, tests, fixtures, package metadata/versions, lockfile, Actions workflows or tags.
- **Public interfaces confirmed:** Node CommonJS exports `KronOTP` class both default and named alias, with two static operations; Python `kron_otp.KronOTP` with two static operations. Total **2 class surfaces and 4 public callable methods**; no public config constructor/hooks/CLI/network service. GUI is separate GitHub-source-only, not PyPI API.
- **Documented source:** exact Node/Python entry modules, dependency versions, normalization and error semantics, 30-second/±one-step flow, Windows CurrentUser DPAPI vault, 8 GUI-focused synthetic tests, 6 RFC + 80 parity regression cases, GitHub CI/Required CI, release tag and version-aware smoke. Formal code/release tests are historical unless explicitly rerun.
- **Mismatches addressed in docs:** legacy v1.0.0-only 'current release' language, false 'no GUI in repo' statement, stale direct inventory and public/private boundary ambiguities; older automation examples clarified as external optional framework integrations.
- **Documentation structure:** compact flat public developer suite with quickstart, complete API, architecture, compatibility, integration, contribution/release, debugging, FAQ, forensic coverage & QA, existing amended installation/usage/automation/testing plus canonical `docs/MINIFEST.md` and `docs/MANIFEST.md` alias. The canonical manifest is mandatory per AGENTS.
- **Executed synthetic-code examples (current documentation task):** Node current source module `KronOTP.generate/verify` **PASS**; Python installed public PyPI v2.0.0 `KronOTP.generate/verify` **PASS** on Windows. No active TOTP credentials were used; no external/browser integration or security penetration testing performed.
- **Final QA/Git closeout:** verify new document links/manifest/source/API references and exact changed-file/whitespace scope after documentation-only commit; record actual results/commit separately. This task is not a package release or full security certification.

### DEVDOCS-01 executed QA closeout (2026-11-19)

- **Initial documentation implementation commit:** `4813faa8d9a41c8bcd631df5880bf7baee9b0687` (new public docs + corrected existing docs + maintainer file map/log); incoming clean main `7aaeb9703b42d4ea1d2c3b83233eb74be35707ce`.
- **Verified Git baseline inventory:** 41 tracked blob files in original baseline tree (52 tree entries including directories), not the earlier provisional 40 count; docs suite now 17 direct Markdown files with 10 new files and 7 updated existing docs.
- **Executed source-aware sample checks:** Python published PyPI `kron-otp==2.0.0` synchronous `generate`/`verify` **PASS**; Node current checked-out source module synchronous `generate`/`verify` **PASS** on Windows, synthetic public RFC key only. This does not imply browser/GUI live-account integration examples were executed in this documentation phase.
- **Automated documentation QA after local fast-forward pull:** 17 direct Markdown files and canonical MINIFEST exact, **110 relative internal links resolved**, **8 Python fenced source snippets parsed** and **7 JavaScript fenced source snippets parsed by Node**, public API references matched two static methods in each language, `git diff --check` PASS, 19 edited/added Markdown paths exactly within `docs/` (17) and `project/` (2), with JS/Python engines/GUI/tests/package metadata/workflows unchanged.
- **Status:** Documentation suite written and locally validated; after final docs-only closeout commit confirm GitHub main=local HEAD=origin/main clean and record exact final SHA in private local notes. No npm/PyPI publication, no tag and no new source/GUI functionality.

## 2026-11-20 — VIBDOCS-01 — Vib Docs Engine developer portal configuration

- **Frozen incoming GitHub main:** `9bb6075590902bb8b6443ecfd2a13418a4fab8af`. Developer portal schema/source specification inspected from `vibtoolshq/vib-docs-engine` commit `d88d6d57bf21e157f5bbaf767ca149ea5b48f9b5` (`docs/vibtools-config.md`, `src/utils/vibtoolsConfig.ts` and schema endpoint generator). Direct portal-hosted URLs were unreachable in this tool environment; no guesswork fields added.
- **Routing:** Added `.vibtools/docs.config.json` with canonical `$schema` URL, `schemaVersion: 1`, `docsType: developer`, `slug: kronotp`, version `2.0.0`, and single `docsPath: docs`. No unrelated `targets` and no invalid/invented `logoPath` (no image asset in repository; portal uses fallback monogram).
- **Source docs structure:** `docs/index.md` remains the only landing page with supported YAML metadata and sidebar ordering, all developer pages have valid page frontmatter. Removed duplicate `docs/README.md` (portal deletes it when index exists), removed typo `docs/MINIFEST.md` (portal would publish it incorrectly); `docs/MANIFEST.md` becomes the only canonical source inventory and is stripped on portal sync. All links to source outside `docsPath` are absolute GitHub source links rather than invalid relative traversals. Updated repository README, `AGENTS.md` and project file map to reflect this necessary portal compatibility exception.
- **Scope:** No JS/Python engine, GUI, tests, fixtures, package metadata, dependencies, workflows or release/tag changes. Official 10-point Vib Docs Engine checklist, schema+frontmatter/link/scope audit results must be recorded from actual checks; do not assert a remote portal build without one.
- **Remote execution blocker:** At task start the authorized Windows Desktop Commander was offline (last seen 3h ago); original Windows private notes/ and live local Git pull were not accessible. A private pre-change scope plan was created outside the repository in assistant temporary storage, not tracked or uploaded to GitHub. Do not mark GitHub/local synchronized until Windows connection returns and local pull/verification runs.

### VIBDOCS-01 staged checklist evidence — 2026-11-20

- Frozen schema extracted from official Vib Docs Engine `docs/vibtools-config.md`; staged `.vibtools/docs.config.json` parsed and checked against permitted schema property types/values, canonical URI, exact version, developer docsType, slug and accent, and safe docsPath. **PASS**. No speculative logoPath or targets.
- Source layout: **15 Markdown files** under docs after removing duplicate `docs/README.md` and non-stripped typo `docs/MINIFEST.md`. **14 published pages** with ordered typed frontmatter and **one source `docs/MANIFEST.md`** intentionally removed by portal sync. The staged relative Markdown links were checked across three batches and all resolve within docsPath, with out-of-root source links converted to absolute GitHub URLs. **PASS**.
- All **10 official AI Agent checklist items** were addressed (**9 PASS + logo N/A**). A live portal sync/build was not performed, and direct portal-hosted spec URLs were unavailable; the source repository contract was used.
- **Local operational blocker:** Windows Desktop Commander was offline (last seen three hours earlier). The user's ignored Windows `notes/` and local Git fast-forward pull could not be accessed; do not assert full GitHub/local sync. GitHub-only completion is separate from full project closeout.

### VIBDOCS-01 live-schema + local synchronization final evidence (2026-11-20)

- **Previously blocked Windows device now ONLINE** and current GitHub configuration commit `54a0421b441c90cdb1e9e142c58ec42601da3007` fast-forward pulled to local `main` and `origin/main`, clean worktree. The earlier offline entry documents the original blocker only.
- Both official sites returned **HTTP 200** for `/vib-docs-engine/vibtools-config.md` and `/schemas/vibtools-docs.schema.json`. Developer/users specification bodies are identical after their source comment; schemas are identical except for portal-dependent `$id`. No schema rules were guessed or altered.
- One focused Python 3.12 QA used temporary (outside repo) `jsonschema==4.23.0` Draft2020-12 and `PyYAML==6.0.2`: both live schema validations PASS; all 10 self-verification conditions satisfied (**9 PASS + logo N/A**); 14 published Markdown pages with real YAML and unique order; 15-source-file MANIFEST exact; **78 valid within-docs Markdown links**; `git diff --check` PASS; 23 scoped patch paths, JS/Python engine, GUI, tests, dependencies, workflows unchanged; `notes/` ignored.
- **Portal publishing still external:** Vib Docs Engine project registries currently do not list this repository, and no live portal ingestion/build was performed. No other repository settings, build, tag, publishing or source code modified.
- Follow-up tracked Markdown-only evidence update preserves historical logs and resolves the explicit sync blocker; final exact GitHub/local HEAD must be reverified after this follow-up commit is fast-forward pulled.

## 2026-11-20 — BRAND-01: KronOTP project and Vib Docs Engine logo

- **Scope / incoming baseline:** `54c4f27d890de3187d16b920b00f2226d2480cf4`; GitHub/local `main` clean before edit. Owner-approved existing generated blue K/stopwatch/shield/OTP image; do not redesign. Private pre-change scope locked in ignored Windows notes.
- **Asset:** Added `.vibtools/logo.webp` (96 × 96 px, 4772 bytes) as an optimized **transparent derivative** of the actual generated PNG; full-resolution source image is retained in the conversation artifact, not placed in the runtime package. Git object SHA `914d4af8ca42c25f11c100ddd2ba4ceee0b745b8` independently matched calculated source Git blob hash; source optimized asset SHA-256 `70b3260851df1c60f2366a8481ed0adebaccd714e04569bbdae5bb16bb18d19e`.
- **Configuration:** Added only root `logoPath: ".vibtools/logo.webp"` to existing `.vibtools/docs.config.json`; all frozen schema/routing/version fields remain unchanged. This is a valid WebP logo path documented by Vib Docs Engine (≤2 MB, safe relative repo location). Root README displays the new asset without creating a duplicate copy.
- **Excluded:** No edits to JavaScript/Python engines, GUI, tests, package versions/dependencies, workflows, release tags or portal registry. Targeted exact binary/config/patch verification and GitHub↔Local clean sync performed as separate acceptance; do not claim a portal build ran.

### BRAND-01 Windows acceptance and consistency (2026-11-20)

- `.vibtools/logo.webp` is 96×96, 4,772-byte transparent WebP; actual source derivative, local file and GitHub Git blob match exact SHA-256 `70b3260851df1c60f2366a8481ed0adebaccd714e04569bbdae5bb16bb18d19e` and Git blob `914d4af8ca42c25f11c100ddd2ba4ceee0b745b8`. WebP RIFF/VP8X and alpha flag PASS.
- `.vibtools/docs.config.json` only gained supported root `logoPath: ".vibtools/logo.webp"`; all existing fields unchanged, both official frozen developer/users JSON Schemas validate, and README image link/file map check PASS.
- Initial GitHub implementation commit `1697a671e10da53e9ff97b04746862be12760009` fast-forward pulled to Windows `main`: HEAD=origin/main, clean, `git diff --check` PASS, five scoped paths, engine/GUI/tests/package/workflows unchanged. No tag/release/portal sync.
- Documentation coverage now distinguishes historical pre-logo N/A from current **logo PASS**. Final docs-only closeout and local sync to be verified separately.

## 2026-11-28 — BASELINE-FREEZE-01: verified GitHub source state, local parity pending

- **Exact live source snapshot:** Public GitHub `vibtoolshq/KronOTP` `main` commit `194e2e38767668e8558d2726004ff91b0b95441c`, tree `d73182057d50f231af1c09713e1eac6b29ad5af4`; 51 tracked Git blobs + 12 directory entries, nontruncated tree. New dated record `project/BASELINE_2026-11-28.md` and 51-path exact SHA inventory `project/BASELINE_FILE_INVENTORY_2026-11-28.md`.
- **Current code and registries:** Both package manifests and live npm/PyPI latest have version 2.0.0. Node/Python exports are static `KronOTP.generate`/`verify`. GUI-02 is GitHub source-only with Windows user-bound DPAPI vault, not part of distributed PyPI. No runtime or registry package changed.
- **Historical validation:** Last observed Actions run `43906779325` succeeded for `d6e19475...`, **not** current main. Release run `43867458691` validated and successfully published npm/PyPI 2.0.0 from annotated `v2.0.0` tag targeting `eefafd9934a44243879068d9b8081005e68aeade`. No new CI or package tests performed in this baseline audit.
- **Open governance and security:** main `protected:false`, required checks enforcement `off` and repo/tag ruleset arrays empty. P03 technically hardened workflow but formal governance gate KO-007 blocked. Historic P01/P02 closed; P04/P05 not accepted. v2 annotated tag verification is unsigned; PyPI wheel/sdist lack provenance attestation. This is not independent production/security certification.
- **Developer portal:** `.vibtools/docs.config.json` developer-only v2.0.0 with `logoPath: .vibtools/logo.webp`. 15 docs Markdown files (14 published + source MANIFEST). Current Vib Docs Engine developer registry lists KronOTP and `/kronotp/` plus `/kronotp/api-reference/` were opened successfully in browser. Old registration-pending reports are superseded by this fresh evidence.
- **Legacy documentation drift:** Early portions of `project/ARCHITECTURE.md` still call JavaScript package 1.0.0; `project/FUNCTION_REFERENCE.md` retains historical language saying public package 1.0.0. Current manifests and registries show 2.0.0. Historic prose unchanged; treat it as a future targeted documentation cleanup, not the version source of truth.
- **Local blocker:** Windows Desktop Commander reported local clone device OFFLINE and alternate MyPC/VARUA connections unavailable. Local HEAD, origin/main, dirty/untracked state and private ignored `notes/` have not been verified on 2026-11-28. The 2026-11-20 sync report is historical. Full GitHub/local clean parity remains **UNVERIFIED**.
- **Documentation-only scope:** baseline/inventory Markdown and minimally linked project/root navigation and this development log. No engine, GUI, tests, package metadata, lockfile, dependency, CI workflow, GitHub settings, tag, release or registry action. Frozen source SHA is the pre-freeze code snapshot, different from subsequent documentation-only commit.
- **Planning exception disclosed:** project policy requires pre-change private ignored notes, but local device unavailable; an out-of-repo working scope document was used instead. Do not invent a notes update; reconcile private notes after reconnection.


## P03-GOV-01 governance enforcement — 2026-11-28

Approved P03-GOV-01 scope and single-maintainer authorization unblock. Baseline b44ed3bc71c55d80f057d4953571cf10eb95d659 / tree 2fe815ede6e70227b02a5344f36c2ca48c56d3bd. On 2026-11-28 (Asia/Dhaka), P03-GOV-01 activated repository rulesets: main governance 28257893, v* tag creation 28257876 and v* tag immutability 28257888. API read-back verified active enforcement. Earlier statements that protection is unconfigured or blocked on administrator access describe the historical state, not the current settings.

Main requires a pull request and strict up-to-date Required CI from GitHub Actions (app 15368), with zero independent approvals as explicitly approved for this single-maintainer repository. Main force-push and deletion are blocked; no main bypass actors. The tag-creation ruleset permits only the authorized individual user technicelnurnobi (85743335) to bypass the creation restriction. Separate tag immutability blocks updates and deletion with no bypass. This does not prevent a sufficiently authorized settings administrator from later changing the rules themselves.

Changed only the six approved tracked Markdown documents. Existing v1/v2 tag refs were unchanged on settings read-back. Configuration read-back passed; formal P03 acceptance remains conditional on this documentation PR passing Required CI and merging normally, final Git/local parity, unchanged historical tags, and recorded closeout evidence. No release tag, publish, deployment or destructive enforcement test is authorized by this phase. P04 and P05 remain outside scope; historical v2.0.0 publication is not full production acceptance.


## P04-S02-A01 runtime qualification — 2026-11-28

Approved A01 baseline 01b10b220f8094aa5b290170a9e8b82f9256ca20. P04-S02/A01 adds `.github/workflows/p04-s02-compatibility.yml`, a PR-only compatibility qualification workflow. Eight Node and eleven Python targets (19 total) on Ubuntu 24.04 x64, Windows Server 2025 x64 and macOS 15 ARM64. Exact Python 3.10.0 is tested on Windows only; Ubuntu 3.10.x remains. Pinned actions, read-only contents permission, unchanged source tests and isolated npm/PyPI 2.0.0 consumer regressions; record runtime, dependencies, package origins and R-04 observations. Qualification acceptance is PENDING until actual dedicated CI and Required CI pass. No existing engine, dependency, workflow, governance or publishing changes.


## P04-S03 dependency and distribution qualification — 2026-11-28

Approved baseline e1613f9670c44c4c20f56c4aaffebe3474d8d9fd. P04-S03 adds `.github/workflows/p04-s03-security.yml`: PR-only, read-only, pinned actions on Ubuntu 24.04. Checks locked npm and isolated public v2 consumer graphs, independent Python source/consumer dependency audits using pip-audit 2.10.1, and official npm/PyPI v2 archives against registry digests, safe payload paths and pinned release source. Registry signatures/provenance metadata are observations, not verified publisher attestations; independent publish jobs are non-atomic. No engine/dependency/UI/publisher changes. Qualification acceptance PENDING until dedicated CI and mandatory Required CI PASS; final evidence in acceptance handoff.


## P04-S04 synthetic consumer qualification — 2026-11-28

Approved baseline 3f70db522abbdbe419cb975367dbf08bc85d8730. P04-S04 adds `.github/workflows/p04-s04-consumer.yml`, `qualification/p04-s04/node-consumer.cjs` and `qualification/p04-s04/python_consumer.py`. PR-only isolated public v2.0.0 consumers exercise 12 named scenarios per engine: RFC current, adjacent, expiry, malformed, wrong account, stateless repeat, replay rollover/recovery, isolation, throttling/reset, rollback denial, concurrent duplicate and concurrent attempt budget. Synthetic caller transaction serializes check/verify/reserve using Node owner event loop and Python thread lock; 8 concurrent requests per case. 120s conservative token reservation, rolling 3/60s attempts, no matched counter inference. Collision tradeoff, single-process state and distributed atomic storage requirement remain; not production authentication, no external accounts. Qualification PENDING until dedicated and mandatory CI PASS. No public API, engine, GUI, dependency, existing workflow or release change.


## P04-S05 bounded performance qualification — 2026-11-28

Approved baseline 129f2950c2baa4779af00cfe4c1f262fbc3e48fe. P04-S05 adds `.github/workflows/p04-s05-performance.yml`, `qualification/p04-s05/benchmark.cjs` and `qualification/p04-s05/benchmark.py`. PR-only Ubuntu24 Node24/Python3.12 isolated public v2 consumers; fixed RFC correctness, monotonic measurement, 20 cold starts, 1000 warm-up operations, 10000 generate and 10000 verify, 1/4/8 independent process workers (2000 operations each), 600s sustained with >=5ms between pair starts, 10s RSS sampling, 20min job timeout. Reports nearest-rank p50/p95/p99, throughput, CPU and RSS, worker results, runtime/dependencies/hardware. Observation only; no numeric SLA. Zero unexpected errors/mismatches/OOM/timeout required. Timing includes deterministic clock shim and process startup where identified. No production load or engine/API/GUI/dependency/existing workflow changes. Acceptance PENDING until actual qualification and mandatory CI PASS.
