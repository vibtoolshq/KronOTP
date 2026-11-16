# KronOTP — Automation Integration & Publishing Guide

> **Scope:** Authorized testing and integration only. Automated publishing is configured in `.github/workflows/release.yml`: stable `vX.Y.Z` tag pushes validate both packages and then publish to npm and PyPI. The manual commands below are alternatives for maintainers. No packages have been published by adding this workflow.
>
> **Compatibility:** Both engines use SHA-1, six digits, and a 30-second period. The Python dependency currently enforces a minimum decoded secret length of 14 bytes; prefer a securely generated 20-byte (160-bit) or longer Base32 secret. Do not use the public example test key for a real account.

## 1. Real-World Automation Integration

### 1.1 Workflow and security prerequisites

1. Configure 2FA on an account or test environment that you own or are authorized to automate. Obtain the **TOTP shared secret** at provisioning time; a password or an already generated six-digit code is not the shared secret.
2. Keep the secret in your automation platform's secret manager, and expose it to the process as the environment variable `KRONOTP_SECRET`. Never commit it, save it to screenshots, or print it in CI logs.
3. Complete the application's **first-factor sign-in** normally, then wait until its TOTP input is visible.
4. Generate a code immediately before filling the input. Submit it once, and check the site's actual authentication result.
5. Synchronize the runner's system clock. Adjust the example selectors and URLs to match **your own application**.

These samples illustrate the TOTP step; they do not defeat, remove, or bypass authentication or obtain a shared secret from a third party. The TOTP is generated locally from an already provisioned secret. Apply rate limits and replay prevention in the application's server-side verifier.

### 1.2 Node.js — Playwright

In an automation project, **after the package is published**, install:

~~~powershell
npm install kron-otp playwright
npx playwright install chromium
~~~

For **local monorepo use before publishing**, change `require('kron-otp')` to a path to `KronOTP/javascript/src/kron-otp.js` and install its `otpauth` dependency in the `javascript/` module first.

Example `playwright-2fa.js` (CommonJS):

~~~javascript
'use strict';

const { chromium } = require('playwright');
const KronOTP = require('kron-otp');

function required(name) {
  const value = process.env[name];
  if (!value) throw new Error(name + ' is required');
  return value;
}

async function main() {
  const secret = required('KRONOTP_SECRET');
  const loginUrl = required('KRONOTP_LOGIN_URL');
  const username = required('TEST_USERNAME');
  const password = required('TEST_PASSWORD');

  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage();
    await page.goto(loginUrl);

    // Example first-factor login; replace selectors for your own test app.
    await page.locator('input[name="username"]').fill(username);
    await page.locator('input[name="password"]').fill(password);
    await page.locator('button[type="submit"]').click();

    // Wait for the second-factor step before generating a short-lived OTP.
    const otpInput = page.locator('input[name="otp"]');
    await otpInput.waitFor({ state: 'visible' });
    await otpInput.fill(KronOTP.generate(secret));
    await page.locator('button[type="submit"]').click();

    // Add an application-specific success assertion after submission.
  } finally {
    await browser.close();
  }
}

main().catch(() => {
  console.error('2FA automation failed; inspect the test app and selectors.');
  process.exitCode = 1;
});
~~~

**Usage:** Supply `KRONOTP_SECRET`, `KRONOTP_LOGIN_URL`, `TEST_USERNAME`, and `TEST_PASSWORD` from a secrets manager, then execute `node playwright-2fa.js`. Avoid storing credentials in a script or a checked-in `.env` file.

### 1.3 Node.js — Puppeteer alternative

If the script already has an authenticated `page` that is waiting at the OTP challenge, reuse it:

~~~javascript
const KronOTP = require('kron-otp');

async function completeSecondFactor(page) {
  const secret = process.env.KRONOTP_SECRET;
  if (!secret) throw new Error('KRONOTP_SECRET is required');

  await page.waitForSelector('input[name="otp"]', { visible: true });
  await page.type('input[name="otp"]', KronOTP.generate(secret));
  await page.click('button[type="submit"]');
}
~~~

Install `puppeteer` in the automation project and call `completeSecondFactor(page)` after normal first-factor authentication. As with Playwright, the element selectors are illustrative.

### 1.4 Python — Selenium

In an automation project, **after the package is published**, install:

~~~powershell
python -m pip install kron-otp selenium
~~~

The `kron-otp` Python distribution exposes the importable module `kron_otp`. For local work, execute `python -m pip install -e .` inside the monorepo's `python/` folder before running the example. Alternatively, when running from that folder without installing the module, use `from src.kron_otp import KronOTP`.

Example `selenium_2fa.py`:

~~~python
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from kron_otp import KronOTP


def required(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} is required")
    return value


