"""Split the generated twelve-pose creature atlas into independent sprites."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools/art/shooting-test/monster-sheet.png"
OUTPUT = ROOT / "game/images/shooting_test/monster"


def main():
    with Image.open(SOURCE) as source:
        assert source.size == (1448,1086) and source.mode == "RGBA"
        OUTPUT.mkdir(parents=True,exist_ok=True)
        for index in range(12):
            row,column = divmod(index,4)
            frame = source.crop((column*362,row*362,(column+1)*362,(row+1)*362))
            name = OUTPUT / ("monster-%02d.png" % index)
            frame.save(name,optimize=True)
            with Image.open(name) as saved:
                assert saved.tobytes() == frame.tobytes()
    print("Verified 12 independent transparent 362x362 monster sprites.")


if __name__ == "__main__":
    main()
