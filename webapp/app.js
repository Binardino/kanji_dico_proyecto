import { MOCK_KANJI } from "./mock-data.js";

// --- Data access -----------------------------------------------------
// Single seam to swap for the real API later:
// replace this body with `return (await fetch(`/api/kanji/${literal}`)).json()`
async function fetchKanjiData(literal) {
  return MOCK_KANJI[literal] ?? null;
}

// --- Rendering ---------------------------------------------------------
function renderInfoPanel(data) {
  document.getElementById("infoLiteral").textContent = data.literal;
  document.getElementById("infoOn").textContent = data.readings.on.join("、") || "—";
  document.getElementById("infoKun").textContent = data.readings.kun.join("、") || "—";
  document.getElementById("infoMeanings").textContent =
    data.meanings
      .filter((m) => m.lang === "en")
      .map((m) => m.text)
      .join(", ") || "—";
  document.getElementById("infoJlpt").textContent = data.jlpt ? `N${data.jlpt}` : "—";
  document.getElementById("infoGrade").textContent = data.grade ?? "—";
  document.getElementById("infoStrokes").textContent = data.stroke_count ?? "—";
}

const BASE_SPREAD = 170; // px offset applied to a depth-1 child, halved-ish at each deeper level

// Flattens the recursive decomposition tree into a positioned list.
// Each child is offset from its parent based on its IDS position (left/right/top/bottom);
// parentX/parentY are kept so the node can animate outward from where its parent landed.
function layoutTree(node, depth = 0, x = 0, y = 0, parentX = 0, parentY = 0, out = []) {
  out.push({ ...node, depth, x, y, parentX, parentY });

  const spread = BASE_SPREAD / (depth + 1);
  for (const child of node.children ?? []) {
    let cx = x;
    let cy = y;
    if (child.position === "left") cx = x - spread;
    else if (child.position === "right") cx = x + spread;
    else if (child.position === "top") cy = y - spread;
    else if (child.position === "bottom") cy = y + spread;

    layoutTree(child, depth + 1, cx, cy, x, y, out);
  }

  return out;
}

function buildStepCaption(nodesAtDepth) {
  return nodesAtDepth
    .map((n) => (n.is_radical ? `${n.char} (${n.radical_name})` : n.char))
    .join(" + ");
}

function renderDeconstruction(decomposition) {
  const section = document.getElementById("deconstruction");
  const stage = document.getElementById("stage");
  const stepsContainer = document.getElementById("steps");
  const depthNav = document.getElementById("depthNav");
  const atomicNote = document.getElementById("atomicNote");
  const nodeDetail = document.getElementById("nodeDetail");

  const flat = layoutTree(decomposition);
  const maxDepth = Math.max(...flat.map((n) => n.depth));

  nodeDetail.hidden = true;
  stage.classList.remove("has-zoom");
  stage.querySelectorAll(".decomp-node").forEach((el) => el.remove());
  stepsContainer.innerHTML = "";
  depthNav.innerHTML = "";

  if (maxDepth === 0) {
    section.hidden = true;
    atomicNote.hidden = false;
    return null;
  }

  atomicNote.hidden = true;
  section.hidden = false;

  for (const node of flat) {
    const el = document.createElement("div");
    el.className = "decomp-node" + (node.is_radical ? " is-radical" : "");
    el.dataset.depth = String(node.depth);
    el.style.setProperty("--x", `${node.x}px`);
    el.style.setProperty("--y", `${node.y}px`);
    el.style.setProperty("--px", `${node.parentX}px`);
    el.style.setProperty("--py", `${node.parentY}px`);
    el.style.setProperty("--char-size", `${Math.max(1.2, 3 - node.depth * 0.7)}rem`);

    const charEl = document.createElement("div");
    charEl.className = "decomp-node-char";
    charEl.textContent = node.char;
    el.appendChild(charEl);

    if (node.is_radical) {
      const label = document.createElement("div");
      label.className = "decomp-node-label";
      label.textContent = node.radical_name;
      el.appendChild(label);
    }

    el.addEventListener("click", () => toggleZoom(el, node, nodeDetail, stage));
    stage.appendChild(el);
  }

  // depth 0 (the assembled kanji) is always shown, scrolling reveals depth 1..maxDepth
  stage.querySelectorAll('.decomp-node[data-depth="0"]').forEach((el) => el.classList.add("visible"));

  for (let depth = 1; depth <= maxDepth; depth++) {
    const nodesAtDepth = flat.filter((n) => n.depth === depth);

    const step = document.createElement("div");
    step.className = "scrolly-step";
    step.dataset.depth = String(depth);
    step.innerHTML = `<div class="scrolly-step-caption">${buildStepCaption(nodesAtDepth)}</div>`;
    stepsContainer.appendChild(step);

    const navBtn = document.createElement("button");
    navBtn.type = "button";
    navBtn.title = `Niveau ${depth}`;
    navBtn.dataset.depth = String(depth);
    navBtn.addEventListener("click", () => step.scrollIntoView({ behavior: "smooth", block: "center" }));
    depthNav.appendChild(navBtn);
  }

  return maxDepth;
}

