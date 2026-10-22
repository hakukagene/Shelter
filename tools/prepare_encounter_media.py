"""Build Ren'Py VP9/Opus clips and stable stills without changing framing.

Run git lfs pull first. Retired MP4s may be absent when the committed WebM
exists. Source/output hashes avoid re-encoding unchanged footage on each build.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / 'tools/encounter_media.json').read_text())
CACHE_PATH = ROOT / 'game/images/encounter-media-manifest.json'
ENCODING = 'vp9-crf25-speed5-opus128-v1'


def digest(path):
    with path.open('rb') as stream:
        if stream.read(64).startswith(b'version https://git-lfs.github.com/spec/v1'):
            raise RuntimeError(f'{path}: LFS pointer; run git lfs pull first')
        stream.seek(0)
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def build_clip(item, previous):
    who, key, source_name = item
    source = ROOT / 'game/Video' / who / source_name
    output = source.with_name(key + '.webm')
    if not source.exists():
        # The author can remove source MP4s after committing playback WebMs.
        if not output.exists():
            raise RuntimeError(f'{who}/{key}: neither source MP4 nor playback WebM exists')
        digest(output)
        print(f'{who}/{key}: keeping committed WebM (source retired)', flush=True)
        return who + '/' + key, previous.get(who + '/' + key)

    fingerprint = digest(source)
    old = previous.get(who + '/' + key) or {}
    if (old.get('source_sha256') == fingerprint and old.get('encoding') == ENCODING
            and output.exists() and old.get('output_sha256') == digest(output)):
        print(f'{who}/{key}: unchanged', flush=True)
        return who + '/' + key, old

    temporary = output.with_name(output.stem + '.building.webm')
    try:
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
                        '-c:v', 'libvpx-vp9', '-crf', '25', '-b:v', '0', '-cpu-used', '5',
                        '-row-mt', '1', '-threads', '2', '-pix_fmt', 'yuv420p',
                        '-c:a', 'libopus', '-b:a', '128k', str(temporary)], check=True)
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    print(f'{who}/{key}: converted', flush=True)
    return who + '/' + key, {'source': str(source.relative_to(ROOT / 'game')),
                             'source_sha256': fingerprint, 'output_sha256': digest(output),
                             'encoding': ENCODING}


def build_frame(who, name, clip, position, previous):
    # Always extract from the actual playback clip, including when MP4s are retired.
    source = ROOT / 'game/Video' / who / (clip + '.webm')
    output = ROOT / 'game/images' / who / 'frames' / (name + '.jpg')
    spec = {'source': str(source.relative_to(ROOT / 'game')),
            'source_sha256': digest(source), 'position': position}
    old = previous.get(who + '/' + name, {})
    if (all(old.get(k) == value for k, value in spec.items()) and output.exists()
            and old.get('image_sha256') == digest(output)):
        return who + '/' + name, old
    output.parent.mkdir(parents=True, exist_ok=True)
    command = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-threads', '2']
    command += ['-sseof', '-1'] if position == 'end' else ['-ss', str(position)]
    command += ['-i', str(source), '-an']
    if position == 'end':
        command += ['-vf', 'reverse']
    command += ['-frames:v', '1', '-q:v', '2', '-update', '1', str(output)]
    subprocess.run(command, check=True)
    spec['image_sha256'] = digest(output)
    print(f'{who}/{name}: extracted {clip} at {position}', flush=True)
    return who + '/' + name, spec


def main():
    previous = json.loads(CACHE_PATH.read_text()) if CACHE_PATH.exists() else {}
    jobs = [(who, key, name) for who, config in MANIFEST.items() for key, name in config['clips'].items()]
    with ThreadPoolExecutor(max_workers=2) as pool:
        clips = dict(pool.map(lambda item: build_clip(item, previous.get('clips', {})), jobs))
    frames = dict(build_frame(who, name, clip, position, previous.get('frames', {}))
                  for who, config in MANIFEST.items()
                  for name, (clip, position) in config['frames'].items())
    CACHE_PATH.write_text(json.dumps({'clips': {key: value for key, value in clips.items() if value},
                                     'frames': frames}, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
