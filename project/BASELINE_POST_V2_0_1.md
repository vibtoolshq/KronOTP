# KronOTP — Post-v2.0.1 canonical continuation baseline

**Baseline ID:** BASELINE-FREEZE-02
**Audited:** 2026-11-28 (Asia/Dhaka); live Git/governance observations 00:02:52 UTC and registry bytes 00:03:18 UTC.
**Status:** source/published v2.0.1 scoped acceptance GO; baseline documentation closure requires protected PR Required CI and clean final Git parity. This is the current reference, superseding the earlier v2.0.0 snapshot for continuation only.

## 1. Read first — three distinct anchors

| Anchor | Exact value |
| --- | --- |
| GitHub authority | [vibtoolshq/KronOTP](https://github.com/vibtoolshq/KronOTP), main |
| Audited incoming main = local HEAD = origin/main | `f23a9739efdeadde17a8562ab49f8506a5eba7bc` |
| Incoming Git tree | `94328f842bb6a6308b1b293db12993d4ce05e6e9` |
| Immutable release source | `c732cae0e58fe7e21bc0160f3814dc99d27990d1` |
| Release Git tree | `e17b9416f9d5e68d94e1b0cf569825f1b26c4d72` |
| v2.0.1 annotated tag object | `a6b26704cdc80e502b637da4df72ed4806f3703e` |
| Final continuation HEAD | Resolve merged BASELINE-FREEZE-02 documentation PR, compare exact scope and tree; final SHA is recorded after merge in closeout and Drive. Do not mistake incoming snapshot for final docs-only HEAD. |

Incoming working tree clean, zero open PRs; 68 tracked blobs/18 directories, exact remote/local metadata match. [Complete inventory](./BASELINE_FILE_INVENTORY_POST_V2_0_1.md). Relative to release source only README.md, docs/TESTING_AND_RELEASES.md, project/CI_AND_RELEASE.md, project/DEVELOPMENT_LOG.md differ (88 insertions/16 deletions). No runtime changes after release. Historical tags: v1.0.0 object 7d8fd974af349d1a193a6124cb3681e0bcc8235e -> e77155eefd7d18d49fcde489b510f4fd8df5d797; v2.0.0 object 44665efaee1cf1e7c0bf19a79329a055fc57fc50 -> eefafd9934a44243879068d9b8081005e68aeade. No tag movement. Freeze is a reference, not a new tag or branch lock.

Evidence vocabulary: LIVE = checked in this audit; CODE = inspected exact tracked source; HISTORICAL PASS/FAIL/SKIPPED = previous actual run; OWNER CONFIRMED = attestation, not independently verified settings; OPEN = future work or unresolved risk. A missing result is not PASS.

## 2. Architecture and invariant product contract (CODE)

MIT two-language synchronous stateless TOTP libraries, not a web service, authentication server, or desktop package. JS CommonJS `javascript/src/kron-otp.js` exports class directly and via .KronOTP; Python `python/src/kron_otp.py` imported with `from kron_otp import KronOTP`. Public static generate(secret) -> six-digit string and verify(secret, token) -> boolean only. SHA1, 6 ASCII digits, period 30 seconds, previous/current/next step; fixed parameters. No public timestamp/window/digest configuration, storage, user enrollment, replay protection, throttling, network or login API. Preserve existing API and normalization contract.

| Boundary | Behavior |
| --- | --- |
| Base32 | ASCII whitespace only, case-insensitive, canonical padding/unused bits, decoded length >=14 bytes; recommend >=20 random bytes; raw max4096, normalized max1024 |
| JS validation | private #createTOTP, invalid generate TypeError; malformed verify returns false; other unexpected exceptions may propagate |
| Python validation | _normalize_secret / _totp; generate ValueError for invalid secret, distinct negative-clock ValueError, sanitized expected generation failures; verify False on expected invalid input |
| Epoch | Python verify special case 0–29 seconds checks current and next, avoids negative predecessor. generate reads time once after secret validation. |
| Packages | npm and PyPI both 2.0.1, lock root aligned; Node >=20.19.0, Python >=3.10; use maintained patched runtime, not merely declared minimum. |
| Runtime graph | OTPAuth ^9.6.0; npm lock resolves 9.6.0 + @noble/hashes 2.4.0. PyOTP >=2.12,<3; last actual resolution 2.12.2, not fully pinned. |
| Packaging | npm package.json files src/README/LICENSE; Python setuptools single py-module, MANIFEST.in includes tests/totp_vectors.json in sdist only. GUI excluded from installed library. |

Exact core blobs: JS f7e17fda583d71f7ea2e5dfccc4b7463382b5240; Python 1e75a30c0bda3aa78adcbf0d81412e401608d723. The two confirmed source defects (R-04 negative-clock diagnostic, missing sdist test vectors) fixed and delivered in 2.0.1. No other confirmed open source defect identified by this baseline review; not a claim of exhaustive bug absence.

### Source-only GUI

`python/tests/gui/{app.py,vault.py,test_app.py,README.md}`: Tkinter app up to 100 accounts, search/add/edit/delete, compatible otpauth URI, temporary unsaved secret, live OTP/countdown, conditional clipboard clear 15s, local verify, privacy lock / 5min inactivity, Windows DPAPI CurrentUser vault (not independent password lock), non-Windows temporary use. Historical Windows 8/8 GUI tests PASS on 2.0.0. **Exact installed-version guard still targets 2.0.0**. Do not blindly change its pin or claim 2.0.1 GUI qualification. No EXE, QR-camera or remote login acceptance.

## 3. File and control-flow map

| Location | Responsibility |
| --- | --- |
| javascript/src, python/src | Runtime engine; two small wrappers |
| javascript/tests/test.js; python/tests/test_kron_otp.py; python/tests/totp_vectors.json | Shared 6 RFC-derived +80 parity vectors; Python current 13 methods |
| python/tests/gui | Source-only local desktop demo/vault |
| qualification/p04-s04 | Synthetic caller security fixtures |
| qualification/p04-s05 | Bounded performance benchmarks |
| qualification/p05-a04 | 21 synthetic release contract methods |
| scripts/release/registry_contract.py | Build, inspect safe archive/metadata/RECORD, verify bundle/binding, query registries, classify/reconcile, smoke gate |
| scripts/release/requirements-build.lock | 50 exact hash-locked tooling packages, Linux CPython 3.12.16 |
| .github/workflows | Ten workflows; see below |
| .vibtools/ | Developer portal config/logo; config version still 2.0.0; docs/index.md frontmatter 2.0.0. Actual live portal not reverified. |
| docs/ | Public docs, docs/index.md landing and docs/MANIFEST.md source inventory |
| project/ | Tracked maintainer technical reference |
| notes/ | Ignored local private evidence; never publish or copy raw notes into Git |

## 4. Workflow, governance and release boundary (LIVE + CODE + previous qualification)

| Workflow | Role / trigger |
| --- | --- |
| ci.yml | PR + path-filtered branch pushes; Required CI aggregator, Node/Python tests only when relevant |
| p04-s02-compatibility.yml | PR qualification, 19 selected targets |
| p04-s03-security.yml | PR security/archive audit |
| p04-s04-consumer.yml | PR caller security scenarios |
| p04-s05-performance.yml | PR bounded workload |
| p05-sdist.yml | PR extracted sdist / derived wheel |
| p05-a04-release-contract.yml | PR release contracts |
| p05-a05-toolchain.yml | PR tooling/advisory/reproducibility, version manifest/lock triggers |
| release.yml | Tag-only publishing; main-path/manual nonpublishing validation |
| registry-smoke.yml | Main path, manual exact version, reusable post-publish |

Three live active rulesets: 28257893 main PR, strict Required CI app15368, deletion/non-fast-forward prohibited, zero independent approvals; 28257876 tag creation restricted to authorized owner actor; 28257888 tag update/delete forbidden, no bypass. Single-maintainer and administrative rule-change risk. Existing organization token authentication NPM_TOKEN/PYPI_API_TOKEN, values never inspect. Owner confirmed validity/scope and accepted shared-token/unsigned-tag/provenance limitations **for v2.0.1 only**. No permanent acceptance for future releases.

Release build uses Ubuntu24.04 x64, Node24.22.3/npm11.19.1, CPython3.12.16, 50 pinned tools including pip26.3/build1.6.1/setuptools84.2.1/wheel0.48.0/twine7.0.0/pip-audit2.10.1. Hash-only compatible wheels, exact installed graph, no backend downloads, commit-derived epoch, canonical sdist, wheel from sdist, immutable bound manifest/bundle. Two publishers independent, not atomic. Preflight all absent, compare actual registry bytes, classify full exact/partial/conflict/unknown. No blind rerun or upload retry. Release workflow still has immediate visibility reconciliation; future improvement not implemented.

## 5. Acceptance evidence (historical, not new tests)

| Phase | Actual acceptance |
| --- | --- |
| P01–P03 | Closed; input/time/CI hardening, protected rules verified |
| P04 runtime | [46058729635](https://github.com/vibtoolshq/KronOTP/actions/runs/46058729635) 19 targets, 38 source/published 2.0.0 suites; exact Python3.10.0 Windows only |
| P04 security | [46059824623](https://github.com/vibtoolshq/KronOTP/actions/runs/46059824623) 4 graphs zero reported vulns at scan, 3 archives verified |
| P04 caller | [46060701345](https://github.com/vibtoolshq/KronOTP/actions/runs/46060701345) 24/24 synthetic scenarios |
| P04 performance | [46061887435](https://github.com/vibtoolshq/KronOTP/actions/runs/46061887435) two 600s bounded workloads, zero unexpected error/mismatch/OOM/timeout |
| P05-A01 | [46068002722](https://github.com/vibtoolshq/KronOTP/actions/runs/46068002722) 13/13, R-04 fixed |
| P05-A02 | [46071499080](https://github.com/vibtoolshq/KronOTP/actions/runs/46071499080) 13/13 each extracted source/derived wheel, fixture verified |
| P05-A03/A01 | Owner-confirmed old exposed token revoked/replaced; release-specific risk disposition recorded; no secret inspection |
| P05-A04 | [46076859856](https://github.com/vibtoolshq/KronOTP/actions/runs/46076859856) 21/21 synthetic contracts |
| P05-A05/A01 | Original [46078021001](https://github.com/vibtoolshq/KronOTP/actions/runs/46078021001) FAILURE preserved; [46079118728](https://github.com/vibtoolshq/KronOTP/actions/runs/46079118728) 50 tools, 3 artifacts, 8 marker fixtures, 5 advisory graphs PASS |
| P05-A06 | [46079984869](https://github.com/vibtoolshq/KronOTP/actions/runs/46079984869) docs Required CI PASS; preparation-only NO-GO superseded by recovery |
| v2.0.1 qualification | [46082157882](https://github.com/vibtoolshq/KronOTP/actions/runs/46082157882) same commit 3/3 byte equality, 50 tools, 8 fixtures, 5 graphs zero vulnerabilities/zero Python skips; PR/branch/main CI PASS, main [46082324642](https://github.com/vibtoolshq/KronOTP/actions/runs/46082324642) nonpublish PASS |
| Release | [46082457680](https://github.com/vibtoolshq/KronOTP/actions/runs/46082457680) FAILURE, both publishers PASS, reconciliation PARTIAL, auto smoke SKIPPED |
| Recovery | [46083365483](https://github.com/vibtoolshq/KronOTP/actions/runs/46083365483) new authorized nonpublishing run 3/3 PASS; exact public bytes, installed consumers, JS86/Python13 PASS |
| Recovery docs | PR #13 / [46083482879](https://github.com/vibtoolshq/KronOTP/actions/runs/46083482879) PASS, JS/Python skipped intentionally |

G01–G11 accepted; G12 GO for v2.0.1 through approved recovery route. P01–P05 and six P05 remediation reviews accepted in scope. Original 12 KO findings addressed in scope, not 12 vulnerabilities. Do not conflate the six supplementary reviews with five original P01–P05 roadmap phases. No new build/test/scan in this freeze; current-source exhaustive matrix after R-04 not run. Advisory scan timestamp 2026-11-27 23:23 UTC; zero reported vulnerabilities then, not current perpetual security. Same-commit Linux reproducibility only. Performance observation, not SLA; Python RSS metric discrepancy unresolved. No distributed auth or full security certification.

## 6. Public artifact verification (LIVE)

npm and PyPI latest 2.0.1 at 00:03:18 UTC, downloaded bytes independently matched original recorded release manifest and registry digest metadata.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| kron-otp-2.0.1.tgz | 3188 | 3b963d59cd7d1600f0be5dfd114f88baf9ad4ec5b24a810e9a6da2a76dda31c9 |
| kron_otp-2.0.1-py3-none-any.whl | 5074 | 74ee3702e467bb8d3659162632d0d88c93c1120f0da9c9f136777dfc4553cc2e |
| kron_otp-2.0.1.tar.gz | 7452 | 70f240af3ab525ae6ba9aaeb9ab64582af79aa567bb06685b761fb30c4562231 |

Original manifest SHA256 ec91d48e0a40d88030b608b81695c93be755a597e426383f58e23c3339047df3; retained [artifact 15237494004](https://github.com/vibtoolshq/KronOTP/actions/runs/46082457680/artifacts/15237494004), archive metadata SHA256 10fa3f3191768a36c658575ae0610dcb472017be34a5f388e4ba070b4fff088d, not expired at audit, expiry 2026-12-11 23:26:35 UTC. Original archive not independently redownloaded for this freeze. Recovery artifact 15237916728. npm CLI success 23:26:58Z, reconciliation failed 23:27:22Z, registry publication metadata 23:29:04Z; delayed public visibility, internal cause unknown. No republish. Prior observed npm attestation absent/gitHead missing, PyPI provenance HTTP404, tag unsigned. No cryptographic publisher identity proof. Tag-only procedure, no GitHub Release object created.

## 7. Prioritized open work (NOT APPROVED / NOT IMPLEMENTED)

| ID | Actual condition | Proposed next step |
| --- | --- | --- |
| B01 | Immediate registry reconciliation caused historical failure | RELEASE-HARDENING-01 bounded read-only visibility polling, explicit timeout/conflict/unknown, offline delayed fixtures; no upload retry |
| B02 | Portal metadata and some public installation docs remain 2.0.0 | Separate documentation sync, preserve historical references and verify actual portal; no engine/version bump |
| B03 | GUI exact-version guard 2.0.0 | Separately approve upgrade to 2.0.1 and focused Windows GUI/vault tests |
| B04 | Token-based publish transition and unverified provenance/signing | Verify current registry policy before next release, assess OIDC/staged flow and signing; no permanent waiver |
| B05 | Runtime range future resolution, lifecycle, full matrix and performance limits | Fresh focused advisories and runtime qualification as change requires; no claim of universal compatibility |
| B06 | Original release bundle retention deadline | Preserve evidence before expiry if needed, no new release/rebuild to replace original |

No implementation of these items in baseline freeze. User must approve a new phase. Do not call incomplete visibility polling a source bug or claim release remains partially published.

## 8. Mandatory continuation protocol

1. Read AGENTS.md, AI_INSTRUCTIONS.md, this snapshot, inventory, relevant exact current code and historical evidence. Resolve current authoritative main and actual local branch/HEAD/origin/tree; compare final freeze PR merged commit; stop on drift or dirty tree. Never reset to historical source tag.
2. Establish exact scope and create dated local private note before tracked changes. Recheck real current registry/runner/dependency facts only when relevant. No secret values or private notes in Git.
3. GitHub-first narrow candidate, exact diff, one focused qualification plus automatically triggered Required CI. Preserve failed evidence and differentiate PASS/FAIL/SKIPPED/NOT RUN. Do not approve next phase implicitly.
4. Protected PR, exact tested tree, local fetch and fast-forward only, final GitHub/local/origin parity and clean tree; preserve immutable tags. No release/version bump/deploy unless separately authorized.
5. Update related project/docs and private ledgers; Drive canonical current state/resume/decisions/open items/history/CI evidence; read back. New baseline supersedes by explicit verified checkpoint, never silently overwrite historical evidence.
6. If mandatory gate fails, STOP and record precise blocker; do not merge/publish or launch blind rerun. Caller security obligations remain: secret storage, trusted clock, account binding, atomic durable replay prevention, throttling.

Historical [v2.0.0 source snapshot](./BASELINE_2026-11-28.md) and its inventory are retained unchanged. This record takes precedence for current baseline; historical pending text describes earlier checkpoints.