// --- Scroll animation ----------------------------------------------
let stepObserver = null;

function setActiveDepth(depth) {
  document.querySelectorAll(".decomp-node").forEach((el) => {
    const d = Number(el.dataset.depth);
    el.classList.toggle("visible", d === 0 || d <= depth);
  });
  document.querySelectorAll(".scrolly-step").forEach((el) => {
    el.classList.toggle("is-active", Number(el.dataset.depth) === depth);
  });
  document.querySelectorAll(".depth-nav button").forEach((btn) => {
    btn.classList.toggle("is-active", Number(btn.dataset.depth) === depth);
  });
}

function setupScrollAnimation(maxDepth) {
  if (stepObserver) {
    stepObserver.disconnect();
    stepObserver = null;
  }
  if (maxDepth === null) return;

  setActiveDepth(0);

  // A step counts as "active" once it crosses the vertical center of the viewport.
  stepObserver = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) setActiveDepth(Number(entry.target.dataset.depth));
      }
    },
    { threshold: 0, rootMargin: "-50% 0px -50% 0px" }
  );

  document.querySelectorAll(".scrolly-step").forEach((step) => stepObserver.observe(step));
}

// Click a revealed component to spotlight it and show its radical meaning.
function toggleZoom(el, node, detailPanel, stage) {
  const alreadyZoomed = el.classList.contains("zoomed");
  stage.querySelectorAll(".decomp-node.zoomed").forEach((n) => n.classList.remove("zoomed"));
  stage.classList.remove("has-zoom");

  if (alreadyZoomed || !el.classList.contains("visible")) {
    detailPanel.hidden = true;
    return;
  }

  el.classList.add("zoomed");
  stage.classList.add("has-zoom");

  detailPanel.innerHTML = `
    <div class="node-detail-char">${node.char}</div>
    <div class="node-detail-name">${node.is_radical ? node.radical_name : "Composant (pas un radical recensé)"}</div>
    <div class="node-detail-meaning">${node.is_radical ? node.radical_meaning : ""}</div>
  `;
  detailPanel.hidden = false;
}

// --- Search / selection ----------------------------------------------
function setupSearch(availableLiterals) {
  const input = document.getElementById("kanjiInput");
  const options = document.getElementById("kanjiOptions");
  const quickPicks = document.getElementById("quickPicks");

  options.innerHTML = availableLiterals
    .map((literal) => `<option value="${literal}"></option>`)
    .join("");

  quickPicks.innerHTML = availableLiterals
    .map((literal) => `<button type="button" data-literal="${literal}">${literal}</button>`)
    .join("");

  quickPicks.addEventListener("click", (event) => {
    const literal = event.target.dataset.literal;
    if (!literal) return;
    input.value = literal;
    showKanji(literal);
  });

  input.addEventListener("change", () => showKanji(input.value.trim()));
}

// --- Wiring --------------------------------------------------------------
async function showKanji(literal) {
  const data = await fetchKanjiData(literal);
  const input = document.getElementById("kanjiInput");

  if (!data) {
    input.classList.add("invalid");
    return;
  }
  input.classList.remove("invalid");

  document.getElementById("emptyState").hidden = true;
  document.getElementById("app").hidden = false;
  window.scrollTo({ top: 0 });

  renderInfoPanel(data);
  const maxDepth = renderDeconstruction(data.decomposition);
  setupScrollAnimation(maxDepth);
}

function init() {
  setupSearch(Object.keys(MOCK_KANJI));
}

init();
