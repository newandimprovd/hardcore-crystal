"""Base class for an area spec: trainer classes with their overworld sprites, the type theme and level range."""


class SpecBase:
    pool = ""
    l0, l1 = 5, 24
    theme = {}
    classes = []
    T = None  # the area's text module (SEEN, BEATEN, AFTER)
    extra_sprites = ["SPRITE_POKE_BALL", "SPRITE_ROCK", "SPRITE_BOULDER", "SPRITE_FRUIT_TREE"]

    @property
    def sprites(self):
        return sorted({c[1] for c in self.classes}) + self.extra_sprites

    def pick_class(self, rng):
        total = sum(c[3] for c in self.classes)
        r = rng.uniform(0, total)
        for c in self.classes:
            r -= c[3]
            if r <= 0:
                return c[0], c[1], c[2]
        return self.classes[0][:3]

    def size_progress(self, prog):
        return prog
