"""Independent reader for an Altium PcbDoc (no KiCad involved).

Reads the binary primitive streams directly and returns geometry in Altium units
(1 unit = 1/10000 mil, Y axis pointing up).
"""
import olefile, struct, re

U2MM = 25.4 / 10000000.0  # 1 unit = 1/10000 mil = 1e-7 inch = 2.54e-6 mm


def _records(data, rtype):
    """Yield the payload of each binary primitive record of the given type."""
    i = 0
    while i < len(data):
        t = data[i]; n = struct.unpack_from('<I', data, i + 1)[0]
        payload = data[i + 5:i + 5 + n]
        i += 5 + n
        if t != rtype:
            raise ValueError(f'unexpected record type {t} (expected {rtype}) at {i}')
        yield payload


def _props(blob):
    s = blob.decode('latin1', 'replace')
    return dict(re.findall(r'\|?([A-Za-z0-9_]+)=([^|]*)', s))


class PcbDoc:
    def __init__(self, path):
        self.o = olefile.OleFileIO(path)
        board = self.o.openstream('Board6/Data').read()
        self.board = _props(board[4:])
        self.layer_names = {}
        for k, v in self.board.items():
            m = re.fullmatch(r'LAYER(\d+)NAME', k)
            if m:
                self.layer_names[int(m.group(1))] = v
        self.components = self._components()

    def stream(self, name):
        return self.o.openstream(name + '/Data').read()

    def _components(self):
        data = self.stream('Components6'); out = []; i = 0
        while i < len(data):
            n = struct.unpack_from('<I', data, i)[0]
            out.append(_props(data[i + 4:i + 4 + n])); i += 4 + n
        return out

    def designator(self, comp_index):
        if comp_index == 0xFFFF:
            return None
        c = self.components[comp_index]
        return c.get('SOURCEDESIGNATOR') or c.get('NAME') or str(comp_index)

    def tracks(self):
        for d in _records(self.stream('Tracks6'), 4):
            layer = d[0]; net, poly, comp = struct.unpack_from('<HHH', d, 3)
            x1, y1, x2, y2 = struct.unpack_from('<iiii', d, 13)
            w = struct.unpack_from('<I', d, 29)[0]
            yield dict(layer=layer, net=net, comp=comp, x1=x1, y1=y1, x2=x2, y2=y2, w=w)

    def arcs(self):
        for d in _records(self.stream('Arcs6'), 1):
            layer = d[0]; net, poly, comp = struct.unpack_from('<HHH', d, 3)
            cx, cy = struct.unpack_from('<ii', d, 13)
            r = struct.unpack_from('<I', d, 21)[0]
            a0, a1 = struct.unpack_from('<dd', d, 25)
            w = struct.unpack_from('<I', d, 41)[0]
            yield dict(layer=layer, net=net, comp=comp, cx=cx, cy=cy, r=r, a0=a0, a1=a1, w=w)

    def vias(self):
        for d in _records(self.stream('Vias6'), 3):
            net = struct.unpack_from('<H', d, 3)[0]
            x, y, dia, hole = struct.unpack_from('<iiII', d, 13)
            yield dict(net=net, x=x, y=y, dia=dia, hole=hole)


def _pads(self):
    """Pads6: each pad is a type-2 record made of 6 length-prefixed subrecords."""
    data = self.stream('Pads6'); i = 0
    while i < len(data):
        t = data[i]; i += 1
        assert t == 2, t
        subs = []
        for k in range(6):
            n = struct.unpack_from('<I', data, i)[0]; i += 4
            subs.append(data[i:i + n]); i += n
        name = subs[0][1:1 + subs[0][0]].decode('latin1') if subs[0] else ''
        d = subs[4]
        layer = d[0]; net = struct.unpack_from('<H', d, 3)[0]; comp = struct.unpack_from('<H', d, 7)[0]
        x, y = struct.unpack_from('<ii', d, 13)
        tsx, tsy = struct.unpack_from('<ii', d, 21)
        hole = struct.unpack_from('<I', d, 45)[0]
        tshape = d[49]; rot = struct.unpack_from('<d', d, 52)[0]; plated = d[60]
        holeshape, slotsize = None, None
        s6 = subs[5]
        if len(s6) >= 275:
            # sizes-and-shapes subrecord (same layout as KiCad's Altium importer reads it):
            # 29 x-sizes, 29 y-sizes (int32), 29 shapes (u8), 1 skipped byte, then
            # hole shape (u8: 0 round, 1 square, 2 slot), slot size (int32), slot rotation (double)
            off = 29 * 4 * 2 + 29 + 1
            holeshape = s6[off]
            slotsize = struct.unpack_from('<i', s6, off + 1)[0]
            slotrot = struct.unpack_from('<d', s6, off + 5)[0]
        else:
            slotrot = None
        yield dict(name=name, layer=layer, net=net, comp=comp, x=x, y=y, sx=tsx, sy=tsy, hole=hole,
                   shape=tshape, rot=rot, plated=plated, holeshape=holeshape, slotsize=slotsize, slotrot=slotrot, s6len=len(s6))


PcbDoc.pads = _pads
