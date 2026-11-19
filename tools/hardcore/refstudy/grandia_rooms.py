import os, sys, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drive import *
rom=open(ROMS["grandia"],"rb").read()
BANK0=132
def room_index_from_buffer(m):
    buf=bytes(m[0xC4A0+i] for i in range(360))
    # find in room banks at record starts
    for bank in range(132,163):
        for r in range(18):
            a=bank*0x4000+r*900
            if rom[a:a+360]==buf: return (bank-132)*18+r
    return None
def info(pb):
    m=pb.memory
    return dict(room=room_index_from_buffer(m), X=m[1,0xd022], Y=m[1,0xd021])

def rec(room):
    bank=132+room//18; r=room%18
    a=bank*0x4000+r*900
    t=rom[a:a+360]; at=rom[a+360:a+720]; c=rom[a+720:a+900]
    words=[[c[(rr*10+cc)*2]|(c[(rr*10+cc)*2+1]<<8) for cc in range(10)] for rr in range(9)]
    return t,at,words
def show_col(room):
    t,at,w=rec(room)
    print("room",room,"bank",hex(132+room//18),"rec",room%18)
    for r in range(9): print(" ".join(f"{x:04x}" for x in w[r]))
