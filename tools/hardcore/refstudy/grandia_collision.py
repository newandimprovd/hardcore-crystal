import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grandia_crawl import *
BASE=0xD082
def setword(r,c,val):
    a=BASE+(r*10+c)*2
    m[1,a]=val&0xFF; m[1,a+1]=val>>8
def getword(r,c):
    a=BASE+(r*10+c)*2; return m[1,a]|(m[1,a+1]<<8)
T=(6,5)
stage={"right":(6,4),"left":(6,6),"down":(5,5),"up":(7,5)}
def test(word,d):
    load(pb,"crawl/room527.state"); pb.tick(5,False)
    if not step_to_path(stage[d]): return "nostage"
    p0=xy()
    setword(*T,word)
    for _ in range(30):
        pb.button_press(d); pb.tick(1,False); pb.button_release(d)
    p1=xy()
    dx,dy=p1[0]-p0[0],p1[1]-p0[1]
    mv={"right":dx,"left":-dx,"down":dy,"up":-dy}[d]
    return mv
def step_to_path(goal):
    t,at,w=rec(527)
    path=bfs(w,cell(),{goal})
    if path is None: return False
    for rc in path[1:]:
        if not step_to(rc): return False
    # fine align
    r,c=goal; align_axis("x",c*16); align_axis("y",r*16+15)
    return cell()==goal
if __name__=="__main__":
    words=[0x0000,0x02ff,0x0100,0x0c00,0x0011,0x0e55,0x0aff,0x01ff,0x08ff,0x0200,0x0800,0x0a00,0x0e00,0x0001,0x0002,0x0004,0x0008,0x0010,0x0020,0x0040,0x0080,0x0055,0x00aa,0x00ff]
    print("word    "+"  ".join(f"{d:>5}" for d in ["right","left","down","up"]))
    for w in words:
        print(f"{w:04x}   "+"  ".join(f"{test(w,d):>5}" if not isinstance(test(w,d),str) else "  n/a" for d in ["right","left","down","up"]),flush=True)
