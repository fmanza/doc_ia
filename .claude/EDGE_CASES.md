# Casos Límite Conocidos — doc_ia

> Plantilla inicial creada en el bootstrap (2026-06-10). Se puebla con el tiempo:
> cada caso límite descubierto en sesiones de trabajo se registra aquí con su contexto.

## Formato de registro

```markdown
## [área] — Título breve

- **Síntoma**: qué se observa
- **Causa**: por qué ocurre (verificado, no especulado)
- **Tratamiento**: cómo lo maneja el código o la instrucción IA
- **Sesión**: .ai/sessions/<fecha>/ donde se descubrió
```

## Casos registrados

## [mkdocs.yml] — `navigation.sections` impide colapsar el menú lateral

- **Síntoma**: En la documentación generada, los submenús del panel izquierdo no se pueden
  colapsar con clic. Los grupos del nav aparecen como etiquetas estáticas en gris tenue,
  no como elementos plegables. El botón ◀/▶ de sidebar tampoco aparece aunque
  `sidebar-toggle.js` esté cargado.
- **Causa**: `navigation.sections: true` en `theme.features` de `mkdocs.yml` activa el modo
  de grupos estáticos de Material, que deshabilita `.md-nav__item--nested`. Esto hace que
  `nav.css` (que aplica estilos a `--nested`) no tenga efecto sobre la colapsabilidad.
  Simultáneamente, si faltan `extra_css` y `extra_javascript`, los assets de toggle y Mermaid
  no se cargan en absoluto.
- **Tratamiento**:
  1. Eliminar `navigation.sections` de `theme.features` en `mkdocs.yml`.
  2. Crear `docs/assets/css/nav.css`, `docs/assets/css/mermaid.css`,
     `docs/assets/js/sidebar-toggle.js`
     (copiar desde `doc_ia/docs/assets/`; desde 2026-10-28 ya no se copia `mermaid.js`, ver § Mermaid; cambiar `STORAGE_KEY` en `sidebar-toggle.js`
     al nombre del proyecto, ej. `dpss_sidebar_collapsed`).
  3. Añadir `extra_css` y `extra_javascript` en `mkdocs.yml` referenciando esos assets.
  4. Añadir features universales ausentes: `navigation.tabs.sticky`, `navigation.footer`,
     `toc.follow`, `content.code.annotate`, `content.tabs.link`.
  5. Añadir markdown extensions universales ausentes: `pymdownx.highlight`,
     `pymdownx.inlinehilite`, `pymdownx.snippets`, `pymdownx.emoji`, `attr_list`, `md_in_html`.
- **Prevención**: La sección "Sincronización de Configuración Visual (Fase 0b)" de
  `/document-project` es ahora **OBLIGATORIA** al inicio de toda sesión (creación Y actualización).
  Ver checklist en `.claude/commands/document-project.md`.
- **Sesión**: `.ai/sessions/2026-06-12/` (dpss)

## [plugin MkDocs] — Plugin ZIP no encontrado al ejecutar `mkdocs build`

- **Síntoma**: `ERROR - Config value 'plugins': The "{nombre}_documentation_zip" plugin is not installed.`
  El build falla aunque el plugin fue creado e instalado correctamente.
- **Causa**: el entry point del plugin está registrado en un venv específico
  (`doc_ia\.venv\Lib\site-packages\{nombre}_docs-{versión}.dist-info`). Cuando el terminal
  no tiene ese venv activo, `mkdocs` resuelve a otro Python (p. ej.
  `C:\Users\{user}\AppData\Roaming\Python\Python314\Scripts\mkdocs.exe`) que no conoce el plugin.
  Hay múltiples `mkdocs` en el PATH del sistema; el que "gana" depende del orden del PATH
  y del venv activo en el terminal concreto.
