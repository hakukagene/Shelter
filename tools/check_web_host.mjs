import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { createHash } from "node:crypto";
const base = process.argv[2];
assert(base, "Pass the hosted site's URL.");
const html = await fetch(base);
assert.equal(html.status, 200);
assert((await html.text()).includes('src="shelter-video.js"'), "Game entry page missing");
for (const [file, mime] of [["renpy.wasm", "application/wasm"], ["game.data", null]]) {
  const response = await fetch(new URL(file, base + "/"), { method: "HEAD" });
  assert.equal(response.status, 200, file);
  if (mime) assert(response.headers.get("content-type")?.startsWith(mime), file);
}
for (const file of ["game/Video/Introvideo/Intro.mp4", "game/Video/Chinba/Chinbaa ehlel.mp4"]) {
  const response = await fetch(new URL(file, base + "/"), { headers: { Range: "bytes=0-127" } });
  assert([200, 206].includes(response.status), "MP4 download: " + file);
  assert(response.headers.get("content-type")?.startsWith("video/mp4"));
  if (response.status === 206) assert.equal((await response.arrayBuffer()).byteLength, 128);
  else {
    await response.body.cancel();
    const player = await fetch(new URL("shelter-video.js", base + "/")).then(r => r.text());
    assert(player.includes("URL.createObjectURL(blob)"), "Non-range hosts require the Safari Blob player");
  }
}
const digest = bytes => createHash("sha256").update(bytes).digest("hex");
await Promise.all(["shelter-video.js", "game.data", ...["menu1", "menu2", "shuum"].map(name => `game/audio/Audio/${name}.mp3`)].map(async file => {
  const response = await fetch(new URL(file, base + "/"));
  assert.equal(response.status, 200, file);
  const actual = Buffer.from(await response.arrayBuffer());
  const expected = await readFile(new URL("../dist/web/" + file, import.meta.url));
  assert.equal(digest(actual), digest(expected), "Published file differs from verified build: " + file);
}));
console.log("PASS: public game page, WASM MIME, exact new game data/music/player, Safari Blob fallback and encoded filenames.");
