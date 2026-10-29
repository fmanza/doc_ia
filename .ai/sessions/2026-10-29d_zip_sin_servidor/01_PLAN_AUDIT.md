# PLAN + AUDIT_PLAN — ZIP navegable sin servidor (D5)

## PLAN

**Objetivo**: el ZIP (latest y versionado) se abre con doble clic en `index.html` tras extraerlo:
navega, busca y dibuja Mermaid sin Python, sin servidor y sin red, con MkDocs Material y con
Zensical. `start-server.py` queda como alternativa.

**Mecanismo** (verificado en el spike): plugin `offline` + shim `iframe-worker` servido en local
desde `docs/assets/vendor/iframe-worker/` y declarado en `extra.polyfills`.

### Decisiones (recomendación)
| ID | Decisión | Recomendación |
|---|---|---|
| D1 | `offline` siempre o conmutado con `!ENV` | **Siempre**: el ZIP latest lo genera el hook en cada build; con conmutador, latest y versionado divergen o hay doble build |
| D2 | `use_directory_urls: false` explícito | **Sí**: `doc_trace llms` y `test_downloads_links_point_to_latest_zip` leen la clave; con `true` + plugin, `llms.txt` apuntaría a URLs inexistentes |
| D3 | Validar el sitio antes de empaquetar | **Sí**, en `build_docs_zip.py` (exit 1, sin flag de escape); el hook copiable no cambia |
| D4 | Google Fonts (petición externa con red; sin red degrada a fuentes del sistema) | Fuera de alcance; anotar |
| D5 | Origen del shim | Descarga única del tarball npm con integridad verificada, como Mermaid |

### Capas
| Capa | Ficheros |
|---|---|
| L1 Build | `mkdocs.yml`; `docs/assets/vendor/iframe-worker/{shim, LICENSE, SOURCE.txt}`; `scripts/build_docs_zip.py` (`_offline_problems(site_dir) -> list[str]`); `.github/workflows/ci.yml` (validar también el build MkDocs); `docs/llms.txt` |
| L2 Tests | `tests/test_offline_assets.py` (nuevo); `test_build_docs_zip.py` (fixture válido + 5 casos del validador, dos disposiciones de índice); `test_docs_conformance.py` (invertir la guarda de `index.html`) |
| L3 Producto + docs | `TEMPLATE_mkdocs.yml`; `VER_DOCUMENTACION.template.md` + instancia; prompt, comando, agente, SHARED, CLAUDE.md, DOCUMENTATION_STANDARD, docs.instructions (Fase 0b: 5 → 6 recursos; Paso B3; Fase 7b); `downloads.md`; páginas `build_docs_zip`; reference; troubleshooting; EDGE_CASES; notas de `docs-zip-release.yml`; CHANGELOG; `.ai/{product,glossary}.md` |

**Tipos**: ninguno público. CLI sin cambios de argumentos; postcondición nueva: exit 1 si
`site/` no es navegable por `file://`.

## AUDIT_PLAN

### Riesgos funcionales
| ID | Riesgo | Mitigación |
|---|---|---|
| F1 | Búsqueda por `file://` verificada solo a nivel de build | Condición C2: prueba de humo en navegador real |
| F2 | Doble clic dentro del ZIP sin extraer (Explorador de Windows) abre `index.html` suelto, sin CSS/JS | Instrucciones: «Extraer todo» primero; fila en problemas frecuentes |
| F3 | URLs pasan a `*.html`: marcadores a `/api/x/` dejan de valer | doc_ia sin Pages; en destinos con web publicada, aviso en el RESUMEN |
| F4 | `downloads.md` enlaza `../doc_ia-docs-latest.zip` | Pasa a `doc_ia-docs-latest.zip`; el test existente ya deriva la ruta de la clave |
| F5 | Releases ≤ 0.3.0 no son navegables sin servidor | Nota en §4 de la plantilla, como C5 de 2026-10-29b |
| F6 | Secciones fijas de `VER_DOCUMENTACION` | Encabezados intactos; cambia el contenido de §1 y §4 |

