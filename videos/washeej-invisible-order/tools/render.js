// Deterministic frame renderer: each HTML exposes window.seek(t) (seconds).
// usage: node render.js <html> <outdir> <seconds> <w> <h> <alpha:0|1> [fps=30] [query]
const {chromium}=require('playwright'); const fs=require('fs'); const path=require('path');
(async()=>{
 const [html,out,dur,w,h,alpha,fpsArg,query]=process.argv.slice(2);
 const fps=+(fpsArg||30), n=Math.round(+dur*fps); fs.mkdirSync(out,{recursive:true});
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:+w,height:+h},deviceScaleFactor:1});
 await p.goto('file://'+path.resolve(html)+(query?('?'+query):''));
 await p.evaluate(()=>document.fonts.ready);
 for(let i=0;i<n;i++){ await p.evaluate(t=>window.seek(t), i/fps);
   await p.screenshot({path:`${out}/f_${String(i).padStart(4,'0')}.png`,omitBackground:alpha==='1'}); }
 await b.close(); console.log('frames',n);
})();
