"""Build Ren'Py VP9/Opus playback files and stills from the encounter sources.
Run git lfs pull first. Source framing and audio are preserved without scaling.
"""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / 'tools/encounter_media.json').read_text())


def run(*args):
    return subprocess.check_output(args, text=True)


def duration(path):
    return float(run('ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(path)))


def build_clip(item):
    who, key, source_name = item
    source = ROOT / 'game/Video' / who / source_name
    with source.open('rb') as f:
        if f.read(64).startswith(b'version https://git-lfs.github.com/spec/v1'):
            raise RuntimeError(f'{source}: LFS pointer; run git lfs pull before conversion')
    output = source.with_name(key + '.webm')
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
                    '-c:v', 'libvpx-vp9', '-crf', '25', '-b:v', '0', '-cpu-used', '5',
                    '-row-mt', '1', '-threads', '2', '-pix_fmt', 'yuv420p',
                    '-c:a', 'libopus', '-b:a', '128k', str(output)], check=True)
    print(f'{who}/{key}: {duration(output):.3f}s', flush=True)


def main():
    jobs = [(who, key, name) for who, config in MANIFEST.items() for key, name in config['clips'].items()]
    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(build_clip, jobs))
    for who, config in MANIFEST.items():
        folder = ROOT / 'game/images' / who / 'frames'
        folder.mkdir(parents=True, exist_ok=True)
        for name, (clip, position) in config['frames'].items():
            source = ROOT / 'game/Video' / who / config['clips'][clip]
            position = max(0, duration(source) - .1) if position == 'end' else position
            subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-ss', str(position),
                            '-i', str(source), '-frames:v', '1', '-q:v', '2', str(folder / (name + '.jpg'))], check=True)


if __name__ == '__main__':
    main()
