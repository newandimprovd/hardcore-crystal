import sys, json, time, glob, re, collections; sys.path[:0]=[__import__("os").path.dirname(__import__("os").path.abspath(__file__)),__import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)),"..")]
from gcrawl3 import *
def live_grid():
    return [[m[1,0xD082+(r*10+c)*2]|(m[1,0xD082+(r*10+c)*2+1]<<8) for c in range(10)] for r in range(9)]
def reach(w,start):
    seen={start}; q=collections.deque([start])
    while q:
        u=q.popleft()
        for v,d,k in moves(w,u):
            if v not in seen: seen.add(v); q.append(v)
    return seen
def goto(w,rc):
    here=cell()
    if here==rc: return True
    path=bfs3(w,here,{rc})
    if not path: return False
    for dst,dd,k in path:
        src=cell()
        if k=="walk":
            if not step_to(dst): return False
        else:
            if not do_jump(dd,src,dst): return False
    return True
def diff(a,b):
    return [(r,c,hex(a[r][c]),hex(b[r][c])) for r in range(9) for c in range(10) if a[r][c]!=b[r][c]]
def sweep_room(R,limit=150):
    t0=time.time()
    load(pb,f"crawl/room{R}.state"); pb.tick(3,False)
    base=live_grid(); w=base
    cells=sorted(reach(w,cell()))
    events=[]
    for rc in cells:
        if time.time()-t0>limit: break
        load(pb,f"crawl/room{R}.state"); pb.tick(3,False)
        if not goto(w,rc): continue
        pb.tick(15,False)
        g=live_grid()
        if room_index_from_buffer(m)!=R: events.append(("room",rc,room_index_from_buffer(m))); continue
        dd=diff(base,g)
        if dd: events.append(("step",rc,dd))
        for key in ("up","down","left","right"):
            pb.button_press(key); pb.tick(3,False); pb.button_release(key); pb.tick(2,False)
            pb.button_press("a"); pb.tick(2,False); pb.button_release("a"); pb.tick(30,False)
            # clear dialogue
            for _ in range(3):
                pb.button_press("b"); pb.tick(2,False); pb.button_release("b"); pb.tick(10,False)
            g=live_grid(); dd=diff(base,g)
            if room_index_from_buffer(m)!=R and m[0xFF43]==0: events.append(("A-room",rc,key,room_index_from_buffer(m))); break
            if dd: 
                events.append(("A",rc,key,dd)); 
                save_state(f"crawl/ev_{R}_{rc[0]}{rc[1]}{key}.state"); break
    return base,cells,events
if __name__=="__main__":
    rooms=[int(x) for x in sys.argv[1:]]
    for R in rooms:
        base,cells,ev=sweep_room(R)
        print("ROOM",R,"reachable cells",len(cells),"events",len(ev),flush=True)
        for e in ev[:12]: print("   ",e)
