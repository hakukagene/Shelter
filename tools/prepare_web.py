"""Finalize Ren'Py's web output with Safari video, UI and streaming assets."""
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from pathlib import Path
import argparse
import json
import shutil
import subprocess
import zipfile
from prepare_transition_frames import clips, playback_ends

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".web-build" / "mp4-v1"
PLAYBACK_ENDS = playback_ends()
SOURCE_ENDS = {source: PLAYBACK_ENDS.get(visitor + "/" + clip) for visitor, clip, source in clips()}


def convert(source):
    target = CACHE / source.relative_to(ROOT / "game").with_suffix(".mp4")
    target.parent.mkdir(parents=True, exist_ok=True)
    stamp = target.with_suffix(".sha256")
    end = SOURCE_ENDS.get(source)
    digest = sha256(source.read_bytes() + (str(end).encode() if end else b"")).hexdigest()
    if not target.exists() or not stamp.exists() or stamp.read_text() != digest:
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
            *(["-to", str(end)] if end else []),
            "-vf", "scale=1280:-2", "-c:v", "libx264", "-preset", "fast",
            "-crf", "25", "-maxrate", "1800k", "-bufsize", "3600k",
            "-threads", "4", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k",
            "-movflags", "+faststart", str(target),
        ], check=True)
        stamp.write_text(digest)
    print("MP4 ready:", source.relative_to(ROOT / "game"), flush=True)
    return target


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args()
    destination = args.destination.resolve()
    if not destination.is_relative_to(ROOT) or not (destination / "index.html").is_file():
        raise SystemExit("Destination must be an existing web build inside this project.")
    sources = sorted((ROOT / "game/Video").rglob("*.webm"))
    with ThreadPoolExecutor(max_workers=2) as pool:
        converted = list(pool.map(convert, sources))

    # Only shipped MP4 derivatives are hosted; never send source videos twice.
    for old in (destination / "game/Video").rglob("*"):
        if old.is_file() and old.suffix.lower() in (".webm", ".mp4"):
            old.unlink()
    for source in converted:
        target = destination / "game" / source.relative_to(CACHE)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    ui = destination / "shelter-ui"
    ui.mkdir(exist_ok=True)
    for filename in ("button.png", "selected.png"):
        shutil.copy2(ROOT / "game/gui/shelter/metal" / filename, ui / filename)
    for name in ("shoot", "lower", "reject", "admit"):
        shutil.copy2(ROOT / "game/gui/shelter/actions" / (name + ".png"), ui)
    shutil.copy2(ROOT / "game/gui/shelter/protocol/rules.svg", ui)
    for filename in ("RobotoCondensed-Regular.ttf", "RobotoCondensed-Bold.ttf"):
        shutil.copy2(ROOT / "game/fonts" / filename, ui)
    # Posters must be HTTP assets even when their Ren'Py counterparts are bundled.
    for source in (ROOT / "game/images").rglob("*.jpg"):
        target = destination / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    for filename in ("shelter-video.js", "shelter-web.css"):
        shutil.copy2(ROOT / "web" / filename, destination / filename)

    html_path = destination / "index.html"
    html = html_path.read_text(encoding="utf-8")
    html = html.replace('lang="en-us"', 'lang="mn"')
    html = html.replace("<title>Shelter</title>", "<title>Хорогдох байр</title>")
    html = html.replace(
        'content="width=device-width, initial-scale=1.0"',
        'content="width=device-width, initial-scale=1.0, viewport-fit=cover"')
    html = html.replace("</head>", '<link rel="stylesheet" href="shelter-web.css">\n</head>')
    html = html.replace('<script src="renpy-pre.js"></script>',
                        (ROOT / "web/video-overlay.html").read_text(encoding="utf-8")
                        + '\n<script src="renpy-pre.js"></script>')
    # Avoid installing a worker with the SDK's pre-customization asset catalog.
    start = html.index("      // Register the service worker.")
    end = html.index("  </script>", start)
    html = html[:start] + html[end:]
    html = html.replace("Import Saves", "Хадгалалт оруулах").replace("Export Saves", "Хадгалалт татах")
    html_path.write_text(html, encoding="utf-8")
    shutil.copy2(ROOT / "game/gui/shelter/main_menu/bunker.png", destination / "web-presplash.png")
    html_path.write_text(html.replace("web-presplash.jpg", "web-presplash.png"), encoding="utf-8")

    manifest_path = destination / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.update(name="Хорогдох байр", short_name="Хорогдох байр", lang="mn",
                    orientation="landscape", background_color="#070606", theme_color="#070606")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    # A .data extension works on hosts that reserve zip downloads.
    (destination / "game.zip").replace(destination / "game.data")
    html_path.write_text(html_path.read_text(encoding="utf-8").replace(
        "window.gameZipURL = 'game.zip'", "window.gameZipURL = 'game.data'"), encoding="utf-8")
    for name in ("index.html.symbols", "service-worker.js", "web-presplash.jpg"):
        (destination / name).unlink(missing_ok=True)

    files = sorted(p for p in destination.rglob("*") if p.is_file())
    oversized = [str(p.relative_to(destination)) for p in files if p.stat().st_size > 25 * 1024**2]
    if oversized:
        raise SystemExit("Files exceed static hosting's per-file limit: " + ", ".join(oversized))
    archive = ROOT / "dist/Shelter-1.0-web.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for path in files:
            z.write(path, path.relative_to(destination))
    print(f"Web ready: {len(sources)} videos, {len(files)} files, "
          f"{sum(p.stat().st_size for p in files) / 1024**2:.1f} MiB", flush=True)
    print(archive)


if __name__ == "__main__":
    main()
