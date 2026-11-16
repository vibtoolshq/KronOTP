# Quality, Test Coverage, Security Boundaries and Known Gaps

Audit basis: `javascript/tests/test.js`, `python/tests/test_kron_otp.py`, three GitHub workflows and published `v1.0.0` CI evidence as of 2026-11-16. These are facts about current tests, not a security certification.

## Current tested behavior

**JavaScript** `npm test` / `node javascript/tests/test.js` checks sample-secret generation, exact six-digit string format, own-token verification, lowercase/whitespace normalization, malformed/short token format and invalid secrets. Existing JS fixture uses a canonical **80-bit** Base32 key.

**Python** `python -m unittest discover -s tests -v` runs four test methods checking 160-bit sample-secret generation/verification, normalization, invalid tokens and invalid/short secrets. PyOTP >=2.12 rejects 80-bit secrets.

**Release CI** validates both packages, npm pack contents, Python wheel+sdist, wheel smoke import. Published-package smoke CI downloads and installs registry versions into isolated contexts. The published smoke workflow completed successfully in run `43836244524`.

## Limitations and open hardening work (not fixed here)

| Item | Evidence | Scope for a future phase |
| --- | --- | --- |
| Minimum-key policy divergence | JS accepts 80-bit; PyOTP>=2.12 rejects below 112 bits | Define aligned input-strength contract and add cross-language tests |
| Error contract divergence | JS invalid secret throws TypeError; Python verify returns False | Decide and document or harmonize behavior, preserving compatibility |
| RFC/vector automation | Existing JS/Python test scripts generate at current time; no fixed-time RFC vectors in committed test suites | Add deterministic timestamp/vector coverage |
| Boundary testing | No explicit rollover, leading-zero fixed-time, +/- step and replay tests in committed suites | Add focused cases with time injection/mocking |
| CI version drift | `ci.yml` Python pip constraint is wider than `pyproject.toml`; Node job uses `npm install` vs lockfile | Align versions and use reproducible install |
| Published smoke version | `registry-smoke.yml` tests only 1.0.0 | Version-aware target for later tags |
| Stateful replay/abuse defense | APIs are stateless and tolerate one adjacent time step | Enforce single-use timecodes, rate limiting and account lockout on relying-party server |

## Security model

- Raw Base32 shared secrets are supplied by the *caller*, not collected from a website by KronOTP.
- The wrappers have no built-in network transmission or persistence. Real secrets must remain in an external secret manager or secured runtime environment; never print a secret to logs.
- A matching OTP from a generator does not prove successful authentication; the server performs authentication, replay prevention and throttling.
- Host clock synchronization is required; tolerance window expands the set of potentially accepted time steps.
- GitHub Actions secret **names**: `NPM_TOKEN`, `PYPI_API_TOKEN`. Values and external registry account permissions are not stored here.
- This documentation phase does not change, retest or claim fixes for the above gaps.

## Verification conventions

Mark each claim as observed from source, CI log, or direct test. Use PASS/FAIL/SKIPPED. Keep security-related changes narrowly scoped and require verification before releasing a patch version.
