# CI, Packages and Release Pipeline — Technical Map

## Dependency and distribution setup
- Node package `kron-otp@2.0.0` (v1.0.0 remains historical): CommonJS, `javascript/package.json`, `otpauth ^9.6.0`, locked `javascript/package-lock.json`, publishes `src/kron-otp.js`, README, LICENSE, manifest.
- Python distribution `kron-otp==2.0.0` (v1.0.0 remains historical): `python/pyproject.toml`, setuptools, `py-modules=["kron_otp"]` under `python/src`, `pyotp>=2.12,<3`; generated wheel and sdist.
- GitHub: `vibtoolshq/KronOTP`. Initial release tag `v1.0.0` points to commit `e77155eefd7d18d49fcde489b510f4fd8df5d797`.
- Current docs-phase baseline is later; **do not move/reuse historical tags**.

## `.github/workflows/ci.yml`
- Events: pushes and PRs changing `javascript/**`, `python/**`, or the workflow itself.
- `changes` job: checkout and `dorny/paths-filter@v4`, outputs which language directory changed.
- `javascript`: only when relevant, pinned `actions/setup-node` v7 commit, Node 24, reproducible `npm ci --ignore-scripts --no-audit --no-fund` from committed `javascript/package-lock.json`, `node tests/test.js`.
- `python`: only when relevant, Python 3.12, `python -m pip install --disable-pip-version-check -e .` in `python/`, installing the *actual* `pyproject.toml` dependency `pyotp>=2.12,<3`, `PYTHONPATH=.` and `python tests/test_kron_otp.py`.
- **P03 KO-006 fixed in tracked CI:** both dependency installs now match the repository's lockfile or Python distribution metadata. Note Python is manifest-consistent but PyOTP remains a bounded version range, not a fully frozen transitive dependency lock.

## `.github/workflows/release.yml`
- Main branch pushes touching listed release configuration/doc/license paths or workflow file, plus manual dispatch, run the validation job; **publishing jobs skip without a tag**.
- On a **push** event for a stable `vX.Y.Z` tag only, `validate` checks strict stable tag regex, tag points to the **current main HEAD** (not merely any old ancestor), both package versions match tag, essential metadata and licenses/READMEs. Manual dispatch on a tag can validate but **cannot publish**.
- Validation then `npm ci`, `npm test`, `npm pack --dry-run` inspection, Python editable install, Python unit tests, `python -m build`, Twine distribution check, installed-wheel smoke test, and uploads short-lived Python dist artifact.
- `npm` publishes via `npm publish --ignore-scripts --access public` **only for a pushed tag** after validation using `NODE_AUTH_TOKEN: secrets.NPM_TOKEN`. Its job has read-only contents permission; unnecessary `id-token: write` was removed while token-based publishing remains configured.
- `pypi` consumes the Python artifact and uses Twine **only for a pushed tag** after validation with `TWINE_USERNAME=__token__` / `TWINE_PASSWORD: secrets.PYPI_API_TOKEN`. Upload remains separate/non-atomic.
- The workflows do **not** manage or expose secret values. Uploads are separate jobs, **not atomic**: one registry may succeed when another fails.
- Do not push a release tag without new matching package versions, verified access/secret scope and release authorization.

## `.github/workflows/registry-smoke.yml`
- Events: `main` push changing workflow file (smoke target comes from equal current JS/Python manifest versions), plus manual dispatch requiring explicit `version` such as `1.0.0`.
- `resolve` job validates numeric stable `MAJOR.MINOR.PATCH` and package identities before download; npm job fetches `kron-otp@<requested-version>` to a clean directory and checks package metadata **exactly matches requested version**, then runs generation/verification and source tests.
- PyPI job downloads wheel `kron-otp==<requested-version>`, creates isolated venv, installs its dependencies, checks installed distribution metadata **exactly matches requested version**, runs API and source tests. A missing/nonmatching public package fails the job.
- **P03 KO-010 code fix:** workflow is no longer pinned to v1.0.0 for actual downloads. Version selection is validated from a manual input or matching manifests on workflow-file push; inputs not in strict stable SemVer format fail before any registry access. No package publication occurs.

