"""Generate the BJP-branded site images (navy/blue/cyan line art).

Usage: python docs/generate_brand_images.py static/images
Requires Pillow (dev-only, not a site dependency)."""

import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

OUT = Path(sys.argv[1])
DARK, NAVY, MID = (8, 15, 46), (13, 27, 75), (19, 34, 96)
CYAN, BLUE, BLUEL = (0, 198, 255), (21, 101, 192), (30, 136, 229)
SS = 2  # supersample factor for line art


def background(W, H, glow_at, seed, tone=0.0):
    """Navy gradient, soft cyan/blue glow, faint grid, node network, grain."""
    rnd = random.Random(seed)
    g = Image.linear_gradient("L").rotate(-90, expand=True).resize((W, H))
    img = Image.composite(Image.new("RGB", (W, H), MID), Image.new("RGB", (W, H), DARK), g)
    if tone:
        img = Image.blend(img, Image.new("RGB", (W, H), NAVY), tone)
    glow = Image.new("RGB", (W, H))
    gd = ImageDraw.Draw(glow)
    gx, gy = glow_at[0] * W, glow_at[1] * H
    r = max(W, H) * 0.28
    gd.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(0, 85, 140))
    r2 = r * 0.7
    gd.ellipse([gx - r2 * 1.8, gy, gx, gy + r2 * 1.6], fill=(21, 55, 145))
    img = ImageChops.add(img, glow.filter(ImageFilter.GaussianBlur(max(W, H) * 0.09)))
    ov = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(ov)
    step = max(64, W // 30)
    for x in range(0, W, step):
        d.line([(x, 0), (x, H)], fill=(120, 160, 255, 9))
    for y in range(0, H, step):
        d.line([(0, y), (W, y)], fill=(120, 160, 255, 9))
    nodes = []
    n = int(W * H / 40000)
    while len(nodes) < n:
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        dist = math.hypot(x - gx, y - gy) / max(W, H)
        if rnd.random() < max(0.08, 1 - dist * 1.6):
            nodes.append((x, y))
    lim = max(W, H) * 0.09
    for i, a in enumerate(nodes):
        for b in nodes[i + 1 :]:
            dd = math.dist(a, b)
            if dd < lim:
                d.line([a, b], fill=(*CYAN, int(55 * (1 - dd / lim))), width=2)
    for x, y in nodes:
        rr = rnd.choice([3, 4, 5, 6])
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(*CYAN, rnd.randint(70, 190)))
    img = Image.alpha_composite(img.convert("RGBA"), ov)
    return img


class Pen:
    """Line-art drawer on a supersampled RGBA layer, in unit coordinates
    centred on (cx, cy) with scale s (pixels per unit)."""

    def __init__(self, W, H, cx, cy, s):
        self.layer = Image.new("RGBA", (W * SS, H * SS))
        self.d = ImageDraw.Draw(self.layer)
        self.cx, self.cy, self.s = cx * SS, cy * SS, s * SS
        self.W, self.H = W, H

    def p(self, x, y):
        return (self.cx + x * self.s, self.cy + y * self.s)

    def w(self, k=1.0):
        return max(2, int(self.s * 0.035 * k))

    def line(self, pts, col=CYAN, a=230, k=1.0):
        self.d.line([self.p(*q) for q in pts], fill=(*col, a), width=self.w(k), joint="curve")

    def rect(self, x0, y0, x1, y1, col=CYAN, a=230, k=1.0, fill=None, r=0.06):
        self.d.rounded_rectangle(
            [self.p(x0, y0), self.p(x1, y1)],
            radius=int(min(r, abs(y1 - y0) / 2.5, abs(x1 - x0) / 2.5) * self.s),
            outline=(*col, a),
            width=self.w(k),
            fill=fill,
        )

    def circle(self, x, y, r, col=CYAN, a=230, k=1.0, fill=None):
        self.d.ellipse(
            [self.p(x - r, y - r), self.p(x + r, y + r)],
            outline=(*col, a) if k else None,
            width=self.w(k),
            fill=fill,
        )

    def arc(self, x, y, r, a0, a1, col=CYAN, a=230, k=1.0):
        self.d.arc(
            [self.p(x - r, y - r), self.p(x + r, y + r)], a0, a1, fill=(*col, a), width=self.w(k)
        )

    def poly(self, pts, col=CYAN, a=230, k=1.0, fill=None):
        self.d.polygon([self.p(*q) for q in pts], outline=(*col, a), fill=fill, width=self.w(k))

    def dot(self, x, y, r=0.04, col=CYAN, a=255):
        self.circle(x, y, r, k=0, fill=(*col, a))

    def done(self):
        return self.layer.resize((self.W, self.H), Image.LANCZOS)


