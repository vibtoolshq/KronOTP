# KronOTP

**KronOTP** is a multi-language toolkit for time-based one-time passwords (TOTP), designed for authorized two-factor authentication (2FA) integrations and automated testing.

> **Project status: Foundation / in development.** The JavaScript and Python package layouts and dependency configuration are in place, but code generation, verification, and tests have **not** been implemented yet. Do not use this repository as a working authenticator until those phases are completed and verified.

## Language modules

| Language | Directory | Package name | Planned engine dependency | Status |
| --- | --- | --- | --- | --- |
| Node.js / JavaScript | [`javascript/`](./javascript/) | `kron-otp` (npm) | [`otpauth`](https://www.npmjs.com/package/otpauth) | Scaffolded; implementation pending |
| Python | [`python/`](./python/) | `kron-otp` (PyPI) | [`pyotp`](https://pypi.org/project/PyOTP/) | Scaffolded; implementation pending |

Each module has its own package metadata, source directory, and test directory. Implementations will be developed and tested independently while targeting consistent TOTP behavior.

## Repository structure

```text
KronOTP/
├── .gitignore
├── LICENSE                 # Placeholder; license text pending
├── README.md               # Monorepo overview
├── AI_INSTRUCTIONS.md      # Development scope and safety rules
├── javascript/
│   ├── package.json
│   ├── README.md
│   ├── src/
│   │   └── kron-otp.js
│   └── tests/
│       └── test.js
└── python/
    ├── pyproject.toml
    ├── README.md
    ├── src/
    │   ├── __init__.py
    │   └── kron_otp.py
    └── tests/
        ├── __init__.py
        └── test_kron_otp.py
```

## Development roadmap

1. **Foundation:** Create the monorepo structure and package configuration.
2. **Core implementation:** Implement TOTP generation and verification in each language using the configured dependency.
3. **Validation:** Add RFC 6238 test vectors, boundary and invalid-input tests, and cross-language consistency checks.
4. **Release readiness:** Finish module documentation, licensing, CI checks, and package publishing requirements.

These are planned milestones, **not** claims of completed features or standards compliance.

## Local setup

Use a separate package manager in each module:

**Node.js**

```powershell
cd javascript
npm install
```

**Python (3.10+)**

```powershell
cd python
python -m pip install -e .
```

These commands configure dependencies only. The source modules and tests remain placeholders in this phase. The JavaScript test command intentionally reports that tests are not implemented, rather than incorrectly reporting a passing suite.

## Security

TOTP relies on a shared secret and synchronized time. Only generate codes for accounts and test environments you own or are authorized to access. Never commit, log, or expose real TOTP secrets.

## Contributing

Review [`AI_INSTRUCTIONS.md`](./AI_INSTRUCTIONS.md) before making changes. Keep work scoped to the requested phase, preserve module boundaries, and add focused verification when implementing behavior.

## License

The root [`LICENSE`](./LICENSE) file is currently empty. Licensing terms must be added before distributing or publishing KronOTP.
