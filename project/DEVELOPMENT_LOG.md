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
