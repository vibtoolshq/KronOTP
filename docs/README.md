# KronOTP — Public User Documentation

This is the **Git-tracked, public** user manual for the **existing** Node.js and Python TOTP packages. It is not the maintainers' development notebook or a place for unverified planning.

## What you can do with KronOTP today

- Generate a six-digit TOTP string from an **already provisioned Base32 shared secret**.
- Verify a six-digit token locally with an allowed ±one 30-second clock step.
- Use either the published `kron-otp` Node.js CommonJS package or the published Python `kron_otp` module.
- Integrate token generation in your own authorized browser automation or other applications.

**What does not exist:** KronOTP is a pair of libraries. It has **no app window, web page, settings panel, buttons, QR-code UI, API server, database, built-in account storage or browser automation service**. Consequently, there are no product screens or buttons to operate. The Playwright/Puppeteer/Selenium guides are examples of how *your* own application's elements may be handled.

## Start here (actual files)

1. [Install and set up](./INSTALLATION.md) — prerequisites, npm/PyPI versions, install/import, local development setup.
2. [API reference](./API_REFERENCE.md) — existing methods, inputs, outputs, error contracts, defaults, language differences.
3. [Usage & troubleshooting](./USAGE_AND_TROUBLESHOOTING.md) — end-to-end user workflow, samples, invalid keys, time sync and safety.
4. [Automation and publishing](./AUTOMATION_AND_PUBLISHING.md) — working-example Playwright, Puppeteer and Selenium patterns; manual and CI publishing procedures.
5. [Testing & releases](./TESTING_AND_RELEASES.md) — how to test source/published versions and what CI actually verifies.
6. [MINIFEST](./MINIFEST.md) — full inventory of docs folder files.

## Keeping public guidance correct

Every user-facing change (API behavior, install commands, input validation, error handling, features, prerequisites, releases, limitations) **must update the relevant docs in the same commit**. Check actual implementation or passing tests; never guess or promise functionality not in source. Do not expose developer-only local `notes/`, credentials, private planning, or speculative defects as public feature claims. Source-of-truth maintainer reference lives in `project/` (see root `AGENTS.md`).