FILL = (*BLUE, 70)
FILL2 = (*CYAN, 40)


def rings(pen, r=1.25):
    for k, rr in enumerate([r, r * 1.22, r * 1.45]):
        pen.circle(0, 0, rr, a=70 - k * 22, k=0.5)
    for ang in (20, 140, 260):
        t = math.radians(ang)
        pen.dot(r * math.cos(t), r * math.sin(t), 0.05)


# ---- glyphs: each draws roughly within [-1, 1] ----
def g_code(p):
    p.rect(-1, -0.75, 1, 0.75, fill=FILL)
    p.line([(-1, -0.45), (1, -0.45)], k=0.7)
    for i, x in enumerate((-0.85, -0.72, -0.59)):
        p.dot(x, -0.6, 0.035, a=200)
    p.line([(-0.35, -0.15), (-0.6, 0.12), (-0.35, 0.39)], k=1.3)
    p.line([(0.35, -0.15), (0.6, 0.12), (0.35, 0.39)], k=1.3)
    p.line([(0.12, -0.2), (-0.12, 0.44)], col=BLUEL, k=1.3)


def g_web(p):
    p.rect(-1, -0.75, 1, 0.75, fill=FILL)
    p.line([(-1, -0.45), (1, -0.45)], k=0.7)
    p.rect(-0.7, -0.6, 0.85, -0.52, a=120, k=0.5, r=0.03)
    p.rect(-0.85, -0.3, 0.05, 0.25, col=BLUEL, fill=FILL2)
    for y in (-0.25, -0.1, 0.05):
        p.line([(0.2, y), (0.85, y)], a=170, k=0.8)
    p.rect(0.2, 0.15, 0.6, 0.27, fill=(*CYAN, 160), k=0.5)
    for x in (-0.85, -0.3, 0.25):
        p.rect(x, 0.38, x + 0.5, 0.62, a=150, k=0.6)


def g_cloud(p):
    p.arc(-0.45, -0.05, 0.4, 150, 290)
    p.arc(0.05, -0.3, 0.5, 200, 340)
    p.arc(0.55, 0.05, 0.38, 270, 70)
    p.line([(-0.78, 0.4), (0.62, 0.4)])
    p.arc(-0.78, 0.15, 0.25, 90, 200)
    p.arc(0.62, 0.17, 0.23, 300, 90)
    for i, x in enumerate((-0.45, 0.0, 0.45)):
        p.line([(x, 0.4), (x, 0.62)], a=160, k=0.7)
        p.rect(x - 0.17, 0.62, x + 0.17, 0.88, col=BLUEL, fill=FILL, r=0.03)
        p.dot(x - 0.08, 0.75, 0.03)


def g_shield(p):
    pts = [(0, -1), (0.8, -0.7), (0.75, 0.15), (0, 1), (-0.75, 0.15), (-0.8, -0.7)]
    p.poly(pts, fill=FILL, k=1.2)
    p.poly([(x * 0.78, y * 0.78 + 0.02) for x, y in pts], a=90, k=0.5)
    p.rect(-0.28, -0.05, 0.28, 0.42, fill=(*CYAN, 60), r=0.05)
    p.arc(0, -0.05, 0.18, 180, 360, k=1.1)
    p.line([(-0.18, -0.05), (-0.18, -0.07)])
    p.line([(0.18, -0.05), (0.18, -0.07)])
    p.dot(0, 0.15, 0.06)
    p.line([(0, 0.15), (0, 0.3)], k=1.1)


