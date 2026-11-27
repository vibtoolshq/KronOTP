# Quality, Test Coverage, Security Boundaries and Known Gaps

## P05-A01 — Python generation diagnostic correction (source candidate)

This change is limited to Python `KronOTP.generate()`: validate and construct the TOTP before reading the clock, sample `time.time()` once, reject any negative Unix timestamp (including fractional pre-epoch time) with `ValueError("Invalid system clock: TOTP requires a non-negative Unix timestamp.")`, then generate with `totp.at(snapshot)`. Expected construction errors retain the existing sanitized invalid-secret `ValueError`; expected generation-stage errors use `ValueError("TOTP generation failed.")`. Invalid secret takes precedence. No new public parameter, exception class, dependency, algorithm or change to `verify()`.

Four new targeted unittest methods cover negative/fractional pre-epoch times, invalid-secret precedence, independent counter 0/1 references with one clock read, and sanitized dependency-generation ValueError. The nine original methods, six RFC and 80 shared vectors are retained (13 methods proposed total). No fresh cross-platform/GUI/published consumer test is implied.

Source candidate only; acceptance requires the actual protected PR CI and verified closeout. Published PyPI 2.0.0 and npm 2.0.0 remain unchanged; PyPI v2 retains the historical negative-clock misclassification. Do not assume installing v2 delivers this source fix. P05 final release acceptance remains NO-GO.

Previous P04 R-04 OPEN observations below refer to the historical engine before this candidate. Other P05 risks remain unchanged.

## P04 consolidated qualification — 2026-11-28

**Current status (2026-11-28):** P01–P03 closed; P04 qualification evidence verified and consolidation acceptance pending this documentation PR and final closeout. P05 final production/release acceptance has not started. Older dated statements below about deferred governance, unexecuted P04 tests or offline clone are historical, not current status. No new package release or application change.

