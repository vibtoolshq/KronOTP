---
title: "Development, Contribution and Release Process"
description: "Repository structure, local source tests, contribution discipline, GitHub CI and release preparation."
order: 90
draft: false
---

## Checkout and directory map

```sh
git clone https://github.com/vibtoolshq/KronOTP.git
cd KronOTP
```

| Path | What to edit, when explicitly authorized |
| --- | --- |
| `javascript/src/kron-otp.js` | Complete public Node class and private OTPAuth adapter |
| `javascript/tests/test.js` | Node core tests and shared fixed-time cases |
| `javascript/package.json` / `package-lock.json` | npm metadata, runtime constraints and locked install graph |
| `python/src/kron_otp.py` | Complete public Python class and private PyOTP adapter |
| `python/tests/test_kron_otp.py` | Python core tests and epoch-boundary cases |
| `python/tests/totp_vectors.json` | Public RFC / independent synthetic parity fixtures |
| `python/tests/gui/app.py` | GitHub-only Tkinter Authenticator application |
| `python/tests/gui/vault.py` | Windows-only CurrentUser DPAPI encrypted account store |
| `python/tests/gui/test_app.py` | Focused Windows GUI/vault regression tests |
| `.github/workflows/` | CI, validated tag publishing, exact-version public registry smoke |
| `project/` | Git-tracked authoritative maintainer implementation map |
| `docs/` | Git-tracked public developer docs |
| `notes/` | Locally ignored, private pre-change plans; never commit |

## Source development

**Node:** requires Node `>=20.19.0`; the repository's CI uses Node 24.

```sh
cd javascript
npm ci --ignore-scripts --no-audit --no-fund
npm test
```

**Python:** requires Python `>=3.10`; CI runs Python 3.12 on Ubuntu. From `python/` inside an isolated environment:

```sh
python -m pip install -e .
python -m unittest discover -s tests -v
```

`python/tests/test_kron_otp.py` imports `from src.kron_otp import KronOTP` when run in the checked-out tree. A **consumer** instead imports `from kron_otp import KronOTP` after installing PyPI. The shared JSON test fixture is in the monorepo; source tests do not operate from an isolated npm tarball.

**Windows Tkinter/DPAPI focused check:** with installed public `kron-otp==2.0.0` in the same Python interpreter:

```powershell
python -m unittest discover -s python/tests/gui -p test_app.py -v
```

The Windows tests require a GUI-capable desktop and DPAPI. They are **not included in the Linux GitHub CI workflow**. Do not infer Windows GUI success merely from green Ubuntu source tests.

## Maintainer change control (verified repository rules)

The source repository has `AGENTS.md` and `AI_INSTRUCTIONS.md` rather than a separate `CONTRIBUTING.md`. Their documented process requires:

1. Read affected implementation and check clean Git baseline.
2. Create a private dated Scope Lock / test plan in ignored `notes/` **before** tracked edits. Do not commit notes, actual secrets or local env files.
3. Change only the authorized source/config/docs and update relevant `project/` technical references and `docs/` usage in the same commit.
4. Run focused tests and patch whitespace/file-scope audit; record real results in `project/DEVELOPMENT_LOG.md`.
5. Commit and synchronize safely; no force push/reset or unsolicited tag/release.
6. Keep `docs/MINIFEST.md` and the `project/MINIFEST.md` inventories current. The repository's actual mandatory manifest file is spelled **MINIFEST**, not the usual “manifest”.

No verified separate code-style formatter, linter, coverage threshold, contribution sign-off policy or mandatory review count is declared in the package/workflow metadata. Do not invent such requirements.

## CI workflows

- [KronOTP CI](https://github.com/vibtoolshq/KronOTP/blob/main/.github/workflows/ci.yml) runs on all pull requests (with selective JS/Python tests) and on main pushes changing language directories/workflows; stable `Required CI` aggregates relevant jobs. A docs-only main push **does not trigger this CI workflow**.
- [Release workflow](https://github.com/vibtoolshq/KronOTP/blob/main/.github/workflows/release.yml) validates both packages on the configured push paths and manual dispatch. **Publishing** requires an actual pushed stable `vMAJOR.MINOR.PATCH` tag whose commit is the current main HEAD and matches both package versions.
- [Published package smoke](https://github.com/vibtoolshq/KronOTP/blob/main/.github/workflows/registry-smoke.yml) accepts a stable numeric version on manual dispatch or resolves equal package manifest versions on a workflow-file push. It downloads/install-checks exact npm and PyPI artifacts without publishing.

GitHub `Required CI` is a produced check, **not proof that branch protection is active**. At the audited baseline, main/tag ruleset enforcement remains an outstanding governance item.

## Packaging and intentional releases

1. Version both `javascript/package.json` and `python/pyproject.toml` consistently; update `javascript/package-lock.json` root/package version and migration documentation.
2. Verify both source suites and the release validation steps, including `npm pack --dry-run` and `python -m build` / `twine check`.
3. Publish **only when explicitly authorized**: a new annotated `vX.Y.Z` tag at the current main HEAD triggers token-based npm and Twine PyPI jobs. An old tag must never be moved or reused.
4. Inspect each publisher's conclusion independently; npm and PyPI publishing is **non-atomic**. Verify the exact public version using registry smoke after artifacts appear.
5. Update release evidence and remaining assurance gaps. This documentation-only task creates **no tag, registry upload or release**.

Publishing secrets are referenced by name (`NPM_TOKEN` and `PYPI_API_TOKEN`), not inspected here. No assertion is made about their active value, expiration or scope.

[Testing evidence](./TESTING_AND_RELEASES.md) · [Debugging](./DEBUGGING.md) · [Release detail](./AUTOMATION_AND_PUBLISHING.md)
