// Run from repository root with the preinstalled local Playwright package.
const {chromium} = require('C:/Users/user/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const path = require('path');
const {pathToFileURL} = require('url');
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'msedge'});
 const page=await browser.newPage({viewport:{width:800,height:540},deviceScaleFactor:1});
 await page.goto('http://127.0.0.1:8172');
 await page.screenshot({path:'docs/screenshots/visual-01-preview-main.png'});
 await page.setViewportSize({width:560,height:450});
 await page.goto(pathToFileURL(path.resolve('frontend/splash.html')).href+'?reduced-motion=1');
 await page.screenshot({path:'docs/screenshots/visual-01-preview-splash.png'});
 for(const [name,w,h] of [['installer-sidebar',328,628],['installer-header',110,110]]) {
  await page.setViewportSize({width:w,height:h});
  await page.goto(pathToFileURL(path.resolve('frontend/assets/'+name+'.svg')).href);
  await page.screenshot({path:'frontend/assets/'+name+'.png'});
 }
 console.log(JSON.stringify({browser:browser.version(),exports:['installer-sidebar.png 328x628','installer-header.png 110x110']},null,2));
 await browser.close();
})().catch(e=>{console.error(e);process.exitCode=1});
