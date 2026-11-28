# Project — Maintainer Technical Reference

This directory is the **Git-tracked development knowledge base** for KronOTP, not a private scratchpad and not the end-user manual. It records the implementation as it really exists, enabling developers to understand and maintain every feature, function, module and release workflow without guessing.

## Current frozen baseline — read first

**[Current post-v2.0.1 baseline](./BASELINE_POST_V2_0_1.md)** and **[68-file exact pre-freeze inventory](./BASELINE_FILE_INVENTORY_POST_V2_0_1.md)** are the continuation references. The historical v2.0.0 baseline and inventory remain immutable evidence, not current status. Incoming GitHub/local/origin parity verified clean; published v2.0.1 npm/PyPI exact bytes verified; G12 accepted via recovery. Resolve the final protected documentation-freeze merge before beginning the next phase.

## What belongs here
- Architecture, module boundaries, configuration and data/control flow.
- Exact source file/function locations and API behavior, including differences between languages.
- Reasons for choosing each dependency, its actual use and where it is configured.
- The *verified* history of feature work, bug fixes, phase scope and commit references.
- Known limitations and test coverage with evidence from code/CI.

## How to maintain
1. Before a change, record an **untracked private scope/plan** in local `notes/` (see root `AGENTS.md`).
2. Make the scoped code/config change and update affected technical references **in the same tracked commit**.
3. Append date, phase, changed paths, reason, verified result and commit to `DEVELOPMENT_LOG.md`.
4. Update `MINIFEST.md` if any entry under `project/` changes.
5. Do not insert private plans, credentials or raw local notes. Reference source paths instead of making unsupported claims.

## Reading order
[Current frozen baseline](./BASELINE_POST_V2_0_1.md) → [Source file inventory](./BASELINE_FILE_INVENTORY_POST_V2_0_1.md) → [Architecture](./ARCHITECTURE.md) → [File map](./FILE_MAP.md) → [Function reference](./FUNCTION_REFERENCE.md) → [CI/release](./CI_AND_RELEASE.md) → [Quality & gaps](./QUALITY_AND_SECURITY.md) → [Development history](./DEVELOPMENT_LOG.md).

User instructions live in [`docs/`](../docs/index.md). Project-wide rules live in [`AGENTS.md`](../AGENTS.md) and [`AI_INSTRUCTIONS.md`](../AI_INSTRUCTIONS.md).
