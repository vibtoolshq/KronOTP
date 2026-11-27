---
title: "Forensic Documentation Coverage and QA"
description: "Implementation audit and documentation coverage evidence for public APIs, tests, integrations and security limitations."
order: 130
draft: false
---

## P05-A06 — consolidated acceptance (2026-11-28)

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


## P05-A01 — Python generation diagnostic correction (source candidate)

Four new targeted unittest methods cover negative/fractional pre-epoch times, invalid-secret precedence, independent counter 0/1 references with one clock read, and sanitized dependency-generation ValueError. The nine original methods, six RFC and 80 shared vectors are retained (13 methods proposed total). No fresh cross-platform/GUI/published consumer test is implied.

This change is limited to Python `KronOTP.generate()`: validate and construct the TOTP before reading the clock, sample `time.time()` once, reject any negative Unix timestamp (including fractional pre-epoch time) with `ValueError("Invalid system clock: TOTP requires a non-negative Unix timestamp.")`, then generate with `totp.at(snapshot)`. Expected construction errors retain the existing sanitized invalid-secret `ValueError`; expected generation-stage errors use `ValueError("TOTP generation failed.")`. Invalid secret takes precedence. No new public parameter, exception class, dependency, algorithm or change to `verify()`.

Source candidate only; acceptance requires the actual protected PR CI and verified closeout. Published PyPI 2.0.0 and npm 2.0.0 remain unchanged; PyPI v2 retains the historical negative-clock misclassification. Do not assume installing v2 delivers this source fix. P05 final release acceptance remains NO-GO.

## P04 consolidated qualification — 2026-11-28

**Historical P04 consolidation checkpoint:** P01–P03 were closed; P04 acceptance was pending at that checkpoint. P04 is now closed; see the current P05-A06 decision above.

