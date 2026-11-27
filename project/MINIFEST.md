# Project Folder MINIFEST

Inventory of **all direct entries** of `project/` as of the 2026-11-28 baseline freeze. No subfolders are created.

| Entry | Type | Scope / phase | Details |
| --- | --- | --- | --- |
| `README.md` | Markdown | Documentation infrastructure | Purpose, maintenance procedures and navigation |
| `MINIFEST.md` | Markdown | Documentation infrastructure | Authoritative inventory of this folder |
| `ARCHITECTURE.md` | Markdown | Foundation → v1.0.0 | Module layout, dependencies and execution flow |
| `FILE_MAP.md` | Markdown | Foundation → current | Repo file-by-file responsibilities and locations |
| `FUNCTION_REFERENCE.md` | Markdown | Engine phases 03–04 | Class methods, validation, exports, return/error contracts |
| `CI_AND_RELEASE.md` | Markdown | CI 4.5 → v1.0.0 | Workflow paths, triggers, secrets names, release verification |
| `QUALITY_AND_SECURITY.md` | Markdown | Audit → current | Test coverage, identified gaps and server-side security boundaries |
| `DEVELOPMENT_LOG.md` | Markdown | Phases 01–05, release, documentation setup | Confirmed changes/commits, status, ongoing log contract |
| `BASELINE_2026-11-28.md` | Markdown | 2026-11-28 source freeze | GitHub evidence-based exact state, API/CI/release, open gates, resume protocol |
| `BASELINE_FILE_INVENTORY_2026-11-28.md` | Markdown | 2026-11-28 Git tree inventory | All 51 pre-freeze source paths, blob SHAs, sizes and drift procedure |

Update this index **in the same commit** whenever a direct entry changes. Never include `notes/` content here.


## P04-S02-A01 runtime qualification — 2026-11-28

No direct project/ inventory change; new repository workflow indexed in FILE_MAP.md and CI_AND_RELEASE.md. P04-S02/A01 adds `.github/workflows/p04-s02-compatibility.yml`, a PR-only compatibility qualification workflow. Eight Node and eleven Python targets (19 total) on Ubuntu 24.04 x64, Windows Server 2025 x64 and macOS 15 ARM64. Exact Python 3.10.0 is tested on Windows only; Ubuntu 3.10.x remains. Pinned actions, read-only contents permission, unchanged source tests and isolated npm/PyPI 2.0.0 consumer regressions; record runtime, dependencies, package origins and R-04 observations. Qualification acceptance is PENDING until actual dedicated CI and Required CI pass. No existing engine, dependency, workflow, governance or publishing changes.


## P04-S03 dependency and distribution qualification — 2026-11-28

No direct project/ entry added; repository workflow indexed in FILE_MAP.md. P04-S03 adds `.github/workflows/p04-s03-security.yml`: PR-only, read-only, pinned actions on Ubuntu 24.04. Checks locked npm and isolated public v2 consumer graphs, independent Python source/consumer dependency audits using pip-audit 2.10.1, and official npm/PyPI v2 archives against registry digests, safe payload paths and pinned release source. Registry signatures/provenance metadata are observations, not verified publisher attestations; independent publish jobs are non-atomic. No engine/dependency/UI/publisher changes. Qualification acceptance PENDING until dedicated CI and mandatory Required CI PASS; final evidence in acceptance handoff.
