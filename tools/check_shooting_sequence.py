"""Validate the offline animation bake before removing legacy runtime assets."""
from pathlib import Path
from hashlib import sha256
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "game/images/shooting_test/sequence"
NAMES = ["idle"] + ["fire-%02d" % i for i in range(10)] + ["reload-%02d" % i for i in range(45)]


def main():
    hashes = {}
    for name in NAMES:
        with Image.open(DIRECTORY / (name + ".png")) as image:
            assert image.size == (600,500), name
            assert image.mode == "RGBA", name
            low, high = image.getextrema()[3]
            assert low == 0 and high >= 240, name
            hashes[name] = sha256(image.tobytes()).hexdigest()
    reload_hashes = {hashes[name] for name in NAMES if name.startswith("reload-")}
    # The two endpoints deliberately share the exact idle pixels.
    assert len(reload_hashes) == 44, "Interior reload frames must be pixel-distinct"
    assert hashes["reload-00"] == hashes["idle"], "Reload must start at idle"
    assert hashes["reload-44"] == hashes["idle"], "Reload must finish at idle"
    print("Verified 56 RGBA 600x500 sprites, 45 reload files, 44 distinct images, matching idle endpoints.")


if __name__ == "__main__":
    main()
