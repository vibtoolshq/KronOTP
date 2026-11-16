# KronOTP Authenticator — Tkinter desktop application

**A compact, full-featured local TOTP generator** using the *actual published* PyPI engine `kron-otp==2.0.0`. The app code lives in this GitHub folder, **not** inside the PyPI wheel. Python's standard-library Tkinter powers the UI; the KronOTP engine exclusively calculates and verifies OTPs.

## What it does

- Create and switch between **up to 100 named accounts**, search by account/issuer, edit and delete entries.
- Paste a Base32 secret or a standard `otpauth://totp/...` URI. URI issuer/account can fill labels automatically. **Only SHA1, 6 digits, 30 seconds** work (exactly the engine's fixed options); mismatched algorithm/digits/period are rejected.
- **Use once** loads a temporary secret only in memory, without saving it to the vault.
- Selecting an account instantly displays its six-digit TOTP, updated at each 30-second boundary. Remaining time and progress bar stay live.
- **Copy OTP** copies only the code; app tries to clear it after **15 seconds** if the clipboard still contains that same code. It cannot stop other software from reading clipboard contents meanwhile.
- **Local check** calls `KronOTP.verify` against the selected secret; it does *not* establish that a remote site accepted the code.
- Privacy **Lock** hides accounts and forgets in-memory secrets; auto-lock after five minutes without UI activity. Unlock on Windows decrypts saved records using the current Windows user profile. **This is not a separate password/PIN barrier.**
- Optional **Always on top**, keyboard shortcuts (`Ctrl+N` add, `Ctrl+F` search, `Ctrl+L` lock/unlock, `Ctrl+Shift+C` copy), masked secret entry with Show toggle, bounded input/error messages.

## Installation on Windows

Use Python 3.10+ with Tkinter, and the **same interpreter** for installing and running:

```powershell
python -m pip install kron-otp==2.0.0
python python/tests/gui/app.py
```

The second command runs from the repository root, or open this `gui` directory and run `python app.py`. `pip install kron-otp==2.0.0` alone will **not** install `app.py` or the desktop UI.

An isolated environment is recommended:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install kron-otp==2.0.0
.venv\Scripts\python.exe python/tests/gui/app.py
```

The app checks the installed **exact** package version and its module filesystem origin at startup. This prevents accidentally testing the repository's `python/src/kron_otp.py` instead of the released PyPI module.

## How to use

1. Start the GUI, click **+ Add** (for a saved account), or **Use once** (for a temporary, unsaved key).
2. Give the account a name and optional issuer; paste your **own** Base32 provisioning secret or `otpauth://totp/...` URI. Show/Hide controls the input field.
3. Click **Save encrypted** (Windows) or **Use temporarily**. The app checks the key through `KronOTP.generate` before showing/storing it.
4. Pick an account from the list. Read the OTP and countdown or choose **Copy OTP** to paste into an authorized login. Codes renew every 30 seconds as the local clock advances.
5. **Edit/Delete** changes your encrypted records after confirmation; **Lock** hides and unloads secrets. Reopen them with **Unlock** while signed into the same Windows user account.

## Local encrypted data — important security details

- Saved accounts are **opt-in**. Only Windows supports persistent storage using Microsoft **DPAPI CurrentUser**, with vault located at `%LOCALAPPDATA%\KronOTP\vault.dat`. The encrypted vault is atomically replaced, validates record structure and rejects corrupt payloads; secrets are never intentionally written as plaintext files or logged.
- DPAPI uses the **current Windows user identity**; anyone or malware already running in that unlocked user account may be able to decrypt the vault. App Lock only hides in-memory account entries; it **does not reauthenticate a Windows user**. Keep Windows session protected and device encrypted.
- The vault cannot be decrypted with a different Windows user/profile or restored onto an arbitrary computer. There is currently **no portable backup/export/import** and no automatic recovery. Back up your TOTP credentials safely using a trusted separate recovery mechanism before relying on this app as your only authenticator.
- On non-Windows platforms, persistent saving is disabled entirely (session-only Use once). The UI may run with Tkinter, but only Windows desktop behavior is presently exercised and verified.
- The app holds secrets in ordinary Python/Tkinter process memory while unlocked; it cannot promise perfect memory zeroization. Screens, unlocked Windows session, shoulder surfing and clipboard are security risks.

## Limits / not implemented

- No QR camera/image scanning, HOTP, SHA256/512, 8-digit codes, custom period, user login/session server, external site verification, remote account automation, anti-replay or rate-limiting service. These would require capabilities outside the fixed KronOTP engine or outside this local GUI.
- Current OTP depends on accurately synchronized local device time; this tool does **not** synchronize the system clock.
- GitHub `main` branch/tag protection and the original P04 production/cross-platform security assurance remain deferred. This application is **production-oriented for authorized personal Windows use** but cannot be called independently security-audited or certified. Test with noncritical accounts and retain account recovery codes before depending on it.

## Focused local tests

From the monorepo root on Windows, using a Python environment where the published PyPI package is installed:

```powershell
python -m unittest discover -s python/tests/gui -p test_app.py -v
```

Tests use only a published synthetic RFC fixture, validate DPAPI vault roundtrip and corruption, account management, URI/unsupported configurations, clipboard handling and real Tkinter lifecycle. No secrets are committed. The existing Python/JavaScript engine and GitHub publishing workflows are unchanged.
