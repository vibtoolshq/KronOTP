# Testing, Published Packages & Releases

This guide documents **verified existing** test and release workflows, not a promise of new functionality.

## Run tests locally

Node.js (from repo root):

```sh
cd javascript
npm ci
npm test
```

Python (from repo root, in an environment with Python >=3.10):

```sh
cd python
python -m pip install -e .
python -m unittest discover -s tests -v
```

**Development `main` after P02:** Existing input/generation tests remain and both source suites also consume `python/tests/totp_vectors.json`: 6 fixed-time RFC 6238 SHA-1 six-digit reference values (including leading zeros) plus 80 deterministic, public synthetic 160-bit secret/time/OTP cases. JS uses `node:assert/strict` with a temporary `Date.now` mock; Python runs 9 `unittest` methods with a temporary PyOTP clock mock. Both cover Unix times 0,1,29,30,59,60,61, adjacent windows and two-step rejections. This is a **source test**, not a new published version or end-to-end authentication certification.

## GitHub Actions workflows

| Workflow | Trigger | Purpose |
| --- | --- | --- |
| `.github/workflows/ci.yml` | JS/Python or workflow source changes in push/PR | Conditional Node/Python tests; no package publication |
| `.github/workflows/release.yml` | Relevant `main` pushes, matching `v*` tag pushes, or manual dispatch | Full validation; npm and PyPI publishing jobs are **tag-only** |
| `.github/workflows/registry-smoke.yml` | Push changing this workflow on `main` or manual dispatch | Download **v1.0.0** npm/PyPI public artifacts, clean install and smoke verification |

A regular documentation-only change does **not** automatically rerun full package tests when outside configured path filters. Do not claim tests ran if no workflow was triggered.

