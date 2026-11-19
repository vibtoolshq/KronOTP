# Docs MINIFEST — Direct-File Inventory

**Canonical filename:** `MINIFEST.md` as required by the repository's `AGENTS.md`. The [MANIFEST.md](./MANIFEST.md) alias exists because the requested documentation convention uses that spelling. All entries below are direct files; the project uses a deliberately **flat, compact** docs layout with no nested subdirectories.

| Direct file | Audience / purpose |
| --- | --- |
| `README.md` | Public documentation boundary, maintenance rules and navigation |
| `index.md` | Developer homepage, source-informed capability map and developer reading order |
| `MINIFEST.md` | Canonical direct-file inventory (repository-required spelling) |
| `MANIFEST.md` | Compatibility manifest alias that links to canonical MINIFEST |
| `QUICKSTART.md` | Minimal verified Node.js and Python examples |
| `INSTALLATION.md` | Published installation, editable source setup, runtime requirements and uninstallation |
| `API_REFERENCE.md` | Complete public Node/Python KronOTP class/method/error reference |
| `ARCHITECTURE.md` | Engine internals, local TOTP flow, source-only GUI/vault and CI diagrams |
| `CONFIGURATION_AND_COMPATIBILITY.md` | Actual fixed settings, dependencies, runtime compatibility and migration |
| `INTEGRATION_GUIDE.md` | Application integration, secure server obligations, optional GUI/automation links |
| `USAGE_AND_TROUBLESHOOTING.md` | Supported runtime usage, errors, real GUI distinction and recovery |
| `AUTOMATION_AND_PUBLISHING.md` | Optional Playwright/Puppeteer/Selenium integration and manual/pipeline publishing |
| `TESTING_AND_RELEASES.md` | Actual source/GUI tests, workflow triggers, published v2.0.0 evidence and release gates |
| `DEVELOPMENT_AND_CONTRIBUTING.md` | Repo structure, contribution discipline, source tests and release procedure |
| `DEBUGGING.md` | Safe diagnosis, input/clock/import failures, Windows vault troubleshooting |
| `FAQ.md` | Concise developer questions and capability boundaries |
| `COVERAGE_AND_QA.md` | Forensic public-interface coverage, documented modules and actual QA limits |

**Total:** 17 direct Markdown files. Update this inventory and [documentation homepage](./index.md) in the same documentation change when adding/removing/renaming any docs file. Source implementation lives outside `docs/`; private ignored `notes/` must never be committed or linked as public evidence.
