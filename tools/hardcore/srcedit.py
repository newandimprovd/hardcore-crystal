"""Small source editing helpers for the removal work: every edit must match, so a stale pattern fails loudly instead of silently doing nothing."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _p(p):
    return os.path.join(ROOT, p)


def read(p):
    with open(_p(p)) as f:
        return f.read()


def write(p, s):
    with open(_p(p), "w") as f:
        f.write(s)


def sub(p, old, new="", count=1):
    s = read(p)
    n = s.count(old)
    assert n == count, f"{p}: expected {count} match(es) of {old[:70]!r}, found {n}"
    write(p, s.replace(old, new))


def del_lines(p, regex, count=None):
    """Delete every line that matches regex (a full-line pattern without the newline)."""
    out, n = [], 0
    for l in read(p).splitlines(keepends=True):
        if re.search(regex, l.rstrip("\n")):
            n += 1
            continue
        out.append(l)
    assert n and (count is None or n == count), f"{p}: {n} lines matched {regex!r}"
    write(p, "".join(out))
    return n


def del_block(p, label, keep_blank=True):
    """Delete a global label (Name: or Name::) and everything under it up to the next global label, INCLUDE or SECTION line."""
    lines = read(p).splitlines(keepends=True)
    start = next((i for i, l in enumerate(lines) if re.match(rf"{re.escape(label)}::?(\s|$)", l)), None)
    assert start is not None, f"{p}: label {label} not found"
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if re.match(r"[A-Za-z_][A-Za-z0-9_]*::?(\s|$)", lines[j]) or re.match(r"(INCLUDE|SECTION)\b", lines[j]):
            end = j
            break
    # take the comment lines right above the label with it
    while start > 0 and lines[start - 1].startswith(";"):
        start -= 1
    del lines[start:end]
    write(p, re.sub(r"\n{3,}", "\n\n", "".join(lines)))


def del_range(p, first, last):
    """Delete from the line that contains `first` up to and including the line that contains `last` (both must be unique)."""
    lines = read(p).splitlines(keepends=True)
    a = [i for i, l in enumerate(lines) if first in l]
    b = [i for i, l in enumerate(lines) if last in l]
    assert len(a) == 1 and len(b) >= 1, f"{p}: {first!r} {len(a)}x, {last!r} {len(b)}x"
    b = next(i for i in b if i >= a[0])
    del lines[a[0]:b + 1]
    write(p, "".join(lines))
