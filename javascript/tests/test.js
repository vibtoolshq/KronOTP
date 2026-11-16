'use strict';

const assert = require('node:assert/strict');
const KronOTP = require('../src/kron-otp');

const secret = 'JBSWY3DPEHPK3PXP'; // Demonstration secret only.

try {
  const token = KronOTP.generate(secret);
  console.log('Generated TOTP:', token);

  assert.match(token, /^\d{6}$/, 'TOTP must contain exactly six digits.');
  assert.equal(KronOTP.verify(secret, token), true, 'Generated token must verify.');
  assert.equal(
    KronOTP.verify('jbsw y3dp ehpk 3pxp', token),
    true,
    'Whitespace and lowercase Base32 secrets must be accepted.',
  );

  assert.equal(KronOTP.verify(secret, 'invalid'), false);
  assert.equal(KronOTP.verify(secret, token.slice(0, 5)), false);
  assert.equal(KronOTP.verify(secret, 123456), false);
  assert.throws(() => KronOTP.generate('not-a-base32-secret!'), TypeError);
  assert.throws(() => KronOTP.verify(' ', token), TypeError);

  console.log('KronOTP JavaScript engine: all tests passed.');
} catch (error) {
  console.error('KronOTP JavaScript engine test failed:', error);
  process.exitCode = 1;
}
