# Safari / web

Play: https://shelter-khorogdoh-bair.upbeat-cedar-1751.chatgpt.site

Build the browser edition with `.\tools\build_web.ps1`. The finished static site
is in `dist/web/`, and the portable upload package is `dist/Shelter-1.0-web.zip`.
The script requires the matching Ren'Py web support and FFmpeg on `PATH`.
It caches MP4 conversions in `.web-build/`; changing a source video invalidates
that video's cached derivative.

The browser edition retains the Ren'Py story, menus, choices and save system.
`game/web_video.rpy` and `web/shelter-video.js` connect each clip to a persistent
inline HTML video element. H.264/AAC MP4s use fast-start metadata and load only
when needed. Each clip downloads into a seekable Blob because Sites' static
host does not return partial HTTP byte ranges. Skipping cancels a pending
download, and finishing releases that clip's Blob to bound memory usage.
Intro captions follow `video.currentTime`, stay on one line, and
use the same fonts and metal skip-button artwork as the game. Pause/resume,
muting, retry after a network error, Safari's tap-to-play prompt, and pausing
when switching tabs are handled by the browser player.

Play in landscape on an iPhone. If Safari requests a tap to start sound, press
**Тоглуулах**. A public web host must serve `.wasm` as `application/wasm` and
MP4 as `video/mp4`. Opening `index.html` as a local file is not
supported. For local testing, run `python tools/serve_web.py` and open the
printed URL on this computer.

Hosting is staged separately under `.web-site/` with Sites project ID
`appgprj_6ad758650d2c8191a32d3782a9f37e25`; preserve this identity on updates.
Only the built browser files are published. APKs, signing keys, tool caches,
test scripts and the source project's Git history are excluded.

Validation uses `node tools/web_browser_check.mjs` with
`python tools/serve_web.py --port 8044`. It runs an isolated headless Chrome profile with a phone-sized viewport
and touch events: Start, inline video, captions, pause/resume, skip, first
visitor, questions/player speech, aiming/lowering, and intro completion.
It also checks menu/gameplay/result music, the complete replacement door knock,
the next visitor and replay. `node tools/check_web_host.mjs <site-url>` checks
hosting headers and compares published game data, music and player hashes
against the verified local build.
All 40 MP4s were checked for codecs, fast-start and matching duration (maximum
change 0.008 seconds). Physical iPhone/Safari testing remains outstanding.
