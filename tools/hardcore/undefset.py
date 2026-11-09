#!/usr/bin/env python3
"""Print the undefined symbols of the last build (builderrs.log), one per line; 'file' mode prints file:line chains."""
import re, sys
log = open("/home/claude/scratch/builderrs.log", errors="replace").read()
syms = sorted(set(re.findall(r"[Uu]ndefined symbol `([^`]+)`", log)))
print("\n".join(syms))
