'use strict';

const OTPAuth = require('otpauth');

class KronOTP {
  static #createTOTP(secret) {
    if (typeof secret !== 'string') {
      throw new TypeError('TOTP secret must be a Base32 string.');
    }

    // Authenticator setup keys may contain spaces, mixed case, or Base32 padding.
    const cleaned = secret.replace(/\s+/g, '').toUpperCase();
    const unpadded = cleaned.replace(/=+$/, '');
    const padding = cleaned.length - unpadded.length;
    const remainder = unpadded.length % 8;

    const validBase32 =
      /^[A-Z2-7]+$/.test(unpadded) &&
      [0, 2, 4, 5, 7].includes(remainder) &&
      (padding === 0 || (remainder !== 0 && padding === 8 - remainder));

    if (!validBase32) {
      throw new TypeError('Invalid TOTP secret: expected a valid Base32 string.');
    }

    try {
      const decoded = OTPAuth.Secret.fromBase32(unpadded);

      // Reject malformed encodings instead of silently accepting altered keys.
      if (decoded.bytes.length === 0 || decoded.base32 !== unpadded) {
        throw new Error('Non-canonical Base32 input.');
      }

      return new OTPAuth.TOTP({
        algorithm: 'SHA1',
        digits: 6,
        period: 30,
        secret: decoded,
      });
    } catch {
      // Never include the secret or dependency error details in an exception.
      throw new TypeError('Invalid TOTP secret: expected a valid Base32 string.');
    }
  }

  static generate(secret) {
    return KronOTP.#createTOTP(secret).generate();
  }

  static verify(secret, token) {
    const totp = KronOTP.#createTOTP(secret);

    // Preserve leading zeros: OTP tokens must be six-character strings.
    if (typeof token !== 'string' || !/^\d{6}$/.test(token)) {
      return false;
    }

    // Allow one 30-second time step of clock drift on either side.
    return totp.validate({ token, window: 1 }) !== null;
  }
}

module.exports = KronOTP;
module.exports.KronOTP = KronOTP;
