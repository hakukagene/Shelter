"""Extract exact first/last decoded frames of every playable encounter movie.

Run after updating WebMs. --check validates committed posters against sources;
--audit additionally decodes every complete video/audio stream with FFmpeg.
No footage, framing, or sound is modified.
"""
import argparse
import ast
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "game/images/transitions"
CONSTANTS = {"Chinba": "CHINBA_CLIPS", "Maral": "SHELTER_CLIPS",
             "Swat": "SWAT_CLIPS", "Bayra": "BAYRA_CLIPS", "anu": "ANU_CLIPS",
             "deeremchin": "DEEREMCHIN_CLIPS", "ganba": "GANBA_CLIPS",
             "ganzo": "GANZO_CLIPS", "naraa": "NARAA_CLIPS",
             "margad": "MARGAD_CLIPS", "undral": "UNDRAL_CLIPS"}


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def clips():
    # Clip tables live in one character file each. Reading all scripts keeps
    # this audit utility working as visitors are added in their own files.
    script = "\n".join(path.read_text(encoding="utf-8-sig")
                       for path in sorted((ROOT / "game").glob("*.rpy")))
    for visitor, constant in CONSTANTS.items():
        match = re.search(r"^define " + constant + r" = (\{.*?\})", script, re.M | re.S)
        for clip, (filename, _) in ast.literal_eval(match[1]).items():
            yield visitor, clip, ROOT / "game/Video" / visitor / filename


def playback_ends():
    script = (ROOT / "game/encounter_media.rpy").read_text(encoding="utf-8-sig")
    return ast.literal_eval(re.search(r"^define SHELTER_CLIP_ENDS = (\{.*?\})", script, re.M | re.S)[1])


def playback_starts():
    script = (ROOT / "game/encounter_media.rpy").read_text(encoding="utf-8-sig")
    return ast.literal_eval(re.search(r"^define SHELTER_CLIP_STARTS = (\{.*?\})", script, re.M | re.S)[1])


def authored_posters(visitor, clip):
    # Share each visitor's authored images without generating duplicate stills.
    script = (ROOT / "game" / (visitor + ".rpy")).read_text(encoding="utf-8-sig")
    def table(name):
        return ast.literal_eval(re.search(r"^define " + name + r" = (\{.*?\})", script, re.M | re.S)[1])
    posters = table(visitor.upper() + "_POSTERS")
    states = table(visitor.upper() + "_POSTER_STATES")[clip]
    return {edge: ROOT / "game" / posters[state]
            for edge, state in zip(("start", "end"), states)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--visitor", choices=CONSTANTS,
                        help="process one visitor while preserving the rest of the manifest")
    args = parser.parse_args()
    manifest = OUT / "manifest.json"
    previous = json.loads(manifest.read_text()) if manifest.exists() else {}
    starts = playback_starts()
    ends = playback_ends()

    def process(job):
        visitor, clip, source = job
        key = visitor + "/" + clip
        with source.open("rb") as stream:
            if stream.read(64).startswith(b"version https://git-lfs.github.com/spec/v1"):
                raise RuntimeError(str(source) + ": run git lfs pull first")
        fingerprint = digest(source)
        start_time = starts.get(key)
        end_time = ends.get(key)
        folder = OUT / visitor
        targets = {edge: folder / (clip + "-" + edge + ".jpg") for edge in ("start", "end")}
        if visitor in ("naraa", "undral"):
            targets = authored_posters(visitor, clip)
            for path in targets.values():
                if not path.is_file():
                    raise RuntimeError(str(path) + ": missing authored visitor image")
        old = previous.get(key, {})
        ready = old.get("source_sha256") == fingerprint and old.get("start_time") == start_time and old.get("end_time") == end_time and all(
            path.exists() and digest(path) == old.get(edge + "_sha256") for edge, path in targets.items())
        if not ready and visitor not in ("naraa", "undral"):
            if args.check:
                raise RuntimeError(key + ": missing/stale transition frames; run this tool without --check")
            folder.mkdir(parents=True, exist_ok=True)
            for edge, path in targets.items():
                command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-threads", "2"]
                # Reverse only the last second, so the exported end is the
                # actual final video frame, not duration-minus-an-arbitrary-offset.
                if edge == "start" and start_time is not None:
                    command += ["-ss", str(start_time)]
                elif edge == "end":
                    command += ["-ss", str(max(0, end_time - 1)), "-to", str(end_time)] if end_time else ["-sseof", "-1"]
                command += ["-i", str(source), "-an"]
                if edge == "end":
                    command += ["-vf", "reverse"]
                command += ["-frames:v", "1", "-q:v", "2", "-update", "1", str(path)]
                subprocess.run(command, check=True)
        if args.audit:
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-xerror",
                            "-threads", "2", "-i", str(source), "-map", "0:v:0", "-map", "0:a?",
                            "-f", "null", "-"], check=True)
        data = {"source": str(source.relative_to(ROOT / "game")), "source_sha256": fingerprint,
                "start_time": start_time, "end_time": end_time}
        data.update({edge + "_sha256": digest(path) for edge, path in targets.items()})
        if visitor in ("naraa", "undral"):
            data.update({edge + "_image": str(path.relative_to(ROOT / "game"))
                         for edge, path in targets.items()})
            if args.check and old != data:
                raise RuntimeError(key + ": stale authored-poster manifest; run this tool without --check")
        print(key + (": checked + decoded" if args.audit else ": checked"), flush=True)
        return key, data

    jobs = [job for job in clips() if not args.visitor or job[0] == args.visitor]
    with ThreadPoolExecutor(max_workers=2) as pool:
        result = dict(pool.map(process, jobs))
    if not args.check:
        previous.update(result)
        manifest.write_text(json.dumps(previous, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    elif not args.visitor and set(previous) != set(result):
        raise RuntimeError("Transition manifest has missing or obsolete clip entries")
    print("Verified", len(result), "playable clips and", len(result)*2, "poster references")


if __name__ == "__main__":
    main()
