#!/usr/bin/env python3
"""Vibe Code Studio - thumbnail & cover builder.

Original work for this kit. Turns a photo (or a frame pulled from a video)
plus a headline into platform-ready covers: YouTube 1280x720 and vertical
1080x1920 (TikTok / Reels / Shorts).

Inputs are only ever read. Outputs land in a folder you choose, so your
original photos and footage stay untouched.
"""
import argparse, json, os, subprocess, sys, textwrap

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
FORMATS = {
    "youtube": (1280, 720),
    "vertical": (1080, 1920),
}

def fail(msg, hint=None):
    print(f"ERROR: {msg}", file=sys.stderr)
    if hint:
        print(f"FIX:   {hint}", file=sys.stderr)
    sys.exit(1)

def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        fail(f"preset not found: {path}", "run `python3 thumb.py presets` to list available presets")
    except json.JSONDecodeError as e:
        fail(f"preset is not valid JSON: {path} ({e})")

def resolve(path):
    return path if os.path.isabs(path) else os.path.join(REPO_ROOT, path)

def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def get_font(font_path, size):
    from PIL import ImageFont
    try:
        return ImageFont.truetype(font_path, size)
    except Exception:
        return None

def vertical_gradient(size, top, bottom):
    from PIL import Image
    w, h = size
    base = Image.new("RGB", (1, h))
    t, b = hex_rgb(top), hex_rgb(bottom)
    for y in range(h):
        f = y / max(h - 1, 1)
        base.putpixel((0, y), tuple(int(t[i] + (b[i] - t[i]) * f) for i in range(3)))
    return base.resize((w, h))

def overlay_gradient(canvas, box, color=(0, 0, 0), max_alpha=190, direction="vertical"):
    """Dark gradient over box=(x0,y0,x1,y1) for text legibility. Vertical fades
    top->bottom; horizontal fades left->right. Fades to 0 so no hard seam shows."""
    from PIL import Image
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    if direction == "horizontal":
        grad = Image.new("L", (w, 1))
        for x in range(w):
            grad.putpixel((x, 0), int(max_alpha * (1 - x / max(w - 1, 1))))
    else:
        grad = Image.new("L", (1, h))
        for y in range(h):
            grad.putpixel((0, y), int(max_alpha * (1 - y / max(h - 1, 1))))
    alpha = grad.resize((w, h))
    layer = Image.new("RGBA", (w, h), color + (0,))
    layer.putalpha(alpha)
    canvas.alpha_composite(layer, (x0, y0))

def remove_bg(img):
    try:
        from rembg import remove
    except ImportError:
        fail("background removal needs the optional 'rembg' package",
             "pip install rembg  (or pass a photo that already has a transparent background and drop --cutout)")
    return remove(img)

