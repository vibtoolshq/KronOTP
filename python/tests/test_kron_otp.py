"""Focused tests for the Python KronOTP engine.

Run from python/: python -m unittest discover -s tests -v
"""

import unittest

from src.kron_otp import KronOTP


class KronOTPTests(unittest.TestCase):
    # RFC 6238 SHA-1 reference key: 20 decoded bytes (160 bits).
    SECRET = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"

    def test_generate_and_verify(self) -> None:
        token = KronOTP.generate(self.SECRET)
        print(f"Generated TOTP: {token}")

        self.assertRegex(token, r"^[0-9]{6}$")
        self.assertTrue(KronOTP.verify(self.SECRET, token))

    def test_secret_normalization(self) -> None:
        token = KronOTP.generate(self.SECRET)
        self.assertTrue(
            KronOTP.verify("gezd gnbv gy3t qojq gezd gnbv gy3t qojq", token)
        )

    def test_invalid_tokens(self) -> None:
        for token in ("", "12345", "1234567", "abcdef", 123456, None):
            with self.subTest(token=token):
                self.assertFalse(KronOTP.verify(self.SECRET, token))

    def test_invalid_secrets(self) -> None:
        # The former 80-bit fixture is below PyOTP 2.12+'s 112-bit minimum.
        for secret in ("", "   ", "not-base32!", "A", "AB", None, "JBSWY3DPEHPK3PXP"):
            with self.subTest(secret=secret):
                with self.assertRaises(ValueError):
                    KronOTP.generate(secret)
                self.assertFalse(KronOTP.verify(secret, "123456"))


if __name__ == "__main__":
    unittest.main()
