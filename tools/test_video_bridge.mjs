// Real bridge code with a deterministic DOM/video clock. No dependencies.
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import vm from "node:vm";

class Element {
  constructor() {
    this.hidden = true;
    this.style = {};
    this.dataset = {};
    this.listeners = {};
    this.children = [];
    this.classList = { toggle() {} };
    this.currentTime = 0;
    this.complete = true;
    this.naturalWidth = 1920;
    this.paused = true;
    this.clears = 0;
    this.readyState = 0;
    this.videoFrames = new Map();
    this.videoSerial = 0;
  }
  addEventListener(type, fn) { this.listeners[type] = fn; }
  setAttribute() {}
  removeAttribute(name) { delete this[name]; }
  append(...nodes) { this.children.push(...nodes); }
  replaceChildren() { this.children = []; }
  getBoundingClientRect() { return { left: 0, top: 0, width: 1920, height: 1080 }; }
  pause() { this.paused = true; }
  play() { this.paused = false; return Promise.resolve(); }
  load() { this.clears++; this.readyState = 0; this.currentTime = 0; }
  requestVideoFrameCallback(fn) { this.videoFrames.set(++this.videoSerial, fn); return this.videoSerial; }
  cancelVideoFrameCallback(id) { this.videoFrames.delete(id); }
  presentFrame() {
    this.readyState = 2;
    const pending = [...this.videoFrames.values()]; this.videoFrames.clear();
    pending.forEach(fn => fn());
  }
}
const elements = new Map();
const element = name => {
  if (!elements.has(name)) elements.set(name, new Element());
  return elements.get(name);
};
let serial = 0;
const frames = new Map();
const nextFrame = () => {
  const pending = [...frames.values()]; frames.clear();
  pending.forEach(fn => fn());
};
const context = {
  window: { addEventListener() {} },
  document: { getElementById: element, createElement: () => new Element(), addEventListener() {} },
  requestAnimationFrame(fn) { frames.set(++serial, fn); return serial; },
  cancelAnimationFrame(id) { frames.delete(id); },
  AbortController, URL, Blob, encodeURI,
  fetch: async () => ({ ok: true, blob: async () => new Blob(["test"]) }),
};
vm.runInNewContext(await readFile(new URL("../web/shelter-video.js", import.meta.url), "utf8"), context);
const api = context.window.ShelterVideo;
const root = element("shelter-video"), video = element("story-video");
const options = { src: "test.mp4", cues: [], volume: 1, muted: false, intro: false,
  poster: "start.jpg", endPoster: "end.jpg" };
const flush = async () => { for (let i=0; i<8; i++) await Promise.resolve(); };

// Instructions pause the same decoder and uncover the Ren'Py guide, not EOF.
api.start(options); await flush();
video.currentTime = 2.4;
element("video-guide").listeners.click();
assert.equal(video.paused, true);
assert.equal(root.hidden, true);
assert.equal(api.finished, false);
assert.equal(api.takeGuideRequest(), true);
assert.equal(api.takeGuideRequest(), false);
api.resumeFromGuide(); await flush();
assert.equal(video.currentTime, 2.4);
assert.equal(video.paused, false);
assert.equal(root.hidden, false);
video.pause();
element("video-guide").listeners.click();
api.resumeFromGuide(); await flush();
assert.equal(video.paused, true, "Keep a pre-existing user pause when closing instructions");
api.close(); nextFrame(); nextFrame();
console.log("PASS: instructions pause/resume the same video and preserve an existing pause.");

api.start(options); await flush();
assert.equal(video.paused, false);
assert.equal(video.style.opacity, "0", "Download/play must not cover the canvas with an empty video");
video.listeners.playing();
assert.equal(video.style.opacity, "0", "Playing alone does not prove a video frame was submitted");
video.presentFrame();
assert.equal(video.style.opacity, "1", "Reveal only after the first decoded frame");
console.log("PASS: the current still stays visible until the first composited video frame.");
element("video-caption").hidden = false;
video.listeners.ended();
assert.equal(api.finished, true);
assert.equal(root.hidden, false, "EOF must hold the movie until canvas handoff");
assert.equal(element("video-caption").hidden, true, "EOF must clear captions");
element("video-resume").listeners.click(); await flush();
assert.equal(video.paused, true, "Resume after EOF must not replay the movie");
const clears = video.clears;
api.close();
assert.equal(root.hidden, false);
assert.equal(video.clears, clears, "Do not clear the final frame too early");
nextFrame(); assert.equal(root.hidden, false);
nextFrame(); assert.equal(root.hidden, true);
assert.equal(video.clears, clears+1);
console.log("PASS: EOF holds frame; close waits for two compositor frames.");

