// Isolated headless Chrome smoke test; does not touch the user's browser profile.
import { spawn } from "node:child_process";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import assert from "node:assert/strict";
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const output = path.join(root, "tmp/web-tests");
await mkdir(output, { recursive: true });
const browser = spawn("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe", [
  "--headless=new", "--remote-debugging-port=9227", "--no-first-run",
  "--no-default-browser-check", "--autoplay-policy=user-gesture-required",
  `--user-data-dir=${path.join(root, ".web-build/chrome-test")}`, "about:blank",
], { windowsHide: true, stdio: "ignore" });
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
let socket;
let diagnose = async () => {};
try {
  let target;
  for (let attempt = 0; attempt < 40; attempt++) {
    try {
      target = await fetch("http://127.0.0.1:9227/json/new?about:blank", { method: "PUT" }).then(r => r.json());
      break;
    } catch { await sleep(250); }
  }
  assert(target, "Chrome did not start");
  socket = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise(resolve => socket.addEventListener("open", resolve, { once: true }));
  let id = 0;
  const calls = new Map(), errors = [];
  socket.addEventListener("message", event => {
    const message = JSON.parse(event.data);
    if (message.id) {
      const pending = calls.get(message.id);
      calls.delete(message.id);
      if (message.error) pending.reject(new Error(JSON.stringify(message.error)));
      else pending.resolve(message.result);
    } else if (message.method === "Runtime.exceptionThrown") errors.push(message.params.exceptionDetails.text);
  });
  const send = (method, params = {}) => new Promise((resolve, reject) => {
    const callId = ++id;
    calls.set(callId, { resolve, reject });
    socket.send(JSON.stringify({ id: callId, method, params }));
  });
  const evaluate = async expression => {
    const result = await send("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true });
    if (result.exceptionDetails) throw new Error(JSON.stringify(result.exceptionDetails));
    return result.result.value;
  };
  const until = async (expression, timeout = 60000) => {
    const deadline = Date.now() + timeout;
    while (Date.now() < deadline) {
      if (await evaluate(expression)) return;
      await sleep(250);
    }
    throw new Error("Timed out: " + expression);
  };
  const click = async (x, y) => {
    await send("Input.dispatchTouchEvent", { type: "touchStart", touchPoints: [{ x, y }] });
    await sleep(100);
    await send("Input.dispatchTouchEvent", { type: "touchEnd", touchPoints: [] });
  };
  const button = async selector => {
    const pos = await evaluate(`(()=>{const r=document.querySelector(${JSON.stringify(selector)}).getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()`);
    await click(pos.x, pos.y);
  };
  const playback = async (seconds = 0.3) => {
    const deadline = Date.now() + 60000;
    while (Date.now() < deadline) {
      if (await evaluate(`!document.getElementById('shelter-video').hidden && !document.getElementById('story-video').paused && document.getElementById('story-video').currentTime > ${seconds}`)) return;
      if (await evaluate("!document.getElementById('video-prompt').hidden")) await button("#video-resume");
      await sleep(250);
    }
    throw new Error("Video did not begin playing");
  };
  const get = expression => evaluate(`renpy_get(${JSON.stringify(expression)})`);
  const movie = async clip => {
    const source = await get(`"Video/" + shelter_visitor + "/" + shelter_data("clips")[${JSON.stringify(clip)}][0]`);
    const suffix = encodeURI(source.replace(/\.webm$/i, ".mp4"));
    await until(`!document.getElementById('shelter-video').hidden && document.getElementById('story-video').dataset.source.endsWith(${JSON.stringify(suffix)})`);
  };
  const firstVisitor = async () => {
    await until('renpy_get("bool(shelter_run_order) and not shelter_outcomes and shelter_visitor == shelter_run_order[0]")');
    const order = await get("list(shelter_run_order)");
    const roster = await get("list(SHELTER_VISITOR_ORDER)");
    assert.deepEqual([...order].sort(), [...roster].sort());
    assert.equal(new Set(order).size, roster.length);
    await movie("intro");
    return order;
  };
  const music = expected => until(`renpy_get("renpy.music.get_playing()").then(value => ${JSON.stringify(expected)} === null ? value === null : (value || "").includes(${JSON.stringify(expected)}))`);
  const screen = name => until(`renpy_get("bool(renpy.get_screen('${name}'))")`);
  const finishClip = async () => {
    await playback();
    await evaluate("document.getElementById('story-video').currentTime = document.getElementById('story-video').duration - .2");
    await until("document.getElementById('shelter-video').hidden", 10000);
  };
  const screenshot = async name => {
    const image = await send("Page.captureScreenshot", { format: "png" });
    await writeFile(path.join(output, name + ".png"), Buffer.from(image.data, "base64"));
  };
  diagnose = async () => {
    await screenshot("99-failure");
    console.log("Page status:", await evaluate("document.body.innerText"));
    console.log("Browser errors:", errors);
  };
  await send("Page.enable");
  await send("Runtime.enable");
  await send("Emulation.setDeviceMetricsOverride", { width: 844, height: 390, deviceScaleFactor: 1, mobile: true });
  await send("Emulation.setTouchEmulationEnabled", { enabled: true });
  await send("Page.navigate", { url: process.argv[2] || "http://127.0.0.1:8044" });
  await until("typeof window.renpy_get === 'function' && !document.getElementById('presplash')", 90000);
  await sleep(3000);
  await screenshot("01-menu");
  await music("menu1.mp3");
  console.log("PASS: Ren'Py loaded at phone landscape size.");
  // 1920x1080 is centered in the 844x390 viewport.
  const scale = 390 / 1080, offset = (844 - 1920 * scale) / 2;
  const gameClick = (x, y) => click(offset + x * scale, y * scale);
  await gameClick(1540, 481);
  await until("!document.getElementById('shelter-video').hidden");
  await playback(2);
  await music(null);
  assert(await evaluate("document.getElementById('story-video').currentSrc.startsWith('blob:')"), "Safari must receive a seekable local Blob");
  assert(await evaluate("!document.getElementById('video-caption').hidden"), "Intro caption missing");
  await screenshot("02-intro");
  await button("#video-pause");
  const paused = await evaluate("document.getElementById('story-video').currentTime");
  await sleep(500);
  assert.equal(await evaluate("document.getElementById('story-video').currentTime"), paused);
  await button("#video-resume");
  await until(`document.getElementById('story-video').currentTime > ${paused + .2}`);
  await button("#video-skip");
  const order = await firstVisitor();
  await playback(1);
  await music("shuum.mp3");
  await until('renpy_get("(renpy.music.get_pos() or 0) > .2")');
  await screenshot("03-visitor");
  console.log("PASS: Start, inline intro, subtitle, pause/resume, skip, random first visitor.", order);
  await finishClip();
  await screen("shelter_questions");
  await screenshot("04-questions");
  // Follow the actual shuffled order. Maral's admission still ends the run,
  // regardless of which position she occupies.
  for (const [index, visitor] of order.entries()) {
    assert.equal(await get("shelter_visitor"), visitor);
    assert.equal(await get("shelter_visitors_seen"), index);
    if (index === 0 || visitor === "Maral") {
      const backdrop = await get("shelter_wait_image(shelter_still)");
      await gameClick(441, 740);
      await movie("answer1");
      await playback(1);
      await screenshot(`05-${visitor}-answer`);
      await finishClip();
      await screen("shelter_decision");
      assert.equal(await get("shelter_still"), "answer1");
      if (visitor === "Maral") {
        assert.equal(await get("shelter_wait_image(shelter_still)"), backdrop,
          "Maral's first answer must preserve the doorway framing");
        await screenshot("08-maral-after-question");
      }
    }
    if (index === 0) {
      await gameClick(1479, 740);
      await movie("aim");
      await finishClip();
      await screen("shelter_decision");
      await gameClick(1062, 970);
      await movie("lower");
      await finishClip();
      await screen("shelter_decision");
      console.log("PASS: question/player speech, answer, aim and lower-weapon choices.");
    }
    if (visitor === "Maral") {
      await gameClick(1062, 970);
      await movie("admit");
      await finishClip();
      break;
    }
    await gameClick(858, 970);
    await movie("reject");
    await finishClip();
    await screen("shelter_next_visitor_card");
    await until(`renpy_get("renpy.music.get_playing(channel='shelter_knock')").then(value => (value || '').includes('ES_Doors'))`);
    await until(`renpy_get("(renpy.music.get_pos(channel='shelter_knock') or 0) > 5.5")`, 10000);
    assert(await get("bool(renpy.get_screen('shelter_next_visitor_card'))"));
    await until(`renpy_get("shelter_visitor").then(value => value === ${JSON.stringify(order[index + 1])})`);
    await movie("intro");
    await finishClip();
    await screen("shelter_questions");
  }
  await screen("shelter_result");
  await music("menu2.mp3");
  await screenshot("06-result");
  await gameClick(772, 718);
  await firstVisitor();
  assert.equal(await get("shelter_visitors_seen"), 0);
  await playback();
  await music("shuum.mp3");
  console.log("PASS: shuffled progression, Maral framing, ending music and shuffled replay.");
  // Return to the menu and exercise natural video EOF without a 100-second wait.
  await send("Page.navigate", { url: process.argv[2] || "http://127.0.0.1:8044" });
  await until("typeof window.renpy_get === 'function' && !document.getElementById('presplash')", 90000);
  await sleep(2500);
  await gameClick(1540, 481);
  await until("!document.getElementById('shelter-video').hidden");
  await playback();
  await until("document.getElementById('story-video').duration > 99");
  await evaluate("document.getElementById('story-video').currentTime = 99.5");
  await firstVisitor();
  console.log("PASS: intro EOF also advances to the first visitor.");
  assert.deepEqual(errors, [], "Browser runtime exceptions");
  console.log("Screenshots:", output);
} catch (error) {
  await diagnose();
  throw error;
} finally {
  socket?.close();
  browser.kill();
}
