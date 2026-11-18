"""Minimum distance from copper (all layers) and from silkscreen to the sensor cutout edge.
usage: edge_clearance.py <board.kicad_pcb>"""
import sys, pcbnew
from shapely.geometry import box, Polygon, LineString, Point
from shapely.ops import unary_union
b = pcbnew.LoadBoard(sys.argv[1]); T = pcbnew.ToMM
cut = box(144.2171, 106.9586, 152.8171, 124.6586)
def polys(sps):
    out = []
    for i in range(sps.OutlineCount()):
        o = sps.Outline(i); pts = [(T(o.CPoint(j).x), T(o.CPoint(j).y)) for j in range(o.PointCount())]
        if len(pts) >= 3: out.append(Polygon(pts).buffer(0))
    return out
res = {}
def add(name, geoms):
    for g in geoms:
        d = g.distance(cut) if not g.intersects(cut) else -g.intersection(cut).area
        if name not in res or d < res[name][0]: res[name] = (round(d, 3), g.representative_point().coords[0])
cu = [l for l in b.GetEnabledLayers().CuStack()]
for f in b.GetFootprints():
    for p in f.Pads():
        for lid in cu:
            if p.IsOnLayer(lid):
                s = pcbnew.SHAPE_POLY_SET(); p.TransformShapeToPolygon(s, lid, 0, pcbnew.FromMM(0.002))
                add(f'pad {b.GetLayerName(lid)}', polys(s))
for t in b.Tracks():
    if t.GetClass() == 'PCB_VIA':
        c = t.GetPosition(); add('via', [Point(T(c.x), T(c.y)).buffer(T(t.GetWidth()) / 2)])
    else:
        s, e = t.GetStart(), t.GetEnd()
        add(f'track {b.GetLayerName(t.GetLayer())}', [LineString([(T(s.x), T(s.y)), (T(e.x), T(e.y))]).buffer(T(t.GetWidth()) / 2)])
for z in b.Zones():
    for lid in z.GetLayerSet().Seq():
        if pcbnew.IsCopperLayer(lid):
            add(f'zone {z.GetNetname()} {b.GetLayerName(lid)}', polys(z.GetFilledPolysList(lid)))
for name, (d, at) in sorted(res.items(), key=lambda kv: kv[1][0]):
    print(f'{name:28s} min distance {d:7.3f} mm  near ({at[0]:.2f},{at[1]:.2f})' + ('   <-- OVERLAPS CUTOUT' if d < 0 else ''))
