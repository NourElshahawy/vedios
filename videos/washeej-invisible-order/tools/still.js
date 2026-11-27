// node still.js <html> <out.png> <t> <w> <h> [query] -> one frame (for review)
const {chromium}=require('playwright');const path=require('path');(async()=>{const [h,o,t,w,hh,q]=process.argv.slice(2);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:+w,height:+hh}});
await p.goto('file://'+path.resolve(h)+(q?'?'+q:''));await p.evaluate(()=>document.fonts.ready);
for(const tt of t.split(',')){await p.evaluate(x=>window.seek(x),+tt);await p.screenshot({path:o.replace('.png',`_${tt}.png`)});}await b.close()})();