## Verified history (2026-11-16)
- Tag `v1.0.0` published to npm and PyPI: release workflow run `43835128215`, jobs successful.
- Published-package install smoke workflow run `43836244524`, both npm and PyPI jobs successful after temporary npm registry propagation delay.
- These are test outcomes for configured cases; not complete security certification.

## Maintenance
Log any workflow/package change in `project/DEVELOPMENT_LOG.md`, keep `project/FILE_MAP.md` and `docs/TESTING_AND_RELEASES.md` current, and use `notes/` for the initial private plan. Never record actual token values.

## P03 governance blocker: GitHub settings require admin controls

- Source of truth from GitHub on 2026-11-16: `branches/main` reports `protected: false`, `/rulesets` responds `[]`, and fetching `branches/main/protection` returns **403 Resource not accessible by integration**. The connected GitHub integration exposes no protection/ruleset mutation operation.
- **KO-007 NOT fixed merely by workflow editing.** Branch/tag protection must be set in GitHub repository Settings by an authorized administrator. Require enforced main PR-review + checks, no force-push/deletion, restricted bypass; protect matching `v*` release tags against unauthorized create/update/delete. Configure optional publish environments with required reviewer approval and verify actual enforcement; a YAML environment name is not proof of approval policy.
- The workflow uses verified SHA-pinned third-party actions (current upstream major tags at audit time): checkout v7 `3d3c42e5aac5ba805825da76410c181273ba90b1`; setup-node v7 `949feb2413d6458794dcd2491c4babbbce0c15c1`; setup-python v7 `6d4fd22b20465ccc0f7354476588e8df7c9ca0e0`; upload/download-artifact v4 `ea165f8d65b6e75b540449e92b4886f43607fa02` / `d3f86a106a0bac45b974a628896c90dbdf5c8093`; dorny paths-filter v4 `ceb8a2b8f2d89434be7ff52d3de7ec3738c5cc9d`.
- The previous `v1.0.0` public artifacts are unchanged. Never claim P03 fully CLOSED before actual branch/tag protection can be verified; record **BLOCKED — governance** in private phase ledger even if CI + smoke jobs pass.

## P03 verified workflow jobs — governance still BLOCKED (2026-11-16)

