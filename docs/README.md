# KronOTP — Public Developer Documentation

This Git-tracked directory is the documentation suite for **npm `kron-otp@2.0.0`**, **PyPI `kron-otp==2.0.0`**, and the optional source-only Python Tkinter Authenticator. It is written for developers integrating, testing, extending or maintaining the actual libraries—not for an imagined application, cloud API or CLI.

**Start with [Developer documentation index](./index.md).**

## Public capability and limitations

- The two published libraries each expose a `KronOTP` class with only **two public static methods**: `generate(secret)` and `verify(secret, token)`.
- The engine fixes SHA1 / six digits / 30 seconds, requires a canonical bounded Base32 shared secret and accepts ±one counter for local verification.
- There is no public configurable algorithm, QR scanner, HTTP server, plugin, CLI, database, replay block, rate-limit system or account-provisioning service.
- The **GitHub repository** separately contains a source-only multi-account Tkinter Authenticator; Windows opt-in saves use user-bound DPAPI. That app **does not ship with the PyPI wheel** and is not a supported engine API or complete authentication server.
- Public packages were released as version **2.0.0**; historic v1.0.0 is still available but has incompatible legacy validation behavior.

## Read in this order

[Quickstart](./QUICKSTART.md) → [Install & requirements](./INSTALLATION.md) → [Complete public API](./API_REFERENCE.md) → [Architecture](./ARCHITECTURE.md) → [Integration](./INTEGRATION_GUIDE.md) → [Testing & releases](./TESTING_AND_RELEASES.md).

For configuration/compatibility, debugging, contribution, FAQ and coverage see the [full navigation index](./index.md). [Canonical MINIFEST](./MINIFEST.md) lists **every direct docs file**, while [MANIFEST](./MANIFEST.md) is a compatibility alias.

## Maintenance and privacy policy

Before changing tracked source/docs, follow [AGENTS.md](../AGENTS.md) and [AI_INSTRUCTIONS.md](../AI_INSTRUCTIONS.md). Verify public signatures, metadata, tests and workflows against implementation, update relevant `project/` maps and docs in the same change, and record only executed QA as PASS. Never put live TOTP keys, passwords, registry tokens or private `notes/` content into public documentation. The local `notes/` directory is ignored but not encrypted.

This documentation provides **technical contracts**, not proof of universal production/security certification; actual GitHub branch/tag protection and expanded external P04 assurance remain deferred.
