"""KronOTP: a minimal, stateless TOTP engine backed by PyOTP."""

from __future__ import annotations

import base64
import binascii
import hashlib
import re
import time

import pyotp

# Match the Node runtime's bounded, ASCII-only Base32 acceptance contract.
_MIN_SECRET_BYTES = 14
_MAX_RAW_SECRET_LENGTH = 4096
_MAX_BASE32_LENGTH = 1024
_INVALID_SECRET = "Invalid TOTP secret: expected valid Base32 of an accepted size."


class KronOTP:
    """Generate and verify standard six-digit, 30-second SHA-1 TOTP codes."""

    @staticmethod
    def _normalize_secret(secret: str) -> str:
        """Normalize ASCII Base32 input and reject invalid, weak, or oversized keys."""
        if not isinstance(secret, str):
            raise ValueError("TOTP secret must be a Base32 string.")
        if len(secret) > _MAX_RAW_SECRET_LENGTH:
            raise ValueError(_INVALID_SECRET)

        # Only ASCII whitespace is ignored; reject non-ASCII before uppercasing.
        compact = re.sub(r"[ \t\n\r\f\v]+", "", secret)
        if (
            len(compact) > _MAX_BASE32_LENGTH
            or re.fullmatch(r"[A-Za-z2-7=]+", compact) is None
        ):
            raise ValueError(_INVALID_SECRET)

        cleaned = compact.upper()
        unpadded = cleaned.rstrip("=")
        padding_count = len(cleaned) - len(unpadded)
        remainder = len(unpadded) % 8
        required_padding = (-len(unpadded)) % 8

        if (
            re.fullmatch(r"[A-Z2-7]+", unpadded) is None
            or remainder not in (0, 2, 4, 5, 7)
            or (padding_count and padding_count != required_padding)
        ):
            raise ValueError(_INVALID_SECRET)

        try:
            decoded = base64.b32decode(unpadded + "=" * required_padding)
        except (binascii.Error, ValueError):
            raise ValueError(_INVALID_SECRET) from None

        # PyOTP 2.12+ requires >=14 decoded bytes; enforce it at wrapper boundary.
        if (
            len(decoded) < _MIN_SECRET_BYTES
            or base64.b32encode(decoded).decode("ascii").rstrip("=") != unpadded
        ):
            raise ValueError(_INVALID_SECRET)

        return unpadded

    @staticmethod
    def _totp(secret: str) -> pyotp.TOTP:
        """Create the same fixed configuration as the JavaScript module."""
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
            raise ValueError(_INVALID_SECRET) from None

    @staticmethod
    def verify(secret: str, token: str) -> bool:
        """Verify with a one-step (±30-second) drift window; invalid input is False."""
        if not isinstance(token, str) or re.fullmatch(r"[0-9]{6}", token) is None:
            return False

        try:
            totp = KronOTP._totp(secret)
            now = time.time()

            # Unix counter zero has no -1 predecessor. In PyOTP's +/-1
            # loop a negative counter otherwise raises before checking 0.
            if 0 <= now < totp.interval:
                return bool(
                    totp.verify(token, for_time=now, valid_window=0)
                    or totp.verify(
                        token, for_time=now + totp.interval, valid_window=0
                    )
                )

            # The regular +/-1 window and existing API remain unchanged.
            return bool(totp.verify(token, for_time=now, valid_window=1))
        except (TypeError, ValueError, binascii.Error):
            return False
