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

Actual tests check generation, six-digit formatting, verification, secret normalization, and malformed tokens/secrets. They do **not** contain a complete cross-language fixed-time RFC vector suite. Python's current suite has 4 test methods; JS uses `node:assert/strict`.

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

Do **not** reuse `v1.0.0` or republish `1.0.0`; it is already released. Existing `registry-smoke.yml` is **hardcoded to 1.0.0**, so passing it does not validate a later version without a version update.

## Real security requirements

Do not copy actual shared TOTP secrets, registry tokens or private notes into scripts or documentation. These tests cannot certify server-side OTP replay prevention, account authentication, login UI or unimplemented features.

More integration and manual publishing detail: [Automation and Publishing](./AUTOMATION_AND_PUBLISHING.md).