### Riesgos técnicos
| ID | Riesgo | Mitigación |
|---|---|---|
| T1 | Ambos generadores inyectan unpkg si falta el polyfill local | Test de configuración + validador (ningún `<script src="http…">`) |
| T2 | Disposición del índice distinta y ligada a internos de Zensical (alfa) | Validador acepta las dos; versión exacta ya fijada; EDGE_CASES |
| T3 | `mkdocs.yml` con tags `!!python`: no se puede cargar con `yaml.safe_load` | Lectura textual, como `test_mermaid_assets.py` |
| T4 | Falsos positivos del validador | Solo `href`/`src` relativos (sin esquema) terminados en `/`; spike = 0 en ambos |
| T5 | LSP/ISP: sin interfaces ni async; postcondición más fuerte | Un destino con el script copiado y sin `offline` falla a propósito → CHANGELOG «Changed»; el producto copia script y config juntos |
| T6 | Fixture `_project` actual produce un sitio no válido | Se amplía con índice y shim |
| T7 | +~420 KB sin comprimir por el índice duplicado | Aceptado: `start-server.py` usa el `.json` |

### Riesgos de seguridad
| ID | Riesgo | Mitigación |
|---|---|---|
| S1 | Código de terceros vendorizado | SHA256 fijado en test, integridad npm, LICENSE, SOURCE.txt; revisión del contenido antes de añadirlo |
| S2 | Tentación de documentar flags del navegador (`--allow-file-access-from-files`) | Prohibido en las instrucciones; no hace falta |
| S3 | — | Mejora: el destinatario ya no necesita un servidor escuchando |

### Simplificaciones
Sin conmutador `!ENV`; sin flags CLI nuevos; sin test de navegador automatizado (prueba de humo
manual); `start-server.py` y la Ruta B con servidor se conservan como alternativa.

### Veredicto: GO_CONDICIONAL
- C1 Autorizar la descarga única del shim (red solo en IMPLEMENT, nunca en tests).
- C2 Prueba de humo con el ZIP extraído, MkDocs y Zensical, en Edge/Chrome y Firefox, con la
  red desactivada: 5 páginas, una búsqueda con resultados, un diagrama Mermaid, 0 peticiones fallidas.
- C3 Instrucciones: «Extraer todo» antes del doble clic; nunca flags del navegador.
- C4 D1-D3 confirmadas.
- C5 DoD: ruff, mypy, pytest, `mkdocs build --strict`, `doc_trace drift/matrix/llms` sin pendientes.

---

## Decisión del usuario (2026-10-29)
«IMPLEMENT»: D1-D3 según recomendación; C1 autorizada (descarga única del shim).

## IMPLEMENT
| Capa | Ficheros | Estado |
|---|---|---|
| L1 Build | `docs/assets/vendor/iframe-worker/` (shim 1.0.4: sha512 de npm verificado, SHA256 fijado, contenido revisado: 1,4 KB, sin red); `mkdocs.yml` (`use_directory_urls: false`, `offline`, `extra.polyfills`); `scripts/build_docs_zip.py` (`_offline_problems`, `_check_offline`); `mkdocs_hooks.py` (prioridad -200); `ci.yml` (paso «ZIP navegable sin servidor»); notas de `docs-zip-release.yml`; `docs/llms.txt` (URLs `*.html`) | ✅ |
| L2 Tests | `tests/test_offline_assets.py` (nuevo, 4); `test_build_docs_zip.py` (+10 casos, fixture con índice JS); `test_docs_conformance.py` (guarda de `index.html` invertida: 3 + 6 casos) | ✅ |
| L3 Producto + docs | `TEMPLATE_mkdocs.yml`, `VER_DOCUMENTACION.template.md` + instancia, prompt (Fase 0b 6 recursos, Fase 5b/c, A2-1, Gap V3, B2, B3, Zensical 7b), comando, agente, SHARED, CLAUDE.md, DOCUMENTATION_STANDARD §4.1, docs.instructions; `downloads.md`, `functional/build_docs_zip.md` (regla «Abrir sin servidor», AC-12..15), `api/build_docs_zip.md`, ejemplo, referencia, troubleshooting, `functional/document_project.md`, `api/document_project.md`, mapa funcional (14/15); EDGE_CASES (1 resuelto + 2); CONTRIBUTING «Actualizar iframe-worker»; CHANGELOG; `.ai/{product,glossary}.md` | ✅ |

