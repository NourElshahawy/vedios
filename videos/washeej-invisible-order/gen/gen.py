# Generates start frames (FLUX schnell) and clips (Wan 2.2 I2V) for every shot in plan.SHOTS that lacks a take.
import os,sys,shutil,time,traceback
from gradio_client import Client, handle_file
from plan import SHOTS
ORDER=['S07A','S05A','S05B','S01A','S02A','S02B','S01C','S07C','S08A','S03C','S07B']
SHOTS=sorted(SHOTS,key=lambda s: ORDER.index(s[0]) if s[0] in ORDER else 99)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
F=Client("https://black-forest-labs-flux-1-schnell.hf.space",verbose=False)
W=Client("https://linoyts-wan2-2-i2v-rcm.hf.space",verbose=False)
take=sys.argv[1] if len(sys.argv)>1 else "t1"
for sid,fp,vp,seed in SHOTS:
    out=f"clips/{sid}_{take}.mp4"
    if os.path.exists(out): continue
    fr=f"frames/F_{sid}.png"
    try:
        if not os.path.exists(fr):
            r,_=F.predict(prompt=fp,seed=seed,randomize_seed=False,width=576,height=1024,num_inference_steps=4,api_name="/infer")
            os.system(f"convert '{r}' {fr}"); print("frame",sid,flush=True)
        t=time.time()
        v,_=W.predict(input_image=handle_file(fr),prompt=vp+", cinematic, film grain",steps=6,duration_seconds=5,guidance_scale=1,guidance_scale_2=1,
                      seed=seed+(0 if take=="t1" else 1000),randomize_seed=False,api_name="/generate_video")
        shutil.copy(v["video"] if isinstance(v,dict) else v,out); print("clip",sid,take,round(time.time()-t),"s",flush=True)
    except Exception as e:
        print("FAIL",sid,str(e)[:300],flush=True)
        if "quota" in str(e).lower() or "limit" in str(e).lower(): print("STOP: quota reached",flush=True); break