def main() -> None:
    secret = required("KRONOTP_SECRET")
    login_url = required("KRONOTP_LOGIN_URL")
    username = required("TEST_USERNAME")
    password = required("TEST_PASSWORD")

    driver = webdriver.Chrome()
    try:
        wait = WebDriverWait(driver, 20)
        driver.get(login_url)

        # First-factor sign-in on your own test application.
        wait.until(EC.visibility_of_element_located(
            (By.NAME, "username")
        )).send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        # Generate just in time after the TOTP field becomes available.
        otp_input = wait.until(EC.visibility_of_element_located(
            (By.NAME, "otp")
        ))
        otp_input.send_keys(KronOTP.generate(secret))
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[type="submit"]')
        )).click()

        # Add an application-specific successful-login assertion.
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
~~~

Run `python selenium_2fa.py` with the same four environment variables supplied securely. Selenium requires a supported browser and a working driver/Selenium Manager setup.

### 1.5 Engine API and known limitations

| Runtime | Import after publication | Generate | Verify |
| --- | --- | --- | --- |
| Node.js (CommonJS) | `const KronOTP = require('kron-otp');` | `KronOTP.generate(secret)` | `KronOTP.verify(secret, token)` |
| Python | `from kron_otp import KronOTP` | `KronOTP.generate(secret)` | `KronOTP.verify(secret, token)` |

- Both `generate` methods return a **string**, preserving leading zeroes.
- Verification accepts a six-character string and a one-step (±30-second) clock tolerance. Invalid tokens return `false`/`False`.
- **v2.0.0:** malformed secrets cause JavaScript `generate` to throw `TypeError` and Python `generate` to raise `ValueError`; both `verify` methods return false/False. Both require >=14 decoded bytes, allow only ASCII whitespace and cap input sizes. Historical registry `1.0.0` remains unchanged and JS verify could throw on invalid secrets. Never expose secrets in errors.
- Legacy sample key `JBSWY3DPEHPK3PXP` is 80-bit. In v2.0.0, **both** engines reject it; the historical published npm `1.0.0` may accept it. Use a securely generated >=160-bit secret for new provisioning.
- Automation should never treat a generated code as proof of a successful login; assert the resulting authenticated state explicitly.

## 2. Publishing Guide

### 2.1 Mandatory release-readiness checks

**Release workflow configuration is in place.** Before pushing the first version tag, verify the following:

- Root and module `LICENSE` files contain MIT terms. Confirm that the copyright attribution matches the owners' approved licensing choice before public release.
- Both module READMEs include usage, versions, testing and license guidance. Review content before the first public release.
- JavaScript `private: true` has been removed and `npm test` executes `node tests/test.js`; the lockfile supports reproducible `npm ci`.
- Check npm and PyPI package-name ownership/availability for `kron-otp`. The same project name on two registries does not guarantee the same owner or availability.
- Review package metadata, cross-language behavior, TOTP interoperability, tests, and the contents of distribution archives; do not publish real shared secrets, temporary files, or test credentials.
- `.github/workflows/ci.yml` runs targeted tests. `.github/workflows/release.yml` performs complete release checks on a tag and publishes only when checks succeed. A CI success alone does not authorize a release.

Publishing commands below are **manual alternatives**. The release workflow uses the organization secrets `NPM_TOKEN` and `PYPI_API_TOKEN`, and executes registry uploads only after release validation succeeds.

### 2.2 Automated tag releases

The file [`.github/workflows/release.yml`](../.github/workflows/release.yml) is triggered by `vMAJOR.MINOR.PATCH` tags. Validation checks that both package versions match the tag, the tagged commit is on `main`, tests pass, and the npm and Python distribution contents build successfully. The npm and PyPI publishing jobs run only after validation.

GitHub organization Actions secrets (available to this public repository): `NPM_TOKEN` and `PYPI_API_TOKEN`. Confirm correct access at **GitHub organization Settings → Secrets and variables → Actions**; secret values cannot be read back. The PyPI token appeared in a shared screenshot: **revoke it, create a new appropriately scoped token, and replace the GitHub secret before tagging**.

