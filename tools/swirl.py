import math, sys
INK = "#4a3b30"
CRIMSON = "#9b1c31"
FILL = "#f6eddc"
GAP, SW = 11, 1.4

def spiral(cx, cy, rmax, turns=2.4, a0=0.0):
    n = int(turns * 40); pts = []
    for i in range(n + 1):
        t = i / n; a = a0 + t * turns * 2 * math.pi; r = rmax * t
        pts.append(f"{cx + r*math.cos(a):.1f} {cy + r*math.sin(a):.1f}")
    return "M" + "L".join(pts)

# lobes hugging the top-left corner; inner edge is scalloped
lobes = [
    (30, 20, 135), (215, -20, 110), (380, -40, 95), (-20, 200, 100),
    (150, 115, 68), (300, 70, 60), (440, 40, 48), (60, 245, 56),
    (225, 160, 42), (125, 215, 38), (370, 110, 34), (500, 60, 30),
]
out = []
k = 0
while True:
    active = [(cx, cy, r - k*GAP) for cx, cy, r in lobes if r - k*GAP >= max(r*0.36, 10)]
    if not active: break
    col, op = (CRIMSON, 0.8) if k == 1 else (INK, 0.85)
    # wide strokes first, fills on top -> only the outer union contour stays visible
    out.append(f'<g fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{SW*2}">' +
               "".join(f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}"/>' for cx, cy, r in active) + "</g>")
    out.append(f'<g fill="{FILL}">' + "".join(f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}"/>' for cx, cy, r in active) + "</g>")
    k += 1
for i, (cx, cy, r) in enumerate(lobes):
    kk = 0
    while r - (kk+1)*GAP >= max(r*0.36, 10): kk += 1
    out.append(f'<path d="{spiral(cx, cy, r - kk*GAP - 3, a0=i*1.3)}" fill="none" stroke="{INK}" stroke-opacity="0.85" stroke-width="{SW}" stroke-linecap="round"/>')
svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 320">\n'
       '<!-- original swirl-cloud corner, generated for this site -->\n' + "\n".join(out) + "\n</svg>\n")
open(sys.argv[1], "w", encoding="utf-8").write(svg); print("written", k, "layers")
