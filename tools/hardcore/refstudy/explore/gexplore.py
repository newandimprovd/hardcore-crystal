import sys, json, time, glob, re, hashlib, collections, random; sys.path[:0]=[__import__("os").path.dirname(__import__("os").path.abspath(__file__)),__import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)),"..")]
from gsweep2 import *
from PIL import Image
def sat_info():
    pb.tick(1,True); im=pb.screen.image.convert("RGB")
    px=set(im.getdata())
    import colorsys
    ss=[colorsys.rgb_to_hsv(*(c/255 for c in p)) for p in px]
    hues=set(round(h*12)%12 for h,s,v in ss if s>0.25 and v>0.25)
    return len(px), len(hues), max((s for h,s,v in ss),default=0), im
def sig():
    r=room_index_from_buffer(m)
    g=live_grid()
    spr=tuple((m[0xFE00+i*4],m[0xFE00+i*4+1]) for i in range(2,12) if m[0xFE00+i*4])
    return (r,hashlib.md5(repr(g).encode()).hexdigest()[:8],hashlib.md5(repr(spr).encode()).hexdigest()[:6])
def clear_dialogue(R,maxn=300):
    good=0
    for i in range(maxn):
        r=room_index_from_buffer(m)
        if r is not None and m[0xFF43]==0 and m[0xFF42]==0 and (m[0xFF40]&0x80):
            good+=1
            if good>=6: return True
            pb.tick(8,False); continue
        good=0
        pb.button_press("a"); pb.tick(2,False); pb.button_release("a"); pb.tick(14,False)
    return room_index_from_buffer(m) is not None
def interact(w,rc,key):
    if not goto(w,rc): return False
    pb.tick(10,False)
    pb.button_press(key); pb.tick(3,False); pb.button_release(key); pb.tick(3,False)
    pb.button_press("a"); pb.tick(2,False); pb.button_release("a"); pb.tick(20,False)
    return True
if __name__=="__main__":
    limit=float(sys.argv[1]); seeds=sys.argv[2:]
    random.seed(5)
    Q=collections.deque(); seen=set(); k=0
    for s in seeds:
        load(pb,s); pb.tick(3,False); clear_dialogue(None)
        seen.add(sig()); Q.append(s)
    import os; os.makedirs("crawl/ex",exist_ok=True)
    t0=time.time(); best=0; known_rooms=set(int(re.findall(r'room(\d+)\.state',f)[0]) for f in glob.glob("crawl/room*.state"))
    while Q and time.time()-t0<limit:
        s=Q.popleft()
        load(pb,s); pb.tick(3,False); clear_dialogue(None)
        R=room_index_from_buffer(m)
        if R is None: continue
        base=sig(); w=live_grid()
        cells=sorted(reach(w,cell()))
        random.shuffle(cells)
        # exits first
        for d in DIRS:
            load(pb,s); pb.tick(3,False); clear_dialogue(None)
            res=try_exit3(R,d,live_grid())
            if isinstance(res,int) and res!=R:
                if res not in known_rooms:
                    known_rooms.add(res); save_state(f"crawl/room{res}.state"); print("NEW ROOM",res,"from",R,d,flush=True)
                sg=sig()
                if sg not in seen:
                    seen.add(sg); k+=1; p=f"crawl/ex/s{k:04d}.state"; save_state(p); Q.append(p)
        for rc in cells[:70]:
            for key in ("up","down","left","right"):
                if time.time()-t0>limit: break
                load(pb,s); pb.tick(3,False); clear_dialogue(None)
                if not interact(live_grid(),rc,key): continue
                clear_dialogue(R)
                R2=room_index_from_buffer(m)
                if R2 is None: continue
                sg=sig()
                if sg!=base and sg not in seen:
                    seen.add(sg); k+=1; p=f"crawl/ex/s{k:04d}.state"; save_state(p); Q.append(p)
                    nc,nh,ms,im=sat_info()
                    print(f"state {k} room {R2} from {R} cell {rc} {key} colours {nc} hues {nh} maxsat {ms:.2f}",flush=True)
                    if R2 not in known_rooms:
                        known_rooms.add(R2); save_state(f"crawl/room{R2}.state"); print("NEW ROOM",R2,flush=True)
                    if nh>=3 or nc>24:
                        im.resize((320,288),Image.NEAREST).save(f"crawl/ex/color_{k}.png"); print("   COLOURFUL screen saved",flush=True)
    print("done states",k,"known rooms",sorted(known_rooms),int(time.time()-t0))
