"""Focused GUI-02 tests using public synthetic RFC Base32 data only.

Run on Windows with real PyPI engine:
  python -m unittest discover -s python/tests/gui -p test_app.py -v
No account secrets, plaintext backups or production accounts are used.
"""
from __future__ import annotations

from pathlib import Path
import tempfile
import unittest
from unittest import mock
import tkinter as tk
import time

import app
from vault import AccountVault, VaultError, validate_accounts

RFC_KEY = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"


class URIAndInputTests(unittest.TestCase):
    def test_base32_and_supported_uri(self):
        self.assertEqual(app.parse_auth_input(RFC_KEY), ("", "", RFC_KEY))
        uri = (
            "otpauth://totp/Example%3Aalice%40example.test?"
            "secret=" + RFC_KEY + "&issuer=Example&algorithm=SHA1&digits=6&period=30"
        )
        self.assertEqual(app.parse_auth_input(uri), ("Example", "alice@example.test", RFC_KEY))

    def test_unsupported_and_malformed_uri(self):
        for uri in (
            "otpauth://hotp/Example:alice?secret=" + RFC_KEY,
            "otpauth://totp/Example:alice?secret=" + RFC_KEY + "&algorithm=SHA256",
            "otpauth://totp/Example:alice?secret=" + RFC_KEY + "&digits=8",
            "otpauth://totp/Example:alice?secret=" + RFC_KEY + "&period=60",
            "otpauth://totp/Example:alice?secret=" + RFC_KEY + "&secret=" + RFC_KEY,
            "otpauth://totp/Other:alice?secret=" + RFC_KEY + "&issuer=Example",
            "https://example.test/?secret=" + RFC_KEY,
        ):
            with self.subTest(uri=uri[:70]):
                with self.assertRaises(ValueError):
                    app.parse_auth_input(uri)

    def test_input_bounds_and_names(self):
        with self.assertRaises(ValueError):
            app.parse_auth_input("A" * 4097)
        with self.assertRaises(ValueError):
            app.clean_label("  ", required=True, field="Name")
        with self.assertRaises(ValueError):
            app.clean_label("bad\nname", required=True, field="Name")


@unittest.skipUnless(__import__("os").name == "nt", "DPAPI and Tk GUI tested on Windows")
class EncryptedVaultTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="kronotp-gui02-")
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "KronOTP" / "vault.dat"
        self.vault = AccountVault(self.path)
        self.record = {
            "id": "00000000-0000-4000-8000-000000000001",
            "name": "Synthetic account",
            "issuer": "RFC",
            "secret": RFC_KEY,
        }

    def test_encrypted_roundtrip_and_tamper_detection(self):
        self.vault.save([self.record])
        raw = self.path.read_bytes()
        self.assertNotIn(RFC_KEY.encode(), raw)
        self.assertNotIn(b"Synthetic account", raw)
        self.assertEqual(self.vault.load(), [self.record])

        self.path.write_bytes(raw[:25] + b"tampered" + raw[25:])
        with self.assertRaises(VaultError):
            self.vault.load()
        self.assertTrue(self.path.exists(), "Corrupt vault must not be overwritten")

    def test_validation_rejects_bad_records_and_symlink(self):
        with self.assertRaises(VaultError):
            validate_accounts([dict(self.record, id="not-a-uuid")])
        with self.assertRaises(VaultError):
            validate_accounts([self.record, self.record])
        with self.assertRaises(VaultError):
            validate_accounts([dict(self.record, secret="S" * 5000)])
        self.vault.save([])
        self.assertEqual(self.vault.load(), [])