def g_monitor(p):
    p.rect(-1, -0.75, 1, 0.5, fill=FILL)
    p.line([(-0.15, 0.5), (-0.22, 0.78)])
    p.line([(0.15, 0.5), (0.22, 0.78)])
    p.line([(-0.45, 0.8), (0.45, 0.8)], k=1.2)
    p.line(
        [
            (-0.85, -0.1),
            (-0.4, -0.1),
            (-0.25, -0.5),
            (-0.05, 0.3),
            (0.12, -0.25),
            (0.25, -0.1),
            (0.85, -0.1),
        ],
        k=1.2,
    )
    p.dot(0.85, -0.1, 0.06)
    p.circle(0.72, -0.5, 0.12, col=BLUEL, a=200, k=0.8)


def g_payment(p):
    p.rect(-0.95, -0.85, -0.15, 0.85, fill=FILL, r=0.12)
    p.line([(-0.68, -0.72), (-0.42, -0.72)], a=170, k=0.7)
    p.circle(-0.55, 0.68, 0.06, a=170, k=0.6)
    p.rect(-0.8, -0.5, -0.3, -0.05, col=BLUEL, fill=FILL2, r=0.04)
    p.line([(-0.72, 0.1), (-0.38, 0.1)], a=150, k=0.7)
    p.line([(-0.72, 0.25), (-0.48, 0.25)], a=150, k=0.7)
    p.rect(0.05, -0.15, 1.0, 0.45, fill=(*BLUE, 110), r=0.06)
    p.line([(0.05, 0.0), (1.0, 0.0)], k=1.5)
    p.rect(0.15, 0.15, 0.35, 0.3, a=180, k=0.6, r=0.02)
    p.circle(0.72, 0.28, 0.08, a=200, k=0.6)
    p.circle(0.84, 0.28, 0.08, a=200, k=0.6)
    for k, y in enumerate((-0.6, -0.42)):
        p.line([(-0.05, y), (0.35 + k * 0.2, y)], a=200, k=0.8)
    p.line([(0.27, -0.68), (0.37, -0.6), (0.27, -0.52)], a=200, k=0.8)


def g_consult(p):
    p.line([(-1, 0.85), (1, 0.85)], a=180)
    for i, h in enumerate((0.35, 0.6, 0.5, 0.95)):
        x = -0.8 + i * 0.45
        p.rect(x, 0.85 - h, x + 0.28, 0.85, col=BLUEL, fill=FILL, r=0.02, k=0.8)
    p.line([(-0.8, 0.1), (-0.3, -0.2), (0.15, -0.05), (0.85, -0.75)], k=1.3)
    p.line([(0.55, -0.75), (0.85, -0.75), (0.85, -0.45)], k=1.3)
    for x, y in ((-0.8, 0.1), (-0.3, -0.2), (0.15, -0.05)):
        p.dot(x, y, 0.06)


def g_rocket(p):
    p.poly([(0, -1), (0.32, -0.55), (0.32, 0.35), (-0.32, 0.35), (-0.32, -0.55)], fill=FILL, k=1.1)
    p.circle(0, -0.3, 0.14, k=0.9, fill=FILL2)
    p.poly([(-0.32, 0.0), (-0.62, 0.42), (-0.32, 0.35)], col=BLUEL, fill=FILL)
    p.poly([(0.32, 0.0), (0.62, 0.42), (0.32, 0.35)], col=BLUEL, fill=FILL)
    for x, ln in ((-0.15, 0.3), (0, 0.5), (0.15, 0.3)):
        p.line([(x, 0.45), (x, 0.45 + ln)], a=170, k=0.8)


