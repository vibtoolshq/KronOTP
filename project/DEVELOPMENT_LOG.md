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
