"""Prepare Ren'Py Android branding. Requires Pillow; not needed to build an APK.

python tools/prepare_android_branding.py [--presplash /path/to/loading-art.png]
The checked-in root icon.ico is the original supplied by the author.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--presplash", type=Path)
    args = parser.parse_args()

    with Image.open(ROOT / "icon.ico") as ico:
        # Select the largest original frame; don't regenerate the author's art.
        source = ico.ico.getimage(max(ico.ico.sizes(), key=lambda size: size[0]))
        source = source.convert("RGBA").resize((240, 240), Image.Resampling.LANCZOS)
    foreground = Image.new("RGBA", (432, 432), (0, 0, 0, 0))
    foreground.alpha_composite(source, (96, 96))
    foreground.save(ROOT / "android-icon_foreground.png", optimize=True)
    Image.new("RGB", (432, 432), (9, 10, 12)).save(
        ROOT / "android-icon_background.png", optimize=True)

    if args.presplash:
        with Image.open(args.presplash) as art:
            # Fit without distortion; black padding matches RAPT's edge fill.
            art = ImageOps.contain(art.convert("RGB"), (1856, 1016), Image.Resampling.LANCZOS)
            canvas = Image.new("RGB", (1920, 1080), "black")
            canvas.paste(art, ((1920 - art.width) // 2, (1080 - art.height) // 2))
            canvas.save(ROOT / "android-presplash.jpg", quality=94, subsampling=0, optimize=True)


if __name__ == "__main__":
    main()
