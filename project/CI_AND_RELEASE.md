# CI, Packages and Release Pipeline — Technical Map

## Dependency and distribution setup
- Node package `kron-otp@1.0.0`: CommonJS, `javascript/package.json`, `otpauth ^9.6.0`, locked `javascript/package-lock.json`, publishes `src/kron-otp.js`, README, LICENSE, manifest.
- Python distribution `kron-otp==1.0.0`: `python/pyproject.toml`, setuptools, `py-modules=["kron_otp"]` under `python/src`, `pyotp>=2.12,<3`; generated wheel and sdist.
- GitHub: `vibtoolshq/KronOTP`. Initial release tag `v1.0.0` points to commit `e77155eefd7d18d49fcde489b510f4fd8df5d797`.
- Current docs-phase baseline is later; **do not move/reuse historical tags**.

## `.github/workflows/ci.yml`
- Events: pushes and PRs changing `javascript/**`, `python/**`, or the workflow itself.
- `changes` job: checkout and `dorny/paths-filter@v4`, outputs which language directory changed.
- `javascript`: only when relevant, `actions/setup-node@v7`, Node 24, `npm install --no-audit --no-fund --ignore-scripts`, `node tests/test.js`.
- `python`: only when relevant, Python 3.12, `pip install 'pyotp>=2.10,<3'`, `PYTHONPATH=.` and `python tests/test_kron_otp.py`.
- Existing CI version range differs from `pyproject.toml`'s `pyotp>=2.12,<3`; fix only in a dedicated CI hardening phase.

## `.github/workflows/release.yml`
- Main branch pushes touching listed release configuration/doc/license paths or workflow file, plus manual dispatch, run the validation job; **publishing jobs skip without a tag**.
- Tag push named `v*`: `validate` requires regex `^v[0-9]+\.[0-9]+\.[0-9]+$`, commit ancestry on `main`, both package versions match tag, essential metadata and nonempty licenses/READMEs.
- Validation then `npm ci`, `npm test`, `npm pack --dry-run` inspection, Python editable install, Python unit tests, `python -m build`, Twine distribution check, installed-wheel smoke test, and uploads short-lived Python dist artifact.
- `npm` publishes via `npm publish --ignore-scripts --access public` on tag using `NODE_AUTH_TOKEN: secrets.NPM_TOKEN`.
- `pypi` consumes the artifact and uses Twine with `TWINE_USERNAME=__token__` / `TWINE_PASSWORD: secrets.PYPI_API_TOKEN`.
- The workflows do **not** manage or expose secret values. Uploads are separate jobs, **not atomic**: one registry may succeed when another fails.
- Do not push a release tag without new matching package versions, verified access/secret scope and release authorization.

## `.github/workflows/registry-smoke.yml`
- Events: `main` push when workflow file changes, plus manual dispatch.
- npm job downloads `kron-otp@1.0.0` from public npm, installs from downloaded tarball into temporary clean consumer prefix and checks generation, verification, token validation and original JS suite.
- PyPI job downloads wheel `kron-otp==1.0.0`, creates isolated venv, installs release/dependency, checks API, then runs original Python tests.
- This workflow is **hard-coded to v1.0.0**. Future releases require updating it or making it version-aware as a separate task.

## Verified history (2026-11-16)
- Tag `v1.0.0` published to npm and PyPI: release workflow run `43835128215`, jobs successful.
- Published-package install smoke workflow run `43836244524`, both npm and PyPI jobs successful after temporary npm registry propagation delay.
- These are test outcomes for configured cases; not complete security certification.

## Maintenance
Log any workflow/package change in `project/DEVELOPMENT_LOG.md`, keep `project/FILE_MAP.md` and `docs/TESTING_AND_RELEASES.md` current, and use `notes/` for the initial private plan. Never record actual token values.
