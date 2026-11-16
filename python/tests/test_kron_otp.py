"""Focused Python KronOTP tests, including Phase P01 input-contract regressions.

Run from python/: python -m unittest discover -s tests -v
"""

import unittest

from src.kron_otp import KronOTP


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


if __name__ == "__main__":
    unittest.main()
