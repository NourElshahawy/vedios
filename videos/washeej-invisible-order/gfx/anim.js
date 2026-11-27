// tiny timeline helpers (deterministic, no rAF)
const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const prog=(t,a,b)=>clamp((t-a)/(b-a));
const eo=x=>1-Math.pow(1-x,3), eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2, eback=x=>{const c=1.70158,c3=c+1;return 1+c3*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
const expo=x=>x===1?1:1-Math.pow(2,-10*x);
const lerp=(a,b,x)=>a+(b-a)*x;
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
