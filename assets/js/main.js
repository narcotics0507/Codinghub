const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));

function initReveal() {
  const elements = $$(".reveal");
  if (!elements.length) return;
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("visible");
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.12 });
  elements.forEach((el) => observer.observe(el));
}

function initCopyButtons() {
  $$(".copy-btn").forEach((button) => {
    button.addEventListener("click", async () => {
      const target = button.closest(".code-card")?.querySelector("code");
      if (!target) return;
      await navigator.clipboard.writeText(target.innerText.trim());
      const old = button.textContent;
      button.textContent = "已复制";
      setTimeout(() => { button.textContent = old; }, 1300);
    });
  });
}

function initLightbox() {
  const lightbox = $(".lightbox");
  if (!lightbox) return;
  const image = $("img", lightbox);
  $$("img[data-zoom]").forEach((img) => {
    img.addEventListener("click", () => {
      image.src = img.src;
      image.alt = img.alt || "";
      lightbox.classList.add("open");
    });
  });
  lightbox.addEventListener("click", (event) => {
    if (event.target === lightbox || event.target.tagName === "BUTTON") {
      lightbox.classList.remove("open");
      image.removeAttribute("src");
    }
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") lightbox.classList.remove("open");
  });
}

function initRailSpy() {
  const links = $$(".rail-link[href^='#']");
  if (!links.length) return;
  const map = new Map(links.map((link) => [link.getAttribute("href").slice(1), link]));
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      links.forEach((link) => link.classList.remove("active"));
      map.get(entry.target.id)?.classList.add("active");
    });
  }, { rootMargin: "-35% 0px -55% 0px", threshold: 0 });
  [...map.keys()].forEach((id) => {
    const section = document.getElementById(id);
    if (section) observer.observe(section);
  });
}

function initHomeHero() {
  const hero = $("[data-home-hero]");
  const tools = $("[data-home-tools]");
  if (!hero || !tools) return;

  const setMode = (mode) => {
    hero.dataset.mode = mode;
    $$("[data-home-tool]", tools).forEach((button) => {
      const active = button.dataset.homeTool === mode;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", String(active));
    });
    $$("[data-home-panel]", hero).forEach((panel) => {
      const active = panel.dataset.homePanel === mode;
      panel.hidden = !active;
      panel.classList.toggle("active", active);
    });
    $$("[data-home-card]").forEach((card) => {
      card.classList.toggle("is-focused", card.dataset.homeCard === mode);
    });
  };

  tools.addEventListener("click", (event) => {
    const button = event.target.closest("[data-home-tool]");
    if (button) setMode(button.dataset.homeTool);
  });
  $$("[data-home-card]").forEach((card) => {
    card.addEventListener("mouseenter", () => setMode(card.dataset.homeCard));
    card.addEventListener("focusin", () => setMode(card.dataset.homeCard));
  });
  setMode(hero.dataset.mode || "codex");
}

function initCommandGenerator() {
  const form = $("[data-command-generator]");
  if (!form) return;
  const output = $("[data-command-output]");
  const hint = $("[data-command-hint]");
  const shellQuote = (value) => `"${String(value).replace(/(["\\$`])/g, "\\$1")}"`;
  const update = () => {
    const prompt = $("#genPrompt", form).value.trim() || "一张干净的 AI 工具教程封面图";
    const size = $("#genSize", form).value;
    const quality = $("#genQuality", form).value;
    const file = $("#genFile", form).value.trim() || "cover.png";
    output.textContent = [
      "gpt-image \\",
      `  -p ${shellQuote(prompt)} \\`,
      `  -f ${shellQuote(file)} \\`,
      `  --size ${size} \\`,
      `  --quality ${quality}`,
    ].join("\n");
    const notes = [];
    if (/中文|标题|文字/.test(prompt) && quality !== "high") notes.push("包含中文标题时建议选择 high。");
    if (!file.endsWith(".png") && !file.endsWith(".jpg")) notes.push("文件名建议使用 .png 或 .jpg。");
    hint.textContent = notes.join(" ");
  };
  $$("input, select, textarea", form).forEach((el) => {
    el.addEventListener("input", update);
    el.addEventListener("change", update);
  });
  update();
}

function initProgressLine() {
  const bar = $("[data-scroll-progress]");
  if (!bar) return;
  const update = () => {
    const max = document.documentElement.scrollHeight - innerHeight;
    const ratio = max > 0 ? scrollY / max : 0;
    bar.style.transform = `scaleX(${Math.min(1, Math.max(0, ratio))})`;
  };
  addEventListener("scroll", update, { passive: true });
  update();
}

document.addEventListener("DOMContentLoaded", () => {
  initReveal();
  initCopyButtons();
  initLightbox();
  initRailSpy();
  initHomeHero();
  initCommandGenerator();
  initProgressLine();
});