The npm bypass-2FA token is over-privileged if granted all packages and organization write access; scope it to the publishing identity and migrate to [npm Trusted Publishing (OIDC)](https://docs.npmjs.com/trusted-publishers/). npm plans to end direct publication from bypass-2FA granular tokens in January 2027. For a new PyPI project, the first API token must have permission to create the project; afterwards prefer a project-scoped token or [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/using-a-publisher/).

After checking permissions, licensing, registry names, and the validation run, manually push a release tag from an updated `main` branch:

~~~powershell
git switch main
git pull --ff-only origin main
# Replace the placeholder with a NEW, approved version after bumping both manifests.
$Version = "NEW_APPROVED_SEMVER"
git tag -a "v$Version" -m "KronOTP v$Version"
git push origin "v$Version"
~~~

**Expedited v2.0.0 exception (explicit maintainer authorization):** repository main/tag protection has been deferred for this one release, not implemented or certified. Source release validation and publication checks still apply. Protect main/tag rules before future releases where practical; never re-use v1.0.0. Both registries need publishing authority for `kron-otp`; a package name that is unavailable or owned by someone else will reject the upload. Each new release must bump **both** manifest versions and use a new matching tag (e.g. `v1.0.1`). Two separate registries are not atomic: one may publish even if the other rejects the upload. Inspect the release run before retrying; do not reuse an already published version.

### 2.3 Publish `javascript/` to npm manually

From Windows PowerShell:

~~~powershell
cd C:\Users\Administrator\Desktop\project\KronOTP\javascript

# Inspect the package name and currently published versions.
npm view kron-otp version

# Install, test, and inspect the exact package payload.
npm install
npm test
npm pack --dry-run

# Authenticate as an npm publisher, then publish manually.
npm login
npm whoami
npm publish
~~~

**Important:**

- `npm view` may return a not-found error if the name is unused; if it belongs to another publisher, choose a name you control and change `package.json`.
- Unscoped `kron-otp` packages use `npm publish`. For an organization-scoped public name such as `@your-org/kron-otp` (after updating `name` and verifying permissions), use `npm publish --access public`.
- npm publishing generally requires appropriate 2FA or trusted publishing credentials. Never add registry tokens to your repository.
- Published versions cannot simply be overwritten. Increment `version` before every subsequent release.
- From another project, after release: `npm install kron-otp`; use `require('kron-otp')`.

npm documentation: https://docs.npmjs.com/creating-and-publishing-unscoped-public-packages/

### 2.4 Publish `python/` to PyPI manually using Twine

Install Python 3.10+ on the publishing machine first. From Windows PowerShell:

~~~powershell
cd C:\Users\Administrator\Desktop\project\KronOTP\python

# Create a build and upload environment.
python -m pip install --upgrade build twine
python -m pip install -e .

# Run the existing focused Python tests.
python -m unittest discover -s tests -v

# Build source and wheel distributions from pyproject.toml.
python -m build
python -m twine check dist/*

# Authenticate with a PyPI API token when prompted and upload.
python -m twine upload dist/*
~~~

**Important:**

- Check name ownership/availability for `kron-otp` at https://pypi.org before release. PyPI normalizes hyphens/underscores in project names; installed import is still `from kron_otp import KronOTP`.
- For manual API-token upload, use username `__token__` and the full PyPI project-scoped token as the password. Never print, commit, or embed the token in a shell command.
- Optionally practice on TestPyPI using `python -m twine upload --repository testpypi dist/*`, with separately configured TestPyPI credentials.
- Only build fresh, reviewed distributions for each release; do not re-upload an already published version. Bump `[project].version` for each new release.
- GitHub Actions publishing is configured using the stored PyPI API token; for future releases, migrate to PyPI OIDC Trusted Publishing rather than a long-lived secret.

Packaging and PyPI documentation:
- https://packaging.python.org/en/latest/flow/
- https://docs.pypi.org/publishing/publishing-to-pypi/
- https://docs.pypi.org/trusted-publishers/using-a-publisher/

### 2.5 Release verification and support

After a successful automated or manual release, install each package in a fresh environment and run a generation/verification smoke test using an authorized **nonproduction** secret. Ensure both runtimes agree on SHA-1, six digits, a 30-second period, and accepted secrets. Confirm that each package's registry page, module README, license, and version are correct. The separate release workflow publishes from version tags only; regular CI never receives publishing secrets.

### P03 release-workflow hardening (development `main`)

Publishing now requires an actual **push of a valid `vX.Y.Z` tag** at the **current main HEAD**. Manually running Actions against a tag does *not* publish. Workflow third-party Actions use commit-pinned versions; npm publishing via `NPM_TOKEN` no longer requests unneeded OIDC id-token write permission.

The published-package smoke workflow accepts a **manual stable version** (such as `1.0.0`) and downloads/checks exactly that version from both registries; a workflow-file push defaults to matching manifest versions. This is verification, **not a new publication**.

**External blocker:** P03 cannot assert GitHub branch/tag protection; main is currently unprotected, rulesets empty and the connected integration lacks access to protection settings. An authorized GitHub repo administrator must enable and verify effective main and `v*` tag safeguards before the release-security phase can be called complete. No engine logic or public package version was changed.

### Expedited v2.0.0 release and compatibility

A maintainer explicitly authorized v2.0.0 before GitHub branch/tag governance controls and P04 production acceptance were completed. This is a documented security-process exception, not proof of full production hardening. JavaScript v2.0.0 verifies expected invalid secrets by returning `false` rather than throwing; both languages reject Base32 secrets <14 decoded bytes, Unicode-only whitespace and oversized input. Python v2.0.0 fixes epoch-start token verification. The release workflow publishes only on a pushed new version tag matching current main and both manifests, and upload jobs are non-atomic; independently check npm and PyPI after publication. No UI, server state, throttling or replay protection is provided by the library.
