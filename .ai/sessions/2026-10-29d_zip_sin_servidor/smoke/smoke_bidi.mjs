// Prueba de humo C2 en Firefox (WebDriver BiDi): ZIP extraído por file://, sin red (proxy inválido).
// Uso: node smoke_bidi.mjs <firefox.exe> <carpeta extraída> <etiqueta>
import { spawn } from "node:child_process";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { pathToFileURL } from "node:url";

const [browser, root, label] = process.argv.slice(2);
const port = 9400 + Math.floor(Math.random() * 200);
const profile = mkdtempSync(join(tmpdir(), "ffsmoke-"));
writeFileSync(join(profile, "user.js"), [
  'user_pref("network.proxy.type", 1);',
  'user_pref("network.proxy.http", "127.0.0.1");', 'user_pref("network.proxy.http_port", 9);',
  'user_pref("network.proxy.ssl", "127.0.0.1");', 'user_pref("network.proxy.ssl_port", 9);',
  'user_pref("network.proxy.allow_hijacking_localhost", false);',
  'user_pref("browser.shell.checkDefaultBrowser", false);',
].join("\n"));
const proc = spawn(browser, ["-headless", "-no-remote", "-profile", profile, "--remote-debugging-port", String(port)], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

let ws;
for (let i = 0; i < 60 && !ws; i++) {
  await sleep(500);
  try {
    const s = new WebSocket(`ws://127.0.0.1:${port}/session`);
    await new Promise((ok, ko) => { s.addEventListener("open", ok); s.addEventListener("error", ko); });
    ws = s;
  } catch {}
}
let id = 0;
const pending = new Map();
ws.addEventListener("message", (ev) => { const m = JSON.parse(ev.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } });
const send = (method, params = {}) => new Promise((r) => { pending.set(++id, r); ws.send(JSON.stringify({ id, method, params })); });

await send("session.new", { capabilities: {} });
const context = (await send("browsingContext.getTree", {})).result.contexts[0].context;
await send("browsingContext.setViewport", { context, viewport: { width: 1280, height: 900 } });
const evaluate = async (expression) => {
  const r = await send("script.evaluate", { expression: `(async () => JSON.stringify(await (${expression})))()`, target: { context }, awaitPromise: true });
  const v = r.result?.result?.value;
  return v === undefined ? undefined : JSON.parse(v);
};
const poll = async (expression, ms = 15000) => {
  for (let t = 0; t < ms; t += 250) { const v = await evaluate(expression); if (v) return v; await sleep(250); }
  return evaluate(expression);
};
const click = (x, y) => send("input.performActions", { context, actions: [{ type: "pointer", id: "m", parameters: { pointerType: "mouse" },
  actions: [{ type: "pointerMove", x: Math.round(x), y: Math.round(y) }, { type: "pointerDown", button: 0 }, { type: "pointerUp", button: 0 }] }] });
const type = (text) => send("input.performActions", { context, actions: [{ type: "key", id: "k",
  actions: [...text].flatMap((c) => [{ type: "keyDown", value: c }, { type: "keyUp", value: c }]) }] });

const checks = [];
const check = (name, ok, detail = "") => checks.push({ name, ok: !!ok, detail });

await send("browsingContext.navigate", { context, url: pathToFileURL(join(root, "index.html")).href, wait: "complete" });
await sleep(1000);
check("portada", (await evaluate("document.title")).includes("doc_ia"), await evaluate("document.title"));
check("shim activo (Worker = IFrameWorker)", await evaluate("window.Worker === window.IFrameWorker"));

const query = "mermaid";
const rect = await evaluate(`(() => { const q = document.querySelector('[data-md-component="search-query"]') || document.querySelector('.md-search__button');
  const r = q.getBoundingClientRect(); return {x: r.x + r.width / 2, y: r.y + r.height / 2}; })()`);
await click(rect.x, rect.y);
await sleep(500);
// Firefox headless: document.hasFocus() es false y el foco no dispara el evento que abre la
// búsqueda (toggle `search`); con ventana, el clic del usuario lo abre. Se abre como el icono.
await evaluate(`(() => { const t = document.querySelector('[data-md-toggle="search"]'); if (t && !t.checked) t.click(); return true; })()`);
await click(rect.x, rect.y);
await type(query);
const results = await poll(`document.querySelectorAll('.md-search-result__item').length + (document.activeElement?.shadowRoot?.querySelectorAll('a[href]').length ?? 0)`);
check(`búsqueda «${query}» con resultados`, results > 0, `${results} resultados`);

for (const page of ["quickstart.html", "api/build_docs_zip.html", "reference/index.html", "downloads.html"]) {
  const href = await evaluate(`(() => { const a = [...document.querySelectorAll("a[href]")].find(a => a.href.endsWith("/${page}")); if (!a) return null; a.click(); return a.href; })()`);
  if (!href) { check(`navegar a ${page}`, false, "enlace no encontrado"); continue; }
  const loc = await poll(`location.href.endsWith("${page}") && document.readyState === "complete" && location.href`);
  await sleep(500);
  const h1 = await evaluate(`document.querySelector("article h1, h1")?.textContent?.trim() ?? ""`);
  check(`navegar a ${page}`, loc && h1, h1);
  if (page === "api/build_docs_zip.html") {
    const svgs = await poll(`(() => { const hosts = [...document.querySelectorAll("div.mermaid")].filter(e => e.getBoundingClientRect().height > 40);
      return document.querySelectorAll("pre.mermaid").length === 0 && hosts.length >= 2 && hosts.length; })()`);
    check("diagramas Mermaid dibujados", svgs >= 2, `${svgs}`);
  }
}

await send("session.end", {});
ws.close(); proc.kill();
const ok = checks.every((c) => c.ok);
console.log(`== ${label}: ${ok ? "OK" : "FALLO"}`);
for (const c of checks) console.log(`  ${c.ok ? "✅" : "❌"} ${c.name}${c.detail ? ` — ${c.detail}` : ""}`);
process.exit(ok ? 0 : 1);
