#!/usr/bin/env python
"""Generate favicon assets from a source profile JPG.

Creates these files under images/:
 - favicon-16.png
 - favicon-32.png
 - favicon-48.png
 - apple-touch-icon-180x180.png
 - favicon.ico (contains 16x16 and 32x32)

This script uses Pillow (PIL). Run with system python:
    python tools/generate_favicons.py
"""
from pathlib import Path
import sys

try:
    from PIL import Image
except Exception as e:
    print("ERROR: Pillow is required. Install it: python -m pip install --upgrade pillow")
    raise

ROOT = Path(__file__).resolve().parents[1]
IMG_DIR = ROOT / 'images'
SRC = IMG_DIR / 'jgill-profile.jpg'

if not SRC.exists():
    print(f"ERROR: source image not found: {SRC}")
    sys.exit(2)

sizes = {
    'favicon-16.png': (16, 16),
    'favicon-32.png': (32, 32),
    'favicon-48.png': (48, 48),
    'apple-touch-icon-180x180.png': (180, 180),
}

def make_pngs():
    im = Image.open(SRC).convert('RGBA')
    for name, s in sizes.items():
        out = IMG_DIR / name
        o = im.copy()
        o.thumbnail(s, Image.LANCZOS)
        # Ensure exact size
        if o.size != s:
            # center onto transparent background
            bg = Image.new('RGBA', s, (0,0,0,0))
            x = (s[0]-o.size[0])//2
            y = (s[1]-o.size[1])//2
            bg.paste(o, (x,y), o)
            bg.save(out, format='PNG')
        else:
            o.save(out, format='PNG')
        print('WROTE', out)

def make_ico():
    # Create an ICO with 16x16 and 32x32
    im = Image.open(SRC).convert('RGBA')
    icons = []
    for s in [(32,32),(16,16)]:
        o = im.copy()
        o.thumbnail(s, Image.LANCZOS)
        if o.size != s:
            bg = Image.new('RGBA', s, (0,0,0,0))
            x = (s[0]-o.size[0])//2
            y = (s[1]-o.size[1])//2
            bg.paste(o, (x,y), o)
            icons.append(bg)
        else:
            icons.append(o)

    out = IMG_DIR / 'favicon.ico'
    # Pillow writes ICO from first image and sizes param
    icons[0].save(out, format='ICO', sizes=[(32,32),(16,16)])
    print('WROTE', out)


if __name__ == '__main__':
    IMG_DIR.mkdir(exist_ok=True)
    make_pngs()
    make_ico()
    print('\nDone. Check the images/ directory for generated favicons.')
from PIL import Image, ImageOps
import os
src='images/jgill-profile.jpg'
outdir='images'
if not os.path.exists(src):
    raise SystemExit('Source image not found: ' + src)
img=Image.open(src).convert('RGBA')
# Resize canvas to square and try to center a bit higher (face approx)
w,h=img.size
side=min(w,h)
# Try a fit with slight upward centering (0.5,0.45)
resized=ImageOps.fit(img, (side,side), centering=(0.5,0.45))
# Generate several sizes
sizes=[(16,'favicon-16x16.png'),(32,'favicon-32x32.png'),(48,'favicon-48x48.png'),(180,'apple-touch-icon.png')]
for s,fn in sizes:
    im=resized.resize((s,s), Image.LANCZOS)
    im.save(os.path.join(outdir,fn), optimize=True)
# Create favicon.ico (multiple sizes)
ico_path=os.path.join(outdir,'favicon.ico')
ico_sizes=[16,32,48]
ico_images=[resized.resize((s,s), Image.LANCZOS) for s in ico_sizes]
ico_images[0].save(ico_path, format='ICO', sizes=[(s,s) for s in ico_sizes])
print('WROTE:', ico_path)
for _,fn in sizes:
    print('WROTE:', os.path.join(outdir,fn))
