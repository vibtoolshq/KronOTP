# Quality, Test Coverage, Security Boundaries and Known Gaps

Audit basis: `javascript/tests/test.js`, `python/tests/test_kron_otp.py`, three GitHub workflows and published `v1.0.0` CI evidence as of 2026-11-16. These are facts about current tests, not a security certification.

## Current tested behavior

**JavaScript** `npm test` / `node javascript/tests/test.js` checks sample-secret generation, exact six-digit string format, own-token verification, lowercase/whitespace normalization, malformed/short token format and invalid secrets. P01 tests use a **160-bit** public fixture and 1/10/13/14/20-byte boundaries, ASCII/Unicode input and bounded-size cases.

**Python** `python -m unittest discover -s tests -v` runs six test methods checking 160-bit generation/verification, normalization, invalid tokens/secrets, 14-byte acceptance and input-size boundaries. PyOTP >=2.12 rejects under-14-byte secrets. (P01 scope; final CI outcomes recorded in the phase log.)

**Release CI** validates both packages, npm pack contents, Python wheel+sdist, wheel smoke import. Published-package smoke CI downloads and installs registry versions into isolated contexts. The published smoke workflow completed successfully in run `43836244524`.

## Limitations and open hardening work (not fixed here)

| Item | Evidence | Scope for a future phase |
| --- | --- | --- |
| Minimum-key policy divergence | P01 enforces >=14 decoded bytes in both engines (112-bit minimum) | Use cryptographically random >=20-byte secrets for new provisioning; do not treat length as proof of entropy |
| Error contract divergence | P01 makes `verify` return false/False for known malformed input in both; `generate` preserves native exceptions | Breaking JS v1.0.0 verify behavior; migration/release review required |
| RFC/vector automation | Existing JS/Python test scripts generate at current time; no fixed-time RFC vectors in committed test suites | Add deterministic timestamp/vector coverage |
| Boundary testing | No explicit rollover, leading-zero fixed-time, +/- step and replay tests in committed suites | Add focused cases with time injection/mocking |
| CI version drift | `ci.yml` Python pip constraint is wider than `pyproject.toml`; Node job uses `npm install` vs lockfile | Align versions and use reproducible install |
| Published smoke version | `registry-smoke.yml` tests only 1.0.0 | Version-aware target for later tags |
| Stateful replay/abuse defense | APIs are stateless and tolerate one adjacent time step | Enforce single-use timecodes, rate limiting and account lockout on relying-party server |

## P01 additional guardrails

- Both wrappers reject Base32 secrets shorter than 14 decoded bytes, raw input longer than 4096 chars and cleaned Base32 longer than 1024 chars.
- Normalize only ASCII whitespace (space, tab, CR, LF, FF, VT). Reject Unicode BOM/NBSP and non-ASCII case mapping. Reject noncanonical padding bits.
- A 112-bit length threshold only prevents trivially short encoded keys: it does **not** guarantee unpredictability. Provision random 160-bit or longer secrets for new accounts.
- Historical public registry `v1.0.0` binaries are not updated by development `main` changes.

## Security model

- Raw Base32 shared secrets are supplied by the *caller*, not collected from a website by KronOTP.
- The wrappers have no built-in network transmission or persistence. Real secrets must remain in an external secret manager or secured runtime environment; never print a secret to logs.
- A matching OTP from a generator does not prove successful authentication; the server performs authentication, replay prevention and throttling.
- Host clock synchronization is required; tolerance window expands the set of potentially accepted time steps.
- GitHub Actions secret **names**: `NPM_TOKEN`, `PYPI_API_TOKEN`. Values and external registry account permissions are not stored here.
- P01 changes only secret input validation and expected-error handling; SHA-1/6/30 ±1 window and stateless design remain unchanged. Python epoch-boundary bug, CI dependency drift, version-aware registry smoke and release governance remain open.

## Verification conventions

Mark each claim as observed from source, CI log, or direct test. Use PASS/FAIL/SKIPPED. Keep security-related changes narrowly scoped and require verification before releasing a patch version.
