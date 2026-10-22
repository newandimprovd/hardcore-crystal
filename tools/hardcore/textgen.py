"""Text helpers shared by the Hardcore Crystal generators.

Crystal text boxes are 18 characters wide and two lines tall. wrap_pages() word-wraps a
string into pages of two lines, and emit_text() turns pages into text/line/para macros.
<PLAYER> and friends expand to at most 7 characters, so they are measured as 7.
"""
import re

WIDTH = 18
TOKEN = re.compile(r"<[A-Z_]+>")


def vis_len(s):
    """On-screen length of a string, counting each <TOKEN> as 7 characters."""
    return len(TOKEN.sub("xxxxxxx", s))


def wrap_lines(text, width=WIDTH):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if vis_len(w) > width:
            raise ValueError(f"word too long for a text box: {w!r}")
        cand = w if not cur else cur + " " + w
        if vis_len(cand) <= width:
            cur = cand
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def wrap_pages(text):
    """Split text into pages of up to two lines. Paragraph breaks in the source are '\n\n'."""
    pages = []
    for para in re.split(r"\n\s*\n", text.strip()):
        lines = wrap_lines(" ".join(para.split()))
        for i in range(0, len(lines), 2):
            pages.append(lines[i:i + 2])
    return pages


def esc(s):
    return s.replace('"', '\\"')


def emit_text(label, text, end="done"):
    """Return assembly for a text block. Every page after the first starts with para."""
    pages = wrap_pages(text)
    out = [f"{label}:"]
    for pi, page in enumerate(pages):
        first = "text" if pi == 0 else "para"
        out.append(f'\t{first} "{esc(page[0])}"')
        if len(page) > 1:
            out.append(f'\tline "{esc(page[1])}"')
    out.append(f"\t{end}")
    return "\n".join(out) + "\n"


def emit_string(label, text):
    """A plain db string pool entry (text_asm callers): lines joined with 'next', ended with @."""
    lines = wrap_lines(" ".join(text.split()))
    out = [f"{label}:"]
    for i, ln in enumerate(lines):
        out.append(f'\t{"db  " if i == 0 else "next"} "{esc(ln)}{"@" if i == len(lines) - 1 else ""}"')
    return "\n".join(out) + "\n"
