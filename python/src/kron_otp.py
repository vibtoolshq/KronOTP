"""KronOTP: a minimal, stateless TOTP engine backed by PyOTP."""

from __future__ import annotations

import base64
import binascii
import hashlib
import re

import pyotp


class KronOTP:
    """Generate and verify standard six-digit, 30-second SHA-1 TOTP codes."""

    @staticmethod
    def _normalize_secret(secret: str) -> str:
        """Normalize Base32 input and reject invalid or non-canonical keys."""
        if not isinstance(secret, str):
            raise ValueError("TOTP secret must be a Base32 string.")

        # Ignore whitespace and case; retain no copy of the raw secret in errors.
        cleaned = "".join(secret.split()).upper()
        unpadded = cleaned.rstrip("=")
        padding_count = len(cleaned) - len(unpadded)
        remainder = len(unpadded) % 8
        required_padding = (-len(unpadded)) % 8

        if (
            not re.fullmatch(r"[A-Z2-7]+", unpadded)
            or remainder not in (0, 2, 4, 5, 7)
            or (padding_count and padding_count != required_padding)
        ):
            raise ValueError("Invalid TOTP secret: expected valid Base32.")

        try:
            decoded = base64.b32decode(unpadded + "=" * required_padding)
        except (binascii.Error, ValueError):
            raise ValueError("Invalid TOTP secret: expected valid Base32.") from None

        # Reject altered encodings (including nonzero unused padding bits).
        if not decoded or base64.b32encode(decoded).decode("ascii").rstrip("=") != unpadded:
            raise ValueError("Invalid TOTP secret: expected valid Base32.")

        return unpadded

    @staticmethod
    def _totp(secret: str) -> pyotp.TOTP:
        """Create the same TOTP configuration as the JavaScript module."""
        return pyotp.TOTP(
            KronOTP._normalize_secret(secret),
            digits=6,
            interval=30,
            digest=hashlib.sha1,
        )

    @staticmethod
    def generate(secret: str) -> str:
        """Return a six-digit code; raise ValueError for an invalid secret."""
        try:
            return KronOTP._totp(secret).now()
        except (TypeError, ValueError, binascii.Error):
            raise ValueError("Invalid TOTP secret: expected valid Base32.") from None

    @staticmethod
    def verify(secret: str, token: str) -> bool:
        """Verify a code with a one-step (±30-second) clock-drift window."""
        if not isinstance(token, str) or re.fullmatch(r"[0-9]{6}", token) is None:
            return False

        try:
            return bool(KronOTP._totp(secret).verify(token, valid_window=1))
        except (TypeError, ValueError, binascii.Error):
            return False
