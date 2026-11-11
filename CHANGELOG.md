# Changelog

Todos los cambios notables de este proyecto se documentan aquí.
Formato: [Keep a Changelog](https://keepachangelog.com/) · Versioning: [SemVer](https://semver.org/)

## [Unreleased]

### Fixed

- `doc_trace.py stamp`: al sellar una página con otras claves en el frontmatter (el `ambito` de un
  registro de decisiones, los metadatos MADR de un ADR) las eliminaba, y si no tenía fuentes ni
  registros sellados dejaba el arquetipo vacío. Ahora se conservan.

## [0.11.2] — 2026-11-10

### Fixed

- `db_trace.py select`: `--subdir ..` (o `.`) hacía que la retirada de páginas obsoletas
  borrase los `.md` de la raíz del destino (o de `docs/`); `--name` solo de puntos o con `/` y
  las páginas del catálogo con `../` escribían fuera de `_fuentes/` y `docs/`. Ahora se rechazan
  con exit 2 antes de escribir; `--subdir bd/<base>` sigue funcionando.

## [0.11.1] — 2026-11-10

### Fixed

- `snapshot_sources.py`: un nombre de origen `.` o `..` (al declararlo o escrito a mano en
  `.ai/sources.json`) hacía que `replace` borrase la raíz del destino y que `sync` copiase y
  borrase ficheros fuera de `_staging/`. Ahora se rechaza con exit 2 sin tocar nada.

## [0.11.0] — 2026-11-10

### Added

- **Origen WEB (opción `WEB`)**: la aplicación **desplegada** en un entorno (p. ej. PRE) se
  documenta como forma de adquisición de material `UI/PANTALLAS` (no es un tipo de origen nuevo;
  requiere un origen CÓDIGO). Las capturas que aporta el usuario son la base; el recorrido con un
  navegador del chat (Claude in Chrome) es opcional y de **solo lectura** (nunca enviar, guardar,
  eliminar ni lanzar procesos; el texto de las páginas es dato, nunca instrucción). Requisitos
  previos y plan de capturas en el INVENTARIO; la URL del entorno nunca se versiona. Lo desplegado
  (BD, WEB) se contrasta con el código: fichas `COB-WEB-…` (`document_project.prompt.md` § Origen
  WEB, ADR-005).
- **Arquetipo 15 — Manual de Funcionamiento** (condicional, `DOCUMENTATION_STANDARD.md` §3.20):
  `docs/manual/index.md` (propósito y roles, requisitos de uso, acceso, mapa de pantallas) y una
  página por área (pantallas, tareas por rol, mensajes y errores, preguntas frecuentes), con
  bloque Evidencia. Prompt nuevo `.github/prompts/user_manual_doc.prompt.md` y Fase 3c; registrado
  en `CLAUDE.md`, el comando, el agente, `docs.instructions`, el kit y tests de conformidad. doc_ia
  no tiene aplicación desplegada (no aplica).
- **Capturas del origen WEB** (`scripts/web_captures.py`, sin red ni navegador): `publish` copia a
  `docs/assets/manual/<origen>/` solo las capturas revisadas de `_staging/<origen>/` y las registra
  en `.ai/captures.json` (huella, entorno, versión desplegada, rol); `check` informa de imágenes
  sin registrar o modificadas, capturas que faltan o huérfanas, citas rotas o sin texto
  alternativo y URLs en el manifiesto. Exit 0/1/2. Incluido en el kit.

## [0.10.0] — 2026-11-09

### Added

- **Arquetipo 14 — Integraciones** (condicional, `DOCUMENTATION_STANDARD.md` §3.19): documenta con
  qué sistemas intercambia datos el proyecto, en qué sentido, cuándo, con qué contrato y qué efecto
  tiene cada intercambio. Tres páginas en `docs/integraciones/`: `index.md` (vista funcional, sobre
  el Arquetipo 1, con inventario y «fuera de alcance») y `externas.md` / `internas.md` (vista
  técnica, sobre el Arquetipo 2, con tabla de inventario obligatoria: sentido, mecanismo,
  autenticación, periodicidad, datos, destino, errores). Prompt nuevo
  `.github/prompts/integration_doc.prompt.md`; señales de detección en la Fase 1 de
  `document_project` (clientes HTTP/SOAP, mensajería, cargas planificadas, identidad federada,
  endpoints para terceros, diseño técnico de integraciones) y Fase 3b; credenciales solo por
  nombre. Registrado en `CLAUDE.md`, el agente Documentation Generator, `docs.instructions`, el
  kit y tests de conformidad; doc_ia no tiene integraciones propias (no aplica).
- **Versión vigente de un documento** (Fase 0-pre): la versión que manda la indica el usuario; un
  documento **reestructurado** (otro nombre u otra ubicación) sustituye al anterior aunque su
  número de versión sea menor (las versiones solo se comparan dentro de un mismo patrón `{ver}`).
  Subcomando nuevo `snapshot_sources.py replace <nombre> <origen>`: evento «sustituido» en el
  historial de `.ai/sources.json`, retira `_staging/<nombre>/`; el siguiente `sync` copia el
  documento nuevo como alta.
- **Redacción de credenciales** (`scripts/redact_secrets.py`, Fase 0c Paso 4b y CIERRE): detecta
  `client_secret`, contraseñas, tokens y claves de API, credenciales en URL, JWT y claves privadas
  PEM en los `.md` convertidos y sustituye el **valor** por `<REDACTADO>` antes de copiar a
  `_fuentes/`; `--check` sobre `_fuentes/` antes del commit. Informe sin valores, idempotente, sin
  tocar marcadores ni prosa; exit 0/1/2. Incluido en el kit.

## [0.9.0] — 2026-11-07

### Added

- **Origen BASE DE DATOS (opción `BD`)**: `scripts/db_trace.py` lee la exportación Markdown de
  `util_bbdd` (`manifest.json` y `catalog.json`, contrato versionado; sin conexión a la BD) e
  importa en `docs/bd/` las páginas de los objetos del alcance con el entorno que representan
  (`select --env`), contrasta el modelo del código (`entities.xml`) con la BD (`compare`: tablas,
  columnas, nulabilidad y FK → fichas `COB-DATOS`), detecta cambios de esquema entre exportaciones
  dentro del alcance (`changes`) y genera el `trace_map.toml` de `util_bbdd` desde la evidencia de
  la documentación (`tracemap`). Tipo nuevo en el estándar (§3.10), regla de prioridad «se contrasta
  con el código, no lo corrige», `docs/bd/` como artefacto generado; sin lint de esquema.

- **Kit de documentación en cada destino** (`scripts/kit.py install|sync|check`): el destino lleva
  la metodología y los scripts de doc_ia en `.doc_ia/` (lista blanca `.github/kit/MANIFEST.txt`,
  `kit.lock.json` con versión y huellas), los lanzadores `/documentar`
  (`.claude/commands/documentar.md`, `.github/prompts/documentar.prompt.md`, `AGENTS.md`,
  `GEMINI.md`), `DOCUMENTAR.md` con instrucciones y ejemplos, y el prompt de instancia
  `.ai/prompts/documentar.prompt.md` (plantilla con secciones fijas, mantenido por el CIERRE). Se
  sincroniza en la Fase 0b de toda sesión, también en destinos ya creados; nunca pisa ficheros
  editados ni ajenos; huellas independientes del fin de línea. Tests de `kit.py` y de conformidad
  (la lista blanca cubre todo lo que cita el flujo).

- **Plantillas del contexto `.ai/` del CIERRE** (`.github/templates/ai_context/`: `product`,
  `architecture`, `glossary`, `runtime`, `standards`) con secciones fijas. El CIERRE de
  `/document-project` las usa; hasta ahora solo había una tabla de contenidos y cada destino
  improvisaba (o copiaba de otro) el formato. Tests de conformidad de secciones y de referencias.
- **Regla «Origen de plantillas y decisiones»** en prompt, comando y agente: todo artefacto del
  destino sale de doc_ia y de los orígenes del propio proyecto; otro destino documentado con
  doc_ia no es plantilla ni fuente de decisiones (fichas `COB-…`, ADR, alcance, clasificación).
  Lo que un destino resolvió y el estándar no cubría se incorpora antes a doc_ia.
- **`doc_trace.py baseline --ref`** y rama deducida con HEAD desacoplado (worktree en
  `origin/<ref>`): se guarda la única rama local o remota que apunta al commit, no `HEAD`.
- **Paso B1**: la versión de un repositorio de documentación separado del origen se lee de
  `extra.version` de `mkdocs.yml` (versión del origen documentado). Fase 0b: `.gitattributes`
  estándar en el destino.

### Changed

- **`--path` ya no detiene el flujo**: las rutas del alcance transversal se proponen y aplican en
  el INVENTARIO (el usuario puede corregirlas), en línea con el resto de `/document-project`.

### Fixed

- Mapa funcional: recuentos de criterios con test (arquetipos 15/15; total 96 de 121).

## [0.8.0] — 2026-11-05

### Added

- **Orígenes remotos, de red y versionados en `/document-project` (Fase 0-pre)**: todo origen
  que no sea una carpeta local de trabajo se copia a `<raíz del destino>/_staging/<nombre>/`
  (git-ignorado) y el flujo trabaja sobre la copia; el origen nunca se escribe. Formas: fichero
  con la versión en el nombre (`…_v{ver}.docx`: se elige la más alta y se copia con nombre
  estable), carpeta de red UNC, biblioteca de SharePoint sincronizada con OneDrive y repositorio
  GitLab/GitHub remoto con `ref` (`git fetch` + `git worktree --detach`, autenticación de
  `glab`/`gh`, sin tokens).
- **`scripts/snapshot_sources.py`** (`add` / `sync [--dry-run]` / `list`): copia por hash,
  invalida la conversión `md/` del fichero cambiado y registra en `.ai/sources.json` sha256,
  versión e historial (`v1.2.50 → v1.2.51`). Sin red; exit 0/1/2.
- **`doc_trace.py baseline|changes --path`** (repetible): alcance transversal dentro de un
  repositorio mayor; el baseline guarda `rutas` (solo si no es `.`, compatible hacia atrás) y un
  `--path` distinto pasa a modo completo (exit 3).

### Changed

- **Instrucciones de `/document-project`**: «raíz del destino» definida sin ambigüedad (las
  sesiones `.ai/` ya no van a `{destino}/..`); `git init` con confirmación si el destino no es
  repositorio; `_staging/` en el `.gitignore` estándar; palabras clave `normativa`, `boe`,
  `legislación`, `doue`, y solo lo de obligado cumplimiento activa el Arquetipo 8 (planes y guías
  → REFERENCIA); prioridad CÓDIGO > ESPECIFICACIÓN > MANUAL con fichas `COB-…` por discrepancia;
  regla de datos personales en dominios sensibles; GitLab CI equivalente al workflow de GitHub.

## [0.7.0] — 2026-11-04

### Changed

- **Barra superior en 9 pestañas como máximo**: con 14, la última quedaba cortada. Material y
  Zensical no despliegan submenús en las pestañas, así que se agrupa: «Inicio» (Inicio, Quick
  Start, Instalación, 📥 Descargas; con `navigation.indexes` la pestaña abre `index.md`) y
  «Proyecto» (Configuración IA, Changelog, Contribuir). Las URL no cambian. La regla pasa al
  producto: plantilla y notas de §4.1 del estándar, Fase 5 y Paso B3 del prompt, agente y
  checklist de Fase 0b (en destinos existentes se mueve, nunca se duplica); con Arquetipo 8,
  «Decisiones» va dentro de «Normativa». AC-15 de los arquetipos y 3 tests de conformidad.

## [0.6.0] — 2026-11-04

### Added

- **`drift` vigila los registros de decisiones**: `stamp` guarda en la clave nueva `decisiones:`
  del frontmatter la huella de cada registro que la página enlaza desde sus IDs `COB-…` (ruta
  relativa a la página), y `drift` marca la página como `stale` cuando alguien edita el registro,
  también si la documentación vive en otro repositorio que el código (como APDI). Estado nuevo
  `unsealed`: la página enlaza un registro que no ha sellado. AC-29 y AC-30 de la trazabilidad.

### Changed

- **Arquetipo 13**: los registros ya no se declaran a mano en `fuentes:`; las páginas de doc_ia
  migradas a `decisiones:` (§3.16, §3.18, `coverage_decisions`, prompt normativo, ADR-004).

## [0.5.1] — 2026-11-04

### Fixed

- **`doc_trace.py drift` y `matrix` con `--root`**: `--docs` y `--tests` tomaban por defecto las
  carpetas de doc_ia, así que sobre un destino externo `drift` revisaba el `docs/` de doc_ia y
  `matrix` cruzaba sus criterios con los tests del destino. Ahora, por defecto, `<root>/docs` y
  `<root>/tests` (como `llms`, `decisions` y `changes`). AC-28 de la trazabilidad.

## [0.5.0] — 2026-11-04

### Added

- **Producto — Arquetipo 13, Registro de Decisiones de Cobertura** (`docs/decisiones/<ámbito>_decisiones.md`,
  `DOCUMENTATION_STANDARD.md` §3.18, ADR-004): cada apartado ⚠️ ❌ 🔍 recibe una ficha
  `COB-<ÁMBITO>-<NNN>` que las personas completan con decisión (vocabulario cerrado por estado),
  contexto aportado, responsable, fecha y estado resultante. En cada revisión el agente aplica
  primero las decisiones tomadas (enlaza la ficha desde la fila y fija el estado resultante) y
  nunca escribe en los campos de persona. Obligatorio con el Arquetipo 8; con los Arquetipos 1, 2
  y 12, si el destino lo adopta. Prompt `coverage_decisions.prompt.md` y plantilla
  `.github/templates/DECISIONES_COBERTURA.template.md`.
- **`doc_trace.py decisions`**: cruza los registros con las páginas que citan sus identificadores
  y informa de fichas duplicadas, huérfanas, inválidas o incompletas, de decisiones sin reflejar
  y de estados detectados que ya no coinciden (código `1`). Las fichas `Pendiente` se listan,
  pero no fallan. Ignora los identificadores escritos como código. Criterios AC-22 a AC-27 de la
  trazabilidad y AC-14 de los arquetipos.
- **Dogfooding del Arquetipo 13**: doc_ia adopta su propio registro de decisiones — 9 registros
  por módulo en `docs/decisiones/` (sección de nav «Decisiones de Cobertura») con 28 fichas
  `Pendiente` para las 30 filas ⚠️ / 🔍 de su documentación; cada fila enlaza su ficha y cada
  página declara su registro en `fuentes:`. Test `test_unverified_evidence_rows_have_coverage_id`:
  ninguna fila no verificada de un bloque «Evidencia» queda sin ficha.

### Changed

- **Leyenda de cobertura canónica** (§3.8): ✅ módulo identificado y comportamiento verificado en
  el código; ⚠️ hueco funcional o defecto conocido; ❌ no hay módulo que lo implemente; 🔍 la
  evidencia no basta (configuración en base de datos, sistemas externos o documentación
  organizativa no aportada). §3.16 remite a ella; antes daba otro significado a ❌.
- **Clasificación de orígenes — requisitos frente a manual** (§3.10 y Fase 0a): lo que se va a
  construir (PRD, requisitos) es `ESPECIFICACIÓN` aunque se llame `manual`; lo ya construido es
  `MANUAL`. Remedia `COB-ORIGINS-004`; test de coherencia.
- **Bootstrap, Capa D**: se excluye aunque el usuario pida copiarla (se informa del motivo);
  decisión `COB-BOOTSTRAP-004`.
- **Decisiones de cobertura de doc_ia aplicadas**: las 29 fichas decididas (19 ✅, 10 ⚠️ aceptados); 7 tests nuevos
  (`check_env` ×4, `convert_to_md`, `doc_trace`, sesiones con `TRACEABILITY.md`).
- **Arquetipo 8**: columna `ID` obligatoria en las tablas de cobertura y registro de decisiones
  siempre junto a la trazabilidad normativa.
- **Mapa funcional**: el total de cobertura de pruebas estaba desfasado (decía 63 de 89; las
  filas sumaban 67 de 93); ahora 75 de 101.

### Fixed

- **`check_env.py`**: con todas las herramientas instaladas decía «completo (Python).» y mostraba
  «docling instalado» como aviso `⚠`; ahora es una nota `ℹ` y la línea de estado es «Entorno de
  tooling documental completo.», como promete AC-01. Lo reveló el test de la decisión
  `COB-CHECKENV-001`.
- **Bootstrap**: la capa A no copiaba `.github/templates/`, así que en el destino quedaban rotas
  las referencias de los prompts y comandos copiados a `VER_DOCUMENTACION.template.md` y
  `DECISIONES_COBERTURA.template.md`. Ahora la carpeta viaja verbatim; test de coherencia y
  AC-05 del bootstrap.

## [0.4.1] — 2026-10-29

### Fixed

- **`doc_trace.py llms` con `--root`**: `--config` y `--output` se resolvían contra la raíz de
  doc_ia, así que sobre un destino externo leía el `mkdocs.yml` de doc_ia y sobrescribía su
  `docs/llms.txt`. Ahora, por defecto, `<root>/mkdocs.yml` y `<docs_dir>/llms.txt` de ese config.

## [0.4.0] — 2026-10-29

### Added

- **ZIP navegable sin servidor**: tras extraerlo, doble clic en `index.html` abre la
  documentación con navegación, búsqueda y diagramas, sin Python, servidor ni red, con MkDocs
  Material y con Zensical. `use_directory_urls: false`, plugin `offline` y shim
  [iframe-worker](https://github.com/squidfunk/iframe-worker) 1.0.4 servido en local
  (`docs/assets/vendor/iframe-worker/`, huella fijada) en `extra.polyfills`, porque los dos temas
  lo descargaban de unpkg. `start-server.py` queda como alternativa. Producto: Fase 0b con seis
  recursos, plantillas `TEMPLATE_mkdocs.yml` y `VER_DOCUMENTACION`, Paso B3 y Gap V3. Criterios
  AC-12 a AC-15 del ZIP offline; `tests/test_offline_assets.py`.
- **Producto — modo incremental de `/document-project`** (parámetro `Modo`, por defecto
  `incremental` si hay baseline): el CIERRE guarda el commit de cada origen en
  `<destino>/.ai/doc_state.json` (`doc_trace.py baseline`) y la Fase 1 siguiente parte de
  `doc_trace.py changes`: ficheros cambiados desde ese commit (git local, también pendientes y
  sin seguimiento), páginas que los citan como evidencia, páginas que solo los mencionan,
  ejemplos enlazados y ficheros sin página. El resto de páginas queda vigente sin releerlas.
  Código 3 → modo completo (sin baseline, sin git, commit fuera del historial o versión menor de
  doc_ia distinta). Si el destino está dentro del origen, sus artefactos no cuentan como cambios.
  Criterios AC-15 a AC-21 de la trazabilidad y AC-12 de Documentar un Proyecto.
- **Producto — instrucciones de visualización** (Fase 7c de `/document-project`, siempre): el
  destino recibe `VER_DOCUMENTACION.md` (`VIEW_DOCS.md` en inglés) en su raíz, generado desde
  `.github/templates/VER_DOCUMENTACION.template.md`: qué ruta seguir (web, ZIP, código fuente),
  instalación de Python desde cero en Windows, macOS y Linux, servidor local y problemas
  frecuentes, con valores verificados en el destino. Gap V1 (sin `requirements-docs.txt` → se
  crea) y Gap V2 (`EXTRA_FILES` en hook/script). Instancia propia de doc_ia en la raíz.
- Tests: `test_start_server.py`, `test_versioned_zip_matches_latest_layout` (AC-11 del ZIP
  offline) y guardas de coherencia de la Fase 7c (AC-11 de Documentar un Proyecto).

### Changed

- `build_docs_zip.py` comprueba antes de empaquetar que `site/` se abre sin servidor (índice de
  búsqueda en JS, ningún script remoto, ningún enlace a carpeta) y, si no, termina con código 1
  y lista los problemas. Un destino que copie el script sin el plugin `offline` falla a propósito.
  La CI lo ejecuta también sobre el build de MkDocs.
- URLs del sitio en `*.html` (`api/archetypes.html` en lugar de `api/archetypes/`); `llms.txt`
  regenerado.
- `downloads.md`, `VER_DOCUMENTACION.md` y las notas de release: la ruta principal del ZIP es el
  doble clic tras extraerlo; Python solo hace falta para el servidor local y la ruta de código
  fuente.
- `start-server.py` escucha solo en `127.0.0.1` (antes, todas las interfaces), atiende cada
  conexión en su hilo (antes, una conexión ociosa del navegador bloqueaba el servidor), sirve su
  carpeta sin cambiar el directorio de trabajo y, con el puerto ocupado, termina con código 1 y
  sugiere `--port` (en Windows, sin `SO_REUSEADDR`, que permitía compartir el puerto en silencio).
- Los dos ZIP llevan `start-server.py` y `VER_DOCUMENTACION.md` en su raíz (`EXTRA_FILES` en
  `mkdocs_hooks.py` y `build_docs_zip.py`).

### Fixed

- El ZIP `latest` del build con MkDocs no incluía `search/search_index.js`: el hook empaquetaba
  antes de que el plugin `offline` lo escribiera. `mkdocs_hooks.py` corre ahora con prioridad -200.
- Mapa funcional: totales y evidencia desfasados (decía 52 de 75 criterios; son 63 de 89) y
  referencia de `start-server.py` que aún describía el puerto ocupado como excepción no capturada.
- El ZIP versionado (`dist/`, el que publican las Releases) no incluía `start-server.py` y
  contenía anidado `doc_ia-docs-latest.zip` con su `.sha256`: ahora tiene el mismo contenido
  que el ZIP "latest".
- `docs/downloads.md`, el Paso B3 del producto y las notas de release ofrecían abrir `index.html`
  directamente cuando no navegaba (`use_directory_urls: true`, enlaces a carpetas); desde esta
  versión el doble clic sí funciona (ver «ZIP navegable sin servidor»).

## [0.3.0] — 2026-10-29

### Added

- **Regla transversal de diagramas** (`DOCUMENTATION_STANDARD.md` §3.17): fuente única de las
  reglas Mermaid (tipo por arquetipo con columna de colores del tema, una vista por arquetipo,
  máximo 12 nodos y 8 en el Arquetipo 6, etiquetas, accesibilidad, estilo y validación).
- **Tests de conformidad de diagramas**: sin entidades HTML, labels especiales entre comillas,
  `accTitle`/`accDescr` obligatorios y tamaño máximo (criterios AC-11 a AC-13).
- **Job `mermaid` en CI**: valida cada página de `docs/` con el parser real
  (`@mermaid-js/mermaid-cli`) y la misma versión que sirve el sitio.
- **Mermaid servido en local** (`docs/assets/vendor/mermaid/mermaid-12.2.0.min.js` +
  `assets/js/mermaid-theme.js`): los diagramas del sitio y del ZIP offline se dibujan sin conexión,
  con la misma versión en MkDocs Material y Zensical. `tests/test_mermaid_assets.py` vigila versión,
  huella, orden de carga, coherencia con CI y el cargador del tema (AC-10 del ZIP offline).
- **Producto**: la Fase 0b de `/document-project` sincroniza cinco recursos en vez de tres y lleva
  Mermaid local a los proyectos documentados.
- **Producto**: el destino de `/document-project` recibe siempre los documentos convertidos en
  `_fuentes/<nombre_origen>/<ruta relativa al origen>` (Fase 0c, Paso 5), versionados y fuera de
  `docs/`, para que la evidencia y `doc_trace` citen rutas del propio repositorio.
  `test_sources_folder_is_canonical` comprueba la regla en prompt, comando, agente y
  `SHARED_INSTRUCTIONS.md`.

### Changed

- Rediseño de 9 diagramas que superaban 12 nodos o repetían el mismo flujo en varios
  arquetipos (document_project, convert_to_md, archetypes, origin_types, doc_trace); los 24
  diagramas declaran título y descripción accesibles.
- `gitgraph` y `architecture-beta` pasan a OPCIONAL; la "Arquitectura física" usa `flowchart LR`
  con `subgraph`; el Arquetipo 1 §3 admite `flowchart TD` de decisiones.

### Fixed

- La regla `@` → `&#64;` pintaba un `&` sobrante (Mermaid no decodifica entidades HTML): las
  labels con `@ ( ) { }` van entre comillas. Corregido `on_post_build(config)` en
  `docs/api/build_docs_zip.md`.
- **Producto**: los documentos convertidos llegaban al destino con nombres improvisados
  (`.fuentes/` en unas sesiones, `_fuentes/` en otras) porque ninguna instrucción fijaba la
  ubicación. Ahora `_fuentes/` es el único nombre; los otros se migran con confirmación.
- **Producto**: la Fase 0c de `/document-project` describía markitdown como motor principal,
  con enrutado por extensión, plugins y fallback a pandoc que `convert_to_md.py` ya no tiene.
  Ahora usa docling (motor por defecto) y recurre a `--engine markitdown` solo para XLS y a
  `--engine pandoc` para DOC/ODT/RST. Alineados `SHARED_INSTRUCTIONS.md`, `.ai/` y los textos
  de `check_env.py`.

## [0.2.0] — 2026-10-28

### Added

- **Arquetipo 12 — Referencia del Sistema** (`docs/reference/`, condicional): configuración,
  CLI, errores y códigos de salida, eventos e interfaces publicadas; prompt
  `reference_doc.prompt.md`. Primera aplicación: `docs/reference/index.md` de doc_ia.
- **Regla transversal de evidencia y confianza** (`DOCUMENTATION_STANDARD.md` §3.16): bloque
  plegable "Evidencia" en los Arquetipos 1, 2 y 12, citas `ruta::símbolo` en código inline y
  leyenda ✅ ⚠️ 🔍 ❌.
- **Variante 6C**: subapartado §3 › Despliegue (arc42 §7, condicional) y escenarios de calidad
  en §4 (arc42 §10). Aplicado en `docs/architecture.md`.
- **ADR-002** — Use evidence-backed archetypes for repository documentation.
- **Trazabilidad funcional y de pruebas** (P2): columna `Test` en los criterios de aceptación del
  Arquetipo 1 §7, nueva §6 "Verificación y Tests" del Arquetipo 2 y subsección condicional
  "Actores y permisos" en el Arquetipo 1 §2.
- **Mapa Funcional** (Variante 1-I del Arquetipo 1, `docs/functional/index.md`): capacidades,
  recorridos transversales, actores y glosario global del sistema.
- **Arquetipo 12 §6 "Datos"** (condicional): `erDiagram` global y diccionario con sensibilidad
  por campo; aplicado a los ficheros con formato propio de doc_ia.
- **`scripts/doc_trace.py`** (P3): trazabilidad determinista docs ↔ código con subcomandos
  `stamp` (huellas SHA256 en el frontmatter), `drift` (páginas desactualizadas), `matrix`
  (criterios de aceptación ↔ tests) y `llms` (`docs/llms.txt` desde el nav). 20 tests.
- **Frontmatter de trazabilidad** (`arquetipo`, `fuentes`, `revisado`) en las 15 páginas de
  doc_ia con bloque "Evidencia"; `docs/llms.txt` publicado en la raíz del sitio.
- **CI de calidad** (`.github/workflows/ci.yml`, Python 3.12 y 3.14): ruff, formato, mypy strict,
  pytest, `doc_trace` (drift bloqueante, matrix, `llms --check`) y build `--strict` en cada push/PR
  a `develop` y `main`.
- `requirements-docs.txt` (stack MkDocs) y `requirements-dev.txt` (+ ruff, mypy, pytest): la CI y
  los workflows de documentación ya no instalan docling ni torch.
- `tests/test_build_docs_zip.py` (8 tests: script y hook del ZIP) y `tests/test_docs_conformance.py`
  (conformidad de `docs/` con los arquetipos). Cobertura de criterios: 45/67.
- `build_docs_zip.py --builder zensical` ejecuta él mismo los hooks que Zensical ignora:
  `hooks/sync_root_docs.py` antes del build y `mkdocs_hooks.py` (ZIP `latest`) solo si el build
  termina con 0. 4 tests nuevos; criterios AC-07 y AC-08 en `functional/build_docs_zip.md`.
- `check_env.py` avisa si falta `zensical` (generador opcional, `OPTIONAL_DOC_BUILDERS`) y remite a
  `requirements-dev.txt`; no cambia el código de salida. 2 tests nuevos; AC-06 en
  `functional/check_env.md`.
- `tests/test_zensical_compat.py`: guardas para lo que ningún `--strict` detecta. Falla si
  `mkdocs.yml` declara un plugin que Zensical ignoraría en silencio o si los enlaces al ZIP de
  `docs/downloads.md` no resuelven al ZIP `latest`. AC-09 en `functional/build_docs_zip.md`.
- **ADR-003** (PROPUESTO) — Use Zensical as the default documentation generator: cambio
  escalonado con condiciones C1-C5 (Zensical ≥ 0.1, paridad en CI ≥ 2 semanas, revisión visual,
  ZIP `latest` cubierto, antes del fin de vida de Material el 2027-05-05).
- `/document-project` con **Generador = `zensical`**: nueva sección *Reglas por generador: Zensical*
  en `document_project.prompt.md`. Añade la señal `TIENE_PIPELINE_SIN_HOOKS` y el Gap A4 (script de
  build sin pasos pre/post), la comprobación de plugins soportados, el build vía
  `build_docs_zip.py --builder zensical` y la regla de no crear `zensical.toml`. Slash command,
  agentes Generator/Reviewer, `docs.instructions.md` y la norma remiten a ella. AC-08 en
  `functional/document_project.md`. MkDocs Material sigue siendo el generador por defecto para
  destinos.

### Changed

- `build_docs_zip.py` invoca Zensical como `python -m zensical` (antes `zensical` desde el PATH).
- **Mermaid con la integración nativa del tema**: se retiran el CDN `mermaid@11` y
  `docs/assets/js/mermaid.js` de `extra_javascript`. Duplicaban el render: el tema ya pinta cada
  diagrama y el `mermaid.run()` propio dejaba un SVG de error oculto en cada bloque. La pieza
  imprescindible es `custom_fences: mermaid`. Fase 0b y Fase 5 de `/document-project` pasan de 4 a
  3 assets (si un destino tiene el CDN o `mermaid.js`, se retiran). Norma §4.1,
  `docs.instructions.md`, plantilla `TEMPLATE_mkdocs.yml`, agentes, `CLAUDE.md`, `CONTRIBUTING.md`
  y `EDGE_CASES` § Mermaid actualizados. Verificado en navegador (Edge headless + CDP): 23/23
  diagramas visibles con MkDocs y con Zensical, en claro y en oscuro.
- CI: build de paridad con Zensical (`build_docs_zip.py --builder zensical`, no bloqueante) que
  verifica además el ZIP `latest`. `zensical==0.0.73` fijado en `requirements-dev.txt` y
  `requirements.txt` (con `deepmerge` y `tomli`). El resultado real se publica como anotación
  `Paridad Zensical` (OK/FALLO), porque `continue-on-error` marca el paso como `success` aunque falle.
- Workflows: `actions/checkout` y `actions/setup-python` v4 → v7, `actions/upload-artifact` v4 → v7 y
  `softprops/action-gh-release` v2 → v3 (Node 24 nativo; GitHub ya no admite Node 20 en los runners).
- Norma del Arquetipo 1 alineada con su prompt (8 secciones); las páginas con la estructura v1
  siguen siendo válidas en transición.
- Prompt del Arquetipo 2 alineado con la norma (§2 "Modelo de Datos / Contratos"); la directiva
  autodoc solo se usa si el generador tiene mkdocstrings.
- Material `CONTRATO` alimenta también el Arquetipo 12 §5; `INFRAESTRUCTURA` va a 6C §3 › Despliegue.
- `/document-project`: la **Fase 0b** es siempre la sincronización visual (ahora también en el prompt
  multiplataforma); la conversión de documentos a Markdown pasa a llamarse **Fase 0c**.
- Bootstrap: ruta de la guía de Codex corregida (`docs/guides/codex_guide.md`); la Capa B incluye los
  Arquetipos 7, 8, 10 y 12 y ofrece `scripts/doc_trace.py` como tooling opcional.
- `.claude/settings.json.example`: añadido el hook `sync_root_docs.py` como primer PostToolUse.
- `DOCUMENTATION_STANDARD.md` §4.2: la copia del `nav` se sustituye por una referencia a `mkdocs.yml`.
- El sitio no se publica en GitHub Pages: `site_url` solo fija la URL canónica (sitemap y `llms.txt`).
- mypy limpio sin los extras opcionales (overrides para `docling` y `markitdown`).
- `CONTRIBUTING.md`: la sincronización visual pasa a §5.1 y «Release» vuelve a ser §6 (Arquetipo 11).
- `docs/installation.md`: corregido que `requirements.txt` no incluye ruff ni mypy.
- `requirements.txt` regenerado desde el entorno local completo (docling 2.107.0, markitdown con
  plugins PDF/XLS); `pywin32` solo en Windows (`sys_platform == "win32"`), lo que permite instalarlo
  en Linux/macOS. `requirements-docs.txt` y `requirements-dev.txt` alineados con sus versiones.
- `check_env.py`: la ayuda de plugins de markitdown incluye `pdfminer.six`.
- `doc_trace.py stamp --source`: `CLAUDE.md`, la norma §3.16 y las páginas `api`/`reference` aclaran que
  `--source` sustituye la lista entera de fuentes; para re-sellar se usa `stamp <página>` sin él.

### Fixed

- `docs/architecture.md`: el diagrama de Runtime mostraba «Syntax error in text». El nodo
  `B[/document-project…]` abre un paralelogramo en Mermaid 11; pasa a `B[Comando document-project…]`.
  Nuevo test `test_mermaid_nodes_do_not_start_with_slash` (`--strict` no detecta este error).
- `convert_to_md.py --device auto` detecta la GPU: el `CUDA_VISIBLE_DEVICES=""` que el módulo
  fija al importarse ya no se confunde con una elección del usuario.
- `convert_to_md.py` con docling ya no recoge los `.md` del origen: el Markdown ya es legible y
  se reconvertía a `md/` sin necesidad.
- `check_env.py` ya no se interrumpe con `UnicodeEncodeError` al mostrar avisos en una consola
  Windows (cp1252): la salida se reconfigura a UTF-8.
- `convert_to_md.py --metadata` con docling escribe la versión real del motor en `engine_version`
  (antes siempre `unknown`: docling no expone `__version__`).

## [0.1.0] — 2026-06-10

### Added

- **Tooling determinista**: `scripts/check_env.py` (verificación de herramientas del entorno) y
  `scripts/build_docs_zip.py` (ZIP offline con SHA256 y checksums).
- **Bootstrap multiplataforma** (`.github/agents/`, `.github/prompts/`, `.claude/commands/`):
  replica el sistema de instrucciones IA en proyectos destino mediante modelo PULL.
- **Flujo `/document-project`** como comando de entrada único para documentar proyectos:
  validación obligatoria de inputs, inventario por fases, orquestación de arquetipos.
- **Soporte de orígenes heterogéneos** en `/document-project`: Fase 0a de clasificación
  (`CÓDIGO`, `NORMATIVA`, `ESPECIFICACIÓN`, `UI/PANTALLAS`, `REFERENCIA`); estrategias
  `federado`, `hub+satélite` y `monorepo` para múltiples orígenes de código.
- **11 arquetipos formales** de documentación con estructura fija y audiencia definida:
  - 1 — Funcional, 2 — Técnica/API, 3a — How-to (Diátaxis), 3b — Tutorial (Diátaxis),
    4 — Ejemplos de Código, 5 — ADR/MADR 4.0, 6 — Navegación Principal (Variantes A–D),
    7 — Onboarding Dev, 8 — Trazabilidad Normativa (condicional),
    9 — Changelog, 10 — Config Agente IA, 11 — Guía de Contribución.
- **Documentación completa de doc_ia** (dogfooding): 24 páginas en `docs/` cubriendo
  funcional, técnica, ejemplos, guías, arquitectura y ADRs para todos los módulos.
- **Descarga de documentación offline**: `dist/doc_ia-docs-{version}.zip` + SHA256; workflow
  GitHub Actions `docs-zip-release.yml` publica automáticamente en cada release.
- **UX del sitio**: márgenes, sidebar toggle, soporte Mermaid 11, tabs sticky.
- **Estados A/B/C** en el inventario de `/document-project` para distinguir páginas
  a crear, actualizar u omitir.

### Fixed

- Restauración de 10 ficheros de la Capa A corruptos durante el bootstrap inicial.
- Restauración de `config-reviewer.agent.md` y creación de `docs.instructions.md`
  tras corrupción del bootstrap.

[Unreleased]: https://github.com/fmanza/doc_ia/compare/v0.11.2...HEAD
[0.11.2]: https://github.com/fmanza/doc_ia/compare/v0.11.1...v0.11.2
[0.11.1]: https://github.com/fmanza/doc_ia/compare/v0.11.0...v0.11.1
[0.11.0]: https://github.com/fmanza/doc_ia/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/fmanza/doc_ia/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/fmanza/doc_ia/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/fmanza/doc_ia/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/fmanza/doc_ia/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/fmanza/doc_ia/compare/v0.5.1...v0.6.0
[0.5.1]: https://github.com/fmanza/doc_ia/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/fmanza/doc_ia/compare/v0.4.1...v0.5.0
[0.4.1]: https://github.com/fmanza/doc_ia/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/fmanza/doc_ia/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/fmanza/doc_ia/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/fmanza/doc_ia/compare/docs-v0.1.0...v0.2.0
[0.1.0]: https://github.com/fmanza/doc_ia/releases/tag/docs-v0.1.0
