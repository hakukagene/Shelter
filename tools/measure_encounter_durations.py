"""Update a visitor's clip table from its original WebMs, without re-encoding."""
import argparse
import ast
import json
import math
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def measure(visitor):
    if not re.fullmatch(r"[a-z]+", visitor):
        raise ValueError("Expected a lowercase visitor ID")
    path = ROOT / "game" / (visitor + ".rpy")
    source = path.read_text(encoding="utf-8")
    match = re.search(r"^define " + visitor.upper() + r"_CLIPS = (\{.*?\})", source, re.M | re.S)
    clips = ast.literal_eval(match[1])
    for key, (filename, _) in clips.items():
        movie = ROOT / "game/Video" / visitor / filename
        with movie.open("rb") as stream:
            if stream.read(64).startswith(b"version https://git-lfs.github.com/spec/v1"):
                raise RuntimeError(f"{movie}: run git lfs pull first")
        probe = json.loads(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "json", str(movie)], text=True))
        duration = float(probe["format"]["duration"])
        if not math.isfinite(duration) or duration <= 0:
            raise ValueError(f"Invalid duration: {movie}")
        clips[key] = (filename, round(duration, 3))
        print(f"{visitor}/{key}: {duration:.3f}s", flush=True)
    table = "{\n" + "".join(
        f'    "{key}": ("{filename}", {duration:.3f}),\n'
        for key, (filename, duration) in clips.items()) + "}"
    path.write_text(source[:match.start(1)] + table + source[match.end(1):], encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("visitor")
    measure(parser.parse_args().visitor)