| Qualification | Recorded run | Actual result |
| --- | --- | --- |
| Runtime/source/consumer | [46058729635](https://github.com/vibtoolshq/KronOTP/actions/runs/46058729635) | 19/19 jobs; 38/38 suites |
| Dependency/distribution | [46059824623](https://github.com/vibtoolshq/KronOTP/actions/runs/46059824623) | 3/3 jobs; four runtime audit scopes zero known vulnerabilities at scan time; three archives checked |
| Consumer/caller | [46060701345](https://github.com/vibtoolshq/KronOTP/actions/runs/46060701345) | 2/2 jobs; 24/24 named scenarios |
| Bounded performance | [46061887435](https://github.com/vibtoolshq/KronOTP/actions/runs/46061887435) | 2/2 jobs; approved functional gates passed |

Four corresponding Required CI runs [46058729566](https://github.com/vibtoolshq/KronOTP/actions/runs/46058729566), [46059824535](https://github.com/vibtoolshq/KronOTP/actions/runs/46059824535), [46060701180](https://github.com/vibtoolshq/KronOTP/actions/runs/46060701180), [46061887357](https://github.com/vibtoolshq/KronOTP/actions/runs/46061887357) passed; path-filtered engine jobs skipped there, not counted as passes. These are historical executed results from the approved P04 qualification candidates, not new tests executed by this documentation change. P04-S06-A01 documentation acceptance remains conditional on this PR's Required CI, exact diff, protected merge, baseline parity and verified closeout.

Both engines remain stateless synchronous six-digit SHA-1/30-second libraries, with a ±1-step verification window and boolean verify result. A successful verify does not identify the matched counter. Never infer the matched counter from the server's current counter. The relying party must bind the secret to an authenticated account/enrollment, protect it, synchronize trusted time, fail closed on clock anomalies, throttle per account and relevant abuse dimensions, atomically reserve an accepted code before granting authentication, and maintain replay state across replicas/restarts for the full acceptance horizon. Use appropriately protected replay storage; do not log secrets or OTPs. A conservative per-account code reservation spanning the full acceptance window plus boundary margin can reject coincidental equal codes from different counters. The synthetic fixtures use 120 seconds retention, 3 attempts/60 seconds and 8 concurrent requests; these are test parameters, not universal policy. They demonstrate single-process serialization, not distributed atomicity, durable storage or session issuance.

Residual review items: R-04 (Python generate at a simulated negative system clock mislabels the error as invalid secret; 22/22 diagnostic observations), missing shared vector fixture in PyPI v2 sdist (direct sdist regression not run), unsigned historical tag, unverified publisher attestations/signature authenticity, independent non-atomic npm/PyPI publishing, Python range-based dependencies, publisher secret scope and automatic post-release smoke not established. The maintainer explicitly deferred R-04 remediation/final acceptance to P05 for scoped P04 closure only. R-04 stays OPEN, not fixed or permanently waived. No other risk is implicitly accepted. Final production/release acceptance remains NO-GO pending P05 and any separately authorized remediation.

KO-009 is eligible for closure as caller guidance and synthetic fixture evidence only; KO-011 as honest tested/declared/maintained runtime and feature scope; KO-012 as bounded qualification evidence. Formal dispositions require successful docs PR and verified closeout. No independent certification.

Audit basis: `javascript/tests/test.js`, `python/tests/test_kron_otp.py`, three GitHub workflows and published `v1.0.0` CI evidence as of 2026-11-16. These are facts about current tests, not a security certification.

## Current tested behavior

**JavaScript** `npm test` / `node javascript/tests/test.js` checks sample-secret generation, exact six-digit string format, own-token verification, lowercase/whitespace normalization, malformed/short token format and invalid secrets. P01 tests use a **160-bit** public fixture and 1/10/13/14/20-byte boundaries, ASCII/Unicode input and bounded-size cases.

**Python** P02 expands the source `unittest` suite from six to **nine methods** (six P01 tests, one RFC vectors test, one 80-case shared reference test, and one epoch/rollover/drift test). PyOTP >=2.12 rejects under-14-byte secrets. GitHub job verification is recorded in the development log after execution.

**Release CI** validates both packages, npm pack contents, Python wheel+sdist, wheel smoke import. Published-package smoke CI downloads and installs registry versions into isolated contexts. The published smoke workflow completed successfully in run `43836244524`.

## P01 addressed findings and open hardening work

| Item | Evidence | Remaining action / scope |
| --- | --- | --- |
| KO-001: weak-key acceptance | **P01 fixed on development `main`**: both wrappers require >=14 decoded bytes | Provision random >=20-byte secrets; later release migration/semver review required |
| KO-003: invalid-secret verification | **P01 fixed on development `main`**: both `verify` methods return false/False for expected invalid input | JS `1.0.0` previously threw; documented breaking change needs release migration review |
| KO-004: whitespace normalization | **P01 fixed on development `main`**: ASCII whitespace only, reject Unicode BOM/NBSP and pre-uppercase non-ASCII | Review legacy consumers before release |
| KO-008: unbounded input | **P01 fixed on development `main`**: raw <=4096, compact <=1024 characters | Downstream authentication server must still rate-limit requests |
| KO-005: deterministic RFC/vector automation | P02 includes 6 fixed-time RFC SHA-1 6-digit known outputs and 80 independent synthetic reference cases in both source test suites | Verify passing JS/Python CI jobs; supported SHA-1/6/30 only |
| KO-002: boundary verification | P02 guards negative PyOTP drift offset during epoch time 0–29; tests cover 0,1,29,30,59,60,61, leading zero, ±1 and two-step rejection | Verify Python and JS CI, no broader verifier policy |
| KO-006 CI version drift | P03 uses `npm ci` with committed lockfile and Python editable install from `pyproject.toml` | Validate full CI Node and Python jobs; Python dependencies still range-based |
| KO-010 Published smoke version | P03 selects explicit requested stable version or matching manifest defaults; downloaded/installed artifact must equal requested version | Validate current public `1.0.0` and wrong-version failure |
| Stateful replay/abuse defense | APIs are stateless and tolerate one adjacent time step | Enforce single-use timecodes, rate limiting and account lockout on relying-party server |

## P01 additional guardrails

- Both wrappers reject Base32 secrets shorter than 14 decoded bytes, raw input longer than 4096 chars and cleaned Base32 longer than 1024 chars.
- Normalize only ASCII whitespace (space, tab, CR, LF, FF, VT). Reject Unicode BOM/NBSP and non-ASCII case mapping. Reject noncanonical padding bits.
- A 112-bit length threshold only prevents trivially short encoded keys: it does **not** guarantee unpredictability. Provision random 160-bit or longer secrets for new accounts.
- Historical public registry `v1.0.0` binaries are not updated by development `main` changes.
- Focused P01 CI evidence: [KronOTP CI run 43847176070](https://github.com/vibtoolshq/KronOTP/actions/runs/43847176070): Node tests PASS; Python tests 6/6 PASS. [Release validation run 43847175995](https://github.com/vibtoolshq/KronOTP/actions/runs/43847175995): validation PASS, both publish jobs SKIPPED.

## Security model

- Raw Base32 shared secrets are supplied by the *caller*, not collected from a website by KronOTP.
- The wrappers have no built-in network transmission or persistence. Real secrets must remain in an external secret manager or secured runtime environment; never print a secret to logs.
- A matching OTP from a generator does not prove successful authentication; the server performs authentication, replay prevention and throttling.
- Host clock synchronization is required; tolerance window expands the set of potentially accepted time steps.
- GitHub Actions secret **names**: `NPM_TOKEN`, `PYPI_API_TOKEN`. Values and external registry account permissions are not stored here.
- P01 hardens secret input/error behavior; P02 addresses only the Python epoch-boundary bug and deterministic tests. SHA-1/6/30, normal ±1 validation and stateless design remain unchanged. P03 CI dependency drift, version-aware registry smoke and release governance remain open.

## Verification conventions

Mark each claim as observed from source, CI log, or direct test. Use PASS/FAIL/SKIPPED. Keep security-related changes narrowly scoped and require verification before releasing a patch version.

## P02 audit scope and evidence boundary

- Shared fixture is public synthetic data; the reference script independently calculates HMAC-SHA1 TOTP and cross-checks all six known RFC outputs before exporting 80 expected values. Fixture is for source CI tests, not for package runtime or users' secrets.
- The Python time-boundary fix samples time once per call, checks current/next counters 0/+1 explicitly with `valid_window=0` if `0 <= now < 30`, and otherwise retains `valid_window=1` unchanged. Negative timestamps remain failures.
- These checks do not imply all algorithms, concurrency, long-duration memory stability or server replay defense are covered; P03/P04 remain pending.

## P02 focused verification results (2026-11-16)

- [Source CI 43851819951](https://github.com/vibtoolshq/KronOTP/actions/runs/43851819951): change detection, Node and Python jobs all SUCCESS.
- Local Node source tests PASS (six RFC values, 80 independent expected synthetic key/time/code values, edge/window cases), local Python `unittest` **9/9 PASS** including the former Unix-epoch false-rejection case.
- Python current/next counter checks at timecode zero preserve ±one step for normal timecodes; no negative counter is generated. JS runtime and both package metadata remain unchanged.
- This confirms the **configured P02 regression suite**, not comprehensive security certification, concurrency/performance assurance or newly published npm/PyPI artifacts. P03/P04 hardening remains open.

## P03 workflow source hardening vs external repository protection

- CI uses lockfile-safe Node install and Python dependencies defined by distribution metadata; Actions pinned to specific Git commits; release publication constrained to pushed version tags rather than manual tag-targeted dispatch; tag points at current main HEAD.
- Public registry smoke accepts strict stable SemVer, resolves manifest default on workflow pushes and verifies matching installed package metadata on npm/PyPI; no archive modification or publication in smoke.
- **KO-007 remains BLOCKED by GitHub permissions/settings:** main `protected:false`, rulesets `[]`, branch-protection read 403. Administrator action + verification mandatory; workflow edits are not equivalent to actual tag/branch protection.

## P03 verified hardening and remaining unverified governance

- `npm ci` and Python editable install from package metadata verified by CI [43855173877](https://github.com/vibtoolshq/KronOTP/actions/runs/43855173877) (both test jobs SUCCESS).
- Version-aware registry downloads and exact version assertions confirmed for public `1.0.0` by [43855173893](https://github.com/vibtoolshq/KronOTP/actions/runs/43855173893), plus 7 local positive/negative resolver tests. Different future versions will require their own public artifact check.
- Tag-push-only release jobs, current-main-head check and commit-pinned actions validated in release branch run [43855173879](https://github.com/vibtoolshq/KronOTP/actions/runs/43855173879), with publishers SKIPPED.
- **KO-007 remains open:** no actual enforced branch/tag protection. GitHub `main protected:false`, rulesets `[]` and protection read 403; code-only guards are insufficient against unauthorized tag creation/repo edits. P03 cannot be fully closed before admin verification or explicit risk acceptance.

### P03 required-check corrective audit finding

Conditional CI without an always-present PR check could block docs-only PRs when required by branch protection. The P03 scope-locked follow-up added `Required CI` (unconditional PR coverage + fail-closed affected-language gate). No crypto/API/test runtime change; actual GitHub Settings protection remains unconfigured/blocked.

## v2.0.0 release exception (risk not eliminated)

The owner directed an expedited major-version release with GitHub main/`v*` tag rulesets deferred and P04 production assurance still not executed. The missing GitHub governance controls KO-007 remain open; passing engine tests, registry smoke and tag validation do not establish end-to-end supply-chain security, independent CVE absence, OS/minimum-runtime support or relying-party replay/throttle protections. This exception must not be presented as a security certification.

### v2.0.0 independently verified distribution snapshot

Release [43867458691](https://github.com/vibtoolshq/KronOTP/actions/runs/43867458691) passed both publishing jobs. Exact npm and PyPI 2.0.0 public artifacts were clean-installed and tested with public fixture keys (including reject-short-keys and Python epoch 29s); **PASS** in the tested Windows environment. No new v2 GitHub registry-smoke workflow run was made. Main/tag protections and P04 environment/load/CVE qualification remain open; do not convert release success to full security certification.

## GUI-01 security and verification boundary

- GUI-01 is an optional source-only Tkinter consumer with an in-memory masked secret Entry; Show/Hide affects screen visibility, not secret encryption. No key is written to files, external services or stdout by app code. Copy explicitly places only the OTP in the operating-system clipboard.
- Startup validates both installed `kron-otp==2.0.0` distribution metadata and the imported module's filesystem origin; an editable/local source import is rejected. This ensures the example tests the released PyPI engine rather than silently passing on developer source.
- GUI's local time-based OTP display is **not** an account login acceptance test; user/server must protect secrets, synchronize clocks, throttle retries and reject replay. It does not add security protections to the library or claim P04 production assurance.
- GUI-01 focused Tkinter/package integration and code audit results belong to the phase closeout log, not assumed solely from adding a source file. GitHub Python unit CI will not automatically execute an interactive GUI window.

### GUI-01 verified local integration (2026-11-16)

- Isolated Windows Python 3.12 venv installed the **published PyPI `kron-otp==2.0.0`** using the official PyPI index (with PyOTP 2.12.0); module provenance/wrong-version/shadow checks **PASS**.
- The focused real Tkinter test exercised Generate, masked/visible entry, missing/weak input errors, 30-second countdown, boundary refresh, copying OTP (not secret) and state reset on editing; window startup and scheduled-event close **PASS**.
- [GUI-01 CI run 43900702231](https://github.com/vibtoolshq/KronOTP/actions/runs/43900702231): Python tests & Required CI **SUCCESS**, JavaScript job correctly SKIPPED. [Release validation 43900702066](https://github.com/vibtoolshq/KronOTP/actions/runs/43900702066): validation **SUCCESS**; publishers SKIPPED.
- This is verified behaviour only on the tested Windows/Python 3.12 environment and mocked rollover; no multi-OS GUI assurance, external authenticator login verification, secret encryption, replay defense, or P04 security certification was performed.

## GUI-02 production-oriented desktop threat boundaries (2026-11-16)

- Persistent secret storage is available only on Windows using OS-provided DPAPI CurrentUser. It is **user-bound encryption at rest**, not a separate master password, memory hardening, account authorization boundary or solution against malware already executing as that Windows user.
- Add/Edit/Use once inputs are verified using the *installed* PyPI KronOTP engine and URI config is restricted to its actual fixed SHA1/6/30 support. Vault has <=100 account and bounded file/schema limits, rejects corrupt/unreadable entries rather than overwriting them, and atomically saves encrypted bytes. No plaintext export or portable recovery is offered.
- Account secrets are in memory while unlocked and may remain in process memory after lock/exit despite dropping references. Screen exposure, leaked screenshots, clipboard monitors, Windows-user session compromise, unrecoverable Windows profile changes and inaccurate device time remain threats.
- Clipboard auto-clear only checks whether its own previously-copied OTP still remains after 15 seconds; other processes can read it before then, and clearing is not guaranteed across system clipboard interactions. App privacy Lock only hides/unloads app state; it is NOT OS user reauthentication.
- The app cannot validate server login, prevent TOTP replay, impose rate limits, audit account security, scan QR images, protect recovery codes or certify independent security. P03 governance and P04 assurance remain pending despite the source-only Authenticator improvements. Tests and results must distinguish targeted Windows use from full production security certification.

### GUI-02 executed Windows assurance checks (not independent certification)
- Actual isolated Windows Python 3.12 PyPI v2 engine + Tk/DPAPI 8/8 tests PASS, including current-user encryption/decryption, no plaintext synthetic secret at rest, corruption handling, UI account lifecycle, unsupported otpauth URI formats, pending callback cleanup, timed code refresh and clipboard behavior. Tests performed with **synthetic RFC secret only**.
- First run exposed Tcl queued-timer shutdown warnings; GUI-scope callback cancellation/normalization was patched and retested **without warnings**. GitHub engine Python/Required CI passed at [43906779325](https://github.com/vibtoolshq/KronOTP/actions/runs/43906779325).
- Remaining non-tested items: hostile same-user malware, secure memory zeroization, restore from Windows profile corruption, full manually reviewed GUI appearance/keyboard accessibility at all scaling factors, non-Windows encrypted persistence (deliberately disabled), independent vulnerability/penetration test and external authentication provider acceptance. No production security certification asserted.


## P03-GOV-01 governance enforcement — 2026-11-28

On 2026-11-28 (Asia/Dhaka), P03-GOV-01 activated repository rulesets: main governance 28257893, v* tag creation 28257876 and v* tag immutability 28257888. API read-back verified active enforcement. Earlier statements that protection is unconfigured or blocked on administrator access describe the historical state, not the current settings.

KO-007: configuration remediation verified; formal closure pending the PR and final acceptance below. KO-009/011/012 and broader production qualification are unaffected.

Main requires a pull request and strict up-to-date Required CI from GitHub Actions (app 15368), with zero independent approvals as explicitly approved for this single-maintainer repository. Main force-push and deletion are blocked; no main bypass actors. The tag-creation ruleset permits only the authorized individual user technicelnurnobi (85743335) to bypass the creation restriction. Separate tag immutability blocks updates and deletion with no bypass. This does not prevent a sufficiently authorized settings administrator from later changing the rules themselves.

Configuration read-back passed; formal P03 acceptance remains conditional on this documentation PR passing Required CI and merging normally, final Git/local parity, unchanged historical tags, and recorded closeout evidence. No release tag, publish, deployment or destructive enforcement test is authorized by this phase. P04 and P05 remain outside scope; historical v2.0.0 publication is not full production acceptance.


## P05-A05 — controlled release tooling (2026-11-28)

Release builds and Python publishing use isolated hash-locked tooling (50 exact package versions including build, setuptools, wheel, Twine, pip and pip-audit). Controlled Ubuntu 24.04 x64, Node 24.22.3/npm 11.19.1 and CPython 3.12.16. Build subprocesses use the locked interpreter without backend isolation/downloads. The sdist preserves verified member bytes while canonicalizing tar/gzip headers and ordering with commit-derived SOURCE_DATE_EPOCH; wheel built from that sdist. Dedicated PR qualification compares two independent fresh venv/build roots for byte-identical artifacts and checks source/installed-candidate npm/Python runtime and tooling advisory graphs. Runtime dependency ranges, engine and publishing credentials unchanged. Scope is controlled same-commit Linux rebuild, not universal reproducibility or permanent vulnerability guarantee. Production use maintained security-patched runtimes; historical compatibility is not lifecycle support. Qualification pending CI; no live publication. Token validity and registry policy remain mandatory release-preflight.
