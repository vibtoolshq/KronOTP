# KronOTP — Automation Integration & Publishing Guide

> **Scope:** Authorized testing and integration only. This document describes manual publishing; nothing in the repository currently publishes packages automatically. The current CI workflow runs tests only.
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
- For malformed secrets, JavaScript throws `TypeError`; Python `generate` throws `ValueError` and Python `verify` returns `False`. Check errors without exposing the secret.
- The repository's sample key `JBSWY3DPEHPK3PXP` is **too short** for the currently resolved PyOTP version (2.12+); use a suitable shared secret instead.
- Automation should never treat a generated code as proof of a successful login; assert the resulting authenticated state explicitly.

## 2. Publishing Guide

### 2.1 Mandatory release-readiness checks

**Publishing is not enabled yet.** These repository items must be completed and reviewed in a separate release-preparation change before either distribution is publicly released:

- Root `LICENSE` is currently empty. Select and add a real license with correct ownership information, and ensure it is included in both distributions (e.g. by adding a license file under each module or configuring inclusion).
- `javascript/README.md` and `python/README.md` are empty. Add usage, supported Node/Python versions, install guidance, security notes, and a license reference.
- `javascript/package.json` currently has `"private": true` (which blocks npm publication) and an intentionally failing placeholder `npm test` script. Update these during release preparation and verify that `npm test` executes `node tests/test.js`.
- Check npm and PyPI package-name ownership/availability for `kron-otp`. The same project name on two registries does not guarantee the same owner or availability.
- Review package metadata, cross-language behavior, TOTP interoperability, tests, and the contents of distribution archives; do not publish real shared secrets, temporary files, or test credentials.
- Existing `.github/workflows/ci.yml` **tests** changes; it does **not** publish packages. A successful CI run is not itself a release approval.

Publishing commands below are **manual instructions**, not commands that this guide or CI executes.

### 2.2 Publish `javascript/` to npm

From Windows PowerShell:

~~~powershell
cd C:\Users\Administrator\Desktop\project\KronOTP\javascript

# Inspect the package name and currently published versions.
npm view kron-otp version

# Release-preparation edits (review and commit them before publishing).
npm pkg delete private
npm pkg set "scripts.test=node tests/test.js"

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

### 2.3 Publish `python/` to PyPI using Twine

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
- For future *automated* releases, PyPI recommends OIDC **Trusted Publishing** in a dedicated, explicitly approved release workflow, rather than storing long-lived tokens in CI.

Packaging and PyPI documentation:
- https://packaging.python.org/en/latest/flow/
- https://docs.pypi.org/publishing/publishing-to-pypi/
- https://docs.pypi.org/trusted-publishers/using-a-publisher/

### 2.4 Release verification and support

After a successful manual release, install each package in a fresh environment and run a generation/verification smoke test using an authorized **nonproduction** secret. Ensure both runtimes agree on SHA-1, six digits, a 30-second period, and accepted secrets. Confirm that each package's registry page, module README, license, and version are correct. Keep the GitHub CI workflow separate from authenticated publication unless you explicitly design and review a release workflow.