- **Solución definitiva (2026-06-15)**: **no usar el sistema de plugins** para la generación del ZIP.
  Migrar a un hook MkDocs nativo (`mkdocs_hooks.py`) cargado mediante la clave `hooks:` de `mkdocs.yml`.
  El hook no requiere instalación, no usa entry points y funciona con cualquier Python que tenga `mkdocs`.
  Patrón canónico: `doc_ia/mkdocs_hooks.py` (solo cambiar `zip_path` para otro proyecto).
  ```yaml
  # mkdocs.yml — añadir:
  hooks:
    - mkdocs_hooks.py
  # y eliminar el plugin de la sección plugins:
  ```
- **Workaround temporal** (si no es posible migrar aún):
  - Activar el venv antes del build: `doc_ia\.venv\Scripts\Activate.ps1`
  - O invocar explícitamente: `python -m mkdocs build --strict`
    (donde `python` = `doc_ia\.venv\Scripts\python.exe`)
- **Sesión**: `.ai/sessions/2026-06-12/` (descubierto); `.ai/sessions/2026-06-15_hooks_migration/` (resuelto)

## [doc_trace] — `drift` marca páginas tras cambios triviales o tras editar `mkdocs.yml`/`CLAUDE.md`

- **Síntoma**: `python scripts/doc_trace.py drift` lista una página como `stale` aunque su
  contenido sigue siendo correcto.
- **Causa**: la huella es el SHA256 del fichero fuente completo (saltos normalizados a LF). Un
  comentario, un espacio o cualquier edición de una fuente compartida (p. ej. `mkdocs.yml` o
  `CLAUDE.md`, citadas por `docs/reference/index.md`) cambia la huella. Es intencionado: el
  script no interpreta el contenido.
- **Solución**: revisar la página contra el diff de la fuente (`git diff <fuente>`); si sigue
  siendo correcta, re-sellar con `python scripts/doc_trace.py stamp <página>`. No re-sellar a
  ciegas en bloque.
- **No es causa**: sellar una página que es fuente de otra (p. ej. el Mapa Funcional): el
  frontmatter de las fuentes `.md` se excluye de la huella.
- **Sesión**: `.ai/sessions/2026-10-28_archetypes_v2/` (P3)

## [mkdocs_hooks.py] — El ZIP `latest` se regenera aunque `mkdocs build --strict` falle

- **Síntoma**: tras un build estricto que termina con `Aborted with N warnings in strict mode`,
  `site/doc_ia-docs-latest.zip` y su `.sha256` tienen fecha nueva.
- **Causa**: MkDocs 1.6 ejecuta `on_post_build` antes de comprobar los avisos del modo estricto.
- **Decisión (2026-10-28)**: aceptado. El ZIP local de un build fallido no se distribuye: los
  workflows solo publican si el build termina con 0. No usar `site/` tras un build fallido.
  Con `build_docs_zip.py --builder zensical` no ocurre: el ZIP se genera solo tras un build OK.
- **Sesión**: `.ai/sessions/2026-10-28c_quality_pending/`

## [Zensical] — `hooks:` de `mkdocs.yml` se ignora en silencio

- **Síntoma**: `zensical build --strict` falla con `changelog.md: page does not exist` en un
  checkout limpio, o termina bien pero `site/` no contiene `doc_ia-docs-latest.zip` y los enlaces
  de `docs/downloads.md` al ZIP quedan rotos (ningún `--strict` valida `<a href>` en HTML crudo).
- **Causa**: Zensical (0.0.73) no soporta la clave `hooks:` ni la API de plugins de MkDocs y no
  emite ningún aviso (zensical.org/compatibility/configuration). Los plugins no soportados
  también se ignoran en silencio.
- **Tratamiento**: construir siempre con `python scripts/build_docs_zip.py --builder zensical`,
  que ejecuta `hooks/sync_root_docs.py` antes y `mkdocs_hooks.py` después de un build OK.
  `python -m zensical serve` no sincroniza: tras editar `CHANGELOG.md`/`CONTRIBUTING.md`, ejecutar
  `python hooks/sync_root_docs.py` (en Claude Code lo hace el PostToolUse).
