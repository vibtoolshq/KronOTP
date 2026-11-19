# Forensic Documentation Coverage and QA

**Audit date:** 2026-11-19. **Input baseline:** `7aaeb9703b42d4ea1d2c3b83233eb74be35707ce`. Primary evidence: tracked source tree, package metadata and lockfile, runtime source, source and GUI tests, workflow YAML, existing docs and repository instructions. **Documentation-only scope:** `docs/` plus required `project/` technical map/log; no runtime/test/workflow/package changes.

## Audited implementation inventory

- **40 tracked blob files** found in the initial Git tree (including repository policies, docs, metadata, tests, code, workflows and licenses); **52** total Git tree items including directories. No private ignored `notes/` were included.
- **Four implementation modules of interest:** `javascript/src/kron-otp.js`, `python/src/kron_otp.py`, `python/tests/gui/app.py` and `python/tests/gui/vault.py`; **three test modules:** JS core test, Python core test and GUI/vault test.
- **Public package exports:** JavaScript `KronOTP` class exported as default CommonJS and named alias **of the same class**; Python `KronOTP` class import. **Two distinct public class surfaces**, each with `generate` and `verify`: **four callable public methods**. No supported public constants/configuration objects/interfaces/exception classes/CLI flags/events/hooks.
- **Private implementation:** JavaScript `#createTOTP`; Python `_normalize_secret`/`_totp`; Tkinter `Authenticator`, URI/label helpers, Windows `AccountVault` and `VaultError`. These are documented for maintenance but **not** advertised as supported package APIs.
- **Implemented capability groups:** (1) synchronous six-digit TOTP generation; (2) local tolerance-window verification; (3) bounded canonical Base32 validation; (4) shared deterministic RFC/synthetic test parity; (5) GitHub-only GUI account CRUD/search and ephemeral session; (6) Windows DPAPI encrypted saved accounts; (7) GUI compatible `otpauth://totp` ingestion; (8) live code refresh, copy/expiry and privacy controls; (9) selective CI with a stable Required CI producer; (10) tag-gated npm/PyPI build/publish; (11) exact-version public registry smoke. **11 groups**, of which GUI/CI are not public engine APIs.
- **No verified** network API, database, public CLI, framework plugin, custom hash/digits/step configuration, QR camera, remote account authentication, replay/rate-limit engine, async APIs or persistent engine state.

## Audit-to-documentation coverage matrix

| Source/contract | Primary reference | Result |
| --- | --- | --- |
| JS export, class and two static methods | [API](./API_REFERENCE.md), [Architecture](./ARCHITECTURE.md) | Covered |
| Python import, class and two static methods | [API](./API_REFERENCE.md), [Architecture](./ARCHITECTURE.md) | Covered |
| Base32 bounds, errors, time tolerance, v1→v2 | [API](./API_REFERENCE.md), [Compatibility](./CONFIGURATION_AND_COMPATIBILITY.md) | Covered |
| JS/Python metadata and lockfile | [Installation](./INSTALLATION.md), [Compatibility](./CONFIGURATION_AND_COMPATIBILITY.md) | Covered |
| Minimal code examples and caller secret policy | [Quickstart](./QUICKSTART.md), [Integration](./INTEGRATION_GUIDE.md) | Covered |
| GUI and DPAPI internals (not package exports) | [Architecture](./ARCHITECTURE.md), [GUI source guide](../python/tests/gui/README.md) | Covered |
| JS/Python core and GUI suites + shared fixtures | [Development](./DEVELOPMENT_AND_CONTRIBUTING.md), [Testing](./TESTING_AND_RELEASES.md) | Covered |
| Three workflows and token references | [Development](./DEVELOPMENT_AND_CONTRIBUTING.md), [Testing](./TESTING_AND_RELEASES.md) | Covered |
| Failure handling and common issues | [Debugging](./DEBUGGING.md), [FAQ](./FAQ.md) | Covered |
| Public integrations and optional browser tools | [Integration](./INTEGRATION_GUIDE.md), [Automation](./AUTOMATION_AND_PUBLISHING.md) | Covered |
| Repo policies and maintainer workflow | [Development](./DEVELOPMENT_AND_CONTRIBUTING.md), [Agent rules](../AGENTS.md) | Covered |

## Executed checks and release evidence

- **Historical verified source tests:** Node `javascript/tests/test.js`, Python `python/tests/test_kron_otp.py` (9 unittest methods), six fixed-time RFC SHA1 six-digit examples plus 80 synthetic cross-language cases. These tests do not prove third-party account acceptance.
- **Historical verified GUI test:** Windows Python 3.12 installed PyPI v2.0.0; `python/tests/gui/test_app.py` eight focused tests covering UI/vault; existing Linux GitHub CI does **not** run GUI.
- **Public package release:** npm/PyPI v2.0.0 published and install-tested in prior release workflow [43867458691](https://github.com/vibtoolshq/KronOTP/actions/runs/43867458691). This task does not republish or retag.
- **Current documentation-run example checks / link QA / Git sync:** **To be populated from actual post-edit verification before closure.** Do not infer PASS until executed.

## Corrected documentation mismatches

- Old `docs/MINIFEST.md` referenced v1.0.0 as if current and omitted newer project-specific guides.
- Historical `docs/TESTING_AND_RELEASES.md` combined an accurate v1 release history with outdated “only published 1.0.0” descriptions despite the already-published 2.0.0.
- `docs/USAGE_AND_TROUBLESHOOTING.md` denied any UI in the repository; revised boundary: **published libraries have no GUI**, but GitHub source contains optional Tkinter Authenticator.
- Historical roadmap status remains open for GitHub main/tag rulesets and broader P04 assurance; passing CI and v2 publication are not equivalent to closure of those gates.

## Unverified areas and intentional exclusions

No external penetration test, complete multi-platform/low-runtime matrix, sustained performance benchmark, secret-memory zeroization proof, QR scanner, independent live authenticator provider integration or server replay defense validation was performed. No assertion is made about real GitHub publisher secret scope or universally enforced repository protections. The source-only Windows DPAPI app's security depends on the signed-in Windows account and separately retained recovery materials.

This is **documentation verification**, not a new release or security certification. [Document index](./index.md) · [Manifest](./MINIFEST.md).