def wrap_headline(draw, words, font, max_width):
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_headline(canvas, preset, box, headline, accent, align="center"):
    from PIL import ImageDraw
    draw = ImageDraw.Draw(canvas)
    x0, y0, x1, y1 = box
    max_w = x1 - x0
    hspec = preset["headline"]
    font_path = resolve(hspec["font"])
    words = headline.split()
    size = hspec.get("max_size", 150)
    max_lines = hspec.get("max_lines", 4)
    font = None
    lines = []
    while size > 24:
        font = get_font(font_path, size)
        if font is None:
            break
        lines = wrap_headline(draw, words, font, max_w)
        total = int(size * 1.08) * len(lines)
        if (len(lines) <= max_lines
                and all(draw.textlength(l, font=font) <= max_w for l in lines)
                and total <= (y1 - y0)):
            break
        size -= 6
    if font is None:
        print("WARNING: preset font missing, using a basic fallback font", file=sys.stderr)
        from PIL import ImageFont
        font = ImageFont.load_default(size=48)
        lines = wrap_headline(draw, words, font, max_w)
    line_h = int(size * 1.08)
    total_h = line_h * len(lines)
    if len(lines) > max_lines:
        print(f"WARNING: headline wrapped to {len(lines)} lines (max {max_lines}); consider a shorter headline", file=sys.stderr)
    accent_u = (accent or "").upper()
    y = y0 + max(0, ((y1 - y0) - total_h) // 2)
    for line in lines:
        lw = draw.textlength(line, font=font)
        x = x0 + (max_w - lw) / 2 if align == "center" else x0
        # per-word coloring so the accent word pops
        cx = x
        for i, w in enumerate(line.split()):
            word = w + (" " if i < len(line.split()) - 1 else "")
            color = hspec["accent_color"] if accent_u and w.strip("!?.,:;").upper() == accent_u else hspec["color"]
            # shadow for legibility
            draw.text((cx + 3, y + 3), word, font=font, fill=(0, 0, 0, 200))
            draw.text((cx, y), word, font=font, fill=hex_rgb(color) + (255,))
            cx += draw.textlength(word, font=font)
        y += line_h

def compose(preset, image_path, headline, accent, fmt, cutout=False):
    from PIL import Image
    W, H = FORMATS[fmt]
    bg = preset["background"]
    if "gradient" in bg:
        canvas = vertical_gradient((W, H), bg["gradient"][0], bg["gradient"][1]).convert("RGBA")
    else:
        canvas = Image.new("RGBA", (W, H), hex_rgb(bg.get("color", "#000000")) + (255,))
    try:
        subject = Image.open(image_path)
    except FileNotFoundError:
        fail(f"image not found: {image_path}", "pass --image with a real photo, or make one with `python3 thumb.py frame --video ...`")
    if subject.width < W // 2:
        print(f"WARNING: image is only {subject.width}px wide for a {W}px canvas; output may look soft", file=sys.stderr)
    if cutout:
        subject = remove_bg(subject)
    subject = subject.convert("RGBA")
    sz = preset["subject"]
    if fmt == "vertical":
        target_h = int(H * sz.get("height_fraction_vertical", 0.78))
        scale = target_h / subject.height
        if subject.width * scale < W:  # never narrower than the canvas
            scale = W / subject.width
        s = subject.resize((int(subject.width * scale), int(subject.height * scale)))
        x = (W - s.width) // 2
        y = H - s.height  # full-bleed to the bottom edge
        canvas.alpha_composite(s, (x, y))
        # headline zone: top of frame, always ending above the subject so
        # text never sits over the face; bottom app-UI strip stays clear
        ui = preset["safe_zones"]["vertical"]
        bottom_ui = int(H * (1 - ui.get("bottom_ui_fraction", 0.15)))
        hz_bottom = max(min(y - 40, bottom_ui), int(H * 0.18))
        hz = (int(W * 0.06), 60, int(W * 0.94), hz_bottom)
        overlay_gradient(canvas, (0, 0, W, hz[3] + 160))
        draw_headline(canvas, preset, hz, headline, accent, align="center")
    else:  # youtube
        target_h = int(H * sz.get("height_fraction_youtube", 0.92))
        scale = target_h / subject.height
        s = subject.resize((int(subject.width * scale), int(subject.height * scale)))
        margin = int(W * preset["safe_zones"]["youtube"].get("margin_fraction", 0.06))
        x = max(W - s.width - margin, W // 2)
        canvas.alpha_composite(s, (x, H - s.height))
        hz = (margin, int(H * 0.10), min(int(W * 0.64), x - 30), int(H * 0.90))
        overlay_gradient(canvas, (0, 0, int(W * 0.75), H), direction="horizontal")
        draw_headline(canvas, preset, hz, headline, accent, align="left")
    return canvas.convert("RGB")

def cmd_make(a):
    preset = load_json(resolve(a.preset)) if not os.path.isabs(a.preset) and not os.path.exists(a.preset) else load_json(a.preset)
    os.makedirs(a.outdir, exist_ok=True)
    fmts = [f.strip() for f in a.formats.split(",") if f.strip()]
    for f in fmts:
        if f not in FORMATS:
            fail(f"unknown format '{f}'", f"choose from: {', '.join(FORMATS)}")
    made = []
    for f in fmts:
        img = compose(preset, a.image, a.headline, a.accent, f, cutout=a.cutout)
        out = os.path.join(a.outdir, f"thumb-{f}.png")
        img.save(out)
        made.append(out)
        print(f"WROTE {out} ({FORMATS[f][0]}x{FORMATS[f][1]})")
    print("PREVIEW: open the files above and check them before posting.")

def cmd_frame(a):
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except FileNotFoundError:
        fail("ffmpeg is not installed", "macOS: brew install ffmpeg   |   Ubuntu: sudo apt install ffmpeg")
    os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
    r = subprocess.run(["ffmpeg", "-y", "-ss", str(a.time), "-i", a.video, "-frames:v", "1", "-q:v", "2", a.out],
                       capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(a.out):
        fail(f"could not pull a frame at {a.time}s from {a.video}", "check the video plays and the --time value is inside it")
    print(f"WROTE {a.out}")

def cmd_presets(_a):
    pdir = resolve("brand/presets")
    for name in sorted(os.listdir(pdir)):
        if name.endswith(".json"):
            p = load_json(os.path.join(pdir, name))
            print(f"brand/presets/{name}  -  {p.get('description', p.get('name', ''))}")

def cmd_selftest(a):
    from PIL import Image, ImageDraw
    os.makedirs(a.outdir, exist_ok=True)
    # synthetic stand-in subject (drawn, no rights issues)
    subj = Image.new("RGBA", (900, 1400), (0, 0, 0, 0))
    d = ImageDraw.Draw(subj)
    d.ellipse((250, 60, 650, 460), fill=(222, 184, 150, 255))          # head
    d.rounded_rectangle((100, 480, 800, 1400), 120, fill=(35, 35, 40, 255))  # shoulders
    spath = os.path.join(a.outdir, "selftest-subject.png")
    subj.save(spath)
    class A: pass
    args = A(); args.preset = a.preset; args.image = spath
    args.headline = "CLAUDE EDITS MY VIDEOS"; args.accent = "EDITS"
    args.formats = "youtube,vertical"; args.outdir = a.outdir; args.cutout = False
    cmd_make(args)
    from PIL import Image as I
    for f, (w, h) in FORMATS.items():
        p = os.path.join(a.outdir, f"thumb-{f}.png")
        got = I.open(p).size
        assert got == (w, h), f"{p}: expected {(w,h)}, got {got}"
    print("SELFTEST OK - both covers rendered at exact platform sizes")

def main():
    ap = argparse.ArgumentParser(description="Thumbnail & cover builder")
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("make", help="compose covers from a photo")
    m.add_argument("--image", required=True)
    m.add_argument("--headline", required=True)
    m.add_argument("--accent", default="", help="one word of the headline to highlight in the accent color")
    m.add_argument("--preset", default="brand/presets/default.json")
    m.add_argument("--formats", default="youtube,vertical")
    m.add_argument("--cutout", action="store_true", help="remove the photo background first (needs: pip install rembg)")
    m.add_argument("--outdir", default="covers")
    m.set_defaults(fn=cmd_make)
    f = sub.add_parser("frame", help="pull a still frame from a video")
    f.add_argument("--video", required=True)
    f.add_argument("--time", type=float, default=1.0, help="seconds into the video")
    f.add_argument("--out", default="frame.png")
    f.set_defaults(fn=cmd_frame)
    p = sub.add_parser("presets", help="list brand presets")
    p.set_defaults(fn=cmd_presets)
    s = sub.add_parser("selftest", help="render test covers with a synthetic subject and verify sizes")
    s.add_argument("--preset", default="brand/presets/default.json")
    s.add_argument("--outdir", default="sample/out")
    s.set_defaults(fn=cmd_selftest)
    a = ap.parse_args()
    a.fn(a)

if __name__ == "__main__":
    main()
