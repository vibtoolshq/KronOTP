'use strict';

const assert = require('node:assert/strict');
const KronOTP = require('../src/kron-otp');

const secret = 'GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ'; // Public 160-bit RFC key.
const min14 = 'IFAUCQKBIFAUCQKBIFAUCQI'; // 14-byte synthetic key, not a credential.
const below13 = 'IFAUCQKBIFAUCQKBIFAUC'; // 13 bytes.

try {
  const token = KronOTP.generate(secret);
  assert.match(token, /^[0-9]{6}$/, 'TOTP must contain exactly six digits.');
  assert.equal(KronOTP.verify(secret, token), true);
  assert.equal(
    KronOTP.verify('gezd gnbv gy3t qojq gezd gnbv gy3t qojq', token),
    true,
    'ASCII spaces and lowercase must normalize identically.',
  );
  assert.equal(KronOTP.verify('gezd\tgnbv\ngy3t qojq gezd gnbv gy3t qojq', token), true);

  assert.equal(KronOTP.verify(secret, 'invalid'), false);
  assert.equal(KronOTP.verify(secret, token.slice(0, 5)), false);
  assert.equal(KronOTP.verify(secret, 123456), false);
  assert.equal(KronOTP.verify(' ', token), false); // Former JS TypeError contract.
  assert.equal(KronOTP.verify('not-a-base32-secret!', '123456'), false);

  for (const weak of ['IE', 'JBSWY3DPEHPK3PXP', below13]) {
    assert.throws(() => KronOTP.generate(weak), TypeError);
    assert.equal(KronOTP.verify(weak, '123456'), false);
  }

  // 14 bytes remains supported (PyOTP 2.12+ policy); a 20-byte key is preferred.
  const minToken = KronOTP.generate(min14);
  assert.match(minToken, /^[0-9]{6}$/);
  assert.equal(KronOTP.verify(min14 + '=', minToken), true);

  // Canonical padding and Unicode case/space normalization must be strict.
  for (const invalid of [
    'not-a-base32-secret!', '', 'ABCDEFGH=', min14 + '==',
    min14.slice(0, -1) + 'J', // Noncanonical unused pad bits.
    '\uFEFF' + secret, '\u00A0' + secret, '\u0131' + secret,
  ]) {
    assert.throws(() => KronOTP.generate(invalid), TypeError);
    assert.equal(KronOTP.verify(invalid, '123456'), false);
  }
  for (const invalid of [null, undefined, 123, {}, []]) {
    assert.throws(() => KronOTP.generate(invalid), TypeError);
    assert.equal(KronOTP.verify(invalid, '123456'), false);
  }

  const atRawLimit = secret + ' '.repeat(4096 - secret.length);
  assert.equal(KronOTP.verify(atRawLimit, token), true);
  assert.throws(() => KronOTP.generate(atRawLimit + ' '), TypeError);
  assert.equal(KronOTP.verify(atRawLimit + ' ', token), false);

  const atCleanLimit = secret.repeat(32); // 1024 canonical Base32 chars.
  assert.match(KronOTP.generate(atCleanLimit), /^[0-9]{6}$/);
  assert.throws(() => KronOTP.generate(atCleanLimit + 'AA'), TypeError);
  assert.equal(KronOTP.verify(atCleanLimit + 'AA', token), false);

  console.log('KronOTP JavaScript P01 engine tests: PASS.');
} catch (error) {
  console.error('KronOTP JavaScript P01 test failed:', error);
  process.exitCode = 1;
}
