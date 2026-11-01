"""Contact-sheet helper: render plans/recipes with a palette and save them scaled up next to each other."""
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

PALS = {
    "rock": [(255, 255, 255), (120, 134, 170), (52, 58, 104), (0, 0, 0)],
    "green": [(255, 255, 255), (120, 200, 72), (40, 104, 56), (0, 0, 0)],
    "purple": [(255, 255, 255), (160, 112, 216), (80, 40, 136), (0, 0, 0)],
    "fire": [(255, 255, 255), (248, 152, 56), (176, 48, 32), (0, 0, 0)],
    "bone": [(255, 255, 255), (216, 184, 120), (120, 72, 40), (0, 0, 0)],
    "teal": [(255, 255, 255), (64, 184, 200), (24, 80, 136), (0, 0, 0)],
    "blood": [(255, 255, 255), (200, 64, 72), (96, 24, 56), (0, 0, 0)],
}


def sheet(items, path, scale=5, bg=(70, 100, 140)):
    """items: list of (img, palname) with img a 2D index array."""
    w = sum(i.shape[1] * scale + 8 for i, _ in items) + 8
    h = max(i.shape[0] for i, _ in items) * scale + 16
    out = Image.new("RGB", (w, h), bg)
    x = 8
    for img, pn in items:
        pal = PALS[pn] if isinstance(pn, str) else pn
        rgb = np.array(pal, np.uint8)[img]
        im = Image.fromarray(rgb).resize((img.shape[1] * scale, img.shape[0] * scale), Image.NEAREST)
        out.paste(im, (x, 8))
        x += img.shape[1] * scale + 8
    out.save(path)
