---
title: "Testing, CI, Published Artifacts and Releases"
description: "Core and GUI test commands, GitHub Actions behavior, current published packages and release verification."
order: 100
draft: false
---

## v2.0.1 verified release — 2026-11-28

**Current release status: published and verified on both npm and PyPI.** [npm 2.0.1](https://www.npmjs.com/package/kron-otp/v/2.0.1) and [PyPI 2.0.1](https://pypi.org/project/kron-otp/2.0.1/) are the latest versions at verification. This status supersedes the earlier candidate and NO-GO checkpoints below. P05/G12 release-specific acceptance is GO via the approved recovery route; documentation closeout requires its own protected PR and final parity.

- Install: `npm install kron-otp@2.0.1` or `pip install kron-otp==2.0.1`. Python negative-clock diagnostics and the sdist vector fixture are corrected; runtime API, algorithm, dependency ranges and engine behavior otherwise unchanged.
- Immutable annotated unsigned [v2.0.1 tag](https://github.com/vibtoolshq/KronOTP/tree/v2.0.1) points to `c732cae0e58fe7e21bc0160f3814dc99d27990d1`. Qualification [46082157882](https://github.com/vibtoolshq/KronOTP/actions/runs/46082157882): 50 locked tools, three byte-identical artifacts, eight marker fixtures and five advisory graphs with zero reported vulnerabilities/zero Python skips at scan time; required regressions and main nonpublishing validation passed.
- Original [release run 46082457680](https://github.com/vibtoolshq/KronOTP/actions/runs/46082457680) remains FAILURE, attempt 1: validation, preflight, npm and PyPI publisher jobs succeeded; immediate reconciliation observed npm absent, so automatic smoke was skipped. npm registry records publication at 2026-11-27 23:29:04 UTC, after the publisher success at 23:26:58 and failed reconciliation at 23:27:22. Delayed public visibility is established; internal registry cause is not independently established. No republish or rerun occurred.
- Independent public downloads at 23:35:13 UTC and approved [nonpublishing recovery smoke 46083365483](https://github.com/vibtoolshq/KronOTP/actions/runs/46083365483) matched all three original artifact SHA-256 digests and registry metadata. Recovery smoke 3/3 jobs PASS, both installed exact-version consumers PASS, source JS 86 vectors and Python 13/13 PASS. This is recovery acceptance, not retroactive automatic-smoke success.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| npm tarball | 3188 | `3b963d59cd7d1600f0be5dfd114f88baf9ad4ec5b24a810e9a6da2a76dda31c9` |
| Python wheel | 5074 | `74ee3702e467bb8d3659162632d0d88c93c1120f0da9c9f136777dfc4553cc2e` |
| Python sdist | 7452 | `70f240af3ab525ae6ba9aaeb9ab64582af79aa567bb06685b761fb30c4562231` |

Original release bundle [15237494004](https://github.com/vibtoolshq/KronOTP/actions/runs/46082457680/artifacts/15237494004), manifest SHA-256 `ec91d48e0a40d88030b608b81695c93be755a597e426383f58e23c3339047df3`. Preserve the historical failure. Release workflow remains unchanged; future releases need separately approved bounded read-only registry visibility reconciliation to avoid premature partial status (no automatic upload retry). Existing token-based publishing, shared credentials, unsigned tag and absent/unverified provenance were explicitly accepted for v2.0.1 only. No cryptographic publisher identity proof, universal runtime compatibility, future vulnerability guarantee, production capacity SLA or distributed authentication assurance. Historical GUI verification remains on v2.0.0. Caller must provide secure secret storage, clock, throttling and atomic replay prevention.


## Historical v2.0.1 release candidate — 2026-11-28

Source npm and PyPI manifests and npm root lock metadata target 2.0.1; runtime dependency ranges and resolved npm dependency entries are unchanged. The release-specific owner decision retains existing organization tokens and accepts shared-credential, unsigned-tag and provenance limitations for this release only. Current public registry policy must permit direct publication; stop on rejection. Exact-version PR qualification, fresh advisory scans, protected merge and main nonpublishing release validation are required before the authorized stable tag. Until actual publication and automatic registry smoke are verified, public npm/PyPI installation examples remain 2.0.0 and G12 remains open. No claim of published 2.0.1 at this candidate checkpoint.


## Historical P05-A06 — consolidated acceptance (2026-11-28)

**Decision:** scoped source and release-tooling qualification is accepted for release preparation; live v2.0.1 publication is **NO-GO** until release-specific mandatory preflight and separate authorization. P01–P04 and P05-A01–A05 scoped remediation are closed. P05-A06 documentation consolidation awaits its protected PR check and verified closeout; G12 final publication acceptance remains open. Published npm/PyPI packages are still 2.0.0. Historical candidate/blocked/OPEN statements below describe their respective checkpoints, not current source status. No source, version or publication change in this documentation update.

| Evidence | Verified result |
| --- | --- |
| P04 runtime [46058729635](https://github.com/vibtoolshq/KronOTP/actions/runs/46058729635) | 19 selected targets / 38 source and installed v2 suites; exact Python 3.10.0 on Windows only |
| P04 security [46059824623](https://github.com/vibtoolshq/KronOTP/actions/runs/46059824623) | Four advisory scopes, zero known vulnerabilities at scan time; three published archive integrity checks |
| P04 caller [46060701345](https://github.com/vibtoolshq/KronOTP/actions/runs/46060701345) | 24/24 synthetic scenarios; single-process replay/throttle/isolation, not distributed auth |
| P04 performance [46061887435](https://github.com/vibtoolshq/KronOTP/actions/runs/46061887435) | Two 600-second bounded workloads, zero unexpected errors/mismatches/OOM/timeout; observation only |
| A01 source fix [46068002722](https://github.com/vibtoolshq/KronOTP/actions/runs/46068002722) | R-04 negative-clock diagnostic corrected in Python generate; 13/13 methods; verify unchanged |
| A02 packaging [46071499080](https://github.com/vibtoolshq/KronOTP/actions/runs/46071499080) | sdist vector fixture exact; source and derived-wheel suites 13/13 each; 86 vectors each |
| A03 publisher | Existing organization token architecture retained for preparation; revocation/replacement of historical exposed PyPI token owner-confirmed, actual credentials unverified |
| A04 [46076859856](https://github.com/vibtoolshq/KronOTP/actions/runs/46076859856) / [46076997809](https://github.com/vibtoolshq/KronOTP/actions/runs/46076997809) | 21/21 synthetic contracts; nonpublishing build and public v2 registry smoke |
| A05 [46079118728](https://github.com/vibtoolshq/KronOTP/actions/runs/46079118728) / [46079278884](https://github.com/vibtoolshq/KronOTP/actions/runs/46079278884) | 50/50 hash-locked tools, 3/3 byte-identical artifacts in two independent same-commit Linux builds, 8/8 marker fixtures, five advisory graphs zero reported vulnerabilities and zero Python skips; main nonpublishing validation passed |

Historical qualification and remediation evidence above/below is preserved; the original failed [46078021001](https://github.com/vibtoolshq/KronOTP/actions/runs/46078021001) remains a failure (optional extra assertion); the corrected new candidate passed, not a rerun. All 12 original KO findings are addressed within scoped qualification; G01–G11 accepted; G12 publication decision remains NO-GO. This docs-only PR is not a new runtime, security or release test.

- R-04 and the missing sdist test fixture are fixed on current source, not in the immutable published PyPI 2.0.0. Current source Python has 13 test methods, not nine. The historical 19-target qualification was not repeated after the narrow Python fix; later targeted regressions and candidate artifact checks passed.
- Caller must provide secure secret storage, trustworthy clock, account binding, throttling and atomic durable replay prevention. No distributed authentication, remote login, new GUI test, independent security certification, production capacity/SLA or 24/7 reliability guarantee. Historical minimum-runtime compatibility is not a maintained-runtime recommendation; Python RSS measurement discrepancy remains unresolved.
- Runtime ranges remain unchanged: npm OTPAuth ^9.6.0; Python PyOTP >=2.12,<3. Latest recorded resolution OTPAuth 9.6.0, @noble/hashes 2.4.0, PyOTP 2.12.2. Advisory evidence is point-in-time (2026-11-27 22:52 UTC), not a guarantee for future dependency resolutions. Reproducibility is same commit, Ubuntu 24.04 x64, controlled Node 24.22.3/npm 11.19.1 and Python 3.12.16 with 50 locked tools; not arbitrary platforms or different commit timestamps.
- Existing three GitHub rulesets enforce PR/Required CI, restricted tag creation and immutable release tags; no independent reviewer requirement. Organization secret names exist, but actual token validity, package scope, expiration, owner authorization/2FA and current registry publishing policy are unverified. OIDC/signing and provenance limitations were deferred for preparation only, not permanently waived. Historical v2 tag unsigned; publisher attestations not established. Check [npm access-token policy](https://docs.npmjs.com/about-access-tokens/) (direct granular-token publishing scheduled to end January 2027), [npm package policy](https://docs.npmjs.com/policies/dual-use/) and [PyPI publishing guidance](https://docs.pypi.org/publishing/publishing-to-pypi/) before authorizing any publication. No credential disclosure.
- Release builds once and verifies a SHA-bound immutable bundle, requires absent registry state, publishes independently, reconciles actual bytes and gates automatic exact-version smoke. Two registries are not atomic. Actual tag-triggered publisher authentication, recovery upload and end-to-end post-publication smoke are not yet exercised; synthetic contracts and independent historical smoke do not prove them. Stop on partial, conflict or uncertainty; preserve run artifacts/manifest before expiry and require separate recovery authorization; no blind rerun, overwrite, unpublish or tag movement.

**Release-preflight (separate approval):** confirm actual owner/token scope, expiry/validity, 2FA and package-specific direct-publish policy using safe nonmutating evidence; explicitly resolve remaining signing/provenance and shared-credential risk for the intended release, without silent waiver. Require v2.0.1 absent or formally reconciled in both registries and new tag absent; both exact public version endpoints returned 404 on 2026-11-27 at 22:58 UTC, not a reservation. Align both manifests and npm root lock version in a separately approved version-only change. Verify fresh exact-version candidate regressions, package metadata/fixture/RECORD, actual dependency advisories, controlled toolchain and release validation on the accepted main SHA. No publishing on branch/PR/manual validation. Only after preflight and explicit release authorization may the authorized tag creator create/push the new stable tag; verify all three registry artifacts and actual post-publish smoke before claiming release success. No automatic partial recovery.


## Historical P04 consolidated qualification — 2026-11-28

**Historical P04 consolidation checkpoint:** P01–P03 were closed; P04 acceptance was pending at that checkpoint. P04 is now closed; see the current P05-A06 decision above.

| Qualification | Recorded run | Actual result |
| --- | --- | --- |
| Runtime/source/consumer | [46058729635](https://github.com/vibtoolshq/KronOTP/actions/runs/46058729635) | 19/19 jobs; 38/38 suites |
| Dependency/distribution | [46059824623](https://github.com/vibtoolshq/KronOTP/actions/runs/46059824623) | 3/3 jobs; four runtime audit scopes zero known vulnerabilities at scan time; three archives checked |
| Consumer/caller | [46060701345](https://github.com/vibtoolshq/KronOTP/actions/runs/46060701345) | 2/2 jobs; 24/24 named scenarios |
| Bounded performance | [46061887435](https://github.com/vibtoolshq/KronOTP/actions/runs/46061887435) | 2/2 jobs; approved functional gates passed |

Four corresponding Required CI runs [46058729566](https://github.com/vibtoolshq/KronOTP/actions/runs/46058729566), [46059824535](https://github.com/vibtoolshq/KronOTP/actions/runs/46059824535), [46060701180](https://github.com/vibtoolshq/KronOTP/actions/runs/46060701180), [46061887357](https://github.com/vibtoolshq/KronOTP/actions/runs/46061887357) passed; path-filtered engine jobs skipped there, not counted as passes. These are historical executed results from the approved P04 qualification candidates, not new tests executed by this documentation change. P04-S06-A01 documentation acceptance remains conditional on this PR's Required CI, exact diff, protected merge, baseline parity and verified closeout.

Performance evidence is observation-only: Ubuntu 24.04 x64, Node 24.22.3 and Python 3.12.16, published v2.0.0, Intel Xeon 6975P-C, four logical CPUs. Each completed 20 cold starts, 1,000 warm-up operations, 10,000 generate and 10,000 verify, and 1/4/8 independent workers at 2,000 operations each. Serial throughput was 167,309.4 / 7,694.5 operations/s (Node/Python); sustained 192.35 / 196.11 pairs/s for 600.000 / 600.003 seconds, below the approved 200 pairs/s cap; 61 RSS samples each including endpoints, zero correctness mismatches/errors/OOM/timeout. Sampled RSS and OS-reported Python peak RSS differ; root cause unverified. No numeric SLA, leak-free claim, 24/7 stability or production service capacity inference. Timing includes synthetic clock instrumentation and runner variability. Raw latency/CPU/RSS/worker results: [46061887435](https://github.com/vibtoolshq/KronOTP/actions/runs/46061887435).

All four qualification workflows are PR-only with scoped paths, pinned actions and read-only permissions; existing Required CI and release/registry smoke triggers remain unchanged. No new release or package publication. Residual review items: R-04 (Python generate at a simulated negative system clock mislabels the error as invalid secret; 22/22 diagnostic observations), missing shared vector fixture in PyPI v2 sdist (direct sdist regression not run), unsigned historical tag, unverified publisher attestations/signature authenticity, independent non-atomic npm/PyPI publishing, Python range-based dependencies, publisher secret scope and automatic post-release smoke not established. The maintainer explicitly deferred R-04 remediation/final acceptance to P05 for scoped P04 closure only. R-04 stays OPEN, not fixed or permanently waived. No other risk is implicitly accepted. Final production/release acceptance remains NO-GO pending P05 and any separately authorized remediation.

## Test organization and verified commands

| Check | Source file | Run from | Command / environment |
| --- | --- | --- | --- |
| Node core | `javascript/tests/test.js` | `javascript/` | `npm ci --ignore-scripts --no-audit --no-fund`, then `npm test` |
| Python core | `python/tests/test_kron_otp.py` | `python/` | `python -m pip install -e .`, then `python -m unittest discover -s tests -v` |
| Windows GUI/vault | `python/tests/gui/test_app.py` | repository root | `python -m unittest discover -s python/tests/gui -p test_app.py -v` with Tkinter, Windows DPAPI and installed public PyPI 2.0.0 |
| Public package smoke | `.github/workflows/registry-smoke.yml` | GitHub Actions | Manually enter published stable `version`; no registry publication |

The Node/Python core suites share `python/tests/totp_vectors.json` (six RFC6238 SHA1 six-digit fixed-time reference values + 80 synthetic cross-language keys/times/codes), and test formatting, input constraints, 30-second rollovers and adjacent-window decisions. The current source Python core suite has **13** `unittest` methods (nine before A01). The GUI Windows suite has **eight** methods testing user-bound encryption and UI state. Count is method count, not number of individual vector cases.

The GUI test suite is **not** invoked by the existing Linux Python CI job. Node source tests depend on the full monorepo fixture; package publishing does **not** bundle that fixture as a public runtime dependency.

## GitHub Actions (exact workflows)

| Workflow | Trigger | Verified behavior |
| --- | --- | --- |
| [KronOTP CI](https://github.com/vibtoolshq/KronOTP/blob/main/.github/workflows/ci.yml) | Pull requests; main pushes affecting `javascript/**`, `python/**` or the workflows | Path-filtered Node 24 / Python 3.12 suites; unconditional stable `Required CI` check aggregating relevant jobs |
| [KronOTP Release](https://github.com/vibtoolshq/KronOTP/blob/main/.github/workflows/release.yml) | Main push affecting package/workflow release files, manual dispatch, pushed `v*` tags | `validate` tests both packages, dry-runs npm payload, builds/tests PyPI distributions; npm/PyPI **publish jobs only run on a tag push** |
| [Published Package Smoke](https://github.com/vibtoolshq/KronOTP/blob/main/.github/workflows/registry-smoke.yml) | Its workflow file push on main or manual dispatch | Strict stable numeric SemVer, exact public npm tarball/PyPI wheel download, clean consumer install and installed-version assertions |

A **docs-only push on main does not automatically trigger the CI or release workflows** under their configured `push.paths`; do not report an absent run as a failure or fake a PASS. Pull requests trigger the `Required CI` producer, but GitHub branch protection enforcement is a separate repository setting.

The release workflow validates pushed tags with stable `vX.Y.Z` pattern and requires the tagged commit to equal current `main` HEAD, plus equal npm/PyPI manifest versions. The npm job uses `NPM_TOKEN`; PyPI uses `PYPI_API_TOKEN` via Twine. Those are GitHub Actions secret **names**, not inspected values. Publishing both registries is **non-atomic**; each upload must be reviewed independently.

## Verified historical results (not tests executed in this docs update)

- **v2.0.0 tag/release:** annotated tag `v2.0.0` at commit `eefafd9934a44243879068d9b8081005e68aeade`. [Tag-push release run 43867458691](https://github.com/vibtoolshq/KronOTP/actions/runs/43867458691) had successful validation and npm/PyPI publish jobs.
- Public npm `kron-otp@2.0.0` and PyPI `kron-otp==2.0.0` were independently downloaded, clean-installed and functionally smoke-tested with public fixture input during the release work. This does not mean all supported runtimes/platforms or auth server behavior were tested.
- [GUI-02 CI 43906779325](https://github.com/vibtoolshq/KronOTP/actions/runs/43906779325) confirmed Python source test and Required CI SUCCESS; JavaScript was correctly SKIPPED on an unrelated GUI-only change. The Windows GUI suite separately passed 8/8 focused tests; it is not part of that Actions job.
- The historical `v1.0.0` tag and public registry artifacts remain untouched. Older source notes describing “only 1.0.0 published” are **historical**, not current status.
- The dedicated version-aware `registry-smoke.yml` was **not manually dispatched for v2.0.0** during the release, so do not cite a nonexistent v2 smoke workflow run; instead use the actual independently executed public-artifact checks.

## Release checklist (only when a new release is approved)

1. Authorize scope and update package metadata in **both** `javascript/package.json` and `python/pyproject.toml`; align `javascript/package-lock.json` root version and migration documentation.
2. Run focused Node/Python tests and the release validation flow, including npm payload and `python -m build`/`twine check`.
3. From verified current main, create a **new** annotated stable `vX.Y.Z` tag matching the manifests. Do not move historical release tags; no tag push without explicit release authorization.
4. Monitor the GitHub release workflow. Check npm/PyPI publish job conclusions independently and handle partial publication without republishing the same immutable version.
5. Use manual Published Package Smoke with the **new public version** to verify exact registry artifacts after publication. Record source SHA, released versions and actual evidence.

Historical release notes predate P03 governance and the P04 qualification evidence above; a successful package smoke is not production security certification. No new tag/release is generated by documentation maintenance.

[Developer contribution process](./DEVELOPMENT_AND_CONTRIBUTING.md) · [Automated publishing](./AUTOMATION_AND_PUBLISHING.md) · [Coverage QA](./COVERAGE_AND_QA.md).


## P05-A02 — source distribution completeness (2026-11-28)

`python/MANIFEST.in` explicitly includes `tests/totp_vectors.json` in future Python source distributions. `.github/workflows/p05-sdist.yml` qualifies candidate sdist and wheel built from that sdist, strict archive paths/source bytes/metadata/RECORD, twine check, and separate 13-method source and installed-wheel regressions with all 86 shared vectors. The wheel consumer adapts only import/mock paths in a disposable copy. No runtime fixture or GUI in the wheel; no engine, dependency, version, existing workflow or publishing change. Build tools are resolved in an isolated CI environment and recorded, not a reproducibility lock. Qualification acceptance pending actual CI and verified closeout. Historical published v2.0.0 sdist remains incomplete and published v2 does not contain the R-04 source fix; no new release.


## P05-A04 — immutable release and recovery contract (2026-11-28)

P05-A04 adds a stdlib release contract helper and offline qualification tests. A release builds exactly one npm tarball and one Python sdist plus a wheel from that sdist, with strict payload, metadata, fixture and RECORD checks. Run-owned artifacts and manifest SHA-256 bind bytes to version, commit, ref, run and attempt; publisher jobs verify the same bundle. Only an initial stable tag push at current main can publish, using existing organization secrets. Public GET preflight requires all three artifacts absent; after terminal publisher outcomes the registry contract classifies all absent, exact full, partial, conflicting or unknown. Only full byte-exact results and successful publishers enable secret-free automatic exact-version registry smoke; manual/main smoke retained. No automatic partial recovery, overwrites, skip-existing or blind reruns. For recovery preserve run URL, bundle, manifest and per-file hashes/status before artifact expiry (14 days requested, subject to repository limits); separately authorize only missing exact artifacts or a new version after reconciliation. Never move/delete a tag or unpublish automatically. Registry publication is still non-atomic. Token validity/permission and policy preflight, build tool reproducibility and actual publisher provenance remain separate gates. Qualification pending actual CI and verified closeout; no live publishing in this change.


## P05-A05 — controlled release tooling (2026-11-28)

Release builds and Python publishing use isolated hash-locked tooling (50 exact package versions including build, setuptools, wheel, Twine, pip and pip-audit). Controlled Ubuntu 24.04 x64, Node 24.22.3/npm 11.19.1 and CPython 3.12.16. Build subprocesses use the locked interpreter without backend isolation/downloads. The sdist preserves verified member bytes while canonicalizing tar/gzip headers and ordering with commit-derived SOURCE_DATE_EPOCH; wheel built from that sdist. Dedicated PR qualification compares two independent fresh venv/build roots for byte-identical artifacts and checks source/installed-candidate npm/Python runtime and tooling advisory graphs. Runtime dependency ranges, engine and publishing credentials unchanged. Scope is controlled same-commit Linux rebuild, not universal reproducibility or permanent vulnerability guarantee. Production use maintained security-patched runtimes; historical compatibility is not lifecycle support. Qualification pending CI; no live publication. Token validity and registry policy remain mandatory release-preflight.
