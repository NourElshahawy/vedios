const {chromium}=require('playwright');const path=require('path');(async()=>{const b=await chromium.launch();
const p=await b.newPage({viewport:{width:2000,height:1400},deviceScaleFactor:2});
await p.goto('file://'+path.resolve('gfx/GFX_07_error_windows.html'));await p.evaluate(()=>document.fonts.ready);
for(let i=1;i<=6;i++){await p.locator('#w'+i).screenshot({path:`renders/GFX_07_window_${i}.png`,omitBackground:true});}
await p.screenshot({path:'/tmp/claude-0/chk/win_all.png',fullPage:true});await b.close();})();