| Qualification | Recorded run | Actual result |
| --- | --- | --- |
| Runtime/source/consumer | [46058729635](https://github.com/vibtoolshq/KronOTP/actions/runs/46058729635) | 19/19 jobs; 38/38 suites |
| Dependency/distribution | [46059824623](https://github.com/vibtoolshq/KronOTP/actions/runs/46059824623) | 3/3 jobs; four runtime audit scopes zero known vulnerabilities at scan time; three archives checked |
| Consumer/caller | [46060701345](https://github.com/vibtoolshq/KronOTP/actions/runs/46060701345) | 2/2 jobs; 24/24 named scenarios |
| Bounded performance | [46061887435](https://github.com/vibtoolshq/KronOTP/actions/runs/46061887435) | 2/2 jobs; approved functional gates passed |

Four corresponding Required CI runs [46058729566](https://github.com/vibtoolshq/KronOTP/actions/runs/46058729566), [46059824535](https://github.com/vibtoolshq/KronOTP/actions/runs/46059824535), [46060701180](https://github.com/vibtoolshq/KronOTP/actions/runs/46060701180), [46061887357](https://github.com/vibtoolshq/KronOTP/actions/runs/46061887357) passed; path-filtered engine jobs skipped there, not counted as passes. These are historical executed results from the approved P04 qualification candidates, not new tests executed by this documentation change. P04-S06-A01 documentation acceptance remains conditional on this PR's Required CI, exact diff, protected merge, baseline parity and verified closeout.

| Hosted environment | Node.js tested versions | Python tested versions |
| --- | --- | --- |
| Ubuntu 24.04 x64 | 20.19.0, 22.23.5, 24.22.3, 26.13.1 | 3.10.22, 3.11.18, 3.12.16, 3.13.18, 3.14.10, 3.15.2 |
| Windows Server 2025 x64 | 20.19.0, 24.22.3 | 3.10.0, 3.10.11, 3.12.10 |
| macOS 15 ARM64 | 20.19.0, 24.22.3 | 3.10.11, 3.12.10 |

19 selected targets, 38 source/installed v2.0.0 suites passed in [46058729635](https://github.com/vibtoolshq/KronOTP/actions/runs/46058729635). Exact Python 3.10.0 on Ubuntu 24.04 was not tested; its lower-bound target was explicitly relocated to Windows. These are observed combinations, not an exhaustive Cartesian product or guarantee of every future patch, platform or dependency resolution. Declared floors remain Node >=20.19.0 and Python >=3.10.

Performance evidence is observation-only: Ubuntu 24.04 x64, Node 24.22.3 and Python 3.12.16, published v2.0.0, Intel Xeon 6975P-C, four logical CPUs. Each completed 20 cold starts, 1,000 warm-up operations, 10,000 generate and 10,000 verify, and 1/4/8 independent workers at 2,000 operations each. Serial throughput was 167,309.4 / 7,694.5 operations/s (Node/Python); sustained 192.35 / 196.11 pairs/s for 600.000 / 600.003 seconds, below the approved 200 pairs/s cap; 61 RSS samples each including endpoints, zero correctness mismatches/errors/OOM/timeout. Sampled RSS and OS-reported Python peak RSS differ; root cause unverified. No numeric SLA, leak-free claim, 24/7 stability or production service capacity inference. Timing includes synthetic clock instrumentation and runner variability. Raw latency/CPU/RSS/worker results: [46061887435](https://github.com/vibtoolshq/KronOTP/actions/runs/46061887435).

Residual review items: R-04 (Python generate at a simulated negative system clock mislabels the error as invalid secret; 22/22 diagnostic observations), missing shared vector fixture in PyPI v2 sdist (direct sdist regression not run), unsigned historical tag, unverified publisher attestations/signature authenticity, independent non-atomic npm/PyPI publishing, Python range-based dependencies, publisher secret scope and automatic post-release smoke not established. The maintainer explicitly deferred R-04 remediation/final acceptance to P05 for scoped P04 closure only. R-04 stays OPEN, not fixed or permanently waived. No other risk is implicitly accepted. Final production/release acceptance remains NO-GO pending P05 and any separately authorized remediation.

The results establish the selected qualification scope only; no live portal, GUI rerun, external authentication, independent penetration test or distributed caller proof is implied.

## Current logo verification — BRAND-01 (2026-11-20)

- **Current status: logo configured and verified.** The previous checklist snapshot below recorded logo N/A *before* BRAND-01; that historical result is now superseded.
- `.vibtools/docs.config.json` explicitly sets its supported root `logoPath` to `.vibtools/logo.webp`; all other frozen schema fields and developer-only routing remain unchanged.
- [`logo.webp`](https://github.com/vibtoolshq/KronOTP/blob/main/.vibtools/logo.webp) is a 96 × 96 transparent WebP (4,772 bytes) derived from the generated blue K/stopwatch/security/OTP icon. Local SHA-256 `70b3260851df1c60f2366a8481ed0adebaccd714e04569bbdae5bb16bb18d19e`, GitHub Git blob SHA `914d4af8ca42c25f11c100ddd2ba4ceee0b745b8`, both byte-identical to the prepared source derivative.
- **Current logo checklist: PASS** — WebP RIFF/VP8X alpha flag, safe existing repo-relative logoPath, matching blob, and both official developer/users JSON Schema Draft 2020-12 validations. The root README image link exists.
- **External boundary:** A live `developer.vibtools.io` ingest/build is not verified; this repository's logo/config validation is not evidence of portal publication.

**Audit date:** 2026-11-19. **Input baseline:** `7aaeb9703b42d4ea1d2c3b83233eb74be35707ce`. Primary evidence: tracked source tree, package metadata and lockfile, runtime source, source and GUI tests, workflow YAML, existing docs and repository instructions. **Documentation-only scope:** `docs/` plus required `project/` technical map/log; no runtime/test/workflow/package changes.

## Audited implementation inventory

- **41 tracked blob files** found in the initial Git tree (including repository policies, docs, metadata, tests, code, workflows and licenses); **52** total Git tree items including directories. No private ignored `notes/` were included.
- **Four implementation modules of interest:** `javascript/src/kron-otp.js`, `python/src/kron_otp.py`, `python/tests/gui/app.py` and `python/tests/gui/vault.py`; **three test modules:** JS core test, Python core test and GUI/vault test.
- **Public package exports:** JavaScript `KronOTP` class exported as default CommonJS and named alias **of the same class**; Python `KronOTP` class import. **Two distinct public class surfaces**, each with `generate` and `verify`: **four callable public methods**. No supported public constants/configuration objects/interfaces/exception classes/CLI flags/events/hooks.
- **Private implementation:** JavaScript `#createTOTP`; Python `_normalize_secret`/`_totp`; Tkinter `Authenticator`, URI/label helpers, Windows `AccountVault` and `VaultError`. These are documented for maintenance but **not** advertised as supported package APIs.
- **Implemented capability groups:** (1) synchronous six-digit TOTP generation; (2) local tolerance-window verification; (3) bounded canonical Base32 validation; (4) shared deterministic RFC/synthetic test parity; (5) GitHub-only GUI account CRUD/search and ephemeral session; (6) Windows DPAPI encrypted saved accounts; (7) GUI compatible `otpauth://totp` ingestion; (8) live code refresh, copy/expiry and privacy controls; (9) selective CI with a stable Required CI producer; (10) tag-gated npm/PyPI build/publish; (11) exact-version public registry smoke. **11 groups**, of which GUI/CI are not public engine APIs.
- **No verified** network API, database, public CLI, framework plugin, custom hash/digits/step configuration, QR camera, remote account authentication, replay/rate-limit engine, async APIs or persistent engine state.

## Audit-to-documentation coverage matrix

| Source/contract | Primary reference | Result |
| --- | --- | --- |
| JS export, class and two static methods | [API](./API_REFERENCE.md), [Architecture](./ARCHITECTURE.md) | Covered |
| Python import, class and two static methods | [API](./API_REFERENCE.md), [Architecture](./ARCHITECTURE.md) | Covered |
| Base32 bounds, errors, time tolerance, v1→v2 | [API](./API_REFERENCE.md), [Compatibility](./CONFIGURATION_AND_COMPATIBILITY.md) | Covered |
| JS/Python metadata and lockfile | [Installation](./INSTALLATION.md), [Compatibility](./CONFIGURATION_AND_COMPATIBILITY.md) | Covered |
| Minimal code examples and caller secret policy | [Quickstart](./QUICKSTART.md), [Integration](./INTEGRATION_GUIDE.md) | Covered |
| GUI and DPAPI internals (not package exports) | [Architecture](./ARCHITECTURE.md), [GUI source guide](https://github.com/vibtoolshq/KronOTP/blob/main/python/tests/gui/README.md) | Covered |
| JS/Python core and GUI suites + shared fixtures | [Development](./DEVELOPMENT_AND_CONTRIBUTING.md), [Testing](./TESTING_AND_RELEASES.md) | Covered |
| Three workflows and token references | [Development](./DEVELOPMENT_AND_CONTRIBUTING.md), [Testing](./TESTING_AND_RELEASES.md) | Covered |
| Failure handling and common issues | [Debugging](./DEBUGGING.md), [FAQ](./FAQ.md) | Covered |
| Public integrations and optional browser tools | [Integration](./INTEGRATION_GUIDE.md), [Automation](./AUTOMATION_AND_PUBLISHING.md) | Covered |
| Repo policies and maintainer workflow | [Development](./DEVELOPMENT_AND_CONTRIBUTING.md), [Agent rules](https://github.com/vibtoolshq/KronOTP/blob/main/AGENTS.md) | Covered |

## Executed checks and release evidence

- **Historical verified source tests:** Node `javascript/tests/test.js`, Python `python/tests/test_kron_otp.py` (9 unittest methods), six fixed-time RFC SHA1 six-digit examples plus 80 synthetic cross-language cases. These tests do not prove third-party account acceptance.
- **Historical verified GUI test:** Windows Python 3.12 installed PyPI v2.0.0; `python/tests/gui/test_app.py` eight focused tests covering UI/vault; existing Linux GitHub CI does **not** run GUI.
- **Public package release:** npm/PyPI v2.0.0 published and install-tested in prior release workflow [43867458691](https://github.com/vibtoolshq/KronOTP/actions/runs/43867458691). This task does not republish or retag.
- **Current documentation-run verified checks:** Windows public-fixture examples — Python **installed PyPI `kron-otp==2.0.0`** generate/verify PASS; Node **current repository source** generate/verify PASS. Focused documentation QA ran on the Git-tracked docs suite after fast-forward local pull: **17 direct Markdown files**, **110 valid internal relative links**, **8 Python fenced code blocks** parsed by `ast.parse`, **7 JavaScript fenced blocks** syntax-checked with Node, canonical MINIFEST exactly matching all docs, and source-code/manifest/workflow blob SHA comparison unchanged against the baseline. `git diff --check` PASS, changes restricted to **19 Markdown paths** (17 docs, 2 project), with clean worktree at the audited SHA. Syntax checks do **not** establish end-to-end execution of every optional automation example; those depend on consumer-specific frameworks/sites. GitHub/local final closeout SHA is verified separately after syncing.

## Corrected documentation mismatches

- Old `docs/MINIFEST.md` referenced v1.0.0 as if current and omitted newer project-specific guides.
- Historical `docs/TESTING_AND_RELEASES.md` combined an accurate v1 release history with outdated “only published 1.0.0” descriptions despite the already-published 2.0.0.
- `docs/USAGE_AND_TROUBLESHOOTING.md` denied any UI in the repository; revised boundary: **published libraries have no GUI**, but GitHub source contains optional Tkinter Authenticator.
- Historical roadmap status remains open for GitHub main/tag rulesets and broader P04 assurance; passing CI and v2 publication are not equivalent to closure of those gates.

## Unverified areas and intentional exclusions

No external penetration test, complete multi-platform/low-runtime matrix, sustained performance benchmark, secret-memory zeroization proof, QR scanner, independent live authenticator provider integration or server replay defense validation was performed. No assertion is made about real GitHub publisher secret scope or universally enforced repository protections. The source-only Windows DPAPI app's security depends on the signed-in Windows account and separately retained recovery materials.

This is **documentation verification**, not a new release or security certification. [Document index](./index.md) · repository inventory `docs/MANIFEST.md`.

## Documentation implementation provenance

Initial new documentation GitHub commit: [4813faa8d9a41c8bcd631df5880bf7baee9b0687](https://github.com/vibtoolshq/KronOTP/commit/4813faa8d9a41c8bcd631df5880bf7baee9b0687). The subsequent documentation-only closeout corrects the verified tracked-file count and adds actual link/code-syntax audit results. **Documentation maintenance does not produce a new workflow run** under the repository's path-filtered main-push triggers; no release/tag or package changes were made.

## Vib Docs Engine developer portal integration (2026-11-20)

The repository now routes **developer documentation only** from `.vibtools/docs.config.json` with `docsType: "developer"`, `docsPath: "docs"`, and `schemaVersion: 1`. `docs/index.md` provides versioned frontmatter and the first sidebar overview; remaining published guides use unique numeric `order` frontmatter. The former `docs/README.md` duplicates the root index and is removed because the engine discards it at sync. The former typo `docs/MINIFEST.md` is removed; **only `docs/MANIFEST.md` remains** as the source repository inventory and is intentionally removed by the portal sync, so no published page links to it. Source-code references outside the configured docs tree use verified absolute GitHub URLs instead of invalid `../` links.

This portal-specific change does not modify package/API behavior or claim user-portal documentation. The official live portal endpoints were not reachable from the current web environment; schema format and 10-point checklist were verified against the open-source Vib Docs Engine canonical `docs/vibtools-config.md` and `src/utils/vibtoolsConfig.ts` at commit `d88d6d57bf21e157f5bbaf767ca149ea5b48f9b5`. Passing static/structural checks does **not** certify that a remote portal sync/deployment has run. Local Windows sync and private `notes/` update also depend on restoring the currently offline Desktop Commander connection.

## Vib Docs Engine 10-point self-verification (repository-stage audit, 2026-11-20)

The checklist below evaluates the staged Git tree against the frozen JSON Schema embedded in the official [Vib Docs Engine configuration specification](https://github.com/vibtoolshq/vib-docs-engine/blob/d88d6d57bf21e157f5bbaf767ca149ea5b48f9b5/docs/vibtools-config.md). This is not an assertion of a live deployment.

| Official checklist | Result | Evidence |
| --- | --- | --- |
| 1. Only canonical config | PASS | Only `.vibtools/docs.config.json`; no alias |
| 2. Strict JSON and schema | PASS | Canonical `$schema` URL, `schemaVersion: 1`, exact property names/types |
| 3. Correct docsType and targets | PASS | `docsType: developer`, one `docsPath: docs`, no unused targets |
| 4. Slug and accent | PASS | `kronotp` and valid six-digit hex `#2563EB` |
| 5. Safe relative paths | PASS | `docs` is within repository; no `logoPath` configured |
| 6. Root index | PASS | `docs/index.md` has versioned title/description frontmatter and real body |
| 7. Valid YAML frontmatter | PASS | All 14 published pages have title, description, numeric order and boolean `draft: false`; root version `2.0.0` |
| 8. No stray typo manifests | PASS | Removed `docs/MINIFEST.md`; `docs/MANIFEST.md` remains as engine-stripped inventory |
| 9. Internal links/assets | PASS | Internal Markdown links remain within `docsPath`; external source links use GitHub URLs; no local assets declared |
| 10. Logo compliance | N/A (valid) | No logoPath/eligible logo asset; fallback monogram supported |

**Limitations:** Live hosted schema/spec URLs could not be retrieved by this environment, so the authoritative open-source engine repository was used. The actual developer portal sync/build was not run or observed. The authorized Windows Desktop Commander was offline; local fast-forward pull, local ignored notes update, and final GitHub/local clean-head matching are **BLOCKED**, not PASS. This does not change the correctness of the staged config/schema audit.

## VIBDOCS-01 live specification re-verification and Windows sync (2026-11-20)

**Update to the historical pending note above:** Windows Desktop Commander was restored and the exact **developer and users portal documents and JSON Schemas were fetched directly with HTTP 200**. The specifications have identical content except for a portal-specific source comment. The schemas have the same 15 permitted properties and identical constraints; only the schema `$id` URL differs per portal.

- Actual live source URLs: [Developer spec](https://developer.vibtools.io/vib-docs-engine/vibtools-config.md), [Users spec](https://docs.vib.tools/vib-docs-engine/vibtools-config.md), [Developer schema](https://developer.vibtools.io/schemas/vibtools-docs.schema.json), [Users canonical schema](https://docs.vib.tools/schemas/vibtools-docs.schema.json).
- Strict **Draft 2020-12 JSON Schema validation** of the existing `.vibtools/docs.config.json` passed against **both** live schemas (temporary Windows-only tooling; no project dependency change). Type-checked frontmatter for 14 published Markdown pages passed using a YAML parser. The one canonical `docs/MANIFEST.md` source inventory exactly covers 15 Markdown files, and all **78 internal published-document links** resolved within `docsPath`.
- All **10 official agent checklist conditions** were satisfied: 9 direct PASS and item 10 N/A, because no logoPath or physical logo/icon file is configured. The official schema and authoring references were checked directly, rather than inferred from another project.
- Windows local `main` was safely fast-forwarded from `9bb6075590902bb8b6443ecfd2a13418a4fab8af` to GitHub commit `54a0421b441c90cdb1e9e142c58ec42601da3007`. Local HEAD matched `origin/main` with clean worktree, and all 23 preceding changes were within the approved docs/config/policy scope; engine, GUI, tests, package manifests, workflows and tag were untouched.
- This update records resolved verification/synchronization blockers; the earlier "offline" record was a historical statement, not the current status. The **actual live developer-portal ingestion/build has not been confirmed**. As inspected, Vib Docs Engine's separate `config/projects.json` and `config/presets/dev-portal/projects.json` do not list KronOTP; registering it is a separate repository action outside this scope. Do not describe the public site as already serving KronOTP.

No package build, new release/tag, secrets, external portal registry mutation, or source-code change occurred in this verification.


## P03-GOV-01 governance enforcement — 2026-11-28

On 2026-11-28 (Asia/Dhaka), P03-GOV-01 activated repository rulesets: main governance 28257893, v* tag creation 28257876 and v* tag immutability 28257888. API read-back verified active enforcement. Earlier statements that protection is unconfigured or blocked on administrator access describe the historical state, not the current settings.

Main requires a pull request and strict up-to-date Required CI from GitHub Actions (app 15368), with zero independent approvals as explicitly approved for this single-maintainer repository. Main force-push and deletion are blocked; no main bypass actors. The tag-creation ruleset permits only the authorized individual user technicelnurnobi (85743335) to bypass the creation restriction. Separate tag immutability blocks updates and deletion with no bypass. This does not prevent a sufficiently authorized settings administrator from later changing the rules themselves.

Governance configuration verification is separate from runtime and security qualification. Configuration read-back passed; formal P03 acceptance remains conditional on this documentation PR passing Required CI and merging normally, final Git/local parity, unchanged historical tags, and recorded closeout evidence. No release tag, publish, deployment or destructive enforcement test is authorized by this phase. P04 and P05 remain outside scope; historical v2.0.0 publication is not full production acceptance.


## P05-A02 — source distribution completeness (2026-11-28)

`python/MANIFEST.in` explicitly includes `tests/totp_vectors.json` in future Python source distributions. `.github/workflows/p05-sdist.yml` qualifies candidate sdist and wheel built from that sdist, strict archive paths/source bytes/metadata/RECORD, twine check, and separate 13-method source and installed-wheel regressions with all 86 shared vectors. The wheel consumer adapts only import/mock paths in a disposable copy. No runtime fixture or GUI in the wheel; no engine, dependency, version, existing workflow or publishing change. Build tools are resolved in an isolated CI environment and recorded, not a reproducibility lock. Qualification acceptance pending actual CI and verified closeout. Historical published v2.0.0 sdist remains incomplete and published v2 does not contain the R-04 source fix; no new release.


## P05-A04 — immutable release and recovery contract (2026-11-28)

P05-A04 adds a stdlib release contract helper and offline qualification tests. A release builds exactly one npm tarball and one Python sdist plus a wheel from that sdist, with strict payload, metadata, fixture and RECORD checks. Run-owned artifacts and manifest SHA-256 bind bytes to version, commit, ref, run and attempt; publisher jobs verify the same bundle. Only an initial stable tag push at current main can publish, using existing organization secrets. Public GET preflight requires all three artifacts absent; after terminal publisher outcomes the registry contract classifies all absent, exact full, partial, conflicting or unknown. Only full byte-exact results and successful publishers enable secret-free automatic exact-version registry smoke; manual/main smoke retained. No automatic partial recovery, overwrites, skip-existing or blind reruns. For recovery preserve run URL, bundle, manifest and per-file hashes/status before artifact expiry (14 days requested, subject to repository limits); separately authorize only missing exact artifacts or a new version after reconciliation. Never move/delete a tag or unpublish automatically. Registry publication is still non-atomic. Token validity/permission and policy preflight, build tool reproducibility and actual publisher provenance remain separate gates. Qualification pending actual CI and verified closeout; no live publishing in this change.


## P05-A05 — controlled release tooling (2026-11-28)

Release builds and Python publishing use isolated hash-locked tooling (50 exact package versions including build, setuptools, wheel, Twine, pip and pip-audit). Controlled Ubuntu 24.04 x64, Node 24.22.3/npm 11.19.1 and CPython 3.12.16. Build subprocesses use the locked interpreter without backend isolation/downloads. The sdist preserves verified member bytes while canonicalizing tar/gzip headers and ordering with commit-derived SOURCE_DATE_EPOCH; wheel built from that sdist. Dedicated PR qualification compares two independent fresh venv/build roots for byte-identical artifacts and checks source/installed-candidate npm/Python runtime and tooling advisory graphs. Runtime dependency ranges, engine and publishing credentials unchanged. Scope is controlled same-commit Linux rebuild, not universal reproducibility or permanent vulnerability guarantee. Production use maintained security-patched runtimes; historical compatibility is not lifecycle support. Qualification pending CI; no live publication. Token validity and registry policy remain mandatory release-preflight.
