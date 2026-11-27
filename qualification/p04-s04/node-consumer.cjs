'use strict';
// Synthetic, single-process caller fixture only. Not a production auth SDK.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {createHash} = require('node:crypto');
const {Worker, isMainThread, parentPort, workerData} = require('node:worker_threads');
const KronOTP = require('kron-otp');
const A = 'GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ'; // public RFC test key
const B = 'JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP'; // synthetic only
const RETENTION = 120, WINDOW = 60;
function at(t, fn) {
  const old = Date.now;
  Date.now = () => t * 1000;
  try { return fn(); } finally { Date.now = old; }
}
const code = (key,t) => at(t, () => KronOTP.generate(key));
const match = (key,token,t) => at(t, () => KronOTP.verify(key,token));
class Caller {
  constructor(limit=3) {
    this.limit=limit; this.last=-1;
    this.accounts=new Map([['a',A],['b',B]]);
    this.attempts=new Map(); this.used=new Map(); this.checks=0;
  }
  // Synchronous, no await: the owning event loop serializes the full transaction.
  // All timestamps are trusted synthetic server-side inputs, not client values.
  submit(id,token,t) {
    if (!Number.isSafeInteger(t) || t<0 || t<this.last) return false;
    this.last=t;
    if (!this.accounts.has(id)) return false;
    const attempts=(this.attempts.get(id)||[]).filter(x=>t-x<WINDOW);
    this.attempts.set(id,attempts);
    if (attempts.length>=this.limit) return false;
    attempts.push(t);
    this.checks++;
    if (!match(this.accounts.get(id),token,t)) return false;
    let used=this.used.get(id);
    if (!used) this.used.set(id,used=new Map());
    for (const [key,expiry] of used) if (expiry<=t) used.delete(key);
    // Boolean verify does not reveal matched counter. Conservatively reserve
    // token fingerprint for 120s after acceptance (90s window + 30s margin).
    // A repeated numeric code can be denied even if it comes from a new counter.
    const fingerprint=createHash('sha256').update(token).digest('hex');
    if (used.has(fingerprint)) return false;
    used.set(fingerprint,t+RETENTION);
    return true;
  }
}
async function concurrent(caller, token, t) {
  const gate=new Int32Array(new SharedArrayBuffer(4));
  const workers=[];
  try {
    const ready=[],results=[];
    for(let i=0;i<8;i++){
      const w=new Worker(__filename,{workerData:{gate:gate.buffer}});
      workers.push(w);
      let mark, fail, done, reject;
      ready.push(new Promise((a,b)=>{mark=a;fail=b;}));
      results.push(new Promise((a,b)=>{done=a;reject=b;}));
      // Avoid an unhandled rejection before the ready barrier resolves.
      results[i].catch(()=>{});
      let requested=false;
      w.on('message',m=>{
        if(m==='ready') mark();
        else if(m==='request'&&!requested){requested=true;done(caller.submit('a',token,t));}
        else {const err=new Error('Unexpected worker message');fail(err);reject(err);}
      });
      w.on('error',e=>{fail(e);reject(e);});
      w.on('exit',n=>{if(!requested){const e=new Error('Worker exited before request: '+n);fail(e);reject(e);}});
    }
    await Promise.all(ready);
    Atomics.store(gate,0,1); Atomics.notify(gate,0,8);
    return await Promise.all(results);
  } finally { await Promise.all(workers.map(w=>w.terminate())); }
}
async function main(){
  const origin=fs.realpathSync(require.resolve('kron-otp'));
  const root=fs.realpathSync(path.join(__dirname,'node_modules','kron-otp'));
  assert(origin.startsWith(root+path.sep),'package origin');
  const pkg=require(path.join(root,'package.json'));
  assert(pkg.version==='2.0.0'&&KronOTP===KronOTP.KronOTP,'public package identity');
  const lock=require('./package-lock.json').packages['node_modules/kron-otp'];
  assert(lock.version==='2.0.0'&&lock.integrity,'package lock evidence');
  console.log(JSON.stringify({version:pkg.version,origin,integrity:lock.integrity,node:process.version}));
  let count=0;
  function pass(name){count++;console.log('PASS '+name);}
  const current=code(A,59), next=code(A,89), other=code(B,59);
  assert(current==='287082','RFC reference mismatch');
  assert(next!==current&&other!==current,'fixture collision');
  assert(match(A,current,59)); pass('current_rfc');
  assert(match(A,next,59)&&match(A,next,119)); pass('adjacent_window');
  assert(!match(A,next,120)); pass('expired');
  for(const bad of [null,123456,'12345','１２３４５６','abcdef']) assert(!match(A,bad,59));
  pass('malformed');
  assert(!match(B,current,59)); pass('wrong_account');
  assert(match(A,current,59)&&match(A,current,59)); pass('stateless_repeat');
  let c=new Caller(16);
  assert(c.submit('a',next,59));assert(!c.submit('a',next,60));assert(!c.submit('a',next,89));assert(!c.submit('a',next,119));
  assert(!c.submit('a',next,120));assert(c.submit('a',code(A,180),180));
  pass('replay_rollover_recovery');
  c=new Caller();assert(c.submit('a',current,59));assert(!c.submit('b',current,59));
  assert(c.submit('b',other,59));assert(!c.submit('unknown',current,59));pass('account_isolation');
  c=new Caller();
  for(let i=0;i<3;i++) assert(!c.submit('a','invalid',59));
  assert(!c.submit('a',current,59));assert(c.checks===3);
  assert(c.submit('b',other,59));assert(c.submit('a',code(A,119),119));pass('throttle_reset_isolation');
  c=new Caller();assert(c.submit('a',current,59));assert(!c.submit('a',current,58));pass('clock_rollback_denied');
  c=new Caller(16);
  let results=await concurrent(c,current,59);
  assert(results.filter(Boolean).length===1&&c.checks===8);pass('concurrent_duplicate_single_winner');
  c=new Caller(3);
  results=await concurrent(c,'invalid',59);
  assert(results.every(x=>x===false)&&c.checks===3);assert(!c.submit('a',current,59));
  pass('concurrent_attempt_budget');
  assert(count===12);console.log('P04_S04_NODE_PASS cases='+count);
}
if(!isMainThread){
  parentPort.postMessage('ready');
  const gate=new Int32Array(workerData.gate);
  if(Atomics.wait(gate,0,0,15000)==='timed-out') throw new Error('Barrier timeout');
  parentPort.postMessage('request');
}else{
  const timeout=setTimeout(()=>{console.error('Fixture timeout');process.exit(1);},30000);
  main().then(()=>clearTimeout(timeout),e=>{clearTimeout(timeout);console.error(e);process.exitCode=1;});
}
