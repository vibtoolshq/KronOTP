"""Small local Tkinter tester for the actual installed PyPI kron-otp==2.0.0.

Run: python python/tests/gui/app.py
This file is a repository example, not part of the published PyPI wheel.
Never stores or logs an authenticator secret.
"""

from __future__ import annotations

import importlib
from importlib import metadata
from pathlib import Path
import sys
import time
import tkinter as tk
from tkinter import messagebox, ttk


PACKAGE_VERSION = "2.0.0"
WINDOW_SIZE = "390x282"
BACKGROUND = "#F7F9FC"
INK = "#1F2937"
MUTED = "#657389"
PRIMARY = "#2359C4"
ERROR = "#B42318"
CARD = "#FFFFFF"


def load_pypi_engine():
    """Refuse wrong versions or accidental imports from the repository source."""
    try:
        installed = metadata.distribution("kron-otp")
    except metadata.PackageNotFoundError as exc:
        raise RuntimeError(
            "KronOTP is not installed. Run: python -m pip install kron-otp==2.0.0"
        ) from exc

    if installed.version != PACKAGE_VERSION:
        raise RuntimeError(
            f"Expected PyPI kron-otp=={PACKAGE_VERSION}; "
            f"installed version is {installed.version}."
        )

    module = importlib.import_module("kron_otp")
    module_file = getattr(module, "__file__", None)
    installed_module = Path(installed.locate_file("kron_otp.py")).resolve()
    if (
        module_file is None
        or Path(module_file).resolve() != installed_module
        or not installed_module.is_file()
    ):
        raise RuntimeError(
            "KronOTP import is not the installed PyPI module. "
            "Remove a local kron_otp.py from the import path and retry."
        )
    return module.KronOTP