def g_bank(p):
    p.poly([(-1, -0.4), (0, -0.95), (1, -0.4)], fill=FILL, k=1.1)
    p.line([(-0.95, -0.3), (0.95, -0.3)])
    for x in (-0.7, -0.25, 0.25, 0.7):
        p.line([(x, -0.2), (x, 0.55)], col=BLUEL, k=1.4)
    p.line([(-0.95, 0.65), (0.95, 0.65)])
    p.line([(-1, 0.85), (1, 0.85)], k=1.2)
    p.circle(0, -0.6, 0.09, k=0.7)


def g_globe(p):
    p.circle(0, -0.1, 0.8, fill=FILL, k=1.1)
    p.d.ellipse([p.p(-0.35, -0.9), p.p(0.35, 0.7)], outline=(*CYAN, 180), width=p.w(0.8))
    p.line([(0, -0.9), (0, 0.7)], a=180, k=0.8)
    p.line([(-0.8, -0.1), (0.8, -0.1)], a=180, k=0.8)
    p.arc(0, -1.3, 1.0, 55, 125, a=150, k=0.7)
    p.arc(0, 1.1, 1.0, 235, 305, a=150, k=0.7)
    p.line([(-0.9, 0.95), (-0.35, 0.6), (0, 0.85), (0.35, 0.6), (0.9, 0.95)], col=BLUEL, k=1.2)


def g_edu(p):
    p.poly([(-1, -0.35), (0, -0.85), (1, -0.35), (0, 0.15)], fill=FILL, k=1.1)
    p.line([(-0.55, -0.12), (-0.55, 0.35)])
    p.line([(0.55, -0.12), (0.55, 0.35)])
    p.arc(0, 0.1, 0.62, 30, 150)
    p.line([(0.85, -0.42), (0.85, 0.2)], col=BLUEL, k=0.8)
    p.dot(0.85, 0.25, 0.07)
    p.line([(-0.9, 0.7), (0, 0.85), (0.9, 0.7)], a=170)
    p.line([(0, 0.85), (0, 0.6)], a=120, k=0.6)


def g_health(p):
    c = [
        (-0.25, -0.85),
        (0.25, -0.85),
        (0.25, -0.35),
        (0.75, -0.35),
        (0.75, 0.15),
        (0.25, 0.15),
        (0.25, 0.65),
        (-0.25, 0.65),
        (-0.25, 0.15),
        (-0.75, 0.15),
        (-0.75, -0.35),
        (-0.25, -0.35),
    ]
    p.poly(c, fill=FILL, k=1.1)
    p.line(
        [
            (-1, 0.88),
            (-0.45, 0.88),
            (-0.3, 0.6),
            (-0.1, 1.05),
            (0.1, 0.75),
            (0.25, 0.88),
            (1, 0.88),
        ],
        col=BLUEL,
        k=1.1,
    )


def g_cart(p):
    p.line([(-1, -0.7), (-0.75, -0.7), (-0.45, 0.35), (0.7, 0.35)], k=1.2)
    p.poly([(-0.62, -0.4), (0.95, -0.4), (0.75, 0.15), (-0.5, 0.15)], fill=FILL)
    for x in (-0.15, 0.25, 0.6):
        p.line([(x, -0.4), (x - 0.05, 0.15)], a=120, k=0.6)
    p.circle(-0.35, 0.65, 0.13, col=BLUEL, k=1.1)
    p.circle(0.55, 0.65, 0.13, col=BLUEL, k=1.1)
    p.rect(-0.25, -0.95, 0.25, -0.5, a=170, k=0.7, r=0.03)