- **Guardas**: `tests/test_zensical_compat.py` falla si `mkdocs.yml` declara un plugin fuera de
  `ZENSICAL_SUPPORTED_PLUGINS` o si los enlaces al ZIP de `docs/downloads.md` no resuelven al
  ZIP `latest` (p. ej. al cambiar `use_directory_urls`). Al actualizar Zensical, revisar la lista
  contra zensical.org/compatibility/plugins.
- **Sesión**: `.ai/sessions/2026-10-28d_zensical_migration/` (F1, F4)

## [Mermaid] — CDN propio + `mermaid.run()` duplican el render del tema

- **Síntoma**: los diagramas se ven, pero cada bloque `.mermaid` contiene además un SVG de error
  de Mermaid oculto. Con carreras de carga, en algún diagrama puede llegar a verse «Syntax error
  in text».
- **Causa** (verificada con Edge headless + CDP, `DOM.getDocument(pierce=True)`): con
  `custom_fences: mermaid`, Material (y Zensical) cargan Mermaid por sí mismos y pintan cada
  diagrama en un shadow root **cerrado**. El `mermaid.run()` de `assets/js/mermaid.js` (más el CDN
  `mermaid@11`) procesa después el mismo bloque, ya transformado, y falla: 23/23 SVG de error
  ocultos en doc_ia.
- **Contraprueba**: sin `custom_fences` no se genera ningún `.mermaid` y el diagrama sale como
  código. Ni el CDN ni `mermaid.js` lo arreglan, porque también buscan `.mermaid`. La pieza
  imprescindible es `custom_fences`. La RCA de 2026-06-12a (socyalpro) atribuyó el fallo a la
  falta del CDN.
- **Tratamiento**: `extra_javascript` sin CDN de Mermaid ni `assets/js/mermaid.js`; `custom_fences`
  obligatorio (Fase 0b / Fase 5). Verificado en doc_ia: 23/23 diagramas visibles con MkDocs y con
  Zensical, en claro y en oscuro; en oscuro el tema aplica sus colores. Mermaid se sigue cargando
  desde CDN (lo hace el tema): el ZIP offline necesita red para los diagramas hasta F10 (`privacy`).
- **Prevención**: `tests/test_docs_conformance.py::test_mermaid_nodes_do_not_start_with_slash`
  para errores de sintaxis que `--strict` no ve; verificación visual con CDP antes de cambiar la
  integración.
- **Sesión**: `.ai/sessions/2026-10-28d_zensical_migration/` (F6a, F6)

## [Mermaid] — Entidades HTML en labels se pintan con un `&` sobrante

- **Síntoma**: `H[on_post_build&#40;config&#41;]` se ve como `on_post_build&(config&)`; la regla
  `@` → `&#64;` (sesión 2026-06-12b) pinta `Cl&@ve`. El build `--strict` pasa y Mermaid no da error.
- **Causa** (verificada renderizando con mermaid@11 y @12 en Edge headless): Mermaid no decodifica
  entidades HTML; su sintaxis propia es `#64;` (sin `&`). El `&` queda como texto.
- **Diagnóstico previo correcto, remedio incorrecto**: sin comillas, `@`, `(`, `)`, `{` o `}`
  dentro de `[...]` o `{...}` sí son parse error en v11 y v12.
- **Tratamiento**: label entre comillas dobles (`A["Cl@ve (firma)"]`); una `"` interna → `#quot;`.
  `#`, `#64;`, `A@{ shape: … }` y `["/ruta"]` entre comillas renderizan bien.
- **Prevención**: `tests/test_docs_conformance.py::test_mermaid_no_html_entities` y
  `::test_mermaid_special_chars_quoted` (detector calibrado con fixtures renderizadas).
