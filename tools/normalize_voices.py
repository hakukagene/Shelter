"""Match the Chingune speech clips without clipping or changing cue timings."""
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from pathlib import Path
import json
import shutil
import subprocess
import wave

ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / ".audio-originals"
REPORT = BACKUP / "normalization.json"
TARGET = "I=-16:TP=-1.5:LRA=11"


def measure(path):
    result = subprocess.run([
        "ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
        "-af", f"loudnorm={TARGET}:print_format=json", "-f", "null", "-",
    ], capture_output=True, text=True, check=True)
    return json.JSONDecoder().raw_decode(result.stderr[result.stderr.rfind("{"):])[0]


def samples(path):
    with wave.open(str(path)) as audio:
        return audio.getnframes(), audio.getframerate(), audio.getnchannels()


def normalize(path, previous):
    digest = sha256(path.read_bytes()).hexdigest()
    if previous.get("output_sha256") == digest:
        return previous
    saved = BACKUP / digest / path.name
    saved.parent.mkdir(parents=True, exist_ok=True)
    if not saved.exists():
        shutil.copy2(path, saved)
    before = measure(saved)
    frames, rate, channels = samples(saved)
    filters = (f"loudnorm={TARGET}:measured_I={before['input_i']}"
               f":measured_TP={before['input_tp']}:measured_LRA={before['input_lra']}"
               f":measured_thresh={before['input_thresh']}:offset={before['target_offset']}"
               ":linear=true")
    output = saved.with_name("normalized-" + saved.name)
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(saved),
        "-af", filters, "-ar", str(rate), "-ac", str(channels),
        "-c:a", "pcm_s16le", str(output),
    ], check=True)
    after = measure(output)
    out_frames, out_rate, out_channels = samples(output)
    assert (rate, channels) == (out_rate, out_channels), path
    assert abs(out_frames - frames) <= 1, (path, frames, out_frames)
    assert float(after["input_tp"]) <= -1.2, (path, "true peak", after)
    assert -18 <= float(after["input_i"]) <= -14.5, (path, "loudness", after)
    result = {
        "file": path.name,
        "before_lufs": float(before["input_i"]),
        "after_lufs": float(after["input_i"]),
        "true_peak_dbtp": float(after["input_tp"]),
        "sample_count": out_frames, "sample_rate": rate,
        "original": str(saved.relative_to(ROOT)),
        "output_sha256": sha256(output.read_bytes()).hexdigest(),
    }
    # Replace only after the new clip passes timing and clipping checks.
    output.replace(path)
    return result


def main():
    previous = json.loads(REPORT.read_text()) if REPORT.exists() else {}
    files = sorted((ROOT / "game/audio/Chingune").glob("*.wav"))
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda p: normalize(p, previous.get(p.name, {})), files))
    REPORT.write_text(json.dumps({r["file"]: r for r in results}, indent=2), encoding="utf-8")
    for result in results:
        print(f"{result['file']}: {result['before_lufs']:.1f} -> "
              f"{result['after_lufs']:.1f} LUFS; peak {result['true_peak_dbtp']:.1f} dBTP")
    print("PASS: original sample counts/rates preserved; originals backed up locally.")


if __name__ == "__main__":
    main()