@unittest.skipUnless(__import__("os").name == "nt", "Tk multi-account integration tested on Windows")
class TkAppTests(unittest.TestCase):
    def setUp(self):
        self.engine = app.load_pypi_engine()
        self.assertEqual(app.metadata.version("kron-otp"), "2.0.0")
        self.temp = tempfile.TemporaryDirectory(prefix="kronotp-gui02-ui-")
        self.addCleanup(self.temp.cleanup)
        self.vault = AccountVault(Path(self.temp.name) / "KronOTP" / "vault.dat")
        self.ui = app.Authenticator(self.engine, vault=self.vault)
        self.ui.withdraw()
        self.addCleanup(self._destroy_ui)

    def _destroy_ui(self):
        try:
            if self.ui.winfo_exists():
                self.ui._close()
        except tk.TclError:
            pass

    def test_save_search_edit_lock_unlock_delete_and_transient(self):
        self.assertFalse(self.ui._locked)
        uri = (
            "otpauth://totp/Example%3Aalice%40example.test?"
            "secret=" + RFC_KEY + "&issuer=Example"
        )
        saved = self.ui.add_account("", "", uri, persist=True)
        self.assertEqual(saved["name"], "alice@example.test")
        self.assertEqual(saved["issuer"], "Example")
        self.assertEqual(len(self.ui._accounts), 1)
        self.assertTrue(self.vault.exists())
        self.assertNotIn(RFC_KEY.encode(), self.vault.path.read_bytes())
        self.assertEqual(self.ui._selected_id, saved["id"])
        self.assertEqual(self.ui._code, self.engine.generate(RFC_KEY))

        self.ui.search.set("not-present")
        self.assertEqual(len(self.ui.tree.get_children()), 0)
        self.ui.search.set("alice")
        self.assertEqual(len(self.ui.tree.get_children()), 1)
        self.ui.search.set("")
        self.ui.edit_account(saved["id"], "Updated", "Example", RFC_KEY)
        self.assertEqual(self.vault.load()[0]["name"], "Updated")

        self.ui.copy_otp()
        self.ui.update()
        self.assertEqual(self.ui.clipboard_get(), self.ui._code)
        self.ui.clipboard_clear()
        self.ui.clipboard_append("USER-SAVED-CLIPBOARD")
        self.ui._clear_owned_clipboard()
        self.assertEqual(self.ui.clipboard_get(), "USER-SAVED-CLIPBOARD")

        self.ui._privacy_lock()
        self.assertTrue(self.ui._locked)
        self.assertEqual(self.ui._accounts, [])
        self.assertIsNone(self.ui._code)
        self.ui._privacy_lock()
        self.assertFalse(self.ui._locked)
        self.assertEqual(self.ui._accounts[0]["name"], "Updated")
        self.ui.delete_account(saved["id"])
        self.assertEqual(self.vault.load(), [])

        session = self.ui.add_account("One-off", "", RFC_KEY, persist=False)
        self.assertIsNotNone(self.ui._session)
        self.assertEqual(self.ui._code, self.engine.generate(RFC_KEY))
        self.ui.delete_account(session["id"])
        self.assertIsNone(self.ui._session)
        self.assertEqual(self.vault.load(), [])

    def test_invalid_input_keeps_persistent_state_and_idle_lock(self):
        with self.assertRaises(ValueError):
            self.ui.add_account("Invalid", "", "IE", persist=True)
        self.assertFalse(self.vault.exists())

        record = self.ui.add_account("Real fixture", "", RFC_KEY, persist=True)
        with mock.patch.object(self.vault, "save", side_effect=VaultError("disk unavailable")):
            with self.assertRaises(VaultError):
                self.ui.edit_account(record["id"], "Changed", "", RFC_KEY)
        self.assertEqual(self.ui._accounts[0]["name"], "Real fixture")

        with mock.patch.object(app.time, "monotonic", return_value=self.ui._last_activity + 301):
            self.ui._tick()
        self.assertTrue(self.ui._locked)
        self.assertEqual(self.ui.otp_display.get(), "••••••")
        self.assertIsNone(self.ui._session)

    def test_rollover_and_clipboard_expiry(self):
        self.ui.add_account("Fixture", "", RFC_KEY, persist=False)
        with mock.patch.object(app.time, "time", return_value=59):
            self.ui._show_current(force=True)
            first = self.ui._code
            self.assertEqual(self.ui.countdown.get()[:3], "01s")
            self.ui.copy_otp()
            self.ui.update()
            self.assertEqual(self.ui.clipboard_get(), first)
        self.ui._clear_owned_clipboard()
        with self.assertRaises(tk.TclError):
            self.ui.clipboard_get()
        with mock.patch.object(app.time, "time", return_value=60):
            self.ui._tick()
            self.assertEqual(self.ui.countdown.get()[:3], "30s")
            self.assertNotEqual(self.ui._code, first)
        self.ui.after(100, self.ui._close)
        self.ui.deiconify()
        self.ui.mainloop()


if __name__ == "__main__":
    unittest.main()
