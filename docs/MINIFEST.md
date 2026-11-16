# Docs Folder MINIFEST

Inventory of **all direct files** in `docs/` following the documentation-infrastructure setup. No subfolders are created.

| File | Audience / phase | Purpose and contents |
| --- | --- | --- |
| `README.md` | Public docs home / documentation infrastructure | Purpose, navigation, supported features and maintenance rules |
| `MINIFEST.md` | Public index / documentation infrastructure | This exact list of documents |
| `INSTALLATION.md` | All users / v1.0.0 | npm/PyPI installation, environments, local checkout and setup |
| `API_REFERENCE.md` | Integrators / engines 03–04 | All real public methods, arguments, return values, constraints, differences |
| `USAGE_AND_TROUBLESHOOTING.md` | End users and integrators / v1.0.0 | Setup→generate→verify steps, errors, common issues and security |
| `AUTOMATION_AND_PUBLISHING.md` | Integrators/maintainers / phase 05 + release | Playwright, Puppeteer, Selenium and package publishing workflows |
| `TESTING_AND_RELEASES.md` | Maintainers and users / CI 4.5 + v1.0.0 | Test commands, CI jobs, registry verification, tag release procedure |

When adding/deleting/renaming a file, update this inventory and its owning README in the same commit. Never copy private `notes/` into public `docs/`.
