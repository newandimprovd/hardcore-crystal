"""Painting helpers shared by the area tilesets (all coordinates are pixels on a 32x32 block canvas)."""
from tilebuild import Canvas, GRAY


def brick(cv, cx, cy, cw=1, ch=1, mortar=2, hi=1, base=0, offset=0):
    """Running-bond brick, tile-periodic (so every cell dedupes): bricks 8x4, courses offset by 4."""
    for y in range(cy * 8, (cy + ch) * 8):
        for x in range(cx * 8, (cx + cw) * 8):
            X, Y = x % 8, y % 8
            jx = (0 if Y < 4 else 4 + offset) % 8
            v = base
            if Y % 4 == 3:
                v = mortar
            elif X == jx:
                v = mortar
            elif Y % 4 == 0 and X == (jx + 2) % 8 and hi is not None:
                v = hi
            cv.set(x, y, v)


def slabs(cv, cx, cy, cw=1, ch=1, stone=1, gap=0, shade=2):
    """Cobbles: stones 3 wide, courses offset by 2; gap rows between courses."""
    for y in range(cy * 8, (cy + ch) * 8):
        for x in range(cx * 8, (cx + cw) * 8):
            X, Y = x % 8, y % 8
            if Y < 4:
                gx = X % 4 == 3
            else:
                gx = X in (1, 5)
            if Y % 4 == 3 or gx:
                v = gap
            elif Y % 4 == 2:
                v = shade
            else:
                v = stone
            cv.set(x, y, v)


def pointed_arch(cv, x, y, w, h, glass=1, dark=2, line=3, lattice=True, base=0):
    """A pointed gothic window with a mullion and a transom; (x, y) is the top-left of its bounding box."""
    cx = x + w // 2
    for yy in range(h):
        # half width of the opening at this row: pointed top for the first w//2 + 1 rows
        top = w // 2 + 2
        if yy < top:
            half = max(0, int((yy + 1) * (w / 2) / top + 0.5))
        else:
            half = w // 2
        x0, x1 = cx - half, cx + half - (1 if w % 2 == 0 else 0)
        if w % 2 == 0:
            x0 = cx - half
            x1 = cx + half - 1
        for xx in range(x0, x1 + 1):
            edge = xx in (x0, x1) or yy == 0 or yy == h - 1
            cv.set(xx, y + yy, line if edge else glass)
    # mullion and transom
    if lattice:
        mid = x + (w - 1) // 2
        cv.vline(mid, y + 4, h - 5, dark)
        if w % 2 == 0:
            cv.vline(mid + 1, y + 4, h - 5, dark)
        cv.hline(x + 1, y + h // 2 + 1, w - 2, dark)


def sill(cv, x, y, w, hi=1, shade=2, line=3):
    cv.hline(x, y, w, hi)
    cv.hline(x, y + 1, w, shade)
    cv.hline(x, y + 2, w, line)


def rose(cv, cx, cy, r, glass=1, dark=2, line=3, spokes=8):
    cv.disc(cx, cy, r, line)
    cv.disc(cx, cy, r - 1, glass)
    # spokes
    import math
    for k in range(spokes):
        a = 2 * math.pi * k / spokes
        cv.line(cx, cy, int(round(cx + (r - 1) * math.cos(a))), int(round(cy + (r - 1) * math.sin(a))), dark)
    cv.disc(cx, cy, 1, line)