def g_team(p):
    pos = [(0, -0.35, 0.3), (-0.75, 0.05, 0.23), (0.75, 0.05, 0.23)]
    for i, (x, y, r) in enumerate(pos):
        for j, (x2, y2, _) in enumerate(pos):
            if j > i:
                p.line([(x, y), (x2, y2)], a=110, k=0.7)
    for x, y, r in pos:
        p.circle(x, y, r, fill=FILL, k=1.1)
        p.circle(x, y - r * 0.25, r * 0.32, k=0.9, fill=FILL2)
        p.arc(x, y + r * 0.62, r * 0.55, 205, 335, k=0.9)


def g_skyline(p):
    xs = [
        (-1, 0.4),
        (-0.78, 0.75),
        (-0.55, 0.5),
        (-0.35, 1.15),
        (-0.12, 0.7),
        (0.1, 0.95),
        (0.32, 0.55),
        (0.52, 0.85),
        (0.75, 0.45),
    ]
    for (x, h), (x2, _) in zip(xs, xs[1:] + [(0.98, 0)]):
        p.rect(x + 0.02, 0.9 - h, x2 - 0.02, 0.9, col=BLUEL, fill=FILL, r=0.01, k=0.7)
        for wy in range(int(h / 0.18)):
            p.dot((x + x2) / 2, 0.8 - wy * 0.18, 0.018, a=170)
    p.line([(-1.05, 0.9), (1.05, 0.9)], k=1.1)
    p.line([(-0.24, -0.25), (-0.24, -0.45)], k=0.8)
    p.dot(-0.24, -0.47, 0.05)


def g_chat(p):
    p.rect(-1, -0.8, 0.45, 0.15, fill=FILL, r=0.15)
    p.poly([(-0.65, 0.15), (-0.75, 0.45), (-0.4, 0.15)], fill=FILL)
    for x in (-0.55, -0.27, 0.01):
        p.dot(x, -0.32, 0.07)
    p.rect(-0.1, -0.15, 1.0, 0.6, col=BLUEL, fill=FILL2, r=0.15)
    p.poly([(0.6, 0.6), (0.72, 0.85), (0.4, 0.6)], col=BLUEL, fill=FILL2)
    p.line([(0.1, 0.12), (0.8, 0.12)], a=170, k=0.8)
    p.line([(0.1, 0.3), (0.55, 0.3)], a=170, k=0.8)


def g_hexes(p):
    for i, (x, y) in enumerate(
        [(0, 0), (0.62, -0.36), (0.62, 0.36), (0, 0.72), (-0.62, 0.36), (-0.62, -0.36), (0, -0.72)]
    ):
        pts = [
            (
                x + 0.33 * math.cos(math.radians(60 * k + 30)),
                y + 0.33 * math.sin(math.radians(60 * k + 30)),
            )
            for k in range(6)
        ]
        p.poly(pts, col=CYAN if i == 0 else BLUEL, fill=FILL if i else (*CYAN, 90), k=0.9)
        p.dot(x, y, 0.05, a=220 if i == 0 else 150)


def place(p, g, dx, dy, k=0.32):
    sub = Pen.__new__(Pen)
    sub.layer, sub.d, sub.W, sub.H = p.layer, p.d, p.W, p.H
    sub.s = p.s * k
    sub.cx, sub.cy = p.cx + dx * p.s, p.cy + dy * p.s
    sub.circle(0, 0, 1.35, a=60, k=0.6, fill=(*NAVY, 160))
    g(sub)


def hex_icons(p, glyphs):
    """First glyph in the centre, the rest on a ring around it."""
    pts = [(0, 0)] + [
        (0.95 * math.cos(math.radians(60 * k - 90)), 0.95 * math.sin(math.radians(60 * k - 90)))
        for k in range(6)
    ]
    for (x, y), (x2, y2) in zip(pts[1:], pts[2:] + pts[1:2]):
        p.line([(x, y), (x2, y2)], a=60, k=0.6)
    for x, y in pts[1:]:
        p.line([(0, 0), (x, y)], a=60, k=0.6)
    for g, (x, y) in zip(glyphs, pts):
        place(p, g, x, y, 0.27)


