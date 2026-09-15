// CV Builder Dashboard — frontend logic
(() => {
  "use strict";

  const els = {
    input: document.getElementById("input"),
    urlToggle: document.getElementById("urlToggle"),
    urlField: document.getElementById("urlField"),
    generateBtn: document.getElementById("generateBtn"),
    log: document.getElementById("log"),
    health: document.getElementById("health"),
    clearLog: document.getElementById("clearLog"),
  };

  let abortController = null;

  // ---- Helpers -----------------------------------------------------------
  function logLine(msg, cls) {
    const span = document.createElement("span");
    span.className = cls || "line-info";
    span.textContent = msg;
    els.log.appendChild(span);
    els.log.scrollTop = els.log.scrollHeight;
  }

  function isUrlLike(value) {
    return /^https?:\/\//i.test(value.trim());
  }

  function setInputTypeFromValue() {
    if (isUrlLike(els.input.value)) els.urlToggle.checked = true;
  }

  // ---- Health check ------------------------------------------------------
  async function checkHealth() {
    try {
      const res = await fetch("/health");
      els.health.textContent = res.ok ? "server online" : "server offline";
    } catch {
      els.health.textContent = "server offline";
    }
  }

  // ---- SSE streaming (state machine) ------------------------------------
  async function runGeneration() {
    const input = els.input.value.trim();
    const inputType = els.urlToggle.checked ? "url" : "text";

    if (!input) {
      logLine("✗ Please enter a Job Description or URL.", "line-error");
      return;
    }

    abortController = new AbortController();
    els.generateBtn.disabled = true;
    els.generateBtn.textContent = "Generating…";
    logLine(`Starting generation (type: ${inputType})…`, "line-info");

    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input, input_type: inputType }),
        signal: abortController.signal,
      });

      if (!res.ok || !res.body) {
        logLine(`✗ Request failed (${res.status})`, "line-error");
        return;
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      let pendingType = null; // "progress" | "error" | "done" from the first data: line

      const readLoop = async () => {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          buffer += decoder.decode(value, { stream: true });

          const lines = buffer.split("\n");
          buffer = lines.pop(); // last element is the partial (unterminated) line

          for (const rawLine of lines) {
            const line = rawLine.trim();
            if (line === "") {
              // blank line = event boundary; do NOT reset pendingType so a
              // trailing single-line "data: done" event is not lost.
              continue;
            }
            if (line.startsWith("data: ")) {
              const payload = line.slice(6);
              if (pendingType === null) {
                // First data: line is the event type ("progress" | "error" | "done")
                pendingType = payload;
              } else {
                // Second data: line is the message
                if (pendingType === "error") logLine(payload, "line-error");
                else if (pendingType === "done") logLine(payload, "line-done");
                else if (payload.startsWith("\u2713")) logLine(payload, "line-done"); // a completed check → green
                else logLine(payload, "line-info");
                pendingType = null;
              }
            }
          }
        }
      };

      await readLoop();
      // The "done" event is emitted as a single-line frame ("data: done"),
      // so it never triggers the emit path above; handle it explicitly here.
      if (pendingType === "done") {
        logLine("✓ All documents generated successfully.", "line-done");
      } else {
        logLine("✓ Stream complete.", "line-done");
      }
    } catch (err) {
      if (err.name === "AbortError") {
        logLine("Aborted.", "line-warn");
      } else {
        logLine(`✗ ${err.message}`, "line-error");
      }
    } finally {
      els.generateBtn.disabled = false;
      els.generateBtn.textContent = "Generate Documents";
    }
  }

  // ---- Wire up -----------------------------------------------------------
  els.generateBtn.addEventListener("click", runGeneration);
  els.urlToggle.addEventListener("change", () => {
    els.urlField.classList.toggle("hidden", !els.urlToggle.checked);
    if (els.urlToggle.checked && els.input.value.trim()) setInputTypeFromValue();
    else els.input.value = "";
  });
  els.input.addEventListener("input", setInputTypeFromValue);
  els.clearLog.addEventListener("click", () => { els.log.innerHTML = ""; });

  checkHealth();
})();
