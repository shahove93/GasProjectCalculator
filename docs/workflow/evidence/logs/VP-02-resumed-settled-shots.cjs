const {chromium}=require('C:/Users/user/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs');
const path=require('path');
const {pathToFileURL}=require('url');
const assert=require('assert/strict');
const ROOT=process.cwd(), SHOTS='docs/screenshots/visual-02-resumed-', LOG='docs/workflow/evidence/logs/VP-02-resumed-browser.json';
const out={cases:[],requests:[],responses:[],pageErrors:[],externalRequests:[],reducedMotion:{}};
const expected={gsn:68250,gsv:75600,combined:158550};
async function metrics(page) {return page.evaluate(()=>{
 const rect=el=>{const r=el.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height,bottom:r.bottom,visible:!!r.width&&!!r.height,viewport:r.top>=0&&r.bottom<=innerHeight}};
 const active=[...document.querySelectorAll('.result-body')].find(e=>getComputedStyle(e).display!=='none');
 return {inner:[innerWidth,innerHeight],scroll:[scrollX,scrollY],document:[document.documentElement.scrollWidth,document.documentElement.scrollHeight],dpr:devicePixelRatio,action:rect(document.querySelector('#submit-btn')),totals:[...document.querySelectorAll('.total-block')].filter(e=>e.getBoundingClientRect().height).map(rect),art:[...document.querySelectorAll('.pipe-art,.pipe-footer svg')].map(rect)};
});}
async function setup(page,mode) {
 await page.locator(`[data-mode="${mode}"]`).click();
 await page.evaluate(mode=>{
  const q=id=>document.getElementById(id),set=(id,v)=>q(id).value=v;
  set('customer_type','частное лицо');set('length',10);set('angles',0);set('excavator_hours',0);
  ['hdd','hydraulic_hammer','has_grpsh'].forEach(id=>q(id).checked=false);
  [4,0,4].forEach((v,i)=>set(['gsv-length-up-to-25','gsv-length-32-40','gsv-length-57'][i],v));
  set('gsv-holes',0);set('gsv-sakz',0);q('gsv-sakz').dispatchEvent(new Event('input'));
  q('is_district').checked=mode==='combined';
 },mode);
}
async function submit(page,mode,total) {
 const response=page.waitForResponse(r=>r.url().includes('/calculate')&&r.request().method()==='POST');
 await page.locator('#submit-btn').click(); const r=await response;assert.equal(r.status(),200);
 await page.waitForFunction(()=>!document.getElementById('submit-btn').disabled);
 const id={gsn:'total',gsv:'gsv-total',combined:'combined-total'}[mode];
 const text=await page.locator('#'+id).innerText();assert.equal(Number(text.replace(/\D/g,'')),total);
 return {total:text,response:await r.json()};
}
(async()=>{
 const port=JSON.parse(fs.readFileSync('C:/Users/user/AppData/Local/Temp/opencode/vp-02-resume/settled-port.json','utf8')).port;
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const page=await browser.newPage({viewport:{width:800,height:540},deviceScaleFactor:1});
 await page.goto('http://127.0.0.1:'+port);
 await setup(page,'gsv');
 const result=[];
 for(const [label,values,total] of [['D1',[4,0,4],75600],['D2',[2,4,3],79275],['D3',[0,5,2],71400],['D4',[3,1,1],63000],['D5',[8,0,0],70875]]) {
  await page.evaluate(values=>values.forEach((v,i)=>document.getElementById(['gsv-length-up-to-25','gsv-length-32-40','gsv-length-57'][i]).value=v),values);
  const value=await submit(page,'gsv',total);
  await page.evaluate(()=>Promise.all(document.getAnimations().map(a=>a.finished)));
  const opacity=await page.locator('#result-gsv .total-block').evaluate(e=>getComputedStyle(e).opacity);
  assert.equal(opacity,'1');
  const file=SHOTS+`desktop-gsv-${label}-settled.png`;
  await page.screenshot({path:file});result.push({label,values,expected:total,...value,opacity,file,metrics:await metrics(page)});
 }
 fs.writeFileSync('docs/workflow/evidence/logs/VP-02-resumed-settled-shots.json',JSON.stringify(result,null,2));
 await browser.close();console.log('5 stable screenshots; animation finished, opacity=1; original screenshots preserved');
})().catch(e=>{console.error(e);process.exitCode=1});
