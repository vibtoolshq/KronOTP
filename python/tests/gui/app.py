"""KronOTP Authenticator — compact source-only Tkinter app.

All OTP generation and local verification use the installed PyPI kron-otp==2.0.0.
Windows DPAPI is used only for opt-in account storage; no plaintext vault.
"""
from __future__ import annotations

import importlib
from importlib import metadata
from pathlib import Path
import os
import re
import sys
import time
import tkinter as tk
from tkinter import messagebox, ttk
from urllib.parse import parse_qs, unquote, urlsplit
import uuid

from vault import AccountVault, VaultError


PACKAGE_VERSION = "2.0.0"
WINDOW_SIZE = "440x535"
IDLE_LOCK_SECONDS = 300
COPY_CLEAR_MS = 15_000
BACKGROUND = "#F6F8FC"
CARD = "#FFFFFF"
INK = "#1D2939"
MUTED = "#66768E"
PRIMARY = "#235CC7"
ERROR = "#B42318"


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
    path = getattr(module, "__file__", None)
    installed_path = Path(installed.locate_file("kron_otp.py")).resolve()
    if (
        path is None
        or Path(path).resolve() != installed_path
        or not installed_path.is_file()
    ):
        raise RuntimeError(
            "KronOTP import is not the installed PyPI module. "
            "Remove local kron_otp.py shadowing and retry."
        )
    return module.KronOTP


def parse_auth_input(value: str) -> tuple[str, str, str]:
    """Extract SHA1/6/30 TOTP key and optional labels; never implement OTP."""
    if not isinstance(value, str) or not 1 <= len(value) <= 4096:
        raise ValueError("Paste a valid Base32 secret or otpauth:// URI.")
    raw = value.strip(" \t\r\n\f\v")
    if not raw.lower().startswith("otpauth://"):
        if "://" in raw:
            raise ValueError("Only otpauth://totp URIs or Base32 keys are accepted.")
        return "", "", raw

    parts = urlsplit(raw)
    if parts.scheme.lower() != "otpauth" or parts.netloc.lower() != "totp":
        raise ValueError("Only otpauth://totp is supported.")
    if parts.fragment or parts.username or parts.password or parts.port:
        raise ValueError("Invalid authenticator URI.")
    query = parse_qs(parts.query, keep_blank_values=True, max_num_fields=16)
    for field in ("secret", "issuer", "algorithm", "digits", "period"):
        if len(query.get(field, [])) > 1:
            raise ValueError("Duplicate authenticator URI parameter.")
    if query.get("algorithm", ["SHA1"])[0].upper() != "SHA1":
        raise ValueError("This engine supports SHA1 only.")
    if query.get("digits", ["6"])[0] != "6":
        raise ValueError("This engine supports 6 digits only.")
    if query.get("period", ["30"])[0] != "30":
        raise ValueError("This engine supports a 30-second period only.")
    secret = query.get("secret", [""])[0]
    if not secret or len(secret) > 4096:
        raise ValueError("Authenticator URI is missing a valid secret.")

    label = unquote(parts.path.lstrip("/"))
    path_issuer, sep, account = label.partition(":")
    name = account if sep else label
    issuer = query.get("issuer", [""])[0] or (path_issuer if sep else "")
    if sep and query.get("issuer", [""])[0]:
        if path_issuer.casefold() != issuer.casefold():
            raise ValueError("Authenticator URI has conflicting issuers.")
    return issuer, name, secret


def clean_label(value: str, *, required: bool, field: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"Invalid {field}.")
    result = value.strip()
    if len(result) > 80 or not result.isprintable() or (required and not result):
        raise ValueError(f"{field} must be printable and at most 80 characters.")
    return result


