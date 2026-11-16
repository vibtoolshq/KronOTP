# KronOTP — Public User Documentation

This is the **Git-tracked, public** user manual for the **existing** Node.js and Python TOTP packages. It is not the maintainers' development notebook or a place for unverified planning.

## What you can do with KronOTP today

- Generate a six-digit TOTP string from an **already provisioned Base32 shared secret**.
- Verify a six-digit token locally with an allowed ±one 30-second clock step.
- Use either the published `kron-otp` Node.js CommonJS package or the published Python `kron_otp` module.
- Integrate token generation in your own authorized browser automation or other applications.

**Product scope:** KronOTP is a pair of libraries with no installed GUI, web page, HTTP API server or browser automation service. The GitHub repository also contains a **source-only local Tkinter Authenticator app** at `python/tests/gui/app.py`, providing multi-account OTP generation with optional encrypted Windows DPAPI vault. The app is not in the published PyPI wheel, does not store a server account or log into remote sites, and uses only the installed PyPI engine for TOTP. See its [installation and security guide](../python/tests/gui/README.md).

## Start here (actual files)

1. [Install and set up](./INSTALLATION.md) — prerequisites, npm/PyPI versions, install/import, local development setup.
2. [API reference](./API_REFERENCE.md) — existing methods, inputs, outputs, error contracts, defaults, language differences.
3. [Usage & troubleshooting](./USAGE_AND_TROUBLESHOOTING.md) — end-to-end user workflow, samples, invalid keys, time sync and safety.
4. [Automation and publishing](./AUTOMATION_AND_PUBLISHING.md) — working-example Playwright, Puppeteer and Selenium patterns; manual and CI publishing procedures.
5. [Testing & releases](./TESTING_AND_RELEASES.md) — how to test source/published versions, run the optional Tkinter GUI and understand what CI actually verifies.
6. [MINIFEST](./MINIFEST.md) — full inventory of docs folder files.

## Keeping public guidance correct

Every user-facing change (API behavior, install commands, input validation, error handling, features, prerequisites, releases, limitations) **must update the relevant docs in the same commit**. Check actual implementation or passing tests; never guess or promise functionality not in source. Do not expose developer-only local `notes/`, credentials, private planning, or speculative defects as public feature claims. Source-of-truth maintainer reference lives in `project/` (see root `AGENTS.md`).
