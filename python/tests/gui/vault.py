"""Windows DPAPI-encrypted, current-user credential vault for the KronOTP GUI.

Never stores plaintext TOTP secrets on disk. Windows-only by design.
"""
from __future__ import annotations

import ctypes
from ctypes import wintypes
import json
import os
from pathlib import Path
import stat
import tempfile
import uuid


FORMAT_VERSION = 1
MAX_ACCOUNTS = 100
MAX_BLOB_BYTES = 1_048_576


class VaultError(RuntimeError):
    """Safe, non-sensitive vault error for GUI display."""


class _DATA_BLOB(ctypes.Structure):
    _fields_ = [
        ("cbData", wintypes.DWORD),
        ("pbData", ctypes.POINTER(ctypes.c_ubyte)),
    ]


def _dpapi(data: bytes, *, decrypt: bool) -> bytes:
    if os.name != "nt":
        raise VaultError("Encrypted account storage requires Windows DPAPI.")
    if not isinstance(data, bytes) or not data or len(data) > MAX_BLOB_BYTES:
        raise VaultError("Invalid or oversized vault payload.")

    crypt32 = ctypes.windll.crypt32
    kernel32 = ctypes.windll.kernel32
    operation = crypt32.CryptUnprotectData if decrypt else crypt32.CryptProtectData
    operation.restype = wintypes.BOOL
    if decrypt:
        operation.argtypes = [
            ctypes.POINTER(_DATA_BLOB), ctypes.c_void_p,
            ctypes.POINTER(_DATA_BLOB), ctypes.c_void_p, ctypes.c_void_p,
            wintypes.DWORD, ctypes.POINTER(_DATA_BLOB),
        ]
    else:
        operation.argtypes = [
            ctypes.POINTER(_DATA_BLOB), wintypes.LPCWSTR,
            ctypes.POINTER(_DATA_BLOB), ctypes.c_void_p, ctypes.c_void_p,
            wintypes.DWORD, ctypes.POINTER(_DATA_BLOB),
        ]
    kernel32.LocalFree.argtypes = [ctypes.c_void_p]
    kernel32.LocalFree.restype = ctypes.c_void_p

    input_buffer = (ctypes.c_ubyte * len(data)).from_buffer_copy(data)
    source = _DATA_BLOB(len(data), ctypes.cast(input_buffer, ctypes.POINTER(ctypes.c_ubyte)))
    target = _DATA_BLOB()
    try:
        if decrypt:
            ok = operation(ctypes.byref(source), None, None, None, None, 1, ctypes.byref(target))
        else:
            ok = operation(ctypes.byref(source), "KronOTP Authenticator", None, None, None, 1, ctypes.byref(target))
        if not ok:
            raise VaultError(
                "Cannot unlock encrypted accounts using this Windows user profile."
                if decrypt else "Windows could not encrypt the account vault."
            )
        return ctypes.string_at(target.pbData, target.cbData)
    finally:
        if target.pbData:
            kernel32.LocalFree(ctypes.cast(target.pbData, ctypes.c_void_p))


def validate_accounts(accounts: object) -> list[dict[str, str]]:
    """Reject malformed/unbounded data before encryption or GUI use."""
    if not isinstance(accounts, list) or len(accounts) > MAX_ACCOUNTS:
        raise VaultError("Account vault has an invalid number of entries.")
    verified = []
    seen = set()
    for item in accounts:
        if not isinstance(item, dict) or set(item) != {"id", "name", "issuer", "secret"}:
            raise VaultError("Account vault contains an invalid record.")
        ident, name, issuer, secret = (item[k] for k in ("id", "name", "issuer", "secret"))
        try:
            if not isinstance(ident, str) or str(uuid.UUID(ident)) != ident or ident in seen:
                raise ValueError
        except (TypeError, ValueError, AttributeError):
            raise VaultError("Account vault contains an invalid identifier.") from None
        if not (isinstance(name, str) and 1 <= len(name) <= 80 and name == name.strip() and name.isprintable()):
            raise VaultError("Account vault contains an invalid account name.")
        if not (isinstance(issuer, str) and len(issuer) <= 80 and issuer == issuer.strip() and (not issuer or issuer.isprintable())):
            raise VaultError("Account vault contains an invalid issuer.")
        if not (isinstance(secret, str) and 1 <= len(secret) <= 4096 and secret.isascii()):
            raise VaultError("Account vault contains an invalid secret format.")
        seen.add(ident)
        verified.append({"id": ident, "name": name, "issuer": issuer, "secret": secret})
    return verified


