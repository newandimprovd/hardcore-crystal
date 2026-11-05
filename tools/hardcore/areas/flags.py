"""Named event flags shared between generator modules: the first call allocates, later calls return the same name."""


def flag_once(w, name):
    d = w.__dict__.setdefault("named_flags", {})
    if name not in d:
        d[name] = w.flag(name)
    return d[name]
