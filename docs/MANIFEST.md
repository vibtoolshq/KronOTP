# KronOTP Developer Documentation — Source Inventory

This source-only inventory is named **MANIFEST.md** as required by Vib Docs Engine. The engine strips it from the generated portal to avoid an extra sidebar route. **Do not rename it to MINIFEST.md.** The portal's actual root page is [index.md](./index.md).

| Source file | Purpose |
| --- | --- |
| `index.md` | Root developer overview and portal metadata |
| `QUICKSTART.md` | JavaScript and Python installation and first TOTP call |
| `INSTALLATION.md` | Package and development environment installation |
| `API_REFERENCE.md` | Entire two-language public generate/verify API |
| `ARCHITECTURE.md` | Source internals, execution flow and GUI/vault boundary |
| `CONFIGURATION_AND_COMPATIBILITY.md` | Fixed TOTP options, deps and runtime compatibility |
| `INTEGRATION_GUIDE.md` | Real integration and server authentication responsibilities |
| `USAGE_AND_TROUBLESHOOTING.md` | Usage, failures and codebase-vs-package distinctions |
| `AUTOMATION_AND_PUBLISHING.md` | Optional consumer automation and package publishing |
| `DEVELOPMENT_AND_CONTRIBUTING.md` | Source setup, tests, maintenance and CI |
| `TESTING_AND_RELEASES.md` | Source tests, registry evidence and release safeguards |
| `DEBUGGING.md` | Safe debugging steps for JavaScript, Python and GUI |
| `FAQ.md` | Actual supported capabilities and limitations |
| `COVERAGE_AND_QA.md` | Source/API evidence and portal compatibility audit |
| `MANIFEST.md` | This source-only governance inventory; stripped during sync |

**Direct Markdown files: 15.** All public developer pages carry supported `title`, `description`, numeric `order` and boolean `draft: false` YAML frontmatter. The root `index.md` additionally carries version `2.0.0`. The `docs/` directory is a **single developer target**, not a dual-portal split. No user documents are inferred or added.

Do not add `docs/README.md` beside `docs/index.md`: the engine discards the README and any links to it break. Do not add `docs/MINIFEST.md`: its typo prevents automatic stripping.

Source spec: https://github.com/vibtoolshq/vib-docs-engine/blob/main/docs/vibtools-config.md
