'use strict';
// Bounded local synthetic benchmark; no authentication server or SLA.
const assert=require('node:assert/strict'), fs=require('node:fs'), os=require('node:os'), path=require('node:path');
const {spawn,spawnSync}=require('node:child_process');
const clock=process.hrtime.bigint;
const ms=(a,b)=>Number(b-a)/1e6;
const KEY='GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ', EXPECTED='287082';
const KronOTP=require('kron-otp');
const origin=fs.realpathSync(require.resolve('kron-otp'));
const pkgroot=fs.realpathSync(path.join(__dirname,'node_modules/kron-otp'));
assert(origin.startsWith(pkgroot+path.sep));
assert.equal(require(path.join(pkgroot,'package.json')).version,'2.0.0');
function fixed(fn){const old=Date.now;Date.now=()=>59000;try{return fn();}finally{Date.now=old;}}
function generate(){const t=clock();const value=fixed(()=>KronOTP.generate(KEY));const dt=ms(t,clock());assert(value===EXPECTED,'generate mismatch');return dt;}
function verify(){const t=clock();const ok=fixed(()=>KronOTP.verify(KEY,EXPECTED));const dt=ms(t,clock());assert(ok===true,'verify mismatch');return dt;}
function pair(){generate();verify();}
function stats(values){assert(values.length>0);assert(values.every(x=>Number.isFinite(x)&&x>=0));const v=values.slice().sort((a,b)=>a-b);const q=p=>v[Math.ceil(p*v.length)-1];return {n:v.length,p50_ms:q(.5),p95_ms:q(.95),p99_ms:q(.99)};}
function mem(){return {rss_bytes:process.memoryUsage.rss(),peak_rss_bytes:process.resourceUsage().maxRSS*1024};}
function cpu(start){const c=process.cpuUsage(start);return (c.user+c.system)/1e6;}
function measured(n){const start=clock(),c=process.cpuUsage(),g=[],v=[];for(let i=0;i<n;i++){g.push(generate());v.push(verify());}const sec=ms(start,clock())/1000;return {pairs:n,operations:2*n,seconds:sec,ops_per_sec:2*n/sec,generate:stats(g),verify:stats(v),cpu_seconds:cpu(c),...mem(),errors:0,mismatches:0};}
function emit(kind,data){console.log(JSON.stringify({kind,...data}));}
function child(){
  return new Promise((resolve,reject)=>{
    const p=spawn(process.execPath,[__filename,'worker'],{stdio:['ignore','pipe','pipe']});
    let out='',err='';
    p.stdout.on('data',x=>out+=x);p.stderr.on('data',x=>err+=x);
    p.on('error',reject);p.on('close',code=>{try{assert.equal(code,0,'worker failed: '+err);resolve(JSON.parse(out));}catch(e){reject(e);}});
  });
}
const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function sustained(){
  const start=clock(), end=start+600000000000n, c=process.cpuUsage();
  const baseline=mem(), samples=[{elapsed_s:0,...baseline}];
  let nextSample=start+10000000000n, last=null, n=0, minGap=Infinity;
  const g=[],v=[];
  while(clock()<end){
    const now=clock();
    if(now>=nextSample){
      const sample={elapsed_s:ms(start,now)/1000,...mem()};samples.push(sample);emit('rss_sample',sample);
      nextSample+=10000000000n;
    }
    if(last!==null&&now-last<5000000n){await sleep(Math.max(1,Math.ceil(Number(5000000n-(now-last))/1e6)));continue;}
    const begin=clock();if(begin>=end)break;
    if(last!==null)minGap=Math.min(minGap,ms(last,begin));
    last=begin;const a=generate(),b=verify();n++;
    if(n%20===0){g.push(a);v.push(b);}
  }
  const elapsed=ms(start,clock())/1000;const final=mem();
  samples.push({elapsed_s:elapsed,...final});
  assert(elapsed>=600&&n>0&&n<=120000&&minGap>=5,'sustained workload');
  assert(samples.length>=61&&samples.slice(1).every((s,i)=>s.elapsed_s-samples[i].elapsed_s<=12),'RSS sampling gap');
  emit('sustained',{seconds:elapsed,pairs:n,operations:n*2,pairs_per_sec:n/elapsed,min_start_gap_ms:minGap,sample_interval_s:10,samples:samples.length,baseline_rss_bytes:baseline.rss_bytes,final_rss_bytes:final.rss_bytes,rss_delta_bytes:final.rss_bytes-baseline.rss_bytes,...final,cpu_seconds:cpu(c),generate_sample:stats(g),verify_sample:stats(v),errors:0,mismatches:0});
}
async function main(){
  emit('environment',{runtime:process.version,platform:process.platform,arch:process.arch,os_release:os.release(),cpu:os.cpus()[0].model,logical_cpus:os.cpus().length,total_memory_bytes:os.totalmem(),image:process.env.ImageVersion,version:'2.0.0',origin});
  const cold=[];
  for(let i=0;i<20;i++){const t=clock();const p=spawnSync(process.execPath,[__filename,'cold'],{encoding:'utf8',timeout:15000});assert(p.status===0&&!p.error&&p.stdout.trim()==='OK','cold process failure');cold.push(ms(t,clock()));}
  emit('cold',stats(cold));
  for(let i=0;i<500;i++)pair();
  emit('warmup',{operations:1000});
  emit('serial',measured(10000));
  for(const workers of [1,4,8]){
    const start=clock(),results=await Promise.all(Array.from({length:workers},child));
    const sec=ms(start,clock())/1000;
    assert(results.every(x=>x.operations===2000&&x.errors===0&&x.mismatches===0));
    emit('parallel',{workers,operations:workers*2000,seconds:sec,ops_per_sec:workers*2000/sec,worker_cpu_seconds:results.reduce((s,x)=>s+x.cpu_seconds,0),max_worker_peak_rss_bytes:Math.max(...results.map(x=>x.peak_rss_bytes)),worker_results:results,errors:0,mismatches:0});
  }
  await sustained();emit('complete',{status:'PASS',errors:0,mismatches:0});
}
if(process.argv[2]==='cold'){pair();console.log('OK');}
else if(process.argv[2]==='worker'){console.log(JSON.stringify(measured(1000)));}
else main().catch(e=>{console.error(e);process.exitCode=1;});
