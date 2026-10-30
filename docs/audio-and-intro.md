# Audio and opening film

## Background music and speech

The start menu loops `game/audio/Audio/menu1.mp3`. The result screen with
**Дахин тоглох / Үндсэн цэс** loops `menu2.mp3`. Both use 50% track volume.
Gameplay loops `shuum.mp3` at 18% so speech remains audible. Starting or
replaying switches tracks with a fade; the opening film stops menu music.
The Music slider adjusts these backgrounds; Voice adjusts dialogue.

Visitor transitions play `game/audio/Audio/door .wav`
once on the sound-effects channel. The transition waits for the full 2.20-second
recording; this short effect is bundled in the web edition to avoid download delays.

The ten `game/audio/Chingune/*.wav` clips are matched to approximately
−16 LUFS with peaks limited to −1.5 dBTP. Original sample counts, sample rates,
and subtitle timing are preserved. Original files and the measurement report
are stored locally in `.audio-originals/`, excluded from builds and Git.
`python tools/normalize_voices.py` processes new/replaced clips and skips
unchanged files that have already been normalized.

## Opening film

- `game/intro.rpy` plays the 100-second opening on its own voice/movie channel.
  The existing metal control artwork is used for **Алгасах** at the upper right.
  Click it or press **Esc** to go straight to the first encounter. Normal clicks,
  Space, Tab, and rollback do not dismiss the film.
- `game/Video/Introvideo/Intro.webm` is the VP9/Opus playback copy of the supplied
  H.264/AAC `Intro.mp4`. Ren'Py desktop cannot decode the original codecs.
  Web builds generate an H.264/AAC MP4 copy from this playback asset.
- `game/Video/Introvideo/Intro.mn.srt` contains 40 editable Mongolian subtitle
  cues. Boundaries were aligned locally against the supplied text and audio,
  including the radio exchange. Small spelling corrections preserve the script.
  Timestamps are measured from the beginning of this specific video.
- Captions use the decoder position, so they stay with the video instead of
  accumulating timer drift. The voice volume control also controls the film;
  muting does not stop playback. Completing or skipping stops its audio before
  the encounter. Loading a gameplay save does not replay the opening.

To rebuild the playback asset after replacing the source:

```powershell
ffmpeg -i game/Video/Introvideo/Intro.mp4 -c:v libvpx-vp9 -crf 25 -b:v 0 -row-mt 1 -threads 8 -cpu-used 4 -pix_fmt yuv420p -c:a libopus -b:a 160k game/Video/Introvideo/Intro.webm
```

Re-align the SRT if the video's edit or narration timing changes.