class Authenticator(tk.Tk):
    """Multi-account viewer with encrypted opt-in vault and temporary sessions."""

    def __init__(self, engine, vault=None):
        super().__init__()
        self.engine = engine
        if vault is None and os.name == "nt":
            vault = AccountVault()
        self.vault = vault
        self._accounts: list[dict[str, str]] = []
        self._session: dict[str, str] | None = None
        self._locked = bool(self.vault and self.vault.exists())
        self._selected_id: str | None = None
        self._code: str | None = None
        self._step: int | None = None
        self._clipboard_code: str | None = None
        self._clipboard_job: str | None = None
        self._last_activity = time.monotonic()

        self.title("KronOTP Authenticator")
        self.geometry(WINDOW_SIZE)
        self.minsize(405, 505)
        self.configure(background=BACKGROUND)
        self.resizable(True, True)

        self.search = tk.StringVar()
        self.otp_display = tk.StringVar(value="••••••")
        self.account_display = tk.StringVar(value="Select an account")
        self.countdown = tk.StringVar(value="6-digit · 30-second TOTP")
        self.status = tk.StringVar(value="Ready. Add an account or use a secret once.")
        self.pin = tk.BooleanVar(value=False)
        self._style_widgets()
        self._build_widgets()

        self.search.trace_add("write", lambda *_: self._populate())
        self.tree.bind("<<TreeviewSelect>>", self._on_selection)
        self.tree.bind("<Double-1>", lambda _event: self._edit_selected())
        self.bind_all("<KeyPress>", self._record_activity, add="+")
        self.bind_all("<ButtonPress>", self._record_activity, add="+")
        self.bind("<Control-n>", lambda _e: self._edit_dialog(), add="+")
        self.bind("<Control-f>", lambda _e: self._focus_search(), add="+")
        self.bind("<Control-l>", lambda _e: self._privacy_lock(), add="+")
        self.bind("<Control-Shift-C>", lambda _e: self.copy_otp(), add="+")
        self.protocol("WM_DELETE_WINDOW", self._close)
        self._populate()
        self.after(200, self._tick)

        if self._locked:
            self._set_status("Saved accounts hidden. Select Unlock.", warn=True)
        elif self.vault is None:
            self._set_status("Session-only: encrypted saving requires Windows.")

    def _style_widgets(self):
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("Auth.TFrame", background=BACKGROUND)
        style.configure("Auth.TLabel", background=BACKGROUND, foreground=INK, font=("Segoe UI", 10))
        style.configure("Sub.TLabel", background=BACKGROUND, foreground=MUTED, font=("Segoe UI", 9))
        style.configure("Error.TLabel", background=BACKGROUND, foreground=ERROR, font=("Segoe UI", 9))
        style.configure("Auth.TEntry", padding=5)
        style.configure("Auth.TButton", padding=(7, 6), font=("Segoe UI", 9))
        style.configure("Primary.TButton", padding=(9, 7), background=PRIMARY,
                        foreground="#FFFFFF", font=("Segoe UI", 10, "bold"))
        style.map("Primary.TButton", background=[("active", "#17479E"), ("disabled", "#A9B9D8")])
        style.configure("Auth.Treeview", rowheight=27, font=("Segoe UI", 9),
                        background=CARD, fieldbackground=CARD)
        style.configure("Auth.Treeview.Heading", font=("Segoe UI", 9, "bold"))
        style.configure("Auth.TCheckbutton", background=BACKGROUND, font=("Segoe UI", 9))
        style.configure("Auth.Horizontal.TProgressbar", background=PRIMARY, troughcolor="#E6EDF7")

    def _build_widgets(self):
        outer = ttk.Frame(self, padding=(16, 11), style="Auth.TFrame")
        outer.pack(fill="both", expand=True)
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(3, weight=1)

        header = ttk.Frame(outer, style="Auth.TFrame")
        header.grid(row=0, column=0, sticky="ew")
        ttk.Label(header, text="KronOTP", font=("Segoe UI", 16, "bold"),
                  background=BACKGROUND, foreground=INK).pack(side="left")
        ttk.Label(header, text="AUTHENTICATOR · 2.0.0",
                  style="Sub.TLabel").pack(side="right")

        search_row = ttk.Frame(outer, style="Auth.TFrame")
        search_row.grid(row=1, column=0, sticky="ew", pady=(11, 7))
        search_row.columnconfigure(0, weight=1)
        self.search_entry = ttk.Entry(search_row, textvariable=self.search, style="Auth.TEntry")
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ttk.Button(search_row, text="+ Add", command=self._edit_dialog,
                   style="Auth.TButton").grid(row=0, column=1, padx=(0, 5))
        ttk.Button(search_row, text="Use once", command=lambda: self._edit_dialog(temporary=True),
                   style="Auth.TButton").grid(row=0, column=2)

        info = ttk.Frame(outer, style="Auth.TFrame")
        info.grid(row=2, column=0, sticky="ew")
        self.counter = ttk.Label(info, text="0 saved accounts", style="Sub.TLabel")
        self.counter.pack(side="left")
        ttk.Label(info, text="Local · SHA1 / 6 / 30", style="Sub.TLabel").pack(side="right")

        table = ttk.Frame(outer, style="Auth.TFrame")
        table.grid(row=3, column=0, sticky="nsew", pady=(6, 4))
        table.columnconfigure(0, weight=1)
        table.rowconfigure(0, weight=1)
        self.tree = ttk.Treeview(
            table, columns=("name", "issuer"), show="headings", height=5,
            selectmode="browse", style="Auth.Treeview",
        )
        self.tree.heading("name", text="Account")
        self.tree.heading("issuer", text="Issuer")
        self.tree.column("name", width=210, anchor="w", stretch=True)
        self.tree.column("issuer", width=125, anchor="w", stretch=True)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(table, orient="vertical", command=self.tree.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scroll.set)

        actions = ttk.Frame(outer, style="Auth.TFrame")
        actions.grid(row=4, column=0, sticky="ew")
        ttk.Button(actions, text="Edit", command=self._edit_selected, style="Auth.TButton").pack(side="left")
        ttk.Button(actions, text="Delete", command=self._delete_selected, style="Auth.TButton").pack(side="left", padx=5)
        self.lock_button = ttk.Button(actions, text="Unlock" if self._locked else "Lock",
                                      command=self._privacy_lock, style="Auth.TButton")
        self.lock_button.pack(side="right")

        card = tk.Frame(outer, background=CARD, highlightbackground="#DCE4F0",
                        highlightthickness=1)
        card.grid(row=5, column=0, sticky="ew", pady=(10, 8))
        tk.Label(card, textvariable=self.account_display, background=CARD,
                 foreground=MUTED, font=("Segoe UI", 9)).pack(pady=(8, 0))
        tk.Label(card, textvariable=self.otp_display, background=CARD,
                 foreground=INK, font=("Consolas", 27, "bold")).pack(pady=(0, 2))
        tk.Label(card, textvariable=self.countdown, background=CARD,
                 foreground=MUTED, font=("Segoe UI", 9)).pack()
        self.progress = ttk.Progressbar(card, length=265, maximum=30,
                                        style="Auth.Horizontal.TProgressbar", mode="determinate")
        self.progress.pack(fill="x", padx=16, pady=(7, 10))

        bottom = ttk.Frame(outer, style="Auth.TFrame")
        bottom.grid(row=6, column=0, sticky="ew")
        bottom.columnconfigure(0, weight=1)
        self.copy_button = ttk.Button(bottom, text="Copy OTP", command=self.copy_otp,
                                       style="Primary.TButton", state="disabled")
        self.copy_button.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ttk.Button(bottom, text="Local check", command=self._verify_dialog,
                   style="Auth.TButton").grid(row=0, column=1)

        foot = ttk.Frame(outer, style="Auth.TFrame")
        foot.grid(row=7, column=0, sticky="ew", pady=(9, 0))
        ttk.Checkbutton(foot, text="Always on top", variable=self.pin,
                        command=lambda: self.attributes("-topmost", self.pin.get()),
                        style="Auth.TCheckbutton").pack(side="left")
        self.status_label = ttk.Label(foot, textvariable=self.status, style="Sub.TLabel",
                                       wraplength=248)
        self.status_label.pack(side="right", anchor="e")

    def _record_activity(self, _event=None):
        self._last_activity = time.monotonic()

    def _focus_search(self):
        self.search_entry.focus_set()
        self.search_entry.select_range(0, "end")

    def _set_status(self, text: str, *, warn: bool = False):
        self.status.set(text)
        self.status_label.configure(style="Error.TLabel" if warn else "Sub.TLabel")

    def _entries(self):
        return self._accounts + ([self._session] if self._session is not None else [])

    def _find(self, ident):
        for record in self._entries():
            if record["id"] == ident:
                return record
        return None

    def _populate(self):
        previous = self._selected_id
        for item in self.tree.get_children():
            self.tree.delete(item)
        if not self._locked:
            needle = self.search.get().casefold()
            for record in self._entries():
                searchable = (record["name"] + " " + record["issuer"]).casefold()
                if needle in searchable:
                    self.tree.insert("", "end", iid=record["id"],
                                     values=(record["name"], record["issuer"] or "—"))
        self.counter.configure(text=f"{len(self._accounts)} saved · {1 if self._session else 0} temporary")
        visible = self.tree.get_children()
        chosen = previous if previous in visible else (visible[0] if visible else None)
        self._selected_id = chosen
        if chosen is None:
            self._clear_code()
        else:
            self.tree.selection_set(chosen)
            self._show_current(force=True)

    def _on_selection(self, _event=None):
        selected = self.tree.selection()
        ident = selected[0] if selected else None
        if ident != self._selected_id:
            self._selected_id = ident
            self._show_current(force=True)

    def _clear_code(self):
        self._code = None
        self._step = None
        self.account_display.set("Select an account")
        self.otp_display.set("••••••")
        self.countdown.set("6-digit · 30-second TOTP")
        self.progress.configure(value=0)
        self.copy_button.configure(state="disabled")

    def _show_current(self, *, force=False):
        if self._locked:
            self._clear_code()
            return
        record = self._find(self._selected_id)
        if not record:
            self._clear_code()
            return
        now = time.time()
        current_step = int(now) // 30
        if force or current_step != self._step or self._code is None:
            try:
                code = self.engine.generate(record["secret"])
                after = time.time()
                if int(after) // 30 != current_step:
                    code = self.engine.generate(record["secret"])
                self._step = int(after) // 30
            except (ValueError, TypeError):
                self._clear_code()
                self._set_status("Invalid stored secret. Edit this account.", warn=True)
                return
            except Exception:
                self._clear_code()
                self._set_status("OTP generator unavailable.", warn=True)
                return
            self._code = code
            self.otp_display.set(code)
            self.account_display.set(record["name"] + (" · " + record["issuer"] if record["issuer"] else ""))
            self.copy_button.configure(state="normal")
        remaining = 30 - (int(time.time()) % 30)
        self.countdown.set(f"{remaining:02d}s remaining · refreshes automatically")
        self.progress.configure(value=remaining)

    def _tick(self):
        if not self._locked and self._entries():
            if time.monotonic() - self._last_activity >= IDLE_LOCK_SECONDS:
                self._privacy_lock(auto=True)
            else:
                self._show_current()
        self.after(250, self._tick)

    def _privacy_lock(self, _event=None, *, auto=False):
        if not self._locked:
            self._accounts.clear()
            self._session = None
            self._selected_id = None
            self._locked = True
            self._clear_owned_clipboard()
            self.lock_button.configure(text="Unlock")
            self._populate()
            self._set_status("Auto-locked after inactivity." if auto else "Accounts hidden. Select Unlock.")
            return
        if self.vault is None:
            self._locked = False
            self.lock_button.configure(text="Lock")
            self._populate()
            self._set_status("Session-only mode. Account secrets were not saved.")
            self._record_activity()
            return
        try:
            loaded = self.vault.load()
        except VaultError as exc:
            self._set_status(str(exc), warn=True)
            messagebox.showerror("Could not unlock", str(exc), parent=self)
            return
        self._accounts = loaded
        self._locked = False
        self.lock_button.configure(text="Lock")
        self._record_activity()
        self._populate()
        self._set_status("Encrypted accounts unlocked with current Windows user.")

    def _require_unlocked(self):
        if self._locked:
            self._privacy_lock()
        return not self._locked

    def add_account(self, name: str, issuer: str, supplied: str, *, persist: bool) -> dict[str, str]:
        if self._locked:
            raise VaultError("Unlock accounts before adding a key.")
        uri_issuer, uri_name, secret = parse_auth_input(supplied)
        name = clean_label(name or uri_name or ("Temporary OTP" if not persist else ""),
                           required=True, field="Account name")
        issuer = clean_label(issuer or uri_issuer, required=False, field="Issuer")
        secret = re.sub(r"[ \t\r\n\f\v]+", "", secret).upper()
        self.engine.generate(secret)  # Real installed KronOTP performs validation and OTP.
        record = {"id": str(uuid.uuid4()), "name": name, "issuer": issuer, "secret": secret}
        if persist:
            if self.vault is None:
                raise VaultError("Encrypted saving is available only on Windows.")
            candidate = self._accounts + [record]
            self.vault.save(candidate)  # Persist before updating live view.
            self._accounts = candidate
        else:
            self._session = record
        self._selected_id = record["id"]
        self.search.set("")
        self._populate()
        self._set_status("Account saved encrypted." if persist else "Temporary code loaded; not saved.")
        return record

    def edit_account(self, ident: str, name: str, issuer: str, supplied: str):
        if self._locked:
            raise VaultError("Unlock accounts before editing.")
        old = next((x for x in self._accounts if x["id"] == ident), None)
        if old is None:
            raise VaultError("Only saved accounts can be edited.")
        uri_issuer, uri_name, secret = parse_auth_input(supplied)
        name = clean_label(name or uri_name, required=True, field="Account name")
        issuer = clean_label(issuer or uri_issuer, required=False, field="Issuer")
        secret = re.sub(r"[ \t\r\n\f\v]+", "", secret).upper()
        self.engine.generate(secret)
        edited = {"id": ident, "name": name, "issuer": issuer, "secret": secret}
        candidate = [edited if x["id"] == ident else x for x in self._accounts]
        self.vault.save(candidate)
        self._accounts = candidate
        self._selected_id = ident
        self.search.set("")
        self._populate()
        self._set_status("Saved account updated.")

    def delete_account(self, ident: str):
        if self._locked:
            raise VaultError("Unlock accounts before deleting.")
        if self._session and ident == self._session["id"]:
            self._session = None
        elif any(x["id"] == ident for x in self._accounts):
            candidate = [x for x in self._accounts if x["id"] != ident]
            self.vault.save(candidate)
            self._accounts = candidate
        else:
            return
        self._selected_id = None
        self._populate()
        self._set_status("Account deleted.")

    def _edit_selected(self):
        if not self._require_unlocked():
            return
        record = self._find(self._selected_id)
        if not record:
            self._set_status("Select an account to edit.")
            return
        if self._session and self._session["id"] == record["id"]:
            self._edit_dialog(temporary=True, initial=record)
        else:
            self._edit_dialog(initial=record)

    def _delete_selected(self):
        if not self._require_unlocked():
            return
        record = self._find(self._selected_id)
        if not record:
            self._set_status("Select an account to delete.")
            return
        if not messagebox.askyesno(
            "Delete account", f"Delete {record['name']}? This cannot be undone.",
            parent=self,
        ):
            return
        try:
            self.delete_account(record["id"])
        except VaultError as exc:
            messagebox.showerror("Vault error", str(exc), parent=self)

    def _edit_dialog(self, _event=None, *, temporary=False, initial=None):
        if not self._require_unlocked():
            return
        if not temporary and self.vault is None:
            self._set_status("Encrypted saving requires Windows; use once instead.", warn=True)
            return

        dialog = tk.Toplevel(self)
        dialog.title("Account details" if initial else "Add authenticator account")
        dialog.geometry("410x315")
        dialog.minsize(375, 295)
        dialog.configure(background=BACKGROUND)
        dialog.transient(self)
        dialog.grab_set()
        body = ttk.Frame(dialog, padding=15, style="Auth.TFrame")
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=1)

        name = tk.StringVar(value=initial["name"] if initial else "")
        issuer = tk.StringVar(value=initial["issuer"] if initial else "")
        secret = tk.StringVar(value=initial["secret"] if initial else "")
        reveal = tk.BooleanVar(value=False)

        ttk.Label(body, text="Account name", style="Auth.TLabel").grid(row=0, column=0, sticky="w")
        name_entry = ttk.Entry(body, textvariable=name, style="Auth.TEntry")
        name_entry.grid(row=1, column=0, sticky="ew", pady=(3, 9))
        ttk.Label(body, text="Issuer / service (optional)", style="Auth.TLabel").grid(row=2, column=0, sticky="w")
        ttk.Entry(body, textvariable=issuer, style="Auth.TEntry").grid(row=3, column=0, sticky="ew", pady=(3, 9))
        ttk.Label(body, text="Base32 secret OR otpauth://totp URI", style="Auth.TLabel").grid(row=4, column=0, sticky="w")
        secret_row = ttk.Frame(body, style="Auth.TFrame")
        secret_row.grid(row=5, column=0, sticky="ew", pady=(3, 4))
        secret_row.columnconfigure(0, weight=1)
        secret_entry = ttk.Entry(secret_row, textvariable=secret, show="•", style="Auth.TEntry")
        secret_entry.grid(row=0, column=0, sticky="ew")
        ttk.Checkbutton(
            secret_row, text="Show", variable=reveal,
            command=lambda: secret_entry.configure(show="" if reveal.get() else "•"),
            style="Auth.TCheckbutton",
        ).grid(row=0, column=1, padx=(8, 0))
        ttk.Label(
            body, text="Only SHA1 / 6 digits / 30s. Save uses Windows encryption.",
            style="Sub.TLabel",
        ).grid(row=6, column=0, sticky="w")

        buttons = ttk.Frame(body, style="Auth.TFrame")
        buttons.grid(row=7, column=0, sticky="ew", pady=(15, 0))
        buttons.columnconfigure(0, weight=1)

        def commit():
            try:
                if initial and not temporary:
                    self.edit_account(initial["id"], name.get(), issuer.get(), secret.get())
                else:
                    self.add_account(
                        name.get(), issuer.get(), secret.get(),
                        persist=not temporary,
                    )
            except (ValueError, VaultError, TypeError):
                messagebox.showerror(
                    "Account input", "Could not save. Check name, Base32 key and vault access.",
                    parent=dialog,
                )
                return
            secret.set("")
            dialog.destroy()

        ttk.Button(buttons, text="Cancel", command=dialog.destroy,
                   style="Auth.TButton").grid(row=0, column=0, sticky="w")
        ttk.Button(
            buttons, text="Use temporarily" if temporary else "Save encrypted",
            command=commit, style="Primary.TButton",
        ).grid(row=0, column=1, sticky="e")
        name_entry.focus_set()
        dialog.bind("<Escape>", lambda _e: dialog.destroy())

    def _verify_dialog(self):
        if self._locked:
            self._set_status("Unlock accounts to check a code.", warn=True)
            return
        record = self._find(self._selected_id)
        if not record:
            self._set_status("Select an account first.")
            return
        dialog = tk.Toplevel(self)
        dialog.title("Local OTP check · not a remote login")
        dialog.geometry("370x170")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        area = ttk.Frame(dialog, padding=15)
        area.pack(fill="both", expand=True)
        ttk.Label(area, text="Check an OTP against the selected local secret").pack(anchor="w")
        supplied = tk.StringVar()
        entry = ttk.Entry(area, textvariable=supplied)
        entry.pack(fill="x", pady=9)
        feedback = ttk.Label(area, text="This is NOT server authentication.")
        feedback.pack(anchor="w")

        def run():
            token = supplied.get()
            matched = self.engine.verify(record["secret"], token)
            feedback.configure(text="Local code matches." if matched else "Code does not match locally.")
            supplied.set("")

        ttk.Button(area, text="Check code", command=run).pack(anchor="e", pady=7)
        entry.focus_set()
        dialog.bind("<Return>", lambda _e: run())
        dialog.bind("<Escape>", lambda _e: dialog.destroy())

    def copy_otp(self):
        if self._locked:
            return
        self._show_current()
        if self._code is None:
            return
        try:
            self.clipboard_clear()
            self.clipboard_append(self._code)
        except tk.TclError:
            self._set_status("Clipboard unavailable.", warn=True)
            return
        self._clipboard_code = self._code
        if self._clipboard_job is not None:
            self.after_cancel(self._clipboard_job)
        self._clipboard_job = self.after(COPY_CLEAR_MS, self._clear_owned_clipboard)
        self._set_status("OTP copied. Clipboard clears in 15s if unchanged.")

    def _clear_owned_clipboard(self):
        self._clipboard_job = None
        if self._clipboard_code is None:
            return
        copied = self._clipboard_code
        self._clipboard_code = None
        try:
            if self.clipboard_get() == copied:
                self.clipboard_clear()
        except tk.TclError:
            pass

    def _close(self):
        self._clear_owned_clipboard()
        self._accounts.clear()
        self._session = None
        self._clear_code()
        self.destroy()


def main() -> int:
    try:
        engine = load_pypi_engine()
    except (RuntimeError, ImportError) as exc:
        print(str(exc), file=sys.stderr)
        try:
            dialog = tk.Tk()
            dialog.withdraw()
            messagebox.showerror("KronOTP Authenticator", str(exc), parent=dialog)
            dialog.destroy()
        except tk.TclError:
            pass
        return 1
    try:
        app = Authenticator(engine)
        app.mainloop()
        return 0
    except (VaultError, tk.TclError) as exc:
        print("Unable to start Authenticator UI:", type(exc).__name__, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
