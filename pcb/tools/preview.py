"""Render a 4-panel preview (top, bottom seen from below, plane 1, plane 2) from Gerber files.
usage: preview.py <gerber prefix> <out.png>"""
import sys, subprocess, os, tempfile
from PIL import Image, ImageDraw, ImageFont

P, OUT = sys.argv[1], sys.argv[2]
x0, y0, x1, y1 = 117.4761 - 1.5, 70.9786 - 1.5, 179.5261 + 1.5, 139.0286 + 1.5
W = 1465
dpi = W / ((x1 - x0) / 25.4)
tmp = tempfile.mkdtemp()


def render(name, layers):
    out = os.path.join(tmp, name + '.png')
    args = ['gerbv', '-x', 'png', '-o', out, f'--dpi={dpi:.3f}', '-O', f'{x0/25.4:.4f}x{-y1/25.4:.4f}',
            '-W', f'{(x1-x0)/25.4:.4f}x{(y1-y0)/25.4:.4f}', '-b', '#1a1a1a']
    for f, c in layers:
        args += [P + f, '-f', c]
    subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return Image.open(out).convert('RGB')


drill = [('-PTH.drl', '#1a1a1aff'), ('-NPTH.drl', '#1a1a1aff')]
edge = [('-Edge_Cuts.gm1', '#f0f0f0ff')]
top = render('top', drill + edge + [('-Top_Overlay.gto', '#f0f0f0ff'), ('-Top_Mask.gts', '#c8a03cff'),
                                    ('-Top_Layer.gtl', '#2f7a45ff')])
bot = render('bot', drill + edge + [('-Bottom_Overlay.gbo', '#f0f0f0ff'), ('-Bottom_Solder.gbs', '#c8a03cff'),
                                    ('-Bottom_Layer.gbl', '#2f7a45ff')]).transpose(Image.FLIP_LEFT_RIGHT)
p1 = render('p1', drill + edge + [('-Plane_1.g2', '#c87533ff')])
p2 = render('p2', drill + edge + [('-Plane_2.g3', '#c87533ff')])
H = top.height
G, T = 30, 60
img = Image.new('RGB', (2 * W + 3 * G, 2 * (H + T) + 2 * G), (26, 26, 26))
d = ImageDraw.Draw(img)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 40)
for i, (im, title) in enumerate(((top, 'L1 Top'), (bot, 'L4 Bottom, viewed from below'),
                                 (p1, 'L2 Plane 1 (GND)'), (p2, 'L3 Plane 2 (GND / 3V3)'))):
    x = G + (i % 2) * (W + G)
    y = G + (i // 2) * (H + T + G)
    d.text((x, y), title, fill=(240, 240, 240), font=font)
    img.paste(im, (x, y + T))
img.save(OUT)
print(OUT, img.size)