api.start(options); await flush();
api.close(); nextFrame();
api.start({ ...options, src: "next-visitor.mp4" }); await flush(); nextFrame();
assert.equal(root.hidden, false, "Stale close must not hide the next visitor");
assert.equal(video.paused, false);
console.log("PASS: delayed close cannot clear or hide a newer clip.");

api.start({ ...options, endTime: 13.11 }); await flush();
video.currentTime = 13.12; nextFrame();
assert.equal(api.finished, true);
assert.equal(video.paused, true);
assert.equal(element("video-end-frame").hidden, false);
assert.equal(root.hidden, false);
console.log("PASS: trimmed EOF freezes the valid end poster before handoff.");
api.close(); nextFrame(); nextFrame();

// A delayed callback from an older clip must not reveal a fresh empty decoder.
api.start(options); await flush();
const staleFrame = [...video.videoFrames.values()][0];
api.start({ ...options, src: "cold-next.mp4" }); await flush();
video.readyState = 2;
staleFrame();
assert.equal(video.style.opacity, "0");
video.presentFrame();
assert.equal(video.style.opacity, "1");
api.close(); nextFrame(); nextFrame();
console.log("PASS: a stale first-frame callback cannot expose a newer empty video.");

const originalFetch = context.fetch;
let resolveDownload;
context.fetch = () => new Promise(resolve => { resolveDownload = resolve; });
api.start(options); await flush(); nextFrame(); nextFrame();
assert.equal(video.style.opacity, "0", "Slow downloads must keep the underlying canvas visible");
assert.equal(element("video-loading").hidden, false);
resolveDownload({ ok: true, blob: async () => new Blob(["slow"]) });
await flush();
assert.equal(video.style.opacity, "0", "Downloaded bytes are not a decoded frame");
video.presentFrame();
assert.equal(video.style.opacity, "1");
context.fetch = originalFetch;
api.close(); nextFrame(); nextFrame();
console.log("PASS: cold/slow download preserves the still through decode.");

const originalPlay = video.play;
video.play = () => Promise.reject(Object.assign(new Error("gesture required"), { name: "NotAllowedError" }));
api.start(options); await flush();
assert.equal(video.style.opacity, "0");
assert.equal(element("video-prompt").hidden, false);
video.play = originalPlay;
element("video-resume").listeners.click(); await flush();
video.presentFrame();
assert.equal(video.style.opacity, "1");
api.close(); nextFrame(); nextFrame();
console.log("PASS: autoplay prompt retains the still until the user starts playback.");

// Exercise the older-browser path without requestVideoFrameCallback.
video.requestVideoFrameCallback = undefined;
api.start(options); await flush();
video.listeners.playing(); nextFrame(); nextFrame();
assert.equal(video.style.opacity, "0", "No fallback reveal before current frame data exists");
video.readyState = 2;
video.listeners.loadeddata();
nextFrame(); assert.equal(video.style.opacity, "0");
nextFrame(); assert.equal(video.style.opacity, "1");
api.close(); nextFrame(); nextFrame();
delete video.requestVideoFrameCallback;
console.log("PASS: legacy browser waits for loaded frame data and paint.");

const css = await readFile(new URL("../web/shelter-web.css", import.meta.url), "utf8");
assert.match(css, /#shelter-video\{[^}]*background:transparent/);
assert.match(css, /#story-video\{[^}]*background:transparent/);
console.log("PASS: encounter overlay backgrounds cannot cover the canvas in black.");

api.start({ ...options, intro: true }); await flush();
element("video-skip").listeners.click();
assert.equal(api.finished, true);
api.close();
api.start(options); await flush(); nextFrame(); nextFrame();
assert.equal(root.hidden, false);
assert.equal(api.finished, false);
console.log("PASS: skipping the intro cannot hide the first encounter.");
api.close(); nextFrame(); nextFrame();

api.start({ ...options, armed: true,
  actions: [["shoot", "Эрэгтэйг буудах"], ["shoot", "Эмэгтэйг буудах"]] });
await flush();
assert.deepEqual(element("video-actions").children.map(item => item.children[1].textContent),
  ["Эрэгтэйг буудах", "Эмэгтэйг буудах"]);
api.close(); nextFrame(); nextFrame();
console.log("PASS: two-person encounter keeps the correct target labels during web playback.");
