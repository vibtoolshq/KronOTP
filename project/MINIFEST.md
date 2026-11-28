# Project Folder MINIFEST

Inventory of **all direct entries** of `project/` as of BASELINE-FREEZE-02; dated historical entries are retained. No subfolders are created.

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
| `BASELINE_POST_V2_0_1.md` | Markdown | Current baseline | Evidence-backed release and continuation snapshot |
| `BASELINE_FILE_INVENTORY_POST_V2_0_1.md` | Markdown | Current source inventory | Exact 68 incoming Git blobs and sizes |

Update this index **in the same commit** whenever a direct entry changes. Never include `notes/` content here.


## P04-S02-A01 runtime qualification — 2026-11-28

No direct project/ inventory change; new repository workflow indexed in FILE_MAP.md and CI_AND_RELEASE.md. P04-S02/A01 adds `.github/workflows/p04-s02-compatibility.yml`, a PR-only compatibility qualification workflow. Eight Node and eleven Python targets (19 total) on Ubuntu 24.04 x64, Windows Server 2025 x64 and macOS 15 ARM64. Exact Python 3.10.0 is tested on Windows only; Ubuntu 3.10.x remains. Pinned actions, read-only contents permission, unchanged source tests and isolated npm/PyPI 2.0.0 consumer regressions; record runtime, dependencies, package origins and R-04 observations. Qualification acceptance is PENDING until actual dedicated CI and Required CI pass. No existing engine, dependency, workflow, governance or publishing changes.


## P04-S03 dependency and distribution qualification — 2026-11-28

No direct project/ entry added; repository workflow indexed in FILE_MAP.md. P04-S03 adds `.github/workflows/p04-s03-security.yml`: PR-only, read-only, pinned actions on Ubuntu 24.04. Checks locked npm and isolated public v2 consumer graphs, independent Python source/consumer dependency audits using pip-audit 2.10.1, and official npm/PyPI v2 archives against registry digests, safe payload paths and pinned release source. Registry signatures/provenance metadata are observations, not verified publisher attestations; independent publish jobs are non-atomic. No engine/dependency/UI/publisher changes. Qualification acceptance PENDING until dedicated CI and mandatory Required CI PASS; final evidence in acceptance handoff.


## P04-S04 synthetic consumer qualification — 2026-11-28

No direct project/ inventory change; three repository additions indexed in FILE_MAP.md. P04-S04 adds `.github/workflows/p04-s04-consumer.yml`, `qualification/p04-s04/node-consumer.cjs` and `qualification/p04-s04/python_consumer.py`. PR-only isolated public v2.0.0 consumers exercise 12 named scenarios per engine: RFC current, adjacent, expiry, malformed, wrong account, stateless repeat, replay rollover/recovery, isolation, throttling/reset, rollback denial, concurrent duplicate and concurrent attempt budget. Synthetic caller transaction serializes check/verify/reserve using Node owner event loop and Python thread lock; 8 concurrent requests per case. 120s conservative token reservation, rolling 3/60s attempts, no matched counter inference. Collision tradeoff, single-process state and distributed atomic storage requirement remain; not production authentication, no external accounts. Qualification PENDING until dedicated and mandatory CI PASS. No public API, engine, GUI, dependency, existing workflow or release change.


## P04-S05 bounded performance qualification — 2026-11-28

No direct project/ inventory change; three additions indexed in FILE_MAP.md. P04-S05 adds `.github/workflows/p04-s05-performance.yml`, `qualification/p04-s05/benchmark.cjs` and `qualification/p04-s05/benchmark.py`. PR-only Ubuntu24 Node24/Python3.12 isolated public v2 consumers; fixed RFC correctness, monotonic measurement, 20 cold starts, 1000 warm-up operations, 10000 generate and 10000 verify, 1/4/8 independent process workers (2000 operations each), 600s sustained with >=5ms between pair starts, 10s RSS sampling, 20min job timeout. Reports nearest-rank p50/p95/p99, throughput, CPU and RSS, worker results, runtime/dependencies/hardware. Observation only; no numeric SLA. Zero unexpected errors/mismatches/OOM/timeout required. Timing includes deterministic clock shim and process startup where identified. No production load or engine/API/GUI/dependency/existing workflow changes. Acceptance PENDING until actual qualification and mandatory CI PASS.


## P05-A02 — source distribution completeness (2026-11-28)

No new direct project/ entries; repository additions indexed in FILE_MAP.md. `python/MANIFEST.in` explicitly includes `tests/totp_vectors.json` in future Python source distributions. `.github/workflows/p05-sdist.yml` qualifies candidate sdist and wheel built from that sdist, strict archive paths/source bytes/metadata/RECORD, twine check, and separate 13-method source and installed-wheel regressions with all 86 shared vectors. The wheel consumer adapts only import/mock paths in a disposable copy. No runtime fixture or GUI in the wheel; no engine, dependency, version, existing workflow or publishing change. Build tools are resolved in an isolated CI environment and recorded, not a reproducibility lock. Qualification acceptance pending actual CI and verified closeout. Historical published v2.0.0 sdist remains incomplete and published v2 does not contain the R-04 source fix; no new release.


## P05-A04 — immutable release and recovery contract (2026-11-28)

New repository paths indexed in FILE_MAP.md; no new direct project Markdown. P05-A04 adds a stdlib release contract helper and offline qualification tests. A release builds exactly one npm tarball and one Python sdist plus a wheel from that sdist, with strict payload, metadata, fixture and RECORD checks. Run-owned artifacts and manifest SHA-256 bind bytes to version, commit, ref, run and attempt; publisher jobs verify the same bundle. Only an initial stable tag push at current main can publish, using existing organization secrets. Public GET preflight requires all three artifacts absent; after terminal publisher outcomes the registry contract classifies all absent, exact full, partial, conflicting or unknown. Only full byte-exact results and successful publishers enable secret-free automatic exact-version registry smoke; manual/main smoke retained. No automatic partial recovery, overwrites, skip-existing or blind reruns. For recovery preserve run URL, bundle, manifest and per-file hashes/status before artifact expiry (14 days requested, subject to repository limits); separately authorize only missing exact artifacts or a new version after reconciliation. Never move/delete a tag or unpublish automatically. Registry publication is still non-atomic. Token validity/permission and policy preflight, build tool reproducibility and actual publisher provenance remain separate gates. Qualification pending actual CI and verified closeout; no live publishing in this change.


## P05-A05 — controlled release tooling (2026-11-28)

New repository files indexed in FILE_MAP.md; no new direct project Markdown. Release builds and Python publishing use isolated hash-locked tooling (50 exact package versions including build, setuptools, wheel, Twine, pip and pip-audit). Controlled Ubuntu 24.04 x64, Node 24.22.3/npm 11.19.1 and CPython 3.12.16. Build subprocesses use the locked interpreter without backend isolation/downloads. The sdist preserves verified member bytes while canonicalizing tar/gzip headers and ordering with commit-derived SOURCE_DATE_EPOCH; wheel built from that sdist. Dedicated PR qualification compares two independent fresh venv/build roots for byte-identical artifacts and checks source/installed-candidate npm/Python runtime and tooling advisory graphs. Runtime dependency ranges, engine and publishing credentials unchanged. Scope is controlled same-commit Linux rebuild, not universal reproducibility or permanent vulnerability guarantee. Production use maintained security-patched runtimes; historical compatibility is not lifecycle support. Qualification pending CI; no live publication. Token validity and registry policy remain mandatory release-preflight.
