# Quality, Test Coverage, Security Boundaries and Known Gaps

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
| CI version drift | `ci.yml` Python pip constraint is wider than `pyproject.toml`; Node job uses `npm install` vs lockfile | Align versions and use reproducible install |
| Published smoke version | `registry-smoke.yml` tests only 1.0.0 | Version-aware target for later tags |
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
