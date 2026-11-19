import sys; sys.path.insert(0,"/home/claude/pokecrystal/tools/hardcore/refstudy")
from boot import *
from PIL import Image
def sheet(paths, out, cols=4):
    ims=[Image.open(p) for p in paths]; w,h=ims[0].size
    rows=(len(ims)+cols-1)//cols
    s=Image.new("RGB",(w*cols,h*rows))
    for n,im in enumerate(ims): s.paste(im,((n%cols)*w,(n//cols)*h))
    s.save(out)

def save(pb, path):
    with open(path, "wb") as f: pb.save_state(f)
def load(pb, path):
    with open(path, "rb") as f: pb.load_state(f)
def run(pb, seq, tag, every=4, scale=1, wait=40):
    paths=[]; n=0
    for i,k in enumerate(seq):
        if isinstance(k, tuple): press(pb, k[0], 6, k[1])
        else: press(pb, k, 6, wait)
        if i % every == every-1:
            p=f"/home/claude/pokecrystal/tools/hardcore/refstudy/{tag}{n:02d}.png"; shot(pb,p,scale); paths.append(p); n+=1
    return paths

def walk(pb, dirs, hold=17, wait=3):
    for d in dirs:
        pb.button(d, hold); pb.tick(hold + wait, False)
def pos(pb, base=0xdc64):
    m = pb.memory
    return (m[1, base], m[1, base+1], m[1, base+3], m[1, base+2])  # group, map, x, y

def step(pb, d, base=0xdc64):
    p0 = pos(pb, base)
    for _ in range(2):
        pb.button(d, 17); pb.tick(20, False)
        if pos(pb, base) != p0: break
    return pos(pb, base)