- **Pendiente fuera de doc_ia**: los destinos que aplicaron la regla `&#64;` (socyalpro) muestran
  el `&`; corregir con un hotfix en cada repositorio.
- **Sesión**: `.ai/sessions/2026-10-28e_mermaid_diagrams/` (M0)

## [Mermaid] — Material y Zensical cargan versiones mayores distintas (RESUELTO: Mermaid local)

- **Síntoma**: el mismo diagrama se ve distinto según el generador; en Zensical los flowchart usan
  otro layout.
- **Causa** (verificada en los bundles instalados): MkDocs Material 9.8.0 carga
  `unpkg.com/mermaid@11/dist/mermaid.min.js` y Zensical 0.0.73 `unpkg.com/mermaid@12/...`. En v12
  el flowchart usa por defecto el layout ELK y el look `neo`. Las dos son versiones mayores
  flotantes y necesitan red, también en el ZIP offline.
- **Tratamiento** (sesión 2026-10-28f): el sitio sirve su propia copia,
  `docs/assets/vendor/mermaid/mermaid-12.2.0.min.js`. Los bundles de los dos temas solo descargan
  de unpkg si `typeof mermaid=="undefined"`, así que ambos dibujan con esa versión y sin red.
  `tests/test_mermaid_assets.py` vigila la coherencia y que el bundle instalado conserve esa
  condición (si una actualización del tema la cambia, el fichero local dejaría de usarse).
- **Ojo al verificar**: renderizar varios diagramas a la vez con `startOnLoad` en una página de
  prueba con mermaid@12 los superpone; no es un fallo de la documentación. Verificar en el sitio
  construido o diagrama a diagrama con `mermaid.render()`.
- **Sesión**: `.ai/sessions/2026-10-28e_mermaid_diagrams/` (M5)

## [Mermaid] — Material + Mermaid 12: subgrafos ilegibles en modo oscuro

- **Síntoma**: con Mermaid 12 cargado por Material, los `subgraph` de los flowchart salen con
  fondos pastel claros y el texto de sus nodos casi no se lee en el esquema `slate`.
- **Causa** (verificada con capturas en Edge headless): Mermaid 12 cambió el tema por defecto del
  flowchart. Zensical inicializa Mermaid con `theme: "default"` y no lo sufre; Material no pasa
  `theme` (su integración se diseñó para v11).
- **Tratamiento**: `docs/assets/js/mermaid-theme.js`, cargado justo después de la librería, envuelve
  `mermaid.initialize` y añade `theme: "default"` y `themeVariables.dropShadow: "none"` (lo mismo
  que Zensical; la configuración del tema prevalece). También fija `startOnLoad: false` en cuanto
  carga, para que la librería no procese los bloques por su cuenta en el evento `load` y duplique
  el render (§ CDN propio + `mermaid.run()`).
- **Verificado**: 24/24 diagramas sin conexión, 0 SVG de error, MkDocs y Zensical, claro y oscuro.
- **Sesión**: `.ai/sessions/2026-10-28f_mermaid_local/` (L1)

## [document-project] — Fuentes convertidas copiadas al destino con nombres distintos

- **Síntoma**: en distintas sesiones de `/document-project` los documentos convertidos a Markdown
  aparecían en el destino como `.fuentes/` o como `_fuentes/`.
- **Causa**: `convert_to_md.py` escribe siempre en `<origen>/md/`, pero ninguna instrucción decía
  si el destino debía recibir una copia ni con qué nombre; el agente lo improvisaba.
- **Tratamiento**: regla única en la Fase 0c (Paso 5) de `document_project.prompt.md`, repetida
  en el comando, el agente y `SHARED_INSTRUCTIONS.md`: copia **siempre** en
  `<raíz del destino>/_fuentes/<nombre_origen>/<ruta relativa al origen>`, versionada y fuera de
  `docs/`; `.fuentes/` o `fuentes/` en la raíz del destino se migran a `_fuentes/` con
  confirmación. `.fuentes/` se descartó por oculta: las búsquedas del agente la saltan.
  `tests/test_docs_conformance.py::test_sources_folder_is_canonical` comprueba las cuatro
  instrucciones.
