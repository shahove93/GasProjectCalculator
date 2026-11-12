// Supplemental literal 390x844 viewport captures (the main pack has full-page mobile captures).
const {chromium}=require('C:/Users/user/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs');
(async()=>{
 const b=await chromium.launch({channel:'msedge',headless:true});const p=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:1});const log=[];
 await p.goto('http://127.0.0.1:8172');
 for(const mode of ['gsn','gsv','combined']) {
  await p.locator(`[data-mode="${mode}"]`).click();
  await p.evaluate(()=>{const q=id=>document.getElementById(id);q('length').value=10;q('gsv-length-up-to-25').value=4;q('gsv-length-57').value=4;});
  await p.screenshot({path:`docs/screenshots/visual-01-mobile-${mode}-viewport-before.png`});
  const wait=p.waitForResponse(r=>r.request().method()==='POST');await p.locator('#submit-btn').click();await wait;await p.waitForFunction(()=>!document.getElementById('submit-btn').disabled);await p.waitForTimeout(350);
  // Ordinary scroll to the action, no CSS/JS layout changes or zoom.
  await p.locator('#submit-btn').scrollIntoViewIfNeeded();
  log.push(await p.evaluate(mode=>{const r=document.getElementById('submit-btn').getBoundingClientRect();const id={gsn:'total',gsv:'gsv-total',combined:'combined-total'}[mode];const t=document.getElementById(id).getBoundingClientRect();return {mode,viewport:[innerWidth,innerHeight],scrollY,documentWidth:document.documentElement.scrollWidth,action:[r.top,r.bottom],total:[t.top,t.bottom],value:document.getElementById(id).textContent}},mode));
  await p.screenshot({path:`docs/screenshots/visual-01-mobile-${mode}-viewport-after.png`});
 }
 await b.close();fs.writeFileSync('docs/workflow/evidence/logs/VP-01-mobile-viewport.json',JSON.stringify(log,null,2));console.log(JSON.stringify(log,null,2));
})().catch(e=>{console.error(e);process.exitCode=1});
