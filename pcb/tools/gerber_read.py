"""Minimal readers for the Gerber profile (Edge_Cuts) and Excellon drill files we generate."""
import re, math


def read_profile(path):
    """Return a list of ('line', (x1,y1), (x2,y2)) and ('arc', start, end, center, cw) in mm (Gerber Y up)."""
    s = open(path).read()
    m = re.search(r'%FSLAX(\d)(\d)Y(\d)(\d)\*%', s); dec = int(m.group(2))
    k = 10 ** -dec
    mode = 'G01'; x = y = None; out = []
    for cmd in re.split(r'\*\s*', s):
        cmd = cmd.strip().lstrip('%')
        for g in re.findall(r'G0[123]', cmd):
            mode = g
        mm = re.search(r'X(-?\d+)Y(-?\d+)(?:I(-?\d+)J(-?\d+))?D0([123])', cmd)
        if not mm:
            continue
        nx, ny = int(mm.group(1)) * k, int(mm.group(2)) * k
        d = mm.group(5)
        if d == '1':
            if mode == 'G01':
                out.append(('line', (x, y), (nx, ny)))
            else:
                cx, cy = x + int(mm.group(3)) * k, y + int(mm.group(4)) * k
                out.append(('arc', (x, y), (nx, ny), (cx, cy), mode == 'G02'))
        x, y = nx, ny
    return out


def read_drill(path):
    """Return list of dict(d, x, y, x2, y2) in mm; x2/y2 set for slots."""
    tools = {}; cur = None; out = []
    for line in open(path):
        line = line.strip()
        m = re.match(r'T(\d+)C([\d.]+)', line)
        if m:
            tools[m.group(1)] = float(m.group(2)); continue
        m = re.fullmatch(r'T(\d+)', line)
        if m:
            cur = tools.get(m.group(1)); continue
        m = re.fullmatch(r'X(-?[\d.]+)Y(-?[\d.]+)G85X(-?[\d.]+)Y(-?[\d.]+)', line)
        if m:
            a = list(map(float, m.groups())); out.append(dict(d=cur, x=a[0], y=a[1], x2=a[2], y2=a[3])); continue
        m = re.fullmatch(r'X(-?[\d.]+)Y(-?[\d.]+)', line)
        if m and cur is not None:
            out.append(dict(d=cur, x=float(m.group(1)), y=float(m.group(2)), x2=None, y2=None))
    return out
