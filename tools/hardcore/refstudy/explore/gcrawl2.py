import sys, json, time, glob, re, collections; sys.path[:0]=[__import__("os").path.dirname(__import__("os").path.abspath(__file__)),__import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)),"..")]
import gcrawl as g
from gcrawl import *
ENTRY={"right":0x04,"left":0x01,"down":0x02,"up":0x08}
EXIT={"right":0x10,"up":0x20,"left":0x40,"down":0x80}
def can_move(w,u,d):
    dr,dc=DIRS[d]; v=(u[0]+dr,u[1]+dc)
    if not(0<=v[0]<9 and 0<=v[1]<10): return None
    wu=w[u[0]][u[1]]; wv=w[v[0]][v[1]]
    if wu&EXIT[d]: return None
    if wv&ENTRY[d]: return None
    if (wv>>8)&1: return None   # pit
    if (wv&0x0F)==0x0F: return None
    return v
def bfs2(w,start,goals):
    q=collections.deque([start]); prev={start:None}
    while q:
        u=q.popleft()
        if u in goals:
            p=[]
            while u: p.append(u); u=prev[u]
            return p[::-1]
        for d in DIRS:
            v=can_move(w,u,d)
            if v and v not in prev: prev[v]=u; q.append(v)
    return None
def edge_goals(w,d):
    out=set()
    n=10 if d in("up","down") else 9
    for i in range(n):
        rc={"right":(i,9),"left":(i,0),"up":(0,i),"down":(8,i)}[d]
        if not (w[rc[0]][rc[1]]&EXIT[d]) and not ((w[rc[0]][rc[1]]>>8)&1) and (w[rc[0]][rc[1]]&0x0F)!=0x0F: out.add(rc)
    return out
def try_exit2(room,d,w):
    goals=edge_goals(w,d)
    if not goals: return None
    path=bfs2(w,cell(),goals)
    if not path: return None
    for rc in path[1:]:
        if not step_to(rc): return "stuck"
    for _ in range(80):
        pb.button_press(d); pb.tick(1,False); pb.button_release(d)
        if m[0xFF43]!=0 or m[0xFF42]!=0: break
        r=room_index_from_buffer(m)
        if r is not None and r!=room: break
    return stable_room()
if __name__=="__main__":
    limit=float(sys.argv[1]) if len(sys.argv)>1 else 900
    try: edges=json.load(open("crawl/edges2.json"))
    except Exception: edges={}
    rooms=sorted(int(re.findall(r'room(\d+)\.state',f)[0]) for f in glob.glob("crawl/room*.state"))
    queue=collections.deque(rooms); seen=set(rooms); t0=time.time(); done=set()
    while queue and time.time()-t0<limit:
        R=queue.popleft()
        if R in done: continue
        done.add(R)
        t,at,w=rec(R)
        for d in DIRS:
            key=f"{R},{d}"
            if key in edges and edges[key] not in ("stuck",): continue
            load(pb,f"crawl/room{R}.state"); pb.tick(2,False)
            if room_index_from_buffer(m)!=R: print("mismatch",R); break
            res=try_exit2(R,d,w)
            edges[key]=res
            if isinstance(res,int) and res!=R:
                print(R,d,"->",res,xy(),flush=True)
                if res not in seen:
                    seen.add(res); save_state(f"crawl/room{res}.state"); queue.append(res)
        json.dump(edges,open("crawl/edges2.json","w"))
    print("rooms",len(seen),sorted(seen),"elapsed",int(time.time()-t0))
