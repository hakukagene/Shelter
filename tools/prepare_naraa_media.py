"""Measure replacement Naraa WebMs before building their transition frames."""
import ast
import json
import math
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    path = ROOT / "game/naraa.rpy"
    source = path.read_text(encoding="utf-8")
    match = re.search(r"^define NARAA_CLIPS = (\{.*?\})", source, re.M | re.S)
    clips = ast.literal_eval(match[1])
    for key, (name, _) in clips.items():
        movie = ROOT / "game/Video/naraa" / name
        with movie.open("rb") as stream:
            if stream.read(64).startswith(b"version https://git-lfs.github.com/spec/v1"):
                raise RuntimeError(f"{movie}: run git lfs pull first")
        probe = json.loads(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "json", str(movie)], text=True))
        duration = float(probe["format"]["duration"])
        if not math.isfinite(duration) or duration <= 0:
            raise ValueError(f"Invalid duration: {movie}")
        clips[key] = (name, round(duration, 3))
        print(f"naraa/{key}: {duration:.3f}s", flush=True)
    table = "{\n" + "".join(
        f'    "{key}": ("{name}", {duration:.3f}),\n'
        for key, (name, duration) in clips.items()) + "}"
    path.write_text(source[:match.start(1)] + table + source[match.end(1):], encoding="utf-8")


if __name__ == "__main__":
    main()
