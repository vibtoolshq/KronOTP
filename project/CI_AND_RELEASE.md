# CI, Packages and Release Pipeline — Technical Map

## Dependency and distribution setup
- Node package `kron-otp@1.0.0`: CommonJS, `javascript/package.json`, `otpauth ^9.6.0`, locked `javascript/package-lock.json`, publishes `src/kron-otp.js`, README, LICENSE, manifest.
- Python distribution `kron-otp==1.0.0`: `python/pyproject.toml`, setuptools, `py-modules=["kron_otp"]` under `python/src`, `pyotp>=2.12,<3`; generated wheel and sdist.
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
