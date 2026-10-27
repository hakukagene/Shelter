"""Export run poses and the replacement alternating-fist creature animation."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools/art/shooting-test/monster-sheet.png"
OUTPUT = ROOT / "game/images/shooting_test/monster"
STRIKE_SOURCE = ROOT / "tools/art/shooting-test/monster-alternating-sheet.png"


def main():
    with Image.open(SOURCE) as source:
        assert source.size == (1448,1086) and source.mode == "RGBA"
        OUTPUT.mkdir(parents=True,exist_ok=True)
        for index in range(8):
            row,column = divmod(index,4)
            frame = source.crop((column*362,row*362,(column+1)*362,(row+1)*362))
            name = OUTPUT / ("monster-%02d.png" % index)
            frame.save(name,optimize=True)
            with Image.open(name) as saved:
                assert saved.tobytes() == frame.tobytes()
    with Image.open(STRIKE_SOURCE) as source:
        assert source.mode == "RGBA"
        for index in range(8):
            row,column = divmod(index,4)
            pose = source.crop((round(column*source.width/4),round(row*source.height/2),
                                round((column+1)*source.width/4),round((row+1)*source.height/2)))
            alpha = pose.getchannel("A")
            bounds = alpha.point(lambda value: 255 if value > 64 else 0).getbbox()
            assert bounds is not None
            left,top,right,bottom = bounds
            # Align by the crown of the head, not by the changing fist outline.
            head = alpha.crop((0,top,pose.width,top+max(1,round((bottom-top)*.07))))
            totals = [sum(head.getpixel((x,y)) for y in range(head.height)) for x in range(head.width)]
            head_x = sum(x*weight for x,weight in enumerate(totals))/sum(totals)
            scale = 350.0/(bottom-top)
            body = pose.crop(bounds).resize((round((right-left)*scale),350),Image.Resampling.LANCZOS)
            frame = Image.new("RGBA",(362,362))
            frame.paste(body,(round(181-(head_x-left)*scale),2))
            name = OUTPUT / ("strike-%02d.png" % index)
            frame.save(name,optimize=True)
            with Image.open(name) as saved:
                assert saved.mode == "RGBA" and saved.size == (362,362)
                assert saved.tobytes() == frame.tobytes()
    # Remove only the four superseded simultaneous-punch runtime frames.
    intended = (ROOT / "game/images/shooting_test/monster").resolve()
    for index in range(8,12):
        obsolete = OUTPUT / ("monster-%02d.png" % index)
        assert obsolete.resolve().parent == intended
        if obsolete.exists():
            obsolete.unlink()
    print("Verified 8 run + 8 alternating strike sprites; removed the old four strike frames.")


if __name__ == "__main__":
    main()
