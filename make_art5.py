#!/usr/bin/env python3
"""Art #5 for AiProve make-art: 'Phyllotaxis Meridian' — a golden-angle
phyllotaxis bloom whose florets cycle the aurora palette by radius, set on a
deep indigo field inside gold ledger rings with meridian ticks. New seed and
geometry vs art #3 (phyllotaxis) and art #4 (aurora ribbons): the two earlier
motifs fused into one dial. Deterministic, PIL only."""
import math, random
from PIL import Image, ImageDraw, ImageFilter, ImageChops

W = H = 1400
random.seed(90210)  # new seed (art3 used a plain spiral, art4 seed 4217)

img = Image.new("RGB", (W, H), (9, 10, 30))
ov = Image.new("RGB", (W, H), (0, 0, 0))
d = ImageDraw.Draw(ov, "RGBA")

# star grain
for _ in range(1100):
    x, y = random.uniform(0, W), random.uniform(0, H)
    b = random.randint(26, 100)
    d.point((x, y), fill=(b, b, b + 24))

# soft aurora wash behind the bloom (low-alpha diagonal ribbons)
palette = [(32, 224, 178), (64, 156, 255), (150, 92, 255), (255, 92, 168), (255, 196, 86)]
for i in range(10):
    t = i / 9
    base_y = 180 + t * 980
    pts_top, pts_bot = [], []
    for x in range(0, W + 24, 24):
        y = base_y + 90 * math.sin(x / 300.0 + i * 0.7)
        pts_top.append((x, y))
        pts_bot.append((x, y + 90))
    d.polygon(pts_top + pts_bot[::-1], fill=palette[i % 5] + (10,))
ov = ov.filter(ImageFilter.GaussianBlur(10))
img = ImageChops.add(img, ov)

d = ImageDraw.Draw(img, "RGBA")
cx = cy = W // 2

# ledger rings + meridian ticks
for r, wdt in ((648, 3), (520, 2), (392, 2)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(214, 175, 92, 190), width=wdt)
for k in range(72):
    a = k * math.pi / 36
    r1, r2 = 648, 668 if k % 6 == 0 else 658
    d.line([cx + r1 * math.cos(a), cy + r1 * math.sin(a),
            cx + r2 * math.cos(a), cy + r2 * math.sin(a)], fill=(214, 175, 92, 220), width=3)

# phyllotaxis bloom: golden angle, radius-coloured florets with glow cores
GOLDEN = math.pi * (3 - math.sqrt(5))
N = 2600
glow = Image.new("RGB", (W, H), (0, 0, 0))
gd = ImageDraw.Draw(glow)
for n in range(N, 0, -1):
    r = 13.4 * math.sqrt(n)
    a = n * GOLDEN
    x, y = cx + r * math.cos(a), cy + r * math.sin(a)
    t = r / 648.0
    col = palette[int(t * 14) % 5]
    s = 3.2 + 7.5 * t
    gd.ellipse([x - s, y - s, x + s, y + s], fill=tuple(c // 3 for c in col))
glow = glow.filter(ImageFilter.GaussianBlur(7))
img = ImageChops.add(img, glow)
d = ImageDraw.Draw(img)
for n in range(N, 0, -1):
    r = 13.4 * math.sqrt(n)
    a = n * GOLDEN
    x, y = cx + r * math.cos(a), cy + r * math.sin(a)
    t = r / 648.0
    col = palette[int(t * 14) % 5]
    s = 2.4 + 5.6 * t
    d.ellipse([x - s, y - s, x + s, y + s], fill=col)
# bright core
d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=(255, 236, 170))

img.save("/home/hatch/workspace/aiprove/round5/art5-phyllotaxis-meridian.png")
print("saved art5")
