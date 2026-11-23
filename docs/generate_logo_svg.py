"""Rebuild the BJP horizontal logo as clean SVG (replaces the jagged PNGs).

The mark is drawn from its geometry: a 3x3 grid with grey dots at the corners and
centre, and two "bone" shapes linking top-middle to middle-right and middle-left to
bottom-middle. The wordmark is Open Sans (weight 680, width 90, matching the original) converted to outlines, so the file
renders identically everywhere without loading a font.

Usage (needs fontTools and an Open Sans variable TTF from google/fonts):
    python docs/generate_logo_svg.py path/to/OpenSans[wdth,wght].ttf static/images/logo
"""

import math
import sys
from io import BytesIO
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

WIDTH, HEIGHT = 692, 73  # same box as the old PNGs, so existing CSS sizes still fit
TEXT = "BJP TECHNOLOGIES (T) LTD"
TEXT_X, TEXT_RIGHT, BASELINE, CAP_HEIGHT = 110, 681, 50, 36
MARK_X, MARK_Y, MARK_SIZE = 6, 5, 63

VARIANTS = {
    # name: (strokes + text colour, dot colour)
    "bjp-logo-horizontal-light.svg": ("#EFE9DF", "#C8C3B8"),  # on navy backgrounds
    "bjp-logo-horizontal-dark.svg": ("#061F60", "#A0A1A6"),  # on light backgrounds
}


def bone(a, b, r):
    """Two circles joined by a smooth concave neck (metaball look)."""
    ux, uy = (b[0] - a[0]), (b[1] - a[1])
    length = math.hypot(ux, uy)
    ux, uy = ux / length, uy / length
    nx, ny = -uy, ux
    theta = math.radians(58)

    def on_circle(c, dirx, diry, sign):
        cos, sin = math.cos(theta), math.sin(theta) * sign
        return (c[0] + r * (dirx * cos - diry * sin), c[1] + r * (diry * cos + dirx * sin))

    a1, a2 = on_circle(a, ux, uy, 1), on_circle(a, ux, uy, -1)
    b1, b2 = on_circle(b, -ux, -uy, -1), on_circle(b, -ux, -uy, 1)
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    w = r * 0.22
    c1 = (mx + nx * w, my + ny * w)
    c2 = (mx - nx * w, my - ny * w)
    f = lambda p: f"{p[0]:.2f},{p[1]:.2f}"  # noqa: E731
    return (
        f"M{f(a1)}Q{f(c1)} {f(b1)}A{r:.2f},{r:.2f} 0 1,0 {f(b2)}"
        f"Q{f(c2)} {f(a2)}A{r:.2f},{r:.2f} 0 1,0 {f(a1)}Z"
    )


def mark(stroke, dot):
    s = MARK_SIZE / 2.66  # grid spacing; dot radius is a third of it
    r = s * 0.33
    centre = lambda col, row: (MARK_X + r + col * s, MARK_Y + r + row * s)  # noqa: E731
    dots = "".join(
        f'<circle cx="{centre(c, w)[0]:.2f}" cy="{centre(c, w)[1]:.2f}" r="{r:.2f}"/>'
        for c, w in [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]
    )
    bones = bone(centre(1, 0), centre(2, 1), r) + bone(centre(0, 1), centre(1, 2), r)
    return f'<g fill="{dot}">{dots}</g><path fill="{stroke}" d="{bones}"/>'


def wordmark(font_path):
    font = TTFont(font_path)
    font = instantiateVariableFont(font, {"wght": 680, "wdth": 90})
    buf = BytesIO()
    font.save(buf)
    font = TTFont(BytesIO(buf.getvalue()))
    glyphs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font["hmtx"]
    scale = CAP_HEIGHT / font["OS/2"].sCapHeight
    names = [cmap[ord(ch)] for ch in TEXT]
    natural = sum(hmtx[n][0] for n in names[:-1]) * scale
    last = glyphs[names[-1]]
    from fontTools.pens.boundsPen import BoundsPen

    bp = BoundsPen(glyphs)
    last.draw(bp)
    natural += bp.bounds[2] * scale
    spacing = (TEXT_RIGHT - TEXT_X - natural) / (len(TEXT) - 1)
    pen = SVGPathPen(glyphs)
    x = TEXT_X
    for name in names:
        tp = TransformPen(pen, (scale, 0, 0, -scale, x, BASELINE))
        glyphs[name].draw(tp)
        x += hmtx[name][0] * scale + spacing
    return pen.getCommands()


def main():
    font_path, out_dir = sys.argv[1], Path(sys.argv[2])
    text_path = wordmark(font_path)
    for filename, (stroke, dot) in VARIANTS.items():
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
            f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="BJP Technologies (T) Ltd">'
            f'{mark(stroke, dot)}<path fill="{stroke}" d="{text_path}"/></svg>\n'
        )
        (out_dir / filename).write_text(svg)
        print(out_dir / filename, len(svg), "bytes")


if __name__ == "__main__":
    main()
