"""Build the small digit fonts used by the ledger and its physical clock.

Usage: python tools/build_ledger_fonts.py /path/to/DejaVuSerif-Bold.ttf
Requires fonttools. The seven-segment glyphs are original geometric artwork;
the ledger digits are a renamed DejaVu subset (see game/fonts/DejaVu-LICENSE.txt).
"""
from pathlib import Path
import sys

from fontTools import subset
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

DEST = Path(__file__).resolve().parents[1] / "game/fonts"


def clock_font():
    segments = {
        "a": [(100, 930), (480, 930), (525, 885), (480, 840), (100, 840), (55, 885)],
        "g": [(100, 545), (480, 545), (525, 500), (480, 455), (100, 455), (55, 500)],
        "d": [(100, 160), (480, 160), (525, 115), (480, 70), (100, 70), (55, 115)],
        "f": [(35, 860), (80, 815), (80, 580), (35, 535), (-10, 580), (-10, 815)],
        "b": [(545, 860), (590, 815), (590, 580), (545, 535), (500, 580), (500, 815)],
        "e": [(35, 465), (80, 420), (80, 185), (35, 140), (-10, 185), (-10, 420)],
        "c": [(545, 465), (590, 420), (590, 185), (545, 140), (500, 185), (500, 420)],
    }
    patterns = ["abcdef", "bc", "abdeg", "abcdg", "bcfg", "acdfg", "acdefg", "abc", "abcdefg", "abcdfg"]
    names = [".notdef", "space", "colon"] + ["digit" + str(i) for i in range(10)]
    glyphs, metrics = {}, {}
    for name in names:
        pen = TTGlyphPen(None)
        shapes = []
        left_edges = []
        if name.startswith("digit"):
            shapes = [segments[s] for s in patterns[int(name[-1])]]
        elif name == "colon":
            shapes = [[(35, y), (120, y), (120, y + 85), (35, y + 85)] for y in (280, 620)]
        for shape in shapes:
            # A slight lean matches the original digital alarm clock.
            points = [(round(x + y * 0.07 + 20), y) for x, y in shape]
            left_edges.extend(x for x, y in points)
            pen.moveTo(points[0])
            for point in points[1:]:
                pen.lineTo(point)
            pen.closePath()
        glyphs[name] = pen.glyph()
        # Keep each segment in its fixed digit cell, particularly the narrow 1.
        metrics[name] = (700 if name.startswith("digit") else 240, min(left_edges) if left_edges else 0)
    builder = FontBuilder(1000, isTTF=True)
    builder.setupGlyphOrder(names)
    builder.setupCharacterMap({32: "space", 58: "colon", **{48 + i: "digit" + str(i) for i in range(10)}})
    builder.setupGlyf(glyphs)
    builder.setupHorizontalMetrics(metrics)
    builder.setupHorizontalHeader(ascent=1000, descent=0)
    builder.setupNameTable({"familyName": "Shelter Clock", "styleName": "Regular", "uniqueFontIdentifier": "ShelterClock-Regular-1", "fullName": "Shelter Clock Regular", "psName": "ShelterClock-Regular"})
    builder.setupOS2(sTypoAscender=1000, sTypoDescender=0, usWinAscent=1000, usWinDescent=0)
    builder.setupPost()
    builder.setupMaxp()
    builder.save(DEST / "ShelterClock.ttf")


def ledger_font(source):
    font = TTFont(source)
    options = subset.Options()
    options.name_IDs = [0, 1, 2, 3, 4, 5, 6, 13, 14]
    options.name_languages = [0x409]
    cutter = subset.Subsetter(options=options)
    cutter.populate(text="0123456789 ")
    cutter.subset(font)
    for record in font["name"].names:
        values = {1: "Shelter Ledger Digits", 2: "Bold", 3: "ShelterLedgerDigits-Bold-1", 4: "Shelter Ledger Digits Bold", 6: "ShelterLedgerDigits-Bold"}
        if record.nameID in values:
            record.string = values[record.nameID].encode(record.getEncoding())
    font.save(DEST / "ShelterLedgerDigits.ttf")


if __name__ == "__main__":
    DEST.mkdir(parents=True, exist_ok=True)
    clock_font()
    ledger_font(sys.argv[1])
