"""Compare fabrication geometry (board profile, cutouts, drill holes) of our Gerber/Excellon output
against the original Altium PcbDoc, read directly (no KiCad importer involved).

usage: verify_fab.py <Madromys.PcbDoc> <gerber dir> [expected-deltas.txt]

The Altium "Board Outline" mechanical layer (board-level AND footprint-level primitives) is taken as
the fabrication profile, and every pad hole and via as a drill hit.
Anything that does not match within TOL is printed, so it can be explained or fixed.
"""
import sys, math
from altium_read import PcbDoc, U2MM
from gerber_read import read_profile, read_drill

TOL = 0.01  # mm
pcb, gdir = sys.argv[1], sys.argv[2]
p = PcbDoc(pcb)
OUTLINE = [k for k, v in p.layer_names.items() if v == 'Board Outline'][0]

# --- transform Altium -> Gerber, fitted from the board-level outline extents
A = [t for t in p.tracks() if t['layer'] == OUTLINE]
AA = [a for a in p.arcs() if a['layer'] == OUTLINE]
gprof = read_profile(f'{gdir}/Madromys-Edge_Cuts.gm1')
ax = [v * U2MM for t in A for v in (t['x1'], t['x2'])]; ay = [v * U2MM for t in A for v in (t['y1'], t['y2'])]
gx = [pt[0] for e in gprof for pt in e[1:3]]; gy = [pt[1] for e in gprof for pt in e[1:3]]
DX = min(gx) - min(ax); DY = max(gy) - max(ay)
T = lambda x, y: (x * U2MM + DX, y * U2MM + DY)
print(f'transform: gerber = altium + ({DX:.4f}, {DY:.4f}) mm')
close = lambda a, b: math.hypot(a[0] - b[0], a[1] - b[1]) < TOL

# --- 1. profile
exp = []
for t in A:
    exp.append(('line', T(t['x1'], t['y1']), T(t['x2'], t['y2']), p.designator(t['comp'])))
for a in AA:
    c = T(a['cx'], a['cy']); r = a['r'] * U2MM
    s = (c[0] + r * math.cos(math.radians(a['a0'])), c[1] + r * math.sin(math.radians(a['a0'])))
    e = (c[0] + r * math.cos(math.radians(a['a1'])), c[1] + r * math.sin(math.radians(a['a1'])))
    exp.append(('arc', s, e, p.designator(a['comp']), c))
used = set(); bad = 0
print('\n[1] profile: Altium Board Outline primitives not found in Edge_Cuts')
for e in exp:
    hit = None
    for i, g in enumerate(gprof):
        if g[0] != e[0]:
            continue
        if (close(g[1], e[1]) and close(g[2], e[2])) or (close(g[1], e[2]) and close(g[2], e[1])):
            if e[0] == 'arc' and not close(g[3], e[4]):
                continue
            hit = i; break
    if hit is None:
        bad += 1; print('   MISSING', e[0], 'owner', e[3] or 'board', [tuple(round(v, 4) for v in pt) for pt in e[1:3]])
    else:
        used.add(hit)
for i, g in enumerate(gprof):
    if i not in used:
        # tiny zero-length closing segments from the import are harmless; report anything longer
        L = math.hypot(g[1][0] - g[2][0], g[1][1] - g[2][1])
        if L > TOL:
            bad += 1; print('   EXTRA in Edge_Cuts', g[0], [tuple(round(v, 4) for v in pt) for pt in g[1:3]])
print('   ->', 'OK' if bad == 0 else f'{bad} difference(s)')

# --- 2. drill holes
want = []
for d in p.pads():
    if d['hole'] <= 0:
        continue
    x, y = T(d['x'], d['y']); dia = d['hole'] * U2MM
    kind = {0: 'round', 1: 'square', 2: 'slot', None: 'round'}[d['holeshape']]
    ln = d['slotsize'] * U2MM if kind == 'slot' else None
    ang = (d['rot'] + (d['slotrot'] or 0)) % 180 if kind == 'slot' else None
    want.append(dict(src=f"pad {p.designator(d['comp'])}:{d['name'] or '-'}", x=x, y=y, d=dia, plated=bool(d['plated']),
                     kind=kind, len=ln, ang=ang))
for v in p.vias():
    x, y = T(v['x'], v['y']); want.append(dict(src='via', x=x, y=y, d=v['hole'] * U2MM, plated=True, kind='round', len=None, ang=None))
have = [dict(h, plated=True) for h in read_drill(f'{gdir}/Madromys-PTH.drl')] + \
       [dict(h, plated=False) for h in read_drill(f'{gdir}/Madromys-NPTH.drl')]
for h in have:
    if h['x2'] is not None:   # slot: centre, length incl. tool diameter, angle
        h['cx'], h['cy'] = (h['x'] + h['x2']) / 2, (h['y'] + h['y2']) / 2
        h['len'] = math.hypot(h['x2'] - h['x'], h['y2'] - h['y']) + h['d']
        h['ang'] = math.degrees(math.atan2(h['y2'] - h['y'], h['x2'] - h['x'])) % 180
    else:
        h['cx'], h['cy'], h['len'], h['ang'] = h['x'], h['y'], None, None
print('\n[2] drill: Altium holes vs our PTH/NPTH files')
taken = set(); issues = 0
for w in want:
    cand = [i for i, h in enumerate(have) if i not in taken and close((h['cx'], h['cy']), (w['x'], w['y']))]
    if not cand:
        issues += 1; print(f"   MISSING {w['src']} at ({w['x']:.3f},{w['y']:.3f}) d={w['d']:.3f} {w['kind']} plated={w['plated']}"
                           + (f" len={w['len']:.3f}" if w['len'] else '')); continue
    i = cand[0]; h = have[i]; taken.add(i); notes = []
    if w['kind'] == 'square':
        notes.append(f"square {w['d']:.3f} hole in Altium (cannot be drilled; must be routed as a cutout)")
    if abs(h['d'] - w['d']) > TOL:
        notes.append(f"diameter {h['d']:.3f} vs Altium {w['d']:.3f}")
    if h['plated'] != w['plated']:
        notes.append(f"plated={h['plated']} vs Altium plated={w['plated']}")
    if (w['len'] is None) != (h['len'] is None) or (w['len'] and abs(w['len'] - h['len']) > TOL):
        notes.append(f"slot length {h['len']} vs Altium {w['len']}")
    if w['ang'] is not None and h['ang'] is not None and min(abs(w['ang'] - h['ang']), 180 - abs(w['ang'] - h['ang'])) > 0.5:
        notes.append(f"slot angle {h['ang']:.1f} vs Altium {w['ang']:.1f}")
    if notes:
        issues += 1; print(f"   DIFF {w['src']} at ({w['x']:.3f},{w['y']:.3f}): " + '; '.join(notes))
for i, h in enumerate(have):
    if i not in taken:
        issues += 1; print(f"   EXTRA hole at ({h['cx']:.3f},{h['cy']:.3f}) d={h['d']:.3f} plated={h['plated']}" + (f" slot len {h['len']:.3f}" if h['len'] else ''))
print(f"   Altium holes {len(want)}, our holes {len(have)} ->", 'OK' if issues == 0 else f'{issues} item(s) to review')
