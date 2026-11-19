# Testing, CI, Published Artifacts and Releases

## Test organization and verified commands

| Check | Source file | Run from | Command / environment |
| --- | --- | --- | --- |
| Node core | `javascript/tests/test.js` | `javascript/` | `npm ci --ignore-scripts --no-audit --no-fund`, then `npm test` |
| Python core | `python/tests/test_kron_otp.py` | `python/` | `python -m pip install -e .`, then `python -m unittest discover -s tests -v` |
| Windows GUI/vault | `python/tests/gui/test_app.py` | repository root | `python -m unittest discover -s python/tests/gui -p test_app.py -v` with Tkinter, Windows DPAPI and installed public PyPI 2.0.0 |
| Public package smoke | `.github/workflows/registry-smoke.yml` | GitHub Actions | Manually enter published stable `version`; no registry publication |

The Node/Python core suites share `python/tests/totp_vectors.json` (six RFC6238 SHA1 six-digit fixed-time reference values + 80 synthetic cross-language keys/times/codes), and test formatting, input constraints, 30-second rollovers and adjacent-window decisions. The Python core suite has **nine** `unittest` methods. The GUI Windows suite has **eight** methods testing user-bound encryption and UI state. Count is method count, not number of individual vector cases.

The GUI test suite is **not** invoked by the existing Linux Python CI job. Node source tests depend on the full monorepo fixture; package publishing does **not** bundle that fixture as a public runtime dependency.

## GitHub Actions (exact workflows)

| Workflow | Trigger | Verified behavior |
| --- | --- | --- |
| [KronOTP CI](../.github/workflows/ci.yml) | Pull requests; main pushes affecting `javascript/**`, `python/**` or the workflows | Path-filtered Node 24 / Python 3.12 suites; unconditional stable `Required CI` check aggregating relevant jobs |
| [KronOTP Release](../.github/workflows/release.yml) | Main push affecting package/workflow release files, manual dispatch, pushed `v*` tags | `validate` tests both packages, dry-runs npm payload, builds/tests PyPI distributions; npm/PyPI **publish jobs only run on a tag push** |
| [Published Package Smoke](../.github/workflows/registry-smoke.yml) | Its workflow file push on main or manual dispatch | Strict stable numeric SemVer, exact public npm tarball/PyPI wheel download, clean consumer install and installed-version assertions |

A **docs-only push on main does not automatically trigger the CI or release workflows** under their configured `push.paths`; do not report an absent run as a failure or fake a PASS. Pull requests trigger the `Required CI` producer, but GitHub branch protection enforcement is a separate repository setting.

The release workflow validates pushed tags with stable `vX.Y.Z` pattern and requires the tagged commit to equal current `main` HEAD, plus equal npm/PyPI manifest versions. The npm job uses `NPM_TOKEN`; PyPI uses `PYPI_API_TOKEN` via Twine. Those are GitHub Actions secret **names**, not inspected values. Publishing both registries is **non-atomic**; each upload must be reviewed independently.

## Verified historical results (not tests executed in this docs update)

- **v2.0.0 tag/release:** annotated tag `v2.0.0` at commit `eefafd9934a44243879068d9b8081005e68aeade`. [Tag-push release run 43867458691](https://github.com/vibtoolshq/KronOTP/actions/runs/43867458691) had successful validation and npm/PyPI publish jobs.
- Public npm `kron-otp@2.0.0` and PyPI `kron-otp==2.0.0` were independently downloaded, clean-installed and functionally smoke-tested with public fixture input during the release work. This does not mean all supported runtimes/platforms or auth server behavior were tested.
- [GUI-02 CI 43906779325](https://github.com/vibtoolshq/KronOTP/actions/runs/43906779325) confirmed Python source test and Required CI SUCCESS; JavaScript was correctly SKIPPED on an unrelated GUI-only change. The Windows GUI suite separately passed 8/8 focused tests; it is not part of that Actions job.
- The historical `v1.0.0` tag and public registry artifacts remain untouched. Older source notes describing “only 1.0.0 published” are **historical**, not current status.
- The dedicated version-aware `registry-smoke.yml` was **not manually dispatched for v2.0.0** during the release, so do not cite a nonexistent v2 smoke workflow run; instead use the actual independently executed public-artifact checks.

## Release checklist (only when a new release is approved)

1. Authorize scope and update package metadata in **both** `javascript/package.json` and `python/pyproject.toml`; align `javascript/package-lock.json` root version and migration documentation.
2. Run focused Node/Python tests and the release validation flow, including npm payload and `python -m build`/`twine check`.
3. From verified current main, create a **new** annotated stable `vX.Y.Z` tag matching the manifests. Do not move historical release tags; no tag push without explicit release authorization.
4. Monitor the GitHub release workflow. Check npm/PyPI publish job conclusions independently and handle partial publication without republishing the same immutable version.
5. Use manual Published Package Smoke with the **new public version** to verify exact registry artifacts after publication. Record source SHA, released versions and actual evidence.

Current P03 branch/tag governance remains deferred and wider P04 support/security testing remains incomplete; a successful package smoke is not production security certification. No new tag/release is generated by documentation maintenance.

[Developer contribution process](./DEVELOPMENT_AND_CONTRIBUTING.md) · [Automated publishing](./AUTOMATION_AND_PUBLISHING.md) · [Coverage QA](./COVERAGE_AND_QA.md).