class LiveTester(tk.Tk):
    """Compact, local-only viewer; key stays in the entry widget's memory."""

    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.title("KronOTP | Live Tester")
        self.geometry(WINDOW_SIZE)
        self.minsize(360, 270)
        self.configure(background=BACKGROUND)
        self.resizable(True, False)

        self.secret = tk.StringVar()
        self.show_secret = tk.BooleanVar(value=False)
        self.otp_display = tk.StringVar(value="••••••")
        self.countdown = tk.StringVar(value="30s period · 6-digit TOTP")
        self.status = tk.StringVar(value="Paste your Base32 authenticator secret.")
        self._active = False
        self._code = None
        self._step = None

        self._configure_style()
        self._make_widgets()
        self.secret.trace_add("write", self._on_secret_changed)
        self.bind("<Return>", lambda _event: self.generate())
        self.after(200, self._tick)

    def _configure_style(self):
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("K.TFrame", background=BACKGROUND)
        style.configure(
            "K.TLabel", background=BACKGROUND, foreground=INK,
            font=("Segoe UI", 10),
        )
        style.configure(
            "K.Secondary.TLabel", background=BACKGROUND, foreground=MUTED,
            font=("Segoe UI", 9),
        )
        style.configure(
            "K.Error.TLabel", background=BACKGROUND, foreground=ERROR,
            font=("Segoe UI", 9),
        )
        style.configure("K.TEntry", padding=6, font=("Segoe UI", 10))
        style.configure(
            "K.Primary.TButton", background=PRIMARY, foreground="#FFFFFF",
            font=("Segoe UI", 10, "bold"), padding=(10, 7),
        )
        style.map(
            "K.Primary.TButton",
            background=[("active", "#1749A9"), ("disabled", "#B9C8DF")],
            foreground=[("disabled", "#526178")],
        )
        style.configure("K.TButton", padding=(10, 7), font=("Segoe UI", 10))
        style.configure("K.TCheckbutton", background=BACKGROUND)

    def _make_widgets(self):
        layout = ttk.Frame(self, padding=(18, 14), style="K.TFrame")
        layout.pack(fill="both", expand=True)
        layout.columnconfigure(0, weight=1)

        top = ttk.Frame(layout, style="K.TFrame")
        top.grid(row=0, column=0, sticky="ew")
        ttk.Label(
            top, text="KronOTP", font=("Segoe UI", 15, "bold"),
            background=BACKGROUND, foreground=INK,
        ).pack(side="left")
        ttk.Label(
            top, text="PYPI · LIVE TESTER", style="K.Secondary.TLabel",
        ).pack(side="right")

        ttk.Label(
            layout, text="Authenticator secret (Base32)",
            style="K.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(13, 5))

        input_row = ttk.Frame(layout, style="K.TFrame")
        input_row.grid(row=2, column=0, sticky="ew")
        input_row.columnconfigure(0, weight=1)
        self.entry = ttk.Entry(
            input_row, textvariable=self.secret, show="•", style="K.TEntry",
        )
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ttk.Checkbutton(
            input_row, text="Show", variable=self.show_secret,
            command=self._toggle_secret, style="K.TCheckbutton",
        ).grid(row=0, column=1)

        card = tk.Frame(
            layout, background=CARD, highlightbackground="#DEE5EF",
            highlightthickness=1,
        )
        card.grid(row=3, column=0, sticky="ew", pady=(12, 10))
        tk.Label(
            card, textvariable=self.otp_display,
            font=("Consolas", 27, "bold"), foreground=INK, background=CARD,
        ).pack(pady=(6, 0))
        tk.Label(
            card, textvariable=self.countdown,
            font=("Segoe UI", 9), foreground=MUTED, background=CARD,
        ).pack(pady=(0, 8))

        actions = ttk.Frame(layout, style="K.TFrame")
        actions.grid(row=4, column=0, sticky="ew")
        actions.columnconfigure(0, weight=1)
        ttk.Button(
            actions, text="Generate OTP", command=self.generate,
            style="K.Primary.TButton",
        ).grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.copy_button = ttk.Button(
            actions, text="Copy OTP", command=self.copy_otp,
            style="K.TButton", state="disabled",
        )
        self.copy_button.grid(row=0, column=1)

        self.status_label = ttk.Label(
            layout, textvariable=self.status, style="K.Secondary.TLabel",
        )
        self.status_label.grid(row=5, column=0, sticky="w", pady=(10, 0))
        self.entry.focus_set()

    def _toggle_secret(self):
        self.entry.configure(show="" if self.show_secret.get() else "•")

    def _reset(self):
        self._active = False
        self._code = None
        self._step = None
        self.otp_display.set("••••••")
        self.countdown.set("30s period · 6-digit TOTP")
        self.copy_button.configure(state="disabled")

    def _on_secret_changed(self, *_args):
        self._reset()
        self._set_status("Secret changed. Select Generate OTP.")

    def _set_status(self, message, *, error=False):
        self.status.set(message)
        self.status_label.configure(
            style="K.Error.TLabel" if error else "K.Secondary.TLabel"
        )

    def _refresh_code(self):
        """Generate from the installed package, never calculate TOTP ourselves."""
        secret = self.secret.get()
        try:
            before = int(time.time()) // 30
            code = self.engine.generate(secret)
            after = int(time.time()) // 30
            if after != before:
                code = self.engine.generate(secret)
            self._step = after
        except (ValueError, TypeError):
            self._reset()
            self._set_status("Invalid Base32 secret (14+ decoded bytes required).",
                             error=True)
            return
        except Exception:
            self._reset()
            self._set_status("Could not generate OTP. Check your environment.",
                             error=True)
            return

        self._code = code
        self._active = True
        self.otp_display.set(code)
        self.copy_button.configure(state="normal")
        self._set_status("Live OTP ready. Secret is not saved.")
        self._update_countdown()

    def generate(self):
        if not self.secret.get().strip():
            self._reset()
            self._set_status("Paste an authenticator Base32 secret first.", error=True)
            return
        self._refresh_code()

    def _update_countdown(self):
        if self._active:
            seconds = 30 - int(time.time()) % 30
            self.countdown.set(f"{seconds:02d}s remaining · auto refresh")

    def _tick(self):
        if self._active:
            if self._step != int(time.time()) // 30:
                self._refresh_code()
            else:
                self._update_countdown()
        self.after(200, self._tick)

    def copy_otp(self):
        if not self._active:
            return
        if self._step != int(time.time()) // 30:
            self._refresh_code()
        if not self._active or self._code is None:
            return
        try:
            self.clipboard_clear()
            self.clipboard_append(self._code)  # Only OTP, never the shared secret.
        except tk.TclError:
            self._set_status("Could not access the system clipboard.", error=True)
            return
        self._set_status("OTP copied to clipboard.")


def main() -> int:
    try:
        engine = load_pypi_engine()
    except (RuntimeError, ImportError) as exc:
        print(str(exc), file=sys.stderr)
        try:
            dialog = tk.Tk()
            dialog.withdraw()
            messagebox.showerror("KronOTP Live Tester", str(exc), parent=dialog)
            dialog.destroy()
        except tk.TclError:
            pass
        return 1

    app = LiveTester(engine)
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
