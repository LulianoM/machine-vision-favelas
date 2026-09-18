import sys
from PIL import Image, ImageDraw
from pathlib import Path
ds = Path(sys.argv[1]); R = int(sys.argv[2]) if len(sys.argv) > 2 else 40; S = 320
out = ds / "crops"; out.mkdir(exist_ok=True); tiles = []
for split in ("train", "val"):
    for lbl in sorted((ds / "labels" / split).glob("*.txt")):
        im = Image.open(ds / "images" / split / (lbl.stem + ".jpg")) if False else sorted((ds / "images" / split).glob("*.jpg")).convert("RGB"); W, H = im.size
        for line in lbl.read_text().splitlines():
            c, xc, yc, w, h = line.split(); xc, yc, w, h = map(float, (xc, yc, w, h))
            cx, cy = xc * W, yc * H; s = S / (2 * R)
            crop = im.crop((int(cx - R), int(cy - R), int(cx + R), int(cy + R))).resize((S, S), Image.NEAREST)
            d = ImageDraw.Draw(crop)
            d.rectangle([(R - w * W / 2) * s, (R - h * H / 2) * s, (R + w * W / 2) * s, (R + h * H / 2) * s], outline=(255, 40, 40) if c == "0" else (40, 200, 255), width=2)
            d.text((4, 4), f"{lbl.stem[-3:]} c{c} {w*W:.0f}x{h*H:.0f}px", fill=(255, 255, 0))
            tiles.append(crop)
cols = 6; rows = max(1, (len(tiles) + cols - 1) // cols)
sheet = Image.new("RGB", (cols * S, rows * S)); [sheet.paste(t, ((i % cols) * S, (i // cols) * S)) for i, t in enumerate(tiles)]
sheet.save(out / "crops_sheet.png"); print("tiles", len(tiles))