class AccountVault:
    """DPAPI CurrentUser envelope. No plaintext export or portable backup."""

    def __init__(self, path: Path | None = None):
        if os.name != "nt":
            raise VaultError("Saved account storage is available only on Windows.")
        base = Path(os.environ.get("LOCALAPPDATA") or (Path.home() / "AppData" / "Local"))
        self.path = Path(path) if path is not None else base / "KronOTP" / "vault.dat"

    def exists(self) -> bool:
        return self.path.exists() or self.path.is_symlink()

    def _ensure_safe_path(self, *, reading: bool) -> None:
        folder = self.path.parent
        if folder.is_symlink() or (folder.exists() and not folder.is_dir()):
            raise VaultError("Unsafe encrypted vault directory.")
        if self.path.is_symlink():
            raise VaultError("Refusing a symbolic-link vault.")
        if self.path.exists():
            info = self.path.stat()
            if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_BLOB_BYTES:
                raise VaultError("Vault must be a regular, bounded file.")
        elif reading:
            return

    def load(self) -> list[dict[str, str]]:
        self._ensure_safe_path(reading=True)
        if not self.path.exists():
            return []
        try:
            encrypted = self.path.read_bytes()
            plaintext = _dpapi(encrypted, decrypt=True)
            decoded = json.loads(plaintext.decode("utf-8"))
            if not isinstance(decoded, dict) or set(decoded) != {"format", "accounts"}:
                raise VaultError("Encrypted vault format is invalid.")
            if type(decoded["format"]) is not int or decoded["format"] != FORMAT_VERSION:
                raise VaultError("Unsupported encrypted vault format.")
            return validate_accounts(decoded["accounts"])
        except (OSError, ValueError, UnicodeError, json.JSONDecodeError) as exc:
            raise VaultError("Could not read the encrypted account vault.") from exc

    def save(self, accounts: list[dict[str, str]]) -> None:
        verified = validate_accounts(accounts)
        payload = json.dumps(
            {"format": FORMAT_VERSION, "accounts": verified},
            ensure_ascii=True, separators=(",", ":"),
        ).encode("utf-8")
        if len(payload) > MAX_BLOB_BYTES - 4096:
            raise VaultError("Encrypted account vault is too large.")
        encrypted = _dpapi(payload, decrypt=False)
        if len(encrypted) > MAX_BLOB_BYTES:
            raise VaultError("Encrypted account vault is too large.")

        self._ensure_safe_path(reading=False)
        folder = self.path.parent
        temp_path = None
        try:
            folder.mkdir(parents=True, exist_ok=True)
            self._ensure_safe_path(reading=False)
            fd, temp_name = tempfile.mkstemp(prefix=".vault-", suffix=".tmp", dir=str(folder))
            temp_path = Path(temp_name)
            try:
                with os.fdopen(fd, "wb") as out:
                    out.write(encrypted)
                    out.flush()
                    os.fsync(out.fileno())
            except BaseException:
                # os.fdopen owns fd after it succeeds; closing twice is safe only
                # when no file object was created, so leave cleanup to context.
                raise
            self._ensure_safe_path(reading=False)
            os.replace(temp_path, self.path)
            temp_path = None
        except OSError as exc:
            raise VaultError("Could not securely save the encrypted account vault.") from exc
        finally:
            if temp_path is not None:
                try:
                    temp_path.unlink(missing_ok=True)
                except OSError:
                    pass
