# minimal LR35902 disassembler
R8=["b","c","d","e","h","l","[hl]","a"]
R16=["bc","de","hl","sp"]; R16S=["bc","de","hl","af"]
CC=["nz","z","nc","c"]
def dis(rom, off, n, base=None, bankaddr=None):
    out=[]; i=off; end=off+n
    def ad(o): 
        # address for display
        return 0x4000+(o%0x4000) if o>=0x4000 else o
    while i<end:
        op=rom[i]; ln=1; t=""
        b1=rom[i+1] if i+1<len(rom) else 0; b2=rom[i+2] if i+2<len(rom) else 0
        w=b1|(b2<<8); s8=b1-256 if b1>127 else b1
        if op==0x00:t="nop"
        elif op==0x10:t="stop";ln=2
        elif op==0x76:t="halt"
        elif op&0xC0==0x40:t=f"ld {R8[(op>>3)&7]},{R8[op&7]}"
        elif op&0xC7==0x06:t=f"ld {R8[(op>>3)&7]},${b1:02x}";ln=2
        elif op&0xCF==0x01:t=f"ld {R16[(op>>4)&3]},${w:04x}";ln=3
        elif op==0x08:t=f"ld [${w:04x}],sp";ln=3
        elif op==0x02:t="ld [bc],a"
        elif op==0x12:t="ld [de],a"
        elif op==0x0a:t="ld a,[bc]"
        elif op==0x1a:t="ld a,[de]"
        elif op==0x22:t="ld [hl+],a"
        elif op==0x2a:t="ld a,[hl+]"
        elif op==0x32:t="ld [hl-],a"
        elif op==0x3a:t="ld a,[hl-]"
        elif op&0xCF==0x03:t=f"inc {R16[(op>>4)&3]}"
        elif op&0xCF==0x0B:t=f"dec {R16[(op>>4)&3]}"
        elif op&0xCF==0x09:t=f"add hl,{R16[(op>>4)&3]}"
        elif op&0xC7==0x04:t=f"inc {R8[(op>>3)&7]}"
        elif op&0xC7==0x05:t=f"dec {R8[(op>>3)&7]}"
        elif op==0x07:t="rlca"
        elif op==0x0f:t="rrca"
        elif op==0x17:t="rla"
        elif op==0x1f:t="rra"
        elif op==0x27:t="daa"
        elif op==0x2f:t="cpl"
        elif op==0x37:t="scf"
        elif op==0x3f:t="ccf"
        elif op==0x18:t=f"jr ${ad(i+2+s8) if False else (i+2+s8)&0xFFFF if False else 0:04x}";ln=2;t=f"jr {s8:+d} (->{ad(i+2+s8):04x})"
        elif op&0xE7==0x20:t=f"jr {CC[(op>>3)&3]},{s8:+d} (->{ad(i+2+s8):04x})";ln=2
        elif op&0xC0==0x80:
            t=["add a,","adc a,","sub ","sbc a,","and ","xor ","or ","cp "][(op>>3)&7]+R8[op&7]
        elif op&0xC7==0xC6:
            t=["add a,","adc a,","sub ","sbc a,","and ","xor ","or ","cp "][(op>>3)&7]+f"${b1:02x}";ln=2
        elif op&0xE7==0xC0:t=f"ret {CC[(op>>3)&3]}"
        elif op==0xC9:t="ret"
        elif op==0xD9:t="reti"
        elif op&0xCF==0xC1:t=f"pop {R16S[(op>>4)&3]}"
        elif op&0xCF==0xC5:t=f"push {R16S[(op>>4)&3]}"
        elif op&0xE7==0xC2:t=f"jp {CC[(op>>3)&3]},${w:04x}";ln=3
        elif op==0xC3:t=f"jp ${w:04x}";ln=3
        elif op==0xE9:t="jp hl"
        elif op&0xE7==0xC4:t=f"call {CC[(op>>3)&3]},${w:04x}";ln=3
        elif op==0xCD:t=f"call ${w:04x}";ln=3
        elif op&0xC7==0xC7:t=f"rst ${op&0x38:02x}"
        elif op==0xE0:t=f"ldh [$ff{b1:02x}],a";ln=2
        elif op==0xF0:t=f"ldh a,[$ff{b1:02x}]";ln=2
        elif op==0xE2:t="ld [$ff00+c],a"
        elif op==0xF2:t="ld a,[$ff00+c]"
        elif op==0xEA:t=f"ld [${w:04x}],a";ln=3
        elif op==0xFA:t=f"ld a,[${w:04x}]";ln=3
        elif op==0xE8:t=f"add sp,{s8:+d}";ln=2
        elif op==0xF8:t=f"ld hl,sp{s8:+d}";ln=2
        elif op==0xF9:t="ld sp,hl"
        elif op==0xF3:t="di"
        elif op==0xFB:t="ei"
        elif op==0xCB:
            c=b1;ln=2
            g=["rlc","rrc","rl","rr","sla","sra","swap","srl"]
            if c<0x40:t=f"{g[c>>3]} {R8[c&7]}"
            else:t=f"{['','bit','res','set'][c>>6]} {(c>>3)&7},{R8[c&7]}"
        else:t=f"db ${op:02x}"
        out.append((i,rom[i:i+ln],t)); i+=ln
    return out
def show(rom, off, n):
    for o,b,t in dis(rom,off,n):
        a=0x4000+(o%0x4000) if o>=0x4000 else o
        print(f"{o//0x4000:02x}:{a:04x}  {b.hex():<8} {t}")