- **Sesión**: `.ai/sessions/2026-10-29_fuentes_destino/`

## [ZIP offline] — Abrir `index.html` sin servidor muestra listados de carpetas (RESUELTO)

- **Síntoma**: tras extraer el ZIP, abrir `index.html` con doble clic carga la portada, pero el
  menú lleva a listados de carpetas (o a nada) y la búsqueda no responde. `downloads.md` y el
  Paso B3 del producto lo ofrecían como «Opción B: todos los menús funcionan».
- **Causa**: `use_directory_urls: true` genera enlaces a carpetas (`api/archetypes/`); con
  `file://` el navegador no resuelve `index.html` dentro de ellas. La búsqueda usa un Web Worker,
  que los navegadores bloquean en `file://`.
- **Tratamiento**: primero, solo servidor local (`start-server.py`, solo `127.0.0.1`). Desde
  2026-10-29d, `use_directory_urls: false` + plugin `offline` + shim iframe-worker local: el ZIP se
  abre con doble clic en `index.html` tras extraerlo (ver los dos casos siguientes);
  `test_zip_opens_with_double_click_after_extracting` vigila las instrucciones y
  `build_docs_zip.py` rechaza un `site/` con enlaces a carpetas o scripts remotos.
- **Sesión**: .ai/sessions/2026-10-29b_ver_documentacion/, .ai/sessions/2026-10-29d_zip_sin_servidor/

## [offline] — Material y Zensical descargan el shim iframe-worker de unpkg

- **Síntoma**: con el plugin `offline`, cada página carga
  `<script src="https://unpkg.com/iframe-worker/shim">`. Sin red, el ZIP navega pero la búsqueda
  no responde, y el build `--strict` no avisa.
- **Causa**: el plugin (Material `plugins/offline/plugin.py`; Zensical `_apply_offline_plugin`)
  añade esa URL a `extra.polyfills` salvo que ya exista una entrada que contenga `iframe-worker`.
  El shim sustituye `Worker` por un iframe cuando `protocol === "file:"`.
- **Tratamiento**: copia local en `docs/assets/vendor/iframe-worker/` (huella fijada, `LICENSE`,
  `SOURCE.txt`) declarada en `extra.polyfills`; los dos generadores emiten la ruta relativa por
  página y no añaden unpkg. `test_config_builds_a_site_that_opens_without_server` y el validador
  de `build_docs_zip.py` (ningún `<script src="http…">`). El índice JS difiere:
  `search/search_index.js` (MkDocs) y `search.js` en la raíz (Zensical); se aceptan los dos.
- **Sesión**: .ai/sessions/2026-10-29d_zip_sin_servidor/

## [mkdocs_hooks.py] — El ZIP `latest` salía sin el índice de búsqueda en JS

- **Síntoma**: con MkDocs, `site/doc_ia-docs-latest.zip` (2,69 MB) no traía
  `search/search_index.js` y el ZIP versionado (2,80 MB) sí: la búsqueda fallaba justo en el ZIP
  que se descarga desde la web.
- **Causa**: el plugin `offline` escribe el índice en su `on_post_build` con prioridad -100
  («last»); el hook, con prioridad 0, empaquetaba antes.
- **Tratamiento**: `on_post_build.mkdocs_priority = -200` en `mkdocs_hooks.py` (lo mismo que
  `mkdocs.plugins.event_priority`, sin importar mkdocs: Zensical carga el hook sin él).
  `test_zip_hook_runs_after_offline_plugin` compara con la prioridad real del plugin. El producto
  lo exige en destinos con hook propio (Gap V3).
- **Sesión**: .ai/sessions/2026-10-29d_zip_sin_servidor/

## [build_docs_zip.py] — El ZIP versionado anidaba el ZIP `latest` y no traía `start-server.py`