- **Implementation SHA:** `10107e53ab68afc83414c1cb0fd542963aa50852`.
- [KronOTP CI run 43855173877](https://github.com/vibtoolshq/KronOTP/actions/runs/43855173877): changes, JavaScript tests and Python tests all **SUCCESS** using aligned dependency commands.
- [Published Package Smoke run 43855173893](https://github.com/vibtoolshq/KronOTP/actions/runs/43855173893): version resolver, npm consumer and PyPI consumer all **SUCCESS**; logs confirmed requested **1.0.0**, public downloads and exact installed version matches; Python source suite 9/9.
- [KronOTP Release validation run 43855173879](https://github.com/vibtoolshq/KronOTP/actions/runs/43855173879): full validation **SUCCESS**, Python wheel install/test and npm payload inspection PASS, both **Publish npm** and **Publish PyPI** jobs **SKIPPED** (branch push, not tag push).
- Offline version-selection negative tests: 7/7 correctly handled (valid 1.0.0, push fallback accepted; malformed v-prefix, prerelease, newline/injection, shell expression and empty input rejected). This is not a live nonexistent-version registry test.
- **P03 status: BLOCKED — governance**. GitHub main `protected:false`, rulesets `[]`, branch-protection endpoint 403; there is no API write permission to enforce or verify main/tag restrictions. Only the workflow/code portion was verified. NO security sign-off or exception assumed.
- Neither package published; no new tag, version bump, credentials or engine changes. Repo admin must configure effective branch/tag controls and provide independently verified evidence before phase can close.

### P03 post-patch CI protection compatibility correction

The source CI workflow now runs on **every pull request** so a stable status exists for documentation-only changes. It retains language-selective Node/Python jobs, includes changes to all three workflow YAMLs in both language filters, and adds a mandatory `Required CI` aggregation job that runs even when individual engines are skipped. The gate fails if changed-language jobs fail or if detection does not succeed; it passes docs-only PRs only when both language jobs are correctly skipped. An authorized admin can select **Required CI** as a main branch protection status check, using the exact context shown by GitHub after CI completion.

**External gate unchanged:** this YAML is a check producer, not a main protection rule. Main/tag rulesets must still be configured in GitHub Settings; P03 remains BLOCKED until effective protection can be verified.

## v2.0.0 expedited release candidate (explicit maintainer instruction, 2026-11-16)

- Version bump in `javascript/package.json`, top-level/root package version in `javascript/package-lock.json`, and `python/pyproject.toml` to **2.0.0**. The original v1.0.0 tag stays immutable. This is **SemVer major** due to JS invalid-secret verification changing from exception to boolean and weak keys no longer accepted.
- **P03 governance deferred, not CLOSED** by explicit owner instruction. GitHub main/tag restrictions are still absent/not verified (`main protected:false`, rulesets `[]` at prior audit); P04 minimum runtimes, independent Python CVEs, app E2E and long-run performance were not tested, and do not become PASS upon release.
- The existing validated tag-push-only workflow performs npm and PyPI publishing from a new tagged main HEAD; separate jobs can partially succeed. Confirm each registry independently and avoid tag/registry overwrite. No `NPM_TOKEN` or `PYPI_API_TOKEN` secret values exposed.
- Release status and actual CI run IDs must be recorded **after** execution, not assumed from documentation.

## v2.0.0 publication confirmation — 2026-11-16

- Annotated tag `v2.0.0` points at release commit `eefafd9934a44243879068d9b8081005e68aeade`, both manifests and npm lockfile root version `2.0.0`.
- GitHub [release workflow 43867458691](https://github.com/vibtoolshq/KronOTP/actions/runs/43867458691): validation **SUCCESS**, Publish npm **SUCCESS**, Publish PyPI **SUCCESS**; PyPI uploaded both wheel and sdist, npm published public tarball.
- Source-independent download/clean install tests (Windows): npm `kron-otp-2.0.0.tgz` in temporary consumer **PASS**, Python `kron_otp-2.0.0-py3-none-any.whl` from official index in new venv **PASS**. Verified version/OTP generation/validation/input guardrails, plus Python epoch-29 case.
- The dedicated *GitHub Actions* version-aware `registry-smoke.yml` was **not dispatched for 2.0.0** in this release; independent clean registry consumer tests were run instead. Do not claim that a 2.0.0 registry-smoke workflow run exists.
- **Explicit one-time process exception:** GitHub main and v* tag protection absent/unverified and P04 cross-platform/security/stability acceptance incomplete. KO-007 and P04 are still open; historical v1.0.0 unmodified. No GitHub Release page (release object) was created by the existing workflow; tag and npm/PyPI packages were created successfully.


## P03-GOV-01 governance enforcement — 2026-11-28

On 2026-11-28 (Asia/Dhaka), P03-GOV-01 activated repository rulesets: main governance 28257893, v* tag creation 28257876 and v* tag immutability 28257888. API read-back verified active enforcement. Earlier statements that protection is unconfigured or blocked on administrator access describe the historical state, not the current settings.

Main requires a pull request and strict up-to-date Required CI from GitHub Actions (app 15368), with zero independent approvals as explicitly approved for this single-maintainer repository. Main force-push and deletion are blocked; no main bypass actors. The tag-creation ruleset permits only the authorized individual user technicelnurnobi (85743335) to bypass the creation restriction. Separate tag immutability blocks updates and deletion with no bypass. This does not prevent a sufficiently authorized settings administrator from later changing the rules themselves.

For a documentation-only PR, the existing Required CI aggregator must succeed; engine tests may legitimately skip. No workflow or release configuration files have changed. Configuration read-back passed; formal P03 acceptance remains conditional on this documentation PR passing Required CI and merging normally, final Git/local parity, unchanged historical tags, and recorded closeout evidence. No release tag, publish, deployment or destructive enforcement test is authorized by this phase. P04 and P05 remain outside scope; historical v2.0.0 publication is not full production acceptance.


## P04-S02-A01 runtime qualification — 2026-11-28

P04-S02/A01 adds `.github/workflows/p04-s02-compatibility.yml`, a PR-only compatibility qualification workflow. Eight Node and eleven Python targets (19 total) on Ubuntu 24.04 x64, Windows Server 2025 x64 and macOS 15 ARM64. Exact Python 3.10.0 is tested on Windows only; Ubuntu 3.10.x remains. Pinned actions, read-only contents permission, unchanged source tests and isolated npm/PyPI 2.0.0 consumer regressions; record runtime, dependencies, package origins and R-04 observations. Qualification acceptance is PENDING until actual dedicated CI and Required CI pass. No existing engine, dependency, workflow, governance or publishing changes.


## P04-S03 dependency and distribution qualification — 2026-11-28

P04-S03 adds `.github/workflows/p04-s03-security.yml`: PR-only, read-only, pinned actions on Ubuntu 24.04. Checks locked npm and isolated public v2 consumer graphs, independent Python source/consumer dependency audits using pip-audit 2.10.1, and official npm/PyPI v2 archives against registry digests, safe payload paths and pinned release source. Registry signatures/provenance metadata are observations, not verified publisher attestations; independent publish jobs are non-atomic. No engine/dependency/UI/publisher changes. Qualification acceptance PENDING until dedicated CI and mandatory Required CI PASS; final evidence in acceptance handoff.


## P04-S04 synthetic consumer qualification — 2026-11-28

P04-S04 adds `.github/workflows/p04-s04-consumer.yml`, `qualification/p04-s04/node-consumer.cjs` and `qualification/p04-s04/python_consumer.py`. PR-only isolated public v2.0.0 consumers exercise 12 named scenarios per engine: RFC current, adjacent, expiry, malformed, wrong account, stateless repeat, replay rollover/recovery, isolation, throttling/reset, rollback denial, concurrent duplicate and concurrent attempt budget. Synthetic caller transaction serializes check/verify/reserve using Node owner event loop and Python thread lock; 8 concurrent requests per case. 120s conservative token reservation, rolling 3/60s attempts, no matched counter inference. Collision tradeoff, single-process state and distributed atomic storage requirement remain; not production authentication, no external accounts. Qualification PENDING until dedicated and mandatory CI PASS. No public API, engine, GUI, dependency, existing workflow or release change.


## P04-S05 bounded performance qualification — 2026-11-28

P04-S05 adds `.github/workflows/p04-s05-performance.yml`, `qualification/p04-s05/benchmark.cjs` and `qualification/p04-s05/benchmark.py`. PR-only Ubuntu24 Node24/Python3.12 isolated public v2 consumers; fixed RFC correctness, monotonic measurement, 20 cold starts, 1000 warm-up operations, 10000 generate and 10000 verify, 1/4/8 independent process workers (2000 operations each), 600s sustained with >=5ms between pair starts, 10s RSS sampling, 20min job timeout. Reports nearest-rank p50/p95/p99, throughput, CPU and RSS, worker results, runtime/dependencies/hardware. Observation only; no numeric SLA. Zero unexpected errors/mismatches/OOM/timeout required. Timing includes deterministic clock shim and process startup where identified. No production load or engine/API/GUI/dependency/existing workflow changes. Acceptance PENDING until actual qualification and mandatory CI PASS.
