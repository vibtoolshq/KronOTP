'use strict';

const OTPAuth = require('otpauth');

// Bound attacker-controlled input before normalization/decoding.
// 14 bytes matches PyOTP >=2.12; use random 20+ byte keys when provisioning.
const MIN_SECRET_BYTES = 14;
const MAX_RAW_SECRET_LENGTH = 4096;
const MAX_BASE32_LENGTH = 1024;
const INVALID_SECRET = 'Invalid TOTP secret: expected valid Base32 of an accepted size.';

class KronOTP {
  static #createTOTP(secret) {
    if (typeof secret !== 'string') {
      throw new TypeError('TOTP secret must be a Base32 string.');
    }
    if (secret.length > MAX_RAW_SECRET_LENGTH) {
      throw new TypeError(INVALID_SECRET);
    }

    // Only ASCII whitespace is ignored, identically in Python and Node.
    // Check ASCII characters BEFORE uppercasing to avoid Unicode case folding.
    const compact = secret.replace(/[ \t\n\r\f\v]+/g, '');
    if (compact.length > MAX_BASE32_LENGTH || !/^[A-Za-z2-7=]+$/.test(compact)) {
      throw new TypeError(INVALID_SECRET);
    }

    const cleaned = compact.toUpperCase();
    const unpadded = cleaned.replace(/=+$/, '');
    const padding = cleaned.length - unpadded.length;
    const remainder = unpadded.length % 8;

    const validBase32 =
      /^[A-Z2-7]+$/.test(unpadded) &&
      [0, 2, 4, 5, 7].includes(remainder) &&
      (padding === 0 || (remainder !== 0 && padding === 8 - remainder));

    if (!validBase32) {
      throw new TypeError(INVALID_SECRET);
    }

    try {
      const decoded = OTPAuth.Secret.fromBase32(unpadded);

      // Enforce PyOTP's minimum and reject non-canonical unused padding bits.
      if (decoded.bytes.length < MIN_SECRET_BYTES || decoded.base32 !== unpadded) {
        throw new TypeError(INVALID_SECRET);
      }

      return new OTPAuth.TOTP({
        algorithm: 'SHA1',
        digits: 6,
        period: 30,
        secret: decoded,
      });
    } catch {
      // Never include secret values or dependency internals in public errors.
      throw new TypeError(INVALID_SECRET);
    }
  }

  static generate(secret) {
    return KronOTP.#createTOTP(secret).generate();
  }

  static verify(secret, token) {
    // Invalid OTPs or expected invalid secrets are nonmatches in both runtimes.
    if (typeof token !== 'string' || !/^[0-9]{6}$/.test(token)) {
      return false;
    }

    let totp;
    try {
      totp = KronOTP.#createTOTP(secret);
    } catch (error) {
      if (error instanceof TypeError) return false;
      throw error;
    }

    // Preserve existing SHA-1, 6 digits, 30-second window and stateless design.
    return totp.validate({ token, window: 1 }) !== null;
  }
}

module.exports = KronOTP;
module.exports.KronOTP = KronOTP;
