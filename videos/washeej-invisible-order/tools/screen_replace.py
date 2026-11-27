#!/usr/bin/env python3
"""Track a phone/laptop screen and replace it with a rendered GFX plate (free alternative to a planar tracker).
usage: python3 tools/screen_replace.py <shot.mp4> <insert.mov> <out.mp4> --corners "x1,y1 x2,y2 x3,y3 x4,y4" [--insert-from 0] [--hold-at SEC] [--luma-key 170]
corners = screen TL TR BR BL on the FIRST frame of the shot (pixel coords of the source file).
--hold-at: freeze the insert at that insert-time (for bullet time) while the camera keeps moving.
Tracking: KLT features in a ring around the screen (the blank screen itself has no texture) → RANSAC homography, chained per frame."""
import cv2,numpy as np,sys,subprocess,os,tempfile
a=sys.argv; shot,ins,out=a[1],a[2],a[3]
opt=lambda k,d=None:a[a.index(k)+1] if k in a else d
C=np.float32([[float(v) for v in p.split(',')] for p in opt('--corners').split()])
ifrom=float(opt('--insert-from',0)); hold=opt('--hold-at'); hold=float(hold) if hold else None
DL=float(opt('--delay',0))   # hold the plate's first frame this many seconds before it starts playing
LK=opt('--luma-key'); LK=float(LK) if LK else None   # only replace pixels brighter than this (keeps fingers over a white screen)
cap=cv2.VideoCapture(shot); fps=cap.get(cv2.CAP_PROP_FPS) or 30
W=int(cap.get(3)); H=int(cap.get(4))
tmp=tempfile.mkdtemp(); ip=os.path.join(tmp,'%05d.png')
subprocess.run(["ffmpeg","-loglevel","error","-ss",str(ifrom),"-i",ins,"-vf",f"fps={fps}",ip],check=True)
plates=sorted(os.listdir(tmp))
def plate(i):
    i=max(0,i-int(round(DL*fps)))
    k=int(round(hold*fps))-int(round(ifrom*fps)) if hold is not None and i/fps+ifrom>=hold else i
    return cv2.imread(os.path.join(tmp,plates[min(max(k,0),len(plates)-1)]))
ok,prev=cap.read(); pg=cv2.cvtColor(prev,cv2.COLOR_BGR2GRAY)
def ring(c):
    m=np.zeros(pg.shape,np.uint8); big=c.mean(0)+(c-c.mean(0))*1.35
    cv2.fillConvexPoly(m,big.astype(np.int32),255); cv2.fillConvexPoly(m,(c.mean(0)+(c-c.mean(0))*0.92).astype(np.int32),0); return m
pts=cv2.goodFeaturesToTrack(pg,600,0.001,5,mask=ring(C)); ref=pts.copy(); refC=C.copy()
wr=cv2.VideoWriter(os.path.join(tmp,'o.mp4'),cv2.VideoWriter_fourcc(*'mp4v'),fps,(W,H))
cur=C.copy(); i=0; frame=prev
while True:
    p=plate(i); ph,pw=p.shape[:2]
    Hm=cv2.getPerspectiveTransform(np.float32([[0,0],[pw,0],[pw,ph],[0,ph]]),cur)
    warp=cv2.warpPerspective(p,Hm,(W,H),flags=cv2.INTER_LANCZOS4)
    mask=np.zeros((H,W),np.float32); cv2.fillConvexPoly(mask,cur.astype(np.int32),1.0,lineType=cv2.LINE_AA)
    if LK is not None:
        Y=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY).astype(np.float32)
        k=np.clip((Y-LK)/25.0,0,1); k=cv2.morphologyEx(k,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8)); mask=mask*cv2.GaussianBlur(k,(5,5),0)
    mask=cv2.GaussianBlur(mask,(3,3),0)[...,None]
    glare=cv2.GaussianBlur(frame,(0,0),9).astype(np.float32)*0.06   # keep a hint of real reflections
    comp=frame*(1-mask)+np.clip(warp+glare,0,255)*mask
    wr.write(comp.astype(np.uint8)); i+=1
    ok,frame=cap.read()
    if not ok: break
    g=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    nxt,st,_=cv2.calcOpticalFlowPyrLK(pg,g,pts,None,winSize=(21,21),maxLevel=3,criteria=(3,30,0.01))
    back,st2,_=cv2.calcOpticalFlowPyrLK(g,pg,nxt,None,winSize=(21,21),maxLevel=3,criteria=(3,30,0.01))
    keep=(st[:,0]==1)&(st2[:,0]==1)&(np.linalg.norm((back-pts).reshape(-1,2),axis=1)<0.7)   # forward-backward check
    ref,pts=ref[keep],nxt[keep]
    if len(ref)>=8:
        Hr,_=cv2.findHomography(ref.reshape(-1,2),pts.reshape(-1,2),cv2.RANSAC,2.0)   # reference frame → now (no drift chaining)
        if Hr is not None: cur=cv2.perspectiveTransform(refC[None],Hr)[0]
    if len(pts)<120:   # re-anchor on the current frame
        pts=cv2.goodFeaturesToTrack(g,600,0.001,5,mask=ring(cur)); ref=pts.copy(); refC=cur.copy()
    pg=g
wr.release()
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",os.path.join(tmp,'o.mp4'),"-c:v","libx264","-crf","14","-pix_fmt","yuv420p",out],check=True)
print("wrote",out,"frames",i,"last corners",np.round(cur).astype(int).tolist())
