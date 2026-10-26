"""Archive-only: extract the original eight poses for the sequence exporter."""
from pathlib import Path
import argparse
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools/art/shooting-test/handgun-v2-sheet.png"
DESTINATION = ROOT / "tools/art/shooting-test/source-poses"
NAMES = ("idle", "fire", "settle", "reload-start", "reload-out",
         "reload-in", "reload-rack", "reload-ready")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, nargs="?", default=SOURCE)
    args = parser.parse_args()
    with Image.open(args.source) as source:
        if source.size != (1774, 887) or source.mode != "RGBA":
            raise ValueError("Expected the new 1774x887 RGBA handgun sheet")
        DESTINATION.mkdir(parents=True, exist_ok=True)
        for index, name in enumerate(NAMES):
            row, column = divmod(index, 4)
            box = (round(column * source.width / 4), round(row * source.height / 2),
                   round((column + 1) * source.width / 4), round((row + 1) * source.height / 2))
            pose = source.crop(box)
            # Preserve pixels; pad the 443/444px cells to one shared baseline.
            frame = Image.new("RGBA", (444, 444))
            frame.paste(pose, ((444 - pose.width) // 2, 444 - pose.height))
            output = DESTINATION / (name + ".png")
            frame.save(output, optimize=True)
            with Image.open(output) as saved:
                if saved.mode != "RGBA" or saved.size != frame.size or saved.tobytes() != frame.tobytes():
                    raise ValueError("Frame pixels changed: %s" % output)
    print("Exported 8 archived source poses. Run Ren'Py test shelter_sprite_export to bake runtime frames.")


if __name__ == "__main__":
    main()
