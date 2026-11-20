import sys, json, time, glob, re, collections; sys.path[:0]=[__import__("os").path.dirname(__import__("os").path.abspath(__file__)),__import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)),"..")]
from gcrawl2 import *
def is_pit(w,rc): return (w[rc[0]][rc[1]]>>8)&1
def enterable(w,u,d,v):
    wu=w[u[0]][u[1]]; wv=w[v[0]][v[1]]
    if wu&EXIT[d]: return False
    if wv&ENTRY[d]: return False
    if (wv&0x0F)==0x0F: return False
    return True
def moves(w,u):
    out=[]
    for d in DIRS:
        dr,dc=DIRS[d]; v=(u[0]+dr,u[1]+dc)
        if not(0<=v[0]<9 and 0<=v[1]<10): continue
        if not enterable(w,u,d,v): continue
        if not is_pit(w,v): out.append((v,d,"walk"))
        else:
            L=(v[0]+dr,v[1]+dc)
            if 0<=L[0]<9 and 0<=L[1]<10 and enterable(w,v,d,L) and not is_pit(w,L): out.append((L,d,"jump"))
    return out
def bfs3(w,start,goals):
    q=collections.deque([start]); prev={start:None}
    while q:
        u=q.popleft()
        if u in goals:
            p=[]
            while prev[u] is not None: p.append((u,prev[u][1],prev[u][2])); u=prev[u][0]
            return p[::-1]
        for v,d,k in moves(w,u):
            if v not in prev: prev[v]=(u,d,k); q.append(v)
    return None
def align_cell(rc):
    r,c=rc; align_axis("x",c*16,60); align_axis("y",r*16+15,60)
def do_jump(d,src,dst):
    align_cell(src)
    pb.button_press(d); pb.tick(3,False); pb.button_press("a"); pb.tick(3,False); pb.button_release("a")
    pb.tick(30,False); pb.button_release(d); pb.tick(8,False)
    return cell()==dst
def edge_goals3(w,d):
    out=set()
    n=10 if d in("up","down") else 9
    for i in range(n):
        rc={"right":(i,9),"left":(i,0),"up":(0,i),"down":(8,i)}[d]
        wv=w[rc[0]][rc[1]]
        if not(wv&EXIT[d]) and not((wv>>8)&1) and (wv&0x0F)!=0x0F: out.add(rc)
    return out
def try_exit3(room,d,w):
    goals=edge_goals3(w,d)
    if not goals: return None
    here=cell()
    if here in goals: path=[]
    else:
        path=bfs3(w,here,goals)
        if path is None: return None
    for dst,dd,k in path:
        src=cell()
        if k=="walk":
            if not step_to(dst): return "stuck"
        else:
            if not do_jump(dd,src,dst): return "jumpfail"
    for _ in range(80):
        pb.button_press(d); pb.tick(1,False); pb.button_release(d)
        if m[0xFF43]!=0 or m[0xFF42]!=0: break
        r=room_index_from_buffer(m)
        if r is not None and r!=room: break
    return stable_room()
if __name__=="__main__":
    limit=float(sys.argv[1]) if len(sys.argv)>1 else 900
    try: edges=json.load(open("crawl/edges3.json"))
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
            if key in edges and edges[key] not in ("stuck","jumpfail"): continue
            load(pb,f"crawl/room{R}.state"); pb.tick(2,False)
            if room_index_from_buffer(m)!=R: print("mismatch",R); break
            res=try_exit3(R,d,w)
            edges[key]=res
            if isinstance(res,int) and res!=R:
                print(R,d,"->",res,xy(),flush=True)
                if res not in seen:
                    seen.add(res); save_state(f"crawl/room{res}.state"); queue.append(res)
            elif res in ("stuck","jumpfail"): print(R,d,res,flush=True)
        json.dump(edges,open("crawl/edges3.json","w"))
    print("rooms",len(seen),sorted(seen),"elapsed",int(time.time()-t0))
