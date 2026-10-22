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
  }
  addEventListener(type, fn) { this.listeners[type] = fn; }
  setAttribute() {}
  removeAttribute(name) { delete this[name]; }
  append(...nodes) { this.children.push(...nodes); }
  replaceChildren() { this.children = []; }
  getBoundingClientRect() { return { left: 0, top: 0, width: 1920, height: 1080 }; }
  pause() { this.paused = true; }
  play() { this.paused = false; return Promise.resolve(); }
  load() { this.clears++; }
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

api.start(options); await flush();
assert.equal(video.paused, false);
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

api.start({ ...options, intro: true }); await flush();
element("video-skip").listeners.click();
assert.equal(api.finished, true);
api.close();
api.start(options); await flush(); nextFrame(); nextFrame();
assert.equal(root.hidden, false);
assert.equal(api.finished, false);
console.log("PASS: skipping the intro cannot hide the first encounter.");
api.close(); nextFrame(); nextFrame();
