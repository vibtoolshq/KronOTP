# KronOTP — Repository Agent Instructions

These are **mandatory repository-local rules** for human and AI development agents. Also read [AI_INSTRUCTIONS.md](./AI_INSTRUCTIONS.md). The new documentation rules **add to** the existing scope-lock, Git safety, security, focused verification, and STOP rules; they do not authorize unrelated changes.

## 1. Three documentation zones (strict privacy boundary)

| Location | Tracking | Audience | Content |
| --- | --- | --- | --- |
| `notes/` | **LOCAL ONLY**; ignored via root `.gitignore` | Active developer only | Working hypotheses, pre-change plans, focused audit evidence, private phase notes |
| `project/` | **Git-tracked** | Maintainers/developers | Accurate architecture, files, functions, design decisions, modules, dependencies, setup, exact implementation locations, feature and phase history |
| `docs/` | **Git-tracked** | Public package users | Accurate installation, API contracts, examples, feature explanations, usage, release and troubleshooting instructions |

**Never commit `notes/`**, copy its raw content into tracked files, or include it in release packages. Private notes are not public docs and must not contain end-user marketing/public information. Do not put credentials, tokens, private keys, actual TOTP provisioning secrets, or personal/sensitive data in **any** of these locations. Git ignore is a Git safeguard, not encryption or a general privacy guarantee.

## 2. Mandatory pre-change documentation — before every create/edit/fix/remove

1. Read the relevant source and existing documentation. Determine current Git HEAD and working-tree status.
2. **Before modifying any tracked project file**, create/update a dated note in the local private `notes/` directory with:
   - task/phase ID, purpose, date, initial baseline;
   - concrete Scope Lock (in scope / out of scope), affected paths and root cause when fixing a bug;
   - proposed step plan and focused verification/rollback or escalation strategy.
3. If a local-only notes directory is not accessible, do not secretly commit a public replacement. Report the prerequisite; preserve privacy.
4. Implement only the approved scope. Follow the repository's established GitHub-first commit → local fast-forward pull workflow where applicable; protect other local changes.
5. At implementation time **update `project/` in the same changeset**: architecture, file/function maps, module decisions, dependencies, data/control flow and a dated phase/change-log entry as relevant. Document what changed, why, where and how it was verified.
6. **Update `docs/` in the same changeset** whenever public functionality, commands, installation, parameters, errors, security notes or release behavior changes. Do not invent interfaces, pages, buttons, features, results or compatibility.
7. After the one appropriately scoped verification and Git sync, append real results to the local note and close the phase only when required checks and baseline matching succeed.

## 3. Documentation zone inventories and Vib Docs Engine compatibility

- **Private `notes/` and tracked `project/` only** retain the established `README.md` and `MINIFEST.md` inventories. Update those inventories when entries change. New subdirectories there follow the same per-folder README/MINIFEST convention.
- **Portal-synced `docs/` exception (Vib Docs Engine authoritative contract):** `docs/index.md` is the only root landing page and includes valid title/description/version/order frontmatter. `docs/MANIFEST.md` is the exact spelled source inventory and is deliberately stripped during portal synchronization. Do **not** create `docs/README.md` beside `docs/index.md` (the engine deletes the duplicate) or `docs/MINIFEST.md` (the engine does not strip the typo).
- If `docs/` later gains subfolders, use an `index.md` and valid Markdown frontmatter where appropriate. Do not impose the private `MINIFEST.md` naming convention on portal-published docs folders.
- Always keep the `docs/MANIFEST.md` source inventory exact and avoid relative public page links to stripped files or outside the configured `docsPath`.
- In `project/`, keep an authoritative technical map showing the location and purpose of each source file, public/private method, module, dependency, workflow, and relevant integration.
- In `docs/`, document real public library APIs, developer integrations, configuration and limitations. The published libraries do not bundle a UI; the repository separately contains a source-only Tkinter Authenticator example and Windows DPAPI vault, not a PyPI public API.
- Link to exact source/config paths. Treat source and verified tests as authoritative; label unverified claims as pending, not implemented.

## 4. Update-log contract

For each future feature/change/fix, record in the **private** note and in the sanitized **tracked** `project/DEVELOPMENT_LOG.md`:
- date, phase/ticket, reason, approved scope;
- changed paths, affected functions/features, important decisions;
- actual focused checks and PASS/FAIL/SKIPPED status;
- commit SHA, release/tag if applicable, unresolved risks, and phase closure status.

Update maps and manifests **in the same commit as related tracked changes**, not in a speculative future phase. If a claimed fact cannot be checked, say so.

## 5. Existing safety and release boundaries

- Existing engine contracts, release behavior and existing `AI_INSTRUCTIONS.md` remain unchanged unless explicitly requested.
- No repeated tests or expansive audits without need; one focused check per phase, broader only for shared/high-risk changes.
- No force push, hard reset, loss of uncommitted work, secret disclosure, unrequested tag creation, or release.
- A passing package smoke test is not equivalent to full RFC/security certification.
- Never write public documentation to `notes/`; never treat developer-only `project/` as product marketing or user instructions; never put private notes into `docs/`.

## 6. Close-out checklist

`notes/` plan exists before tracked edits; `project/` technical details and log are current; `docs/` public behavior matches code; private/maintainer README/MINIFEST and portal docs/index.md + docs/MANIFEST.md inventories are correct; verification results are recorded; GitHub and local heads match; working tree is clean; no private files are tracked. Only then report phase closed.
