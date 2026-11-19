# Developer FAQ

### What is the public API?
The npm and PyPI packages each publish a `KronOTP` class with two **static** methods: `generate(secret)` and `verify(secret, token)`. Both are synchronous. There are no public options, constructors with parameters, hooks, events, async clients or CLI commands. [Full reference](./API_REFERENCE.md).

### Is this a login server or 2FA account manager?
The packages are stateless TOTP libraries; they do not provision accounts or enforce server login. A separate **GitHub-source-only Tkinter Authenticator** adds local multi-account management but is not inside the PyPI wheel. [Architecture](./ARCHITECTURE.md).

### What is the exact current version?
The repository manifests and recorded npm/PyPI release identify **2.0.0** for both languages at the audited commit. Historical 1.0.0 is not overwritten. [Installation](./INSTALLATION.md).

### Can I use 8 digits, SHA256 or 60-second codes?
No. The published interface fixes **SHA1, six digits, 30 seconds**. The GUI rejects mismatched `otpauth://` settings. These algorithms/configurations exist neither as public parameters nor as supported extension points.

### What does `verify` accept?
A six-character ASCII decimal string; by default it accepts the current 30-second counter and the previous/next counter. It does **not** mark a code as used, authorize a specific user or prevent replay.

### What happens with an invalid Base32 secret?
`generate` throws `TypeError` on Node or raises `ValueError` on Python. `verify` returns false/False for ordinary invalid input. Secrets must be canonical Base32 with at least **14 decoded bytes**. Securely generated **20+ bytes** are recommended.

### Is there a way to pass a custom timestamp to `generate`?
No public timestamp parameter is defined. The deterministic source tests mock the clock internally.

### Why does the TOTP look correct but a website rejects it?
Check matching enrollment secret and account, service algorithm/step/digit settings, device clock, expiry and server-side account policies. A locally matching code does not imply successful remote authentication.

### Does `pip install kron-otp` install the GUI?
No. The single-module setuptools distribution ships `kron_otp.py`, not `python/tests/gui/`. Obtain source and run the Tkinter application separately with the installed PyPI engine.

### Does the GUI encrypt saved keys?
On **Windows**, opt-in saved account records go into a CurrentUser DPAPI encrypted vault. There is **no independent master password** or cross-profile portable backup; users must retain account recovery codes. Other operating systems get temporary session-only accounts.

### Does the library expose an environment variable?
No. `TOTP_SECRET` in documentation is a **consumer-defined** way to pass a pre-existing key to sample code. Browser automation examples also define their own environment variables.

### Are all supported systems and security cases certified?
No. Declared package runtime ranges are not a complete test matrix. CI checks Node 24 and Python 3.12 on Ubuntu; Windows Python 3.12 Tkinter/DPAPI has separate focused tests. GitHub branch/tag hardening and broader external assurance remain deferred.

### How are versions published?
A new authorized stable `vX.Y.Z` tag at current main HEAD triggers release validation then independent npm/PyPI publication. The two registry uploads are **not atomic**. No tag or publication is part of documentation maintenance.

[Quickstart](./QUICKSTART.md) · [Troubleshooting](./USAGE_AND_TROUBLESHOOTING.md) · [Compatibility](./CONFIGURATION_AND_COMPATIBILITY.md)
