import sys; sys.path[:0]=[__import__("os").path.dirname(__import__("os").path.abspath(__file__)),__import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)),"..")]
from gexplore import *
def npc_cells():
    out=set()
    hx,hy=xy()
    for i in range(2,40):
        y,x=m[0xFE00+i*4],m[0xFE00+i*4+1]
        if y==0 or y>=160 or x==0 or x>=168: continue
        px=x-8; py=y-16
        # sprite half is 8 wide, 16 tall: cell by its centre
        c=((px+4)//16); r=((py+8)//16)
        if 0<=r<9 and 0<=c<10: out.add((r,c))
    return out
def goto2(rc,maxn=40):
    for _ in range(maxn):
        here=cell()
        if here==rc: return True
        g=[row[:] for row in live_grid()]
        for (r,c) in npc_cells():
            if (r,c)!=here: g[r][c]=0x02ff
        path=bfs3(g,here,{rc})
        if not path: return False
        dst,dd,k=path[0]
        if k=="walk":
            before=xy()
            step_to(dst,maxf=24)
            if xy()==before:
                # blocked by something unseen: nudge by waiting a bit
                pb.tick(10,False)
        else:
            if not do_jump(dd,here,dst): return False
    return cell()==rc