## AUDIT_CODE — GO
| ID | Hallazgo | Resolución |
|---|---|---|
| K1 | **Bug**: con MkDocs, el ZIP `latest` salía sin `search/search_index.js` (2,69 MB frente a 2,80 MB del versionado): `offline` escribe el índice en `on_post_build` con prioridad -100 y el hook empaquetaba antes | `on_post_build.mkdocs_priority = -200` sin importar mkdocs; `test_zip_hook_runs_after_offline_plugin` contra la prioridad real del plugin; EDGE_CASES; Gap V3 en el producto |
| K2 | Material, por `file://`, solo envía el índice al worker al abrir la búsqueda (toggle `search`); una prueba con eventos sintéticos da un falso «Inicializando búsqueda» | Prueba de humo con ratón/teclado reales (CDP `Input.*`) |
| K3 | Zensical monta la búsqueda en un shadow DOM abierto e índice en `search.js` (raíz) | Validador acepta las dos rutas; la prueba cuenta resultados dentro del shadow root |
| K4 | Control negativo: mismo sitio con el shim de unpkg y sin red → búsqueda bloqueada en «Inicializando» | Confirma que la copia local es imprescindible (T1) |
| K5 | Firefox sin ventana: `document.hasFocus()` false, el foco no abre la búsqueda | La prueba abre el toggle como el icono; ⚠️ en la Evidencia; con ventana lo abre el clic |
| K6 | `\bsrc=` también casa `data-src=`; scripts remotos legítimos (analítica, CDN de MathJax) hacen fallar el empaquetado | Aceptado: en un ZIP sin red no funcionarían; el mensaje indica la configuración esperada |
| K7 | Con `zensical`, si `_check_offline` falla el ZIP `latest` ya está en `site/` | Documentado en la técnica (Errores) y la funcional (casos especiales) |
| K8 | Otra sesión (`2026-10-29c_modo_incremental`, commit `fc18349`) trabajó en paralelo en `develop` y tomó el id `29c` | Sesión renombrada a `29d`; diffs verificados: solo cambios propios sobre `fc18349` |
| K9 | Las fuentes de Google y la API de GitHub (`repo_url`) se piden al abrir con red; sin red fallan sin efecto visible | Fuera de alcance (D4) |

**Prueba de humo C2** (`smoke/`, fuera de la CI; navegadores sin ventana, red cortada): Edge,
Chrome y Firefox × MkDocs y Zensical → 6/6 OK: portada, shim activo, búsqueda «mermaid» con
resultados, 4-5 páginas por clic en enlaces, 2 diagramas dibujados, 0 peticiones locales
fallidas, 0 excepciones JS, ninguna petición remota salvo fuentes y API de GitHub.

**DoD**: ruff ✅ · format ✅ · mypy ✅ · pytest 263 ✅ · `mkdocs build --strict` ✅ ·
`build_docs_zip.py` con MkDocs y Zensical ✅ · `doc_trace drift` 0 · `matrix` ✅ · `llms --check` ✅.

## Pendiente
- Comprobación manual de un clic en la búsqueda con Firefox con ventana (K5).
- `VER_DOCUMENTACION.md` nombra `doc_ia-docs-0.3.0.zip`, que aún no se abre con doble clic: al
  publicar la versión siguiente, actualizar el nombre (lo indica la propia guía).
- Sin commit hasta indicación del usuario.