- **Síntoma**: `dist/doc_ia-docs-0.3.0.zip` (el que suben las Releases) tenía 155 entradas, entre
  ellas `doc_ia-docs-latest.zip` y su `.sha256`, y ningún `start-server.py`.
- **Causa**: `_zip` usaba `shutil.make_archive` sobre `site/` entero, donde el hook ya había dejado
  el ZIP `latest`; el servidor solo lo añadía el hook.
- **Tratamiento**: `_zip` replica el contenido del hook: excluye `.zip`/`.sha256` y añade
  `EXTRA_FILES`. Test `test_versioned_zip_matches_latest_layout`.
- **Sesión**: .ai/sessions/2026-10-29b_ver_documentacion/

## [start-server.py] — Una conexión ociosa bloquea el servidor; en Windows dos servidores comparten puerto

- **Síntoma**: con `socketserver.TCPServer`, abrir una conexión sin enviar petición (como la
  preconexión especulativa de Chrome) deja colgadas las demás peticiones. Con
  `ThreadingHTTPServer` tal cual, en Windows un segundo servidor en el mismo puerto arranca sin
  error. Aparte: tras extraer el ZIP en Windows, la primera lectura del Mermaid local (~5 MB) tardó
  11 s incluso sin servidor (análisis del antivirus), y luego fue inmediata.
- **Causa**: `TCPServer` atiende una conexión cada vez. `HTTPServer.allow_reuse_address = True`
  activa `SO_REUSEADDR`, que en Windows permite enlazar un puerto en uso.
- **Tratamiento**: `DocsServer(ThreadingHTTPServer)` con `allow_reuse_address = sys.platform !=
  "win32"`. Tests con loopback real: `test_idle_connection_does_not_block_real_server`,
  `test_second_server_on_same_port_fails`. La primera carga lenta está en «Problemas frecuentes»
  de `VER_DOCUMENTACION.md`.
- **Sesión**: .ai/sessions/2026-10-29b_ver_documentacion/

## [doc_trace changes] — Las menciones en prosa inflan el inventario incremental

- **Síntoma**: probado sobre el historial real de doc_ia (baseline `d25c29a`), la primera versión
  de `changes` marcó 27 páginas a revisar: ADR, changelog, guías y ejemplos que solo **nombran**
  `scripts/build_docs_zip.py` o `CHANGELOG.md`.
- **Causa**: buscaba la ruta en todo el texto de la página. Un ADR que menciona un script no
  queda obsoleto porque el script cambie.
- **Tratamiento**: `pages_citing` separa **citas** (frontmatter `fuentes:` + bloque
  «Evidencia») de **menciones** (resto del cuerpo). Solo las citas van a «Páginas a revisar» (10
  en el mismo caso: justo las revisadas y selladas en la feature anterior); las menciones se
  listan aparte y la Fase 1 las marca B solo si el diff cambia lo descrito.
- **Sesión**: .ai/sessions/2026-10-29c_modo_incremental/

## [doc_trace changes] — Con el destino dentro del origen, cada cierre parece un cambio

- **Síntoma**: si origen y destino son el mismo repositorio (doc_ia), el commit del CIERRE
  (páginas, `.ai/`, `_fuentes/`, `mkdocs.yml`, `VER_DOCUMENTACION.md`) aparece como cambio del
  origen en la sesión siguiente, y `baseline` marcaría siempre `sucio: true`.
- **Causa**: `baseline` se toma antes del commit de documentación y el diff abarca todo el
  repositorio.
- **Tratamiento**: `documentation_paths` excluye `docs_dir` y `DOC_ARTIFACTS` cuando están dentro
  del origen, tanto en `changes` como en el cálculo de `sucio`. Test
  `test_destination_inside_origin_ignores_its_own_artifacts`.
- **Sesión**: .ai/sessions/2026-10-29c_modo_incremental/
