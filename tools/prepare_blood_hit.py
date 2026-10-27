"""Export the generated hit particles as eight separate 256px RGBA sprites."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools/art/shooting-test/blood-hit-sheet.png"
OUTPUT = ROOT / "game/images/shooting_test/blood"


def main():
    OUTPUT.mkdir(parents=True,exist_ok=True)
    with Image.open(SOURCE) as source:
        assert source.mode == "RGBA"
        for index in range(8):
            row,column = divmod(index,4)
            bounds = (round(column*source.width/4),round(row*source.height/2),
                      round((column+1)*source.width/4),round((row+1)*source.height/2))
            frame = source.crop(bounds).resize((256,256),Image.Resampling.LANCZOS)
            name = OUTPUT / ("blood-%02d.png" % index)
            frame.save(name,optimize=True)
            with Image.open(name) as saved:
                assert saved.mode == "RGBA" and saved.size == (256,256)
                assert saved.tobytes() == frame.tobytes()
    print("Verified eight independent 256x256 transparent hit-effect sprites.")


if __name__ == "__main__":
    main()