Verified v1.0.0 test history:
- Release tag `v1.0.0`, based on commit `e77155eefd7d18d49fcde489b510f4fd8df5d797`.
- [Release workflow run 43835128215](https://github.com/vibtoolshq/KronOTP/actions/runs/43835128215): both publish jobs successful.
- [Public artifact smoke run 43836244524](https://github.com/vibtoolshq/KronOTP/actions/runs/43836244524): npm and PyPI download, fresh install and configured functional checks successful.

## Installing a known published version

```sh
npm install kron-otp@1.0.0
```

```sh
python -m pip install kron-otp==1.0.0
```

Registries:
- npm: https://www.npmjs.com/package/kron-otp/v/1.0.0
- PyPI: https://pypi.org/project/kron-otp/1.0.0/

## How maintainers release a future version

The GitHub workflow only publishes when a **new version tag** passes package and metadata validation.

1. Implement a scoped change, write the private pre-change note, and update tracked `project/` and public `docs/` as appropriate in the same commit.
2. Increment version in **both** `javascript/package.json` and `python/pyproject.toml`; keep `javascript/package-lock.json` root version aligned and document tested dependencies. Registry versions cannot be overwritten.
3. Confirm tests/metadata, module license and README, tag ownership, npm and PyPI package publishing authorization.
4. Ensure GitHub organization Actions secrets `NPM_TOKEN` and `PYPI_API_TOKEN` are valid and correctly scoped (never print their contents). Prefer trusted OIDC publishing where configured; the current workflow uses tokens.
5. From synchronized `main`, create a fresh annotated tag matching the manifests (for example `v1.0.1`) and push **only when intentionally authorizing publication**.
6. Monitor the `KronOTP Release` Actions run. Validate npm and PyPI results independently; publishing is **not atomic** across registries.
7. Verify installation/download from both public registries after propagation; update the pinned version in published smoke tests for the next release.

Do **not** reuse `v1.0.0` or republish `1.0.0`; it is already released. After P03, `registry-smoke.yml` supports an explicitly selected stable published version and checks downloaded/installed npm/PyPI metadata. The current public 1.0.0 is still the only version previously released; smoke success for 1.0.0 is not proof of any unpublished P01/P02 fixes.

## Real security requirements

Do not copy actual shared TOTP secrets, registry tokens or private notes into scripts or documentation. These tests cannot certify server-side OTP replay prevention, account authentication, login UI or unimplemented features.

More integration and manual publishing detail: [Automation and Publishing](./AUTOMATION_AND_PUBLISHING.md).

## P02 shared vectors and source test prerequisites

The Node source-test file reads the shared fixture at `../python/tests/totp_vectors.json` relative to the `javascript/` directory (resolved from `javascript/tests/test.js`); it requires the **full KronOTP monorepo checkout**, not an isolated npm tarball. Python source tests read that same JSON next to `python/tests/test_kron_otp.py`. Runtime imports and published package contents do not depend on the test fixture. The P02 fix and regression tests reside on `main`; npm/PyPI published `1.0.0` remains unchanged until an authorized future tag release.

## Source-only P02 verification status (2026-11-16)

- [GitHub Actions CI run 43851819951](https://github.com/vibtoolshq/KronOTP/actions/runs/43851819951) completed successfully for both JavaScript and Python tests (plus change detection).
- Python source suite: **9/9 test methods PASS**, including Unix epoch counter 0 and current/next drift validation. Node source suite PASS. Both assert six fixed RFC and 80 independently generated synthetic reference cases.
- This is **development source on `main`**. Published npm and PyPI version `1.0.0` is unchanged; no new tag, registry upload or public artifact-install verification was performed in P02.

## P03: version-aware published artifact smoke (source on main)

The `KronOTP Published Package Smoke Tests` workflow now accepts a required manual `version` value (example: `1.0.0`) via **Actions → KronOTP Published Package Smoke Tests → Run workflow**. It accepts only stable numeric `MAJOR.MINOR.PATCH`, such as `1.0.0`. A malformed version (or a version not yet on both registries) fails; no download is treated as a successful check without exact installed version matching.

On a push that changes only this workflow on `main`, the smoke target is derived from the matching versions in `javascript/package.json` and `python/pyproject.toml`. This allows an ordinary non-tag test of the already published 1.0.0. To validate a **future** published version, manually run the workflow and enter its exact new published version; the workflow does **not** publish anything.

### Repository administration required — P03 governance BLOCKED

Current GitHub evidence: `main` reports **protected:false**; repository rulesets `[]`; GitHub integration cannot read branch protection (403) or modify rulesets. An authorized repo admin must configure and verify: enforced main branch PR review and appropriate required checks, disallow force pushes and deletion, restricted bypass, and protected `v*` tag creation/update/deletion. Configure environment approval where desired and verify it actually restricts publishing. **A workflow YAML change alone cannot accomplish this.** Do not claim P03 fully CLOSED, or approve P04/P05 release gates, until an authorized owner verifies these controls or explicitly accepts the documented risk.

No new tag, package version, registry upload, credential rotation or production engine change is part of P03.

## Verified P03 workflow results and administrative blocker

- [CI 43855173877](https://github.com/vibtoolshq/KronOTP/actions/runs/43855173877): JavaScript and Python job SUCCESS.
- [Public registry smoke 43855173893](https://github.com/vibtoolshq/KronOTP/actions/runs/43855173893): select version 1.0.0, download/install/test npm & PyPI; all 3 jobs SUCCESS. Invalid manual version strings were rejected in 7 focused offline resolver checks; future versions must still be tested after their publication.
- [Release validation 43855173879](https://github.com/vibtoolshq/KronOTP/actions/runs/43855173879): full validation PASS, **npm/PyPI publication SKIPPED** because no version tag was pushed.

**Not a closed release-security phase:** Current GitHub repo has no effective main/tag protection verified (`main protected:false`, rulesets `[]`, protection endpoint 403). An authorized admin must enable and verify those controls (or explicitly accept the risk) before declaring P03 CLOSED; no change was made to engine source, published packages or tags.
