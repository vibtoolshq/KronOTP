# KronOTP — Tkinter Live TOTP Tester

Small **test/example GUI**, built with Python's standard-library Tkinter. It calls the **installed PyPI kron-otp==2.0.0 engine**, not the repository's `python/src/kron_otp.py`. No additional GUI framework required.

## Install on Windows

1. Install Python 3.10 or newer with Tkinter (typical official Windows Python installs include it).
2. Install the published engine in the SAME Python interpreter that runs the GUI:

```powershell
python -m pip install kron-otp==2.0.0
```

3. Download the repository's `python/tests/gui/` folder (or clone the KronOTP repository). The PyPI engine installation does **not** install this GUI.
4. Run from the repository root:

```powershell
python python/tests/gui/app.py
```

Or change to `python/tests/gui/` and run `python app.py`. If several Python interpreters are installed, use the same interpreter for both commands.

**Isolated environment example (recommended):**

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install kron-otp==2.0.0
.venv\Scripts\python.exe python/tests/gui/app.py
```

Create your virtual environment outside the tracked repository if you do not want extra local files. GUI startup checks the exact installed `kron-otp` distribution version **2.0.0** and that `kron_otp.py` is the module belonging to that installed distribution. A missing/wrong version or accidental import of local source shows an error instead of silently using it.

## Usage

1. Paste a **Base32 TOTP provisioning secret that you own** into the masked field. Show/Hide controls only screen visibility.
2. Click **Generate OTP** (or Enter). The GUI calls `KronOTP.generate(secret)` and displays the six-digit code.
3. It displays the remaining seconds in the current 30-second period and **automatically refreshes** the code on each next period while the key remains unchanged.
4. Click **Copy OTP** to copy the current six-digit code, **not** the key, to the system clipboard. Editing the key clears the old code and disables Copy until Generate is pressed again.
5. Missing, malformed, too-short or oversized secrets are rejected with a non-sensitive status message. This app does not persist your secret to a file, print it or send it to a service.

## Important boundaries

- **Local-only generation demo:** it does not authenticate an account, verify codes against another service, provide secret provisioning/QR setup or store keys. It requires an *existing* Base32 secret provided by you.
- A generated code depends on the **local system clock**. The 30-second countdown and refresh use the device clock; keep it synchronized.
- Treat screen recordings, the visible key, and the **OTP clipboard content** as sensitive. Clear the clipboard after use when needed. The secret remains in memory while the window is open.
- This GUI lives only in the GitHub source repository; the PyPI wheel includes the Python engine only. Installing `kron-otp==2.0.0` by itself does not install `app.py`.
- It does not implement OTP replay blocking, per-user rate limits, secret vaults or login sessions. These belong to a real authentication server.
- Existing JavaScript/Python engine API, package version, unit tests and GitHub workflows are untouched by GUI-01.
