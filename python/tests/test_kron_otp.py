"""Focused Python KronOTP tests, including Phase P01 input-contract regressions.

Run from python/: python -m unittest discover -s tests -v
"""

import json
from pathlib import Path
from unittest import mock
import unittest

from src.kron_otp import KronOTP

_VECTORS = json.loads(
    Path(__file__).with_name("totp_vectors.json").read_text(encoding="utf-8")
)


class KronOTPTests(unittest.TestCase):
    SECRET = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"  # Public 160-bit key.
    MIN14 = "IFAUCQKBIFAUCQKBIFAUCQI"  # Synthetic 14-byte key.
    BELOW13 = "IFAUCQKBIFAUCQKBIFAUC"  # Synthetic 13-byte key.

    def test_generate_and_verify(self) -> None:
        token = KronOTP.generate(self.SECRET)
        self.assertRegex(token, r"^[0-9]{6}$")
        self.assertTrue(KronOTP.verify(self.SECRET, token))

    def test_secret_normalization(self) -> None:
        token = KronOTP.generate(self.SECRET)
        self.assertTrue(
            KronOTP.verify("gezd gnbv gy3t qojq gezd gnbv gy3t qojq", token)
        )
        self.assertTrue(
            KronOTP.verify("gezd\tgnbv\ngy3t qojq gezd gnbv gy3t qojq", token)
        )

    def test_invalid_tokens(self) -> None:
        for token in ("", "12345", "1234567", "abcdef", 123456, None, "１２３４５６"):
            with self.subTest(token=token):
                self.assertFalse(KronOTP.verify(self.SECRET, token))
        self.assertFalse(KronOTP.verify("not-base32!", "123456"))

    def test_invalid_secrets(self) -> None:
        for secret in (
            "", "   ", "not-base32!", "A", "AB", None,
            "IE", "JBSWY3DPEHPK3PXP", self.BELOW13,
            "ABCDEFGH=", self.MIN14 + "==", self.MIN14[:-1] + "J",
            "\ufeff" + self.SECRET, "\u00a0" + self.SECRET,
            "\u0131" + self.SECRET, 123, {},
        ):
            with self.subTest(secret=secret):
                with self.assertRaises(ValueError):
                    KronOTP.generate(secret)
                self.assertFalse(KronOTP.verify(secret, "123456"))

    def test_minimum_and_padding(self) -> None:
        token = KronOTP.generate(self.MIN14)
        self.assertRegex(token, r"^[0-9]{6}$")
        self.assertTrue(KronOTP.verify(self.MIN14 + "=", token))

    def test_input_size_boundaries(self) -> None:
        token = KronOTP.generate(self.SECRET)
        at_raw_limit = self.SECRET + " " * (4096 - len(self.SECRET))
        self.assertTrue(KronOTP.verify(at_raw_limit, token))
        with self.assertRaises(ValueError):
            KronOTP.generate(at_raw_limit + " ")
        self.assertFalse(KronOTP.verify(at_raw_limit + " ", token))

        at_clean_limit = self.SECRET * 32
        self.assertRegex(KronOTP.generate(at_clean_limit), r"^[0-9]{6}$")
        with self.assertRaises(ValueError):
            KronOTP.generate(at_clean_limit + "AA")
        self.assertFalse(KronOTP.verify(at_clean_limit + "AA", token))


    @staticmethod
    def _at(timestamp: int, secret: str) -> str:
        with mock.patch("pyotp.totp.time.time", return_value=timestamp):
            return KronOTP.generate(secret)

    @staticmethod
    def _verify_at(timestamp: int, secret: str, token: str) -> bool:
        with mock.patch("pyotp.totp.time.time", return_value=timestamp):
            return KronOTP.verify(secret, token)

    def test_rfc6238_sha1_six_digit_fixed_vectors(self) -> None:
        cases = _VECTORS["rfc6238_sha1_6digits"]
        self.assertEqual(len(cases), 6)
        self.assertTrue(any(v["otp"].startswith("0") for v in cases))
        for case in cases:
            with self.subTest(timestamp=case["timestamp"]):
                t, expected = case["timestamp"], case["otp"]
                self.assertEqual(self._at(t, self.SECRET), expected)
                self.assertTrue(self._verify_at(t, self.SECRET, expected))

    def test_deterministic_cross_language_reference_vectors(self) -> None:
        cases = _VECTORS["cross_language"]
        self.assertEqual(len(cases), 80)
        for case in cases:
            t, key, expected = case["timestamp"], case["secret"], case["otp"]
            with self.subTest(case=case["case"], timestamp=t):
                self.assertEqual(self._at(t, key), expected)
                self.assertTrue(self._verify_at(t, key, expected))

    def test_epoch_and_drift_boundaries(self) -> None:
        current = self._at(29, self.SECRET)
        next_token = self._at(30, self.SECRET)
        plus_two = self._at(60, self.SECRET)
        self.assertEqual(self._at(0, self.SECRET), current)
        for t in (0, 1, 29):
            with self.subTest(timestamp=t):
                self.assertTrue(self._verify_at(t, self.SECRET, current))
                self.assertTrue(self._verify_at(t, self.SECRET, next_token))
                self.assertFalse(self._verify_at(t, self.SECRET, plus_two))
        for t in (30, 59):
            with self.subTest(timestamp=t):
                self.assertTrue(self._verify_at(t, self.SECRET, current))
                self.assertTrue(self._verify_at(t, self.SECRET, next_token))
                self.assertTrue(self._verify_at(t, self.SECRET, plus_two))

        plus_three = self._at(90, self.SECRET)
        plus_four = self._at(120, self.SECRET)
        for t in (60, 61):
            with self.subTest(timestamp=t):
                self.assertTrue(self._verify_at(t, self.SECRET, next_token))
                self.assertTrue(self._verify_at(t, self.SECRET, plus_two))
                self.assertTrue(self._verify_at(t, self.SECRET, plus_three))
                self.assertFalse(self._verify_at(t, self.SECRET, current))
                self.assertFalse(self._verify_at(t, self.SECRET, plus_four))

        self.assertFalse(self._verify_at(-1, self.SECRET, current))
        self.assertTrue(self._verify_at(29, self.SECRET, current))
        self.assertTrue(self._verify_at(29, self.SECRET, current))


if __name__ == "__main__":
    unittest.main()
