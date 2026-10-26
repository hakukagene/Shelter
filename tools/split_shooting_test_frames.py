"""Split the supplied handgun sheet into lossless, transparent animation PNGs."""
from pathlib import Path
import argparse
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools/art/shooting-test/handgun-sheet.png"
DESTINATION = ROOT / "game/images/shooting_test/frames"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, nargs="?", default=SOURCE)
    args = parser.parse_args()
    with Image.open(args.source) as source:
        if source.size != (2172, 724) or source.mode != "RGBA":
            raise ValueError("Expected the original 2172x724 RGBA handgun sheet")
        DESTINATION.mkdir(parents=True, exist_ok=True)
        for row, (top, height) in enumerate(((0, 380), (395, 293))):
            for column in range(10):
                left = round(column * source.width / 10)
                right = round((column + 1) * source.width / 10)
                frame = source.crop((left, top, right, top + height))
                output = DESTINATION / ("handgun-%02d.png" % (row * 10 + column))
                frame.save(output, optimize=True)
                with Image.open(output) as saved:
                    if saved.mode != "RGBA" or saved.size != frame.size or saved.tobytes() != frame.tobytes():
                        raise ValueError("Frame pixels changed: %s" % output)
    print("Exported and pixel-verified 20 transparent PNG frames to %s" % DESTINATION)


if __name__ == "__main__":
    main()
