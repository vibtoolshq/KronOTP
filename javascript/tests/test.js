'use strict';

const assert = require('node:assert/strict');
const KronOTP = require('../src/kron-otp');
const vectors = require('../../python/tests/totp_vectors.json');

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


  // Deterministic time is isolated to each call; production code is unchanged.
  const originalNow = Date.now;
  function withTime(timestamp, fn) {
    Date.now = () => timestamp * 1000;
    try {
      return fn();
    } finally {
      Date.now = originalNow;
    }
  }
  const generateAt = (timestamp, key) =>
    withTime(timestamp, () => KronOTP.generate(key));
  const verifyAt = (timestamp, key, otp) =>
    withTime(timestamp, () => KronOTP.verify(key, otp));

  const rfc = vectors.rfc6238_sha1_6digits;
  assert.equal(rfc.length, 6);
  assert(rfc.some((v) => v.otp.startsWith('0')));
  for (const v of rfc) {
    assert.equal(generateAt(v.timestamp, secret), v.otp, 'RFC time=' + v.timestamp);
    assert.equal(verifyAt(v.timestamp, secret, v.otp), true);
  }

  const cross = vectors.cross_language;
  assert.equal(cross.length, 80);
  for (const v of cross) {
    assert.equal(generateAt(v.timestamp, v.secret), v.otp);
    assert.equal(verifyAt(v.timestamp, v.secret, v.otp), true);
  }

  const current = generateAt(29, secret);
  const next = generateAt(30, secret);
  const plusTwo = generateAt(60, secret);
  assert.equal(generateAt(0, secret), current);
  for (const timestamp of [0, 1, 29]) {
    assert.equal(verifyAt(timestamp, secret, current), true);
    assert.equal(verifyAt(timestamp, secret, next), true);
    assert.equal(verifyAt(timestamp, secret, plusTwo), false);
  }
  for (const timestamp of [30, 59]) {
    assert.equal(verifyAt(timestamp, secret, current), true);
    assert.equal(verifyAt(timestamp, secret, next), true);
    assert.equal(verifyAt(timestamp, secret, plusTwo), true);
  }
  const plusThree = generateAt(90, secret);
  const plusFour = generateAt(120, secret);
  for (const timestamp of [60, 61]) {
    assert.equal(verifyAt(timestamp, secret, next), true);
    assert.equal(verifyAt(timestamp, secret, plusTwo), true);
    assert.equal(verifyAt(timestamp, secret, plusThree), true);
    assert.equal(verifyAt(timestamp, secret, current), false);
    assert.equal(verifyAt(timestamp, secret, plusFour), false);
  }
  assert.equal(verifyAt(29, secret, current), true); // Stateless by design.

  console.log('KronOTP JavaScript P01+P02 tests: PASS (6 RFC, 80 parity vectors).');
} catch (error) {
  console.error('KronOTP JavaScript P01 test failed:', error);
  process.exitCode = 1;
}