def grid_icons(p, glyphs, cols):
    rows = math.ceil(len(glyphs) / cols)
    for i, g in enumerate(glyphs):
        r, c = divmod(i, cols)
        sub = Pen.__new__(Pen)
        sub.layer, sub.d, sub.W, sub.H = p.layer, p.d, p.W, p.H
        sub.s = p.s * 0.32
        sub.cx = p.cx + (c - (cols - 1) / 2) * p.s * 0.95
        sub.cy = p.cy + (r - (rows - 1) / 2) * p.s * 0.95
        sub.circle(0, 0, 1.35, a=60, k=0.6, fill=(*NAVY, 160))
        g(sub)


def render(name, W, H, glyph, cx=0.5, cy=0.5, scale=0.28, glow=None, seed=1, ring=True, tone=0.0):
    img = background(W, H, glow or (cx, cy), seed, tone)
    s = min(W, H) * scale
    pen = Pen(W, H, W * cx, H * cy, s)
    if ring:
        pen.circle(0, 0, 1.25, k=0, fill=(*NAVY, 150))
        rings(pen)
    glyph(pen)
    art = pen.done()
    img = Image.alpha_composite(img, art.filter(ImageFilter.GaussianBlur(s * 0.06)))
    img = Image.alpha_composite(img, art)
    noise = Image.effect_noise((W, H), 18).convert("RGBA")
    noise.putalpha(9)
    img = Image.alpha_composite(img, noise).convert("RGB")
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, quality=90, method=6)
    return path


SERVICES = {
    "software-development": g_code,
    "website-digital-solutions": g_web,
    "cloud-infrastructure": g_cloud,
    "cybersecurity": g_shield,
    "managed-it-services": g_monitor,
    "payment-system-integrations": g_payment,
    "it-consulting-advisory": g_consult,
}
INDUSTRIES = {
    "startups-smes": g_rocket,
    "financial-institutions": g_bank,
    "ngos-development": g_globe,
    "education": g_edu,
    "healthcare": g_health,
    "retail-wholesale": g_cart,
}

if __name__ == "__main__":
    # About / home
    render("about/bjp-team.webp", 3840, 1653, g_team, cx=0.68, scale=0.3, seed=11)
    render("about/bjp-about-1.webp", 2560, 2157, g_skyline, scale=0.33, seed=12, ring=False)
    render("about/bjp-about-2.webp", 2560, 2157, g_hexes, scale=0.3, seed=13, tone=0.3)
    # Services
    render(
        "service/bjp-services.webp",
        2560,
        2560,
        lambda p: hex_icons(p, list(SERVICES.values())),
        scale=0.4,
        seed=21,
        ring=False,
    )
    render("service/bjp-service-banner.webp", 3840, 1694, g_hexes, cx=0.75, scale=0.3, seed=22)
    render("service/bjp-service-detail.webp", 2560, 2341, g_team, scale=0.3, seed=23, tone=0.3)
    for i, (slug, g) in enumerate(SERVICES.items()):
        render(f"service/bjp-{slug}.webp", 2560, 2341, g, cy=0.4, scale=0.25, seed=30 + i)
    # Industries
    render(
        "industry/bjp-industries.webp",
        2560,
        1634,
        lambda p: grid_icons(p, list(INDUSTRIES.values()), 3),
        scale=0.5,
        seed=41,
        ring=False,
    )
    render(
        "industry/bjp-industry-detail.webp",
        2560,
        1634,
        g_skyline,
        scale=0.36,
        seed=42,
        ring=False,
        tone=0.3,
    )
    for i, (slug, g) in enumerate(INDUSTRIES.items()):
        render(f"industry/bjp-{slug}.webp", 2560, 2033, g, scale=0.3, seed=50 + i)
    # Contact
    render("contact/bjp-contact.webp", 3840, 2062, g_chat, cx=0.72, scale=0.26, seed=61)
