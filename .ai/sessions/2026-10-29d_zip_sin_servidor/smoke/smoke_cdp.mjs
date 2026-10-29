// Prueba de humo C2: ZIP extraído abierto por file:// en Chromium (Edge/Chrome) sin red.
// Uso: node smoke_cdp.mjs <browser.exe> <carpeta extraída> <etiqueta>
import { spawn } from "node:child_process";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { pathToFileURL } from "node:url";

const [browser, root, label] = process.argv.slice(2);
const port = 9300 + Math.floor(Math.random() * 500);
const profile = mkdtempSync(join(tmpdir(), "smoke-"));
const proc = spawn(browser, [
  "--headless=new", `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`,
  "--no-first-run", "--no-default-browser-check", "about:blank",
], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

let target;
for (let i = 0; i < 50 && !target; i++) {
  await sleep(200);
  try {
    const list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
    target = list.find((t) => t.type === "page");
  } catch {}
}
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r));
let id = 0;
const pending = new Map();
const failed = [], remote = [], exceptions = [], urls = new Map();
let loaded = 0;
ws.addEventListener("message", (ev) => {
  const msg = JSON.parse(ev.data);
  if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); return; }
  const p = msg.params;
  if (msg.method === "Network.requestWillBeSent") { urls.set(p.requestId, p.request.url); if (/^https?:/.test(p.request.url)) remote.push(p.request.url); }
  if (msg.method === "Network.loadingFailed" && !/^https?:/.test(urls.get(p.requestId) ?? "")) failed.push(`${p.errorText} ${urls.get(p.requestId)}`);
  if (msg.method === "Network.responseReceived" && p.response.status >= 400) failed.push(`${p.response.status} ${p.response.url}`);
  if (msg.method === "Runtime.exceptionThrown") exceptions.push(p.exceptionDetails.exception?.description ?? p.exceptionDetails.text);
  if (msg.method === "Page.loadEventFired") loaded++;
});
const send = (method, params = {}) => new Promise((resolve) => {
  pending.set(++id, resolve); ws.send(JSON.stringify({ id, method, params }));
});
const evaluate = async (expression) =>
  (await send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true })).result.result.value;
const waitLoad = async (before) => { for (let i = 0; i < 100 && loaded === before; i++) await sleep(100); await sleep(500); };
const poll = async (expression, ms = 15000) => {
  for (let t = 0; t < ms; t += 250) { const v = await evaluate(expression); if (v) return v; await sleep(250); }
  return evaluate(expression);
};

for (const d of ["Network", "Runtime", "Page"]) await send(`${d}.enable`);
await send("Emulation.setDeviceMetricsOverride", { width: 1280, height: 900, deviceScaleFactor: 1, mobile: false });
await send("Network.emulateNetworkConditions", { offline: true, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });

const checks = [];
const check = (name, ok, detail = "") => checks.push({ name, ok: !!ok, detail });

let before = loaded;
await send("Page.navigate", { url: pathToFileURL(join(root, "index.html")).href });
await waitLoad(before);
check("portada", (await evaluate("document.title")).includes("doc_ia"), await evaluate("document.title"));
check("shim activo (Worker = IFrameWorker)", await evaluate("window.Worker === window.IFrameWorker"));
const folderLinks = await evaluate(`[...document.querySelectorAll("a[href]")].map(a => a.getAttribute("href")).filter(h => !/^[a-z]+:|^\\/\\/|^#/i.test(h) && h.split("#")[0].endsWith("/")).length`);
check("sin enlaces a carpeta en la portada", folderLinks === 0, `${folderLinks}`);

// Búsqueda desde la portada.
const query = "mermaid";
const rect = await evaluate(`(() => { const q = document.querySelector('[data-md-component="search-query"]') || document.querySelector('.md-search__button') || document.querySelector('input[type="search"]');
  const r = q.getBoundingClientRect(); return {x: r.x + r.width / 2, y: r.y + r.height / 2, tag: q.tagName}; })()`);
for (const type of ["mousePressed", "mouseReleased"]) await send("Input.dispatchMouseEvent", { type, x: rect.x, y: rect.y, button: "left", clickCount: 1 });
await sleep(300);
await send("Input.insertText", { text: query });
const results = await poll(`document.querySelectorAll('.md-search-result__item').length + (document.activeElement?.shadowRoot?.querySelectorAll('a[href]').length ?? 0)`);
const meta = await evaluate(`(document.querySelector('.md-search-result__meta')?.textContent?.trim() ?? '') + ' | foco: ' + document.activeElement?.tagName + '.' + document.activeElement?.className + ' | valor: ' + (document.activeElement?.value ?? '')`);
check(`búsqueda «${query}» con resultados`, results > 0, `${results} resultados; ${meta}`);
await evaluate(`(() => { const q = document.querySelector('[data-md-component="search-query"]') || document.querySelector('input[type="search"]'); q.value = ""; q.blur(); document.querySelector('[data-md-toggle="search"]') && (document.querySelector('[data-md-toggle="search"]').checked = false); return true; })()`);

// Navegación por clic en enlaces reales (5 páginas).
for (const page of ["quickstart.html", "api/build_docs_zip.html", "functional/build_docs_zip.html", "reference/index.html", "downloads.html"]) {
  const href = await evaluate(`(() => { const a = [...document.querySelectorAll("a[href]")].find(a => a.href.endsWith("/${page}")); if (!a) return null; a.click(); return a.href; })()`);
  if (!href) { check(`navegar a ${page}`, false, "enlace no encontrado"); continue; }
  before = loaded; await waitLoad(before);
  const loc = await evaluate("location.href");
  const h1 = await evaluate(`document.querySelector("article h1, h1")?.textContent?.trim() ?? ""`);
  check(`navegar a ${page}`, loc.endsWith(page) && h1, h1);
  if (page === "api/build_docs_zip.html") {
    const svgs = await poll(`(() => { const hosts = [...document.querySelectorAll("div.mermaid")].filter(e => e.getBoundingClientRect().height > 40);
      return document.querySelectorAll("pre.mermaid").length === 0 && hosts.length >= 2 && hosts.length; })()`);
    check("diagramas Mermaid dibujados", svgs >= 2, `${svgs}`);
  }
}

check("ninguna petición local fallida", failed.length === 0, failed.join(" | "));
check("sin excepciones JS", exceptions.length === 0, exceptions.slice(0, 3).join(" | "));
const unexpectedRemote = [...new Set(remote)].filter((u) => !/^https:\/\/(fonts\.googleapis\.com|api\.github\.com)\//.test(u));
check("ninguna petición remota salvo fuentes y datos del repo", unexpectedRemote.length === 0, unexpectedRemote.join(" | "));

ws.close(); proc.kill();
await sleep(500);
try { rmSync(profile, { recursive: true, force: true }); } catch {}
const ok = checks.every((c) => c.ok);
console.log(`== ${label}: ${ok ? "OK" : "FALLO"}`);
for (const c of checks) console.log(`  ${c.ok ? "✅" : "❌"} ${c.name}${c.detail ? ` — ${c.detail}` : ""}`);
console.log(`  (peticiones remotas intentadas: ${[...new Set(remote)].join(", ") || "ninguna"})`);
process.exit(ok ? 0 : 1);
