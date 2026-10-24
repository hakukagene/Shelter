/* Inline video bridge for Safari. Game progression stays in Ren'Py. */
(() => {
  "use strict";
  const root = document.getElementById("shelter-video");
  const stage = document.getElementById("video-stage");
  const video = document.getElementById("story-video");
  const endFrame = document.getElementById("video-end-frame");
  const caption = document.getElementById("video-caption");
  const speaker = document.getElementById("caption-speaker");
  const words = document.getElementById("caption-words");
  const skip = document.getElementById("video-skip");
  const pause = document.getElementById("video-pause");
  const mute = document.getElementById("video-mute");
  const prompt = document.getElementById("video-prompt");
  const promptText = document.getElementById("video-message");
  const resume = document.getElementById("video-resume");
  const actions = document.getElementById("video-actions");
  const loading = document.getElementById("video-loading");
  const guide = document.getElementById("video-guide");
  let guideOpen = false, guideRequested = false, guideWasPaused = false;
  let active = false, sequence = 0, spec = null, frame = 0, cueIndex = -2;
  let errored = false;
  let download = null, objectUrl = null;
  let firstFrame = null;

  function revealVideo(current) {
    if (!active || api.finished || current !== sequence || video.readyState < 2) return;
    video.style.opacity = "1";
    loading.hidden = true;
  }

  function prepareFirstFrame(current) {
    // Keep the Ren'Py still visible while download, autoplay permission and
    // decoding are pending. A playing event alone is not a painted frame.
    video.style.opacity = "0";
    if (firstFrame !== null) video.cancelVideoFrameCallback?.(firstFrame);
    firstFrame = null;
    if (video.requestVideoFrameCallback) {
      firstFrame = video.requestVideoFrameCallback(() => {
        if (current !== sequence) return;
        firstFrame = null;
        revealVideo(current);
      });
    }
  }

  function revealLegacyVideo() {
    if (video.requestVideoFrameCallback || video.readyState < 2) return;
    const current = sequence;
    // Older browsers: wait for loaded data and two paint opportunities.
    requestAnimationFrame(() => requestAnimationFrame(() => revealVideo(current)));
  }

  function releaseVideo() {
    video.style.opacity = "0";
    if (firstFrame !== null) video.cancelVideoFrameCallback?.(firstFrame);
    firstFrame = null;
    download?.abort();
    download = null;
    video.pause();
    video.removeAttribute("src");
    video.load();
    if (objectUrl) URL.revokeObjectURL(objectUrl);
    objectUrl = null;
  }

  async function loadClip() {
    const current = sequence;
    download?.abort();
    download = new AbortController();
    prompt.hidden = true;
    loading.hidden = false;
    pause.disabled = true;
    loading.textContent = "Видео ачаалж байна…";
    try {
      // Sites' static host returns whole files for Range requests. A local Blob
      // gives Safari a seekable MP4 without depending on server byte ranges.
      // Keep only the current clip in memory, and abort it immediately on Skip.
      const response = await fetch(encodeURI(spec.src), { signal: download.signal });
      if (!response.ok) throw new Error("Video download failed");
      const blob = await response.blob();
      if (!active || api.finished || current !== sequence) return;
      if (objectUrl) URL.revokeObjectURL(objectUrl);
      objectUrl = URL.createObjectURL(blob);
      video.src = objectUrl;
      if (spec.startTime != null) {
        if (video.readyState < 1) {
          await new Promise((resolve, reject) => {
            video.addEventListener("loadedmetadata", resolve, { once: true });
            video.addEventListener("error", reject, { once: true });
          });
        }
        if (!active || api.finished || current !== sequence) return;
        video.currentTime = spec.startTime;
        if (video.seeking) {
          await new Promise((resolve, reject) => {
            video.addEventListener("seeked", resolve, { once: true });
            video.addEventListener("error", reject, { once: true });
          });
        }
      }
      if (!active || api.finished || current !== sequence) return;
      prepareFirstFrame(current);
      await play();
    } catch (error) {
      if (error.name === "AbortError" || !active || current !== sequence || api.finished) return;
      errored = true;
      showPrompt("Видео ачаалагдсангүй. Холболтоо шалгаад дахин оролдоно уу.", "Дахин оролдох");
    }
  }

  function fit() {
    const bounds = document.getElementById("canvas").getBoundingClientRect();
    const scale = Math.min(bounds.width / 1920, bounds.height / 1080);
    stage.style.transform = `translate(-50%, -50%) scale(${scale})`;
    stage.style.left = `${bounds.left + bounds.width / 2}px`;
    stage.style.top = `${bounds.top + bounds.height / 2}px`;
  }

  function showPrompt(message, label = "Үргэлжлүүлэх") {
    promptText.textContent = message;
    resume.textContent = label;
    prompt.hidden = false;
    loading.hidden = true;
  }

  async function play() {
    if (!active || api.finished || guideOpen) return;
    const current = sequence;
    prompt.hidden = true;
    if (errored) {
      errored = false;
      await loadClip();
      return;
    }
    try {
      // Called directly from a touch when Safari requires user activation.
      await video.play();
      if (current !== sequence || !active) return;
      pause.textContent = "Ⅱ";
      pause.setAttribute("aria-label", "Түр зогсоох");
      revealLegacyVideo();
    } catch (error) {
      if (current !== sequence || !active || error.name === "AbortError") return;
      showPrompt(error.name === "NotAllowedError"
        ? "Дуу, дүрсийг эхлүүлэхийн тулд товшино уу."
        : "Видео ачаалагдсангүй. Холболтоо шалгаад дахин оролдоно уу.",
      error.name === "NotAllowedError" ? "Тоглуулах" : "Дахин оролдох");
    }
  }

  function updateCaption() {
    if (!active || api.finished) return;
    if (guideOpen) { frame = requestAnimationFrame(updateCaption); return; }
    const time = video.currentTime;
    if (spec.endTime && time >= spec.endTime) {
      finish();
      return;
    }
    const index = spec.cues.findIndex(cue => cue[0] <= time && time < cue[1]);
    if (index !== cueIndex) {
      cueIndex = index;
      caption.hidden = index === -1;
      if (index >= 0) {
        const cue = spec.cues[index];
        speaker.textContent = cue[2] ? cue[2] + ": " : "";
        words.textContent = cue[3].replace(/\s+/g, " ").trim();
        words.style.fontSize = "";
        // Intro cues stay on one line, including future longer SRT edits.
        if (spec.intro) {
          const available = 1448 - speaker.offsetWidth;
          const required = words.scrollWidth;
          if (required > available) {
            words.style.fontSize = `${36 * available / required}px`;
          }
        }
      }
    }
    frame = requestAnimationFrame(updateCaption);
  }

  function finish() {
    if (!active || api.finished) return;
    api.finished = true;
    download?.abort();
    video.pause();
    loading.hidden = true;
    prompt.hidden = true;
    caption.hidden = true;
    // The trimmed clip's end poster also covers a stale cached, untrimmed MP4.
    if (spec.endTime && endFrame.complete && endFrame.naturalWidth) {
      endFrame.hidden = false;
    }
    cancelAnimationFrame(frame);
    // Hold the last frame until Ren'Py advances; never leave a dangling video.
  }

  const api = window.ShelterVideo = {
    finished: false,
    start(options) {
      sequence++;
      releaseVideo();
      guideOpen = guideRequested = false;
      active = true;
      api.finished = false;
      spec = options;
      cueIndex = -2;
      errored = false;
      root.hidden = false;
      endFrame.hidden = true;
      if (options.endPoster) endFrame.src = encodeURI(options.endPoster);
      else endFrame.removeAttribute("src");
      root.classList.toggle("intro", options.intro);
      caption.hidden = true;
      prompt.hidden = true;
      loading.hidden = false;
      skip.hidden = !options.intro;
      guide.hidden = options.intro;
      actions.hidden = options.intro;
      actions.replaceChildren();
      if (!options.intro) {
        for (const [icon, title] of options.actions || (options.armed
          ? [["shoot", "Буудах"], ["lower", "Буугаа буулгах"]]
          : [["reject", "Хөөх"], ["admit", "Оруулах"]])) {
          const item = document.createElement("div");
          item.className = "inactive-action";
          const img = document.createElement("img");
          img.src = `shelter-ui/${icon}.png`;
          img.alt = "";
          const text = document.createElement("span");
          text.textContent = title;
          item.append(img, text);
          actions.append(item);
        }
      }
      video.poster = options.poster ? encodeURI(options.poster) : "";
      video.dataset.source = encodeURI(options.src);
      video.volume = Math.max(0, Math.min(1, options.volume));
      video.muted = options.muted;
      mute.textContent = video.muted ? "Дуугүй" : "Дуутай";
      mute.setAttribute("aria-pressed", String(video.muted));
      fit();
      cancelAnimationFrame(frame);
      updateCaption();
      loadClip();
    },
    takeGuideRequest() {
      const requested = guideRequested;
      guideRequested = false;
      return requested;
    },
    resumeFromGuide() {
      if (!guideOpen) return;
      guideOpen = guideRequested = false;
      if (!active || api.finished) return;
      root.hidden = false;
      fit();
      if (!guideWasPaused) play();
    },
    close() {
      const closing = ++sequence;
      active = false;
      guideOpen = guideRequested = false;
      cancelAnimationFrame(frame);
      // Ren'Py has just drawn its handoff screen. Let that canvas reach the
      // compositor before uncovering it; never reveal the previous visitor.
      requestAnimationFrame(() => requestAnimationFrame(() => {
        if (closing !== sequence) return;
        root.hidden = true;
        releaseVideo();
      }));
    },
  };

  skip.addEventListener("click", () => { if (spec?.intro) finish(); });
  guide.addEventListener("click", () => {
    if (!active || api.finished || spec?.intro || guideOpen) return;
    guideWasPaused = video.paused;
    guideOpen = guideRequested = true;
    video.pause();
    root.hidden = true;
  });
  resume.addEventListener("click", play);
  pause.addEventListener("click", () => {
    if (video.paused) play();
    else {
      video.pause();
      showPrompt("Түр зогсоосон");
    }
  });
  mute.addEventListener("click", () => {
    video.muted = !video.muted;
    mute.textContent = video.muted ? "Дуугүй" : "Дуутай";
    mute.setAttribute("aria-pressed", String(video.muted));
  });
  video.addEventListener("ended", finish);
  video.addEventListener("loadeddata", revealLegacyVideo);
  video.addEventListener("playing", () => {
    if (!active || api.finished) return;
    prompt.hidden = true;
    pause.disabled = false;
    if (video.style.opacity === "1") loading.hidden = true;
    revealLegacyVideo();
  });
  video.addEventListener("waiting", () => { if (active && prompt.hidden) loading.hidden = false; });
  video.addEventListener("error", () => {
    if (!active || api.finished) return;
    errored = true;
    showPrompt("Видео ачаалагдсангүй. Холболтоо шалгаад дахин оролдоно уу.", "Дахин оролдох");
  });
  video.addEventListener("pause", () => {
    if (active && !api.finished && !video.ended) {
      pause.textContent = "▶";
      pause.setAttribute("aria-label", "Үргэлжлүүлэх");
    }
  });
  document.addEventListener("visibilitychange", () => {
    if (document.hidden && active && !api.finished) {
      video.pause();
      showPrompt("Тоглоомыг үргэлжлүүлэх");
    }
  });
  document.addEventListener("keydown", event => {
    if (!active) return;
    if (event.key === "Escape" && spec.intro) finish();
    if ([" ", "Escape", "Tab"].includes(event.key)) event.preventDefault();
  });
  window.addEventListener("resize", fit);
  window.visualViewport?.addEventListener("resize", fit);
})();
