import os, sys, json, time, collections; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grandia_rooms import *
pb=boot("grandia"); m=pb.memory
DIRS={"right":(0,1),"left":(0,-1),"up":(-1,0),"down":(1,0)}
def xy(): return (m[1,0xd022], m[1,0xd021])
def cell(): 
    X,Y=xy(); return ((Y-8)//16, (X+8)//16)
def settle(n=2): pb.tick(n,False)
def stable_room():
    # wait until SCX==0 and room index stable
    last=None; cnt=0
    for _ in range(200):
        pb.tick(1,False)
        if m[0xFF43]!=0 or m[0xFF42]!=0: cnt=0; continue
        r=room_index_from_buffer(m)
        if r is not None and r==last: cnt+=1
        else: cnt=0; last=r
        if cnt>=12: return r
    return last
def free(w,r,c): return 0<=r<9 and 0<=c<10 and (w[r][c]&0xFF)==0
def bfs(w,start,goals):
    q=collections.deque([start]); prev={start:None}
    while q:
        u=q.popleft()
        if u in goals:
            path=[]
            while u: path.append(u); u=prev[u]
            return path[::-1]
        for dr,dc in DIRS.values():
            v=(u[0]+dr,u[1]+dc)
            if v not in prev and free(w,*v): prev[v]=u; q.append(v)
    return None
def press(key,n=1):
    pb.button_press(key); pb.tick(n,False); pb.button_release(key)
def align_axis(axis,target,maxf=40):
    # axis 'x' or 'y'
    for _ in range(maxf):
        X,Y=xy(); v=X if axis=="x" else Y
        if v==target: return True
        if axis=="x": press("right" if v<target else "left",1)
        else: press("down" if v<target else "up",1)
    return False
def step_to(rc,maxf=60):
    r,c=rc; tx=c*16; ty=r*16+15
    cur=cell()
    for _ in range(maxf):
        cur=cell()
        if cur==rc: 
            return True
        X,Y=xy()
        dr=rc[0]-cur[0]; dc=rc[1]-cur[1]
        if dc!=0:
            # align y first
            if Y!=ty: press("down" if Y<ty else "up",1)
            else: press("right" if dc>0 else "left",1)
        else:
            if X!=tx and abs(X-tx)>0: press("right" if X<tx else "left",1)
            else: press("down" if dr>0 else "up",1)
    return cell()==rc
def try_exit(room, d, w):
    dr,dc=DIRS[d]
    # goal cells: free edge cells on side d
    goals=set()
    for i in range(10 if d in("up","down") else 9):
        rc={"right":(i,9),"left":(i,0),"up":(0,i),"down":(8,i)}[d]
        if free(w,*rc): goals.add(rc)
    if not goals: return None
    here=cell()
    path=bfs(w,here,goals)
    if not path: return None
    for rc in path[1:]:
        if not step_to(rc): return "stuck"
    # now push in direction d until room changes
    for _ in range(80):
        pb.button_press(d); pb.tick(1,False)
        pb.button_release(d)
        if m[0xFF43]!=0 or m[0xFF42]!=0: break
        r=room_index_from_buffer(m)
        if r is not None and r!=room: break
    r2=stable_room()
    return r2
def save_state(path):
    with open(path,"wb") as f: pb.save_state(f)
if __name__=="__main__":
    maxrooms=int(sys.argv[1]) if len(sys.argv)>1 else 40
    load(pb,"gr_s4.state"); pb.tick(20,False)
    start=room_index_from_buffer(m)
    save_state(f"crawl/room{start}.state")
    edges={}; entry={start:xy()}; queue=collections.deque([start]); t0=time.time()
    while queue and len(entry)<maxrooms:
        R=queue.popleft()
        t,at,w=rec(R)
        for d in DIRS:
            load(pb,f"crawl/room{R}.state"); pb.tick(2,False)
            if room_index_from_buffer(m)!=R: 
                print("state mismatch",R); break
            res=try_exit(R,d,w)
            edges[f"{R},{d}"]=res if not isinstance(res,tuple) else list(res)
            print(R,d,"->",res,xy(), f"{time.time()-t0:.0f}s",flush=True)
            if isinstance(res,int) and res!=R and res not in entry:
                entry[res]=xy(); save_state(f"crawl/room{res}.state"); queue.append(res)
        json.dump({"edges":edges,"entry":{k:list(v) for k,v in entry.items()}},open("crawl/edges.json","w"))
    print("done",len(entry),"rooms")
