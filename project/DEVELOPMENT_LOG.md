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
| 2026-11-16 — documentation infrastructure | Local ignored `notes/`; new `AGENTS.md`; tracked `project/` technical A–Z map, `docs/` user guide index; README/MINIFEST requirements and changelog process | **This phase's commit to be recorded in private completion note and next tracked log update** | Documentation-only; focused verification and Git sync planned |

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
