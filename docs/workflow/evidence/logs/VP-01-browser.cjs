const {chromium}=require('C:/Users/user/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs');
const path=require('path');
const {pathToFileURL}=require('url');
const assert=require('assert/strict');
const ROOT=process.cwd(), SHOTS='docs/screenshots/visual-01-', LOG='docs/workflow/evidence/logs/VP-01-browser.json';
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
 const browser=await chromium.launch({channel:'msedge',headless:true});out.browser=browser.version();
 for(const [name,w,h] of [['desktop',800,540],['mobile',390,844]]) {
  const page=await browser.newPage({viewport:{width:w,height:h},deviceScaleFactor:1});
  page.on('pageerror',e=>out.pageErrors.push(String(e)));
  page.on('request',r=>{if(r.url().startsWith('http')&&!r.url().startsWith('http://127.0.0.1:8172'))out.externalRequests.push(r.url());if(r.method()==='POST')out.requests.push({device:name,url:r.url(),payload:r.postDataJSON()});});
  page.on('response',async r=>{if(r.request().method()==='POST')out.responses.push({device:name,url:r.url(),status:r.status(),body:await r.json()});});
  await page.goto('http://127.0.0.1:8172');
  for(const mode of ['gsn','gsv','combined']) {
   await setup(page,mode);const before=await metrics(page);
   await page.screenshot({path:SHOTS+`${name}-${mode}-before.png`,fullPage:name==='mobile'});
   const values=await submit(page,mode,expected[mode]);await page.waitForTimeout(350);
   const after=await metrics(page);
   assert.equal(after.document[0],w);if(name==='desktop'){assert.equal(after.scroll[1],0);assert.equal(after.document[1],h);assert(after.action.viewport);assert(after.totals.every(t=>t.viewport));}
   await page.screenshot({path:SHOTS+`${name}-${mode}-after.png`,fullPage:name==='mobile'});
   out.cases.push({device:name,mode,before,after,...values});
  }
  if(name==='desktop') {
   await setup(page,'gsv');
   for(const [label,values,total] of [['D1',[4,0,4],75600],['D2',[2,4,3],79275],['D3',[0,5,2],71400],['D4',[3,1,1],63000],['D5',[8,0,0],70875]]) {
    await page.evaluate(values=>values.forEach((v,i)=>document.getElementById(['gsv-length-up-to-25','gsv-length-32-40','gsv-length-57'][i]).value=v),values);
    const result=await submit(page,'gsv',total);const rows=await page.locator('#gsv-pipe-breakdown').innerText();
    out.cases.push({device:name,label,values,rows,...result});
    await page.screenshot({path:SHOTS+`desktop-gsv-${label}.png`});
   }
   await page.locator('#gsv-sakz').fill('2');assert.equal(await page.locator('#gsv-panel').isDisabled(),false);
   await page.locator('#gsv-panel').check();await page.locator('#is_district').check();
   out.options=await submit(page,'gsv',111825);
   await page.locator('#gsv-sakz').fill('0');assert.equal(await page.locator('#gsv-panel').isDisabled(),true);assert.equal(await page.locator('#gsv-panel').isChecked(),false);out.panelDependency=true;
  }
  // Exercise a real server 422 without changing production JavaScript.
  await setup(page,'gsv');
  const invalid=page.waitForResponse(r=>r.url().includes('/calculate/gsv')&&r.status()===422);
  await page.evaluate(()=>{document.getElementById('gsv-panel').checked=true;document.getElementById('calculate-form').requestSubmit();});
  const r=await invalid;await page.waitForFunction(()=>!document.getElementById('submit-btn').disabled);
  out[name+'422']={status:r.status(),error:await page.locator('#error').innerText()};assert(out[name+'422'].error.includes('ПК'));
  await page.locator('#error').scrollIntoViewIfNeeded();await page.screenshot({path:SHOTS+`${name}-422.png`});
  await page.locator('[data-mode="gsn"]').click();assert.equal(await page.locator('#error').isVisible(),false);assert.equal(await page.locator('#result-gsv').isVisible(),false);out[name+'SwitchClear']=true;
  await page.screenshot({path:SHOTS+`${name}-switch-clear.png`});await page.close();
 }
 const page=await browser.newPage({viewport:{width:560,height:450}});
 const uri=pathToFileURL(path.resolve('frontend/splash.html')).href;
 for(const [label,reduced,query] of [['animated','no-preference',''],['os','reduce',''],['flag','no-preference','?reduced-motion=1']]) {
  await page.emulateMedia({reducedMotion:reduced});await page.goto(uri+query);
  out.reducedMotion[label]=await page.locator('.gas').evaluate(el=>({animation:getComputedStyle(el).animationName,opacity:getComputedStyle(el).opacity,bounds:[innerWidth,innerHeight]}));
  if(label!=='animated')assert.equal(out.reducedMotion[label].animation,'none');else assert.equal(out.reducedMotion[label].animation,'gas-flow');
  await page.screenshot({path:SHOTS+`splash-${label}.png`});
 }
 assert.equal(out.pageErrors.length,0);assert.equal(out.externalRequests.length,0);
 await browser.close();fs.writeFileSync(LOG,JSON.stringify(out,null,2));console.log(JSON.stringify({cases:out.cases.length,totals:out.cases.map(x=>[x.device,x.label||x.mode,x.total]),errors:out.pageErrors,network:out.externalRequests,reducedMotion:out.reducedMotion},null,2));
})().catch(e=>{fs.writeFileSync(LOG,JSON.stringify(out,null,2));console.error(e);process.exitCode=1});
