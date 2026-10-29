# Prompt: document_project — Punto de entrada único para documentar un proyecto

## Objetivo

Documentar un proyecto de desarrollo (un proyecto origen externo o el propio doc_ia) aplicando
los **arquetipos formales** de `.github/DOCUMENTATION_STANDARD.md` mediante el flujo por fases
del agente **Documentation Generator**. Los orígenes y el destino son **parámetros obligatorios**
de cada ejecución: nunca constantes asumidas.

Este prompt es el **comando de entrada único** del producto doc_ia. No uses prompts de arquetipo
sueltos para documentar un proyecto completo: invoca este flujo y deja que orqueste los arquetipos.

## Contexto a completar (OBLIGATORIO — validar antes de empezar)

- [ ] **Origen(es) a documentar**: ruta(s) raíz del/los proyecto(s) (ej. `c:\repos\mi_api`)
- [ ] **Destino de la documentación**: ruta donde se escribe (ej. `c:\repos\mi_api\docs` o repo aparte)
- [ ] **Generador**: `mkdocs-material` (por defecto en doc_ia) | `zensical`
- [ ] **Idioma**: `es` | `en` | otro

Opcionales:

- **Tipo de cada origen**: `CÓDIGO` | `NORMATIVA` | `ESPECIFICACIÓN` | `UI/PANTALLAS` | `CONTRATO` | `INFRAESTRUCTURA` | `MANUAL` | `REFERENCIA` — autodetectado si se omite; se confirma con el usuario antes de continuar
- **Estrategia** (solo con ≥2 orígenes CÓDIGO): `federado` | `hub+satélite` | `monorepo` — siempre preguntar al usuario, nunca autodetectar
- **Alcance**: módulos o subconjunto a documentar (por defecto: proyecto completo)
- **Arquetipos**: subconjunto a aplicar (por defecto: todos los aplicables según inventario)
- **Verificación**: `--verify-tools` y/o `--verify-build [--serve]` (opt-in, nunca automáticos)
- **Modo**: `incremental` | `completo` — por defecto `incremental` si el destino tiene
  `.ai/doc_state.json` con baseline del origen; si no, `completo` (ver Fase 1 y CIERRE). Pasa a
  `completo` sola si el commit ya no existe, el origen no usa git o cambia la versión
  mayor/menor de doc_ia (las reglas de los arquetipos pueden haber cambiado)

## ⚠️ VALIDACIÓN (bloqueante)

Si **alguno** de los 4 campos obligatorios está vacío, es ambiguo o no es verificable,
**DETENTE AHORA**. Pide los datos al usuario antes de continuar. **No inventes rutas, no asumas
destino, no elijas generador ni idioma por el usuario.** Mismo patrón de validación que
`new_feature`: sin contexto completo no se emite ninguna fase.

Ejemplos de detención:

- "Falta **Destino** → preguntar: ¿la documentación se escribe en `docs/` del propio origen o en otro repositorio?"
- "Origen `c:\repos\mi_api` no existe o no es legible → preguntar ruta correcta antes de inventariar."
- "Generador no indicado → preguntar: ¿MkDocs Material (por defecto) o Zensical?"

## Política innegociable (de `SHARED_INSTRUCTIONS.md` § Principios)

1. **Prohibido incrustar API keys**: ninguna credencial de servicios IA se configura, versiona
   ni incrusta en código, prompts o workflows.
2. **La ejecución IA ocurre siempre en el chat** de la plataforma (Claude Code, Gemini, Copilot,
   Cursor, Codex), guiada por estas instrucciones.
3. **El código Python nunca invoca servicios IA**: `scripts/` es tooling determinista
   (build, ZIP, validaciones). Si una fase parece requerir generación programática vía API,
   la respuesta es NO: se genera en este chat.

## Flujo orquestado (Documentation Generator)

Aplica el flujo por fases de `.github/agents/documentation-generator.agent.md` sobre el
**origen** indicado, escribiendo en el **destino** indicado:

```
Fase 0a — Clasificación de orígenes (solo con ≥2 orígenes, o si el único origen no es CÓDIGO):
         1. Para cada origen, detectar tipo por señales del sistema de ficheros, en este orden
            (se asigna el primer tipo que coincide; REFERENCIA, la última, es el tipo por defecto):
            - CÓDIGO         : archivos fuente (.py, .js, .ts, .cs, .java, .go, .rs, …),
                               pyproject.toml, package.json, pom.xml, Cargo.toml, go.mod,
                               src/, tests/ presentes
            - NORMATIVA      : PDFs/docs con palabras clave en nombre o carpeta:
                               ley, decreto, directiva, rgpd, gdpr, une, iso, reglamento, compliance
            - ESPECIFICACIÓN : Word/PDF de requisitos, user stories, pliego, ficheros .feature (BDD);
                               carpetas specs/, requirements/, ux/, user-stories/
            - UI/PANTALLAS   : wireframes, mockups, capturas (.png, .jpg, .pdf de diseño);
                               carpetas mockups/, screens/, wireframes/, figma-exports/
            - CONTRATO       : especificaciones machine-readable del PROPIO proyecto:
                               .yaml/.json con clave openapi: o asyncapi:; .graphql/.gql; .proto; .avsc;
                               .sql DDL en db//migrations/; .dbml; carpetas api/, contracts/, schemas/, proto/
            - INFRAESTRUCTURA: IaC y despliegue: .tf (Terraform); Dockerfile, docker-compose.yml;
                               YAML en k8s/, deploy/, manifests/, helm/; playbooks Ansible en roles//ansible/
            - MANUAL         : documentación narrativa del PROPIO proyecto: .pdf/.docx/.md con manual/
                               guide/runbook/ayuda/help en nombre; carpetas manuals/, help/, user-docs/; .chm
            - REFERENCIA     : manuales de TERCEROS, RFCs, especificaciones de protocolo AJENAS
                               al proyecto; también lo que no coincide con ningún tipo anterior.
                               Un contrato o manual de un tercero es REFERENCIA (la propiedad decide)
         2. Presentar tabla: | Origen | Tipo detectado | Señales encontradas | Rol propuesto |
         3. DETENER y pedir confirmación al usuario antes de continuar.
         4. Si hay ≥2 orígenes CÓDIGO → preguntar estrategia al usuario:
            - federado     : cada proyecto con docs/ y mkdocs.yml propios, independientes
            - hub+satélite : un proyecto "hub" concentra el destino; los demás son secciones
            - monorepo     : mkdocs.yml raíz único agrupa secciones por proyecto
         5. Caso degenerado — ningún origen CÓDIGO → DETENER con mensaje:
            "No se detecta ningún proyecto de desarrollo. /document-project requiere al menos
             un origen de tipo CÓDIGO. Para documentar solo normativa o especificación,
             usa directamente normative_traceability.prompt.md o functional_doc.prompt.md."
         Mapeo MATERIAL → arquetipos (para orígenes no-CÓDIGO):
            NORMATIVA        → Arquetipo 8 + enriquece §5 (Reglas de Negocio) del Arquetipo 1
            ESPECIFICACIÓN   → enriquece Arquetipo 1 §3+§5+§6+§7 del proyecto principal
            UI/PANTALLAS     → enriquece Arquetipo 1 §3 (Flujo Principal) y Arquetipo 3
            REFERENCIA       → enriquece Arquetipo 2 §4 (Dependencias) o Arquetipo 5 (ADR)
            CONTRATO         → enriquece Arquetipo 2 §1 (Arquitectura/interfaces) y §2 (Modelo de Datos/Contratos) y Arquetipo 12 §5 (Interfaces Publicadas)
            INFRAESTRUCTURA  → enriquece Arquetipo 2 §4 (Dependencias) y Arquetipo 6C §3 › Despliegue
            MANUAL           → enriquece Arq. 3a §3, Arq. 3b §3, Arq. 6A/B §1 (Descripción), Arq. 7 §3 y §5

Fase 0 — Detección de normativa: si el origen referencia normativa de obligado cumplimiento,
         ofrecer Arquetipo 8 (normative_traceability.prompt.md). Si no hay, omitir.
         Nota: si la Fase 0a ya clasificó un origen como NORMATIVA, este paso está cubierto.
Fase 0b — Sincronización visual del destino (OBLIGATORIO en toda sesión, creación o actualización):
         Checklist completo y tabla de theme.features: .claude/commands/document-project.md
         § Sincronización de Configuración Visual. Como mínimo:
           · .gitignore en la raíz del destino con site/, __pycache__/, *.pyc, *.egg-info/,
             .venv/, *.pdf, *.doc, *.docx (crear si no existe; añadir los que falten).
             Nunca ignorar `_fuentes/`: el texto convertido se versiona (Fase 0c, Paso 5)
           · theme.features SIN navigation.sections si nav.css está en extra_css
           · los 6 recursos de docs/assets/ existen y están en extra_css / extra_javascript /
             extra.polyfills (Mermaid local: vendor/mermaid/mermaid-<versión>.min.js y después
             js/mermaid-theme.js; shim local: vendor/iframe-worker/iframe-worker-shim-<versión>.min.js)
           · ZIP sin servidor: use_directory_urls: false + plugin `offline` + el shim en
             extra.polyfills (sin él, el tema lo descarga de unpkg y la búsqueda por file:// falla
             sin red). Si el destino ya publica la web con URLs de carpeta, avisar en RESUMEN: los
             enlaces profundos pasan a *.html
           · custom_fences mermaid presente; sin CDN de Mermaid ni assets/js/mermaid.js
         (La Fase 5 vuelve a verificar la configuración estándar al final.)
Fase 0c — Conversión de documentos no legibles y uso de documentos pre-convertidos:
         Paso 0 — Detectar carpeta md/ pre-existente (ejecutar SIEMPRE, antes del Paso 1):
           · Buscar en todo el árbol del origen subcarpetas llamadas `md/` que contengan
             ficheros `.md`. Criterio de carpeta válida de pre-convertidos: la carpeta `md/`
             existe junto a ficheros binarios en el directorio padre, O sus ficheros `.md`
             tienen nombres que corresponden a binarios del directorio padre (sin extensión).
             Si no se cumplen estos criterios, descartar esa carpeta `md/` para este paso.
           · Buscar también en la raíz del destino `_fuentes/` (copia de una sesión anterior)
             y carpetas con nombre no canónico (`.fuentes/`, `fuentes/`) → Paso 5.
           · Para orígenes clasificados como REFERENCIA o NORMATIVA en Fase 0a, ejecutar
             este paso con prioridad aunque no haya ficheros binarios visibles.
           · Para cada fichero binario encontrado, comprobar si ya tiene equivalente en `md/`
             (mismo nombre relativo, extensión cambiada a `.md`):
               TIENE_MD = true  → marcar OMITIR_CONVERSIÓN
               TIENE_MD = false → añadir a lista de pendientes de conversión (Paso 1)
           · Si TODOS los binarios tienen TIENE_MD = true, O si no hay binarios pero `md/`
             tiene contenido → omitir Pasos 1-4 y pasar directamente al Paso 5.
           · Si `md/` parcial (algunos binarios sin equivalente) → ejecutar Pasos 1-4 solo
             para los pendientes; incluir ya los pre-existentes en Paso 5.
           · Si no existe ninguna `md/` válida NI ficheros binarios → omitir esta fase.
           · Cuando `md/` existe sin binarios visibles (binarios eliminados tras conversión),
             reportar en INVENTARIO con nota "Documentos pre-convertidos sin binario original"
             y confirmar con el usuario antes de usarlos en Fases 2-4.
         Paso 1 — Detectar binarios pendientes y asignar motor (solo si Paso 0 identifica pendientes):
           El motor se elige en cada ejecución con `--engine` (por defecto `docling`); el script
           no reparte por extensión ni cambia de motor por su cuenta. Asignación por extensión:
             docling (por defecto, principal): .pdf, .docx, .pptx, .xlsx, .csv, .html, .htm, .epub,
                       imágenes (.png, .jpg, .jpeg, .tiff, .bmp, .webp), .eml, .msg, .tex, .latex,
                       audio (.wav, .mp3)
             markitdown (alternativa ligera): solo lo que docling no cubre → .xls
             pandoc (complemento):            .doc, .odt, .rst
           Una ejecución por motor necesario, siempre docling primero: cada ejecución solo recoge
           las extensiones de su motor y omite los ficheros cuyo `.md` ya existe.
         Paso 2 — Validación previa (OBLIGATORIO antes de convertir), una por motor del Paso 1:
                python scripts/convert_to_md.py <ruta_origen> --validate-only
                python scripts/convert_to_md.py <ruta_origen> --validate-only --engine markitdown  ← solo si hay .xls
                python scripts/convert_to_md.py <ruta_origen> --validate-only --engine pandoc      ← solo si hay .doc/.odt/.rst
           Comprueba, sin convertir:
             a) Motor instalado: si falta, avisa con su instrucción de instalación (Paso 4).
             b) Integridad de cada fichero: legible y no vacío; ZIP válido en DOCX/PPTX/XLSX/EPUB;
                cabecera correcta en PDF e imágenes; audio de al menos 1 KB.
           Informe por fichero: `OK` | `INVÁLID <motivo>`; termina con código 1 si hay inválidos.
           Si la validación reporta errores:
             · Motor no instalado → Paso 4
             · Ficheros inválidos → reportar al usuario para resolución manual
             · Los válidos se convierten igualmente; los inválidos se registran (Paso 7)
         Paso 3 — Proponer la conversión de los pendientes validados (mismo orden de motores):
                python scripts/convert_to_md.py <ruta_origen>                      ← docling
                python scripts/convert_to_md.py <ruta_origen> --engine markitdown  ← solo si hay .xls
                python scripts/convert_to_md.py <ruta_origen> --engine pandoc      ← solo si hay .doc/.odt/.rst
            Crea una carpeta `md/` dentro del origen con las versiones Markdown convertidas,
            reflejando la estructura de subdirectorios para evitar colisiones de nombres.
            docling: OCR activado (idiomas `es,en`; `--ocr-lang` para otros), CPU por defecto
            (`--device auto` usa GPU NVIDIA si la hay), límite de 300 s por documento (`--timeout`).
            El script se ejecuta desde doc_ia sobre cualquier ruta: no hace falta copiarlo al origen.
            Sin docling (el usuario no quiere instalarlo): `--engine markitdown` cubre PDF, DOCX,
            PPTX, XLSX, CSV, HTML, EPUB y MSG sin OCR; los PDF escaneados y las imágenes quedan
            pendientes (Paso 7).
         Paso 4 — Resolver herramientas faltantes (si la validación detectó carencias):
              docling (principal):      pip install docling   (la primera conversión descarga sus modelos)
              markitdown (alternativa): pip install markitdown
              pandoc (complemento):     Windows: winget install JohnMacFarlane.Pandoc
                                        macOS:   brew install pandoc
                                        Linux:   sudo apt install pandoc | sudo dnf install pandoc
            `python scripts/check_env.py` informa del estado de los tres motores.
         Paso 5 — Sincronizar `_fuentes/` en el destino (SIEMPRE que haya contenido en `md/`,
                  también si origen y destino son el mismo repositorio):
           · Nombre único: `_fuentes/`, en la raíz del destino (la carpeta que contiene
             `mkdocs.yml` / `zensical.toml`; `{destino}/..` cuando el destino es `docs/`).
             Nunca dentro de `docs_dir`. Prohibido otro nombre (`.fuentes/`, `fuentes/`…):
             `.fuentes/` es oculta y las búsquedas del agente la saltan.
           · Ruta: `_fuentes/<nombre_origen>/<ruta relativa al origen>`, sin cambios y con el
             segmento `md/` incluido. `<nombre_origen>` = carpeta raíz del origen; si dos
             orígenes comparten nombre → `<padre>_<nombre>`.
               Ej.: <origen>/Legales/md/CA/ley.md → _fuentes/<nombre_origen>/Legales/md/CA/ley.md
           · Copiar los `.md` de cada carpeta `md/` válida (Paso 0) y las imágenes que
             referencian. Nunca los binarios ni las carpetas de chunks (`--chunk`).
           · Idempotente: copiar solo si el fichero falta o su contenido difiere. Los ficheros
             de `_fuentes/` no se editan a mano: se regeneran desde el origen.
           · Huérfanos (en `_fuentes/` sin equivalente en el origen) → listarlos en INVENTARIO
             y borrarlos solo con confirmación del usuario.
           · Migración (destino con `.fuentes/` o `fuentes/` en su raíz) → listarla en
             INVENTARIO y, con confirmación: `git mv` a `_fuentes/` (si coexisten, fusionar los
             ficheros idénticos; si un mismo fichero difiere → DETENER y preguntar) → reescribir
             las referencias en `docs/**/*.md` (enlaces, evidencia y frontmatter `fuentes:`) →
             volver a sellar esas páginas:
                python scripts/doc_trace.py --root <raíz del destino> stamp <página>
         Paso 6 — Usar `_fuentes/` como contexto en las Fases 2-4:
           · Leer de `_fuentes/` del destino, tanto los recién convertidos como los previos.
           · Tratamiento idéntico a ficheros `.md` nativos del origen.
           · La evidencia (DOCUMENTATION_STANDARD.md §3.16) y el frontmatter `fuentes:` citan
             la ruta `_fuentes/...` del destino, nunca la ruta del origen externo.
           · Son artefactos generados — nunca editarlos directamente.
         Paso 7 — Registrar en INVENTARIO los pendientes no resueltos:
           Si el usuario no instala el motor o decide omitir → registrar en
           INVENTARIO (Fase 1) los ficheros no convertidos con estado A y nota:
           "Pendiente: requiere docling para convertir [nombre.ext]"
           "Pendiente: requiere markitdown para convertir [nombre.xls]"
           "Pendiente: requiere pandoc para convertir [nombre.doc]" (DOC/ODT/RST)
           "Pendiente: fichero inválido [nombre.ext] — <motivo de la validación>"
         Nota: omitir esta fase solo si no existen ficheros binarios NI carpeta `md/` con
         contenido válido en el origen NI `_fuentes/` (o nombre no canónico) en el destino.
Fase 1 — Inventariar y clasificar:
         Modo incremental (por defecto si hay baseline) — antes de leer el origen, por cada
         origen CÓDIGO, desde la raíz del destino (carpeta con mkdocs.yml):
           python <doc_ia>/scripts/doc_trace.py --root <raíz destino> changes --origin <origen> [--name <nombre_origen>]
           · exit 0 → sin cambios: todas sus páginas quedan en ESTADO C sin leerlas.
           · exit 1 → leer SOLO el informe: por cada fichero cambiado,
             `git -C <origen> diff <base> -- <fichero>` (o el fichero entero si es alta A).
               - "Lo citan (Evidencia)" → ESTADO B candidato; confirmar comparando el diff
                 con la página (si el cambio no afecta a lo documentado → C).
               - "Ejemplos enlazados" → revisar junto a su página técnica.
               - "Lo mencionan" → B solo si el diff cambia lo que la página describe.
               - "Ficheros sin página" → clasificar: módulo nuevo (A) o parte de un
                 módulo con página (B de esa página). Pueden ser tests, config o README:
                 revisar Arquetipos 3, 6 y 7 si cambia un punto de entrada o dependencias.
             El resto de páginas → ESTADO C ("sin cambios desde <base>") sin leerlas.
           · exit 3 → modo completo para ese origen; anotar el motivo en INVENTARIO.
           Con `Alcance`, aplicar ambos filtros (intersección). Orígenes MATERIAL: su
           incremental es la Fase 0c (copia por hash a `_fuentes/`) + `doc_trace drift`.
           Las fases 0b, 0c, 5, 6, 7b, 7c y el CIERRE se ejecutan igual en ambos modos.
         Modo completo (o fallback): leer árbol real del origen (README, código, docs/,
         mkdocs.yml del destino, y `_fuentes/` del destino con los documentos convertidos si existe).
         Para cada módulo del origen y cada página existente en el destino, asignar estado:
           ESTADO A — sin doc: no existe página en docs/ para este módulo.
           ESTADO B — desactualizado: página existe pero al menos uno de los siguientes:
             · firma de función/clase pública cambiada (parámetro, nombre o tipo de retorno)
             · nuevo símbolo público en el código no documentado en la página
             · símbolo documentado ya no existe en el módulo actual
             · tests actuales contradicen el comportamiento descrito en la documentación
             · sección marcada "Pendiente de verificación" ya verificable en código actual
           ESTADO C — vigente: página existe y código coincide con lo documentado.
         Acción derivada: A → CREAR | B → ACTUALIZAR | C → OMITIR.
         Prioridad de ejecución: A antes que B; C no se toca.
         Detección de patrón ZIP offline — comprobar en el ORIGEN (tres señales independientes):
           · Si existe `scripts/build_docs_zip.py`                                → TIENE_ZIP_SCRIPT = true
           · Si mkdocs.yml del ORIGEN tiene `hooks: [mkdocs_hooks.py]`              → TIENE_MKDOCS_PLUGIN = true
             (señales alternativas: plugin `*_documentation_zip` en mkdocs.yml,
              o directorio `{nombre}_docs/` con `docs_build_plugin.py`)
           · Si existe `.github/workflows/docs-zip-release.yml` (o equivalente)   → TIENE_WORKFLOW_GITHUB = true
           · Solo con Generador = zensical: TIENE_PIPELINE_SIN_HOOKS y Gap A4 (ver § Reglas por generador: Zensical)
           Variante aplicable en Fase 7b:
             Al menos TIENE_ZIP_SCRIPT=true o TIENE_MKDOCS_PLUGIN=true            → Variante A
               · TIENE_ZIP_SCRIPT=false     → Gap A1: proponer crear script (patrón: doc_ia/scripts/build_docs_zip.py)
               · TIENE_MKDOCS_PLUGIN=false  → Gap A2: crear hook MkDocs (patrón: socyalpro/mkdocs_hooks.py)
               · TIENE_WORKFLOW_GITHUB=false → Gap A3: proponer crear workflow (patrón: doc_ia/.github/workflows/docs-zip-release.yml)
             Las tres señales = false                                              → Variante B: proponer crear los tres
             TIENE_ZIP_SCRIPT=false + TIENE_WORKFLOW_GITHUB=true (con o sin plugin) → inconsistencia — investigar y reportar
           · `docs/downloads.md` es SIEMPRE OBLIGATORIO en el destino — nunca omitir.
           · Si ya existe `docs/downloads.md` → asignar estado B si no coincide con la variante
             correcta o si la tabla tiene valores desactualizados (versión, tamaño, sha256, fecha)
Fase 2 — Mapeo funcional (functional_doc.prompt.md) → [destino]/functional/
         + Mapa Funcional del sistema (Variante 1-I) → [destino]/functional/index.md; columna Test en §7.
Fase 3 — Documentación técnica con Mermaid (technical_doc.prompt.md) → [destino]/api/
         Referencia del sistema (reference_doc.prompt.md, Arquetipo 12) → [destino]/reference/
         SOLO si el INVENTARIO detecta señales (configuración, CLI, códigos de salida, eventos, CONTRATO).
         Evidencia (DOCUMENTATION_STANDARD.md §3.16): las páginas de Arq. 1, 2 y 12 terminan con el
         bloque plegable "Evidencia" (`ruta::símbolo` en código inline + leyenda ✅ ⚠️ 🔍 ❌).
Fase 4 — Ejemplos verificables (example_doc.prompt.md) → [destino]/examples/
         Guías y landing según inventario: howto_doc, tutorial_doc, landing_doc, onboarding_dev, architecture_doc.
Fase 5 — Sincronizar navegación y verificar configuración estándar del generador (mkdocs.yml del destino):
         a. Navegación: añadir/mover/retirar entradas de nav; indentación de 4 espacios extra por nivel.
         b. Configuración estándar (DOCUMENTATION_STANDARD.md §4.1) — verificar y corregir si falta:
            · palette: dos entradas (light con media+toggle, dark con scheme:slate+media+toggle)
            · extra_javascript, en este orden: assets/js/sidebar-toggle.js,
              assets/vendor/mermaid/mermaid-12.2.0.min.js, assets/js/mermaid-theme.js — sin CDN de Mermaid ni
              assets/js/mermaid.js (si existen, retirarlos: duplican el render). El tema usa la
              copia local de Mermaid (window.mermaid) y no descarga nada: diagramas sin conexión
            · pymdownx.superfences con custom_fences mermaid (imprescindible para los diagramas)
            · extra_css: assets/css/mermaid.css + assets/css/nav.css
            · markdown_extensions: attr_list, md_in_html, pymdownx.snippets (base_path:[docs]),
              line_spans:__span y pygments_lang_class:true en pymdownx.highlight
            · plugins: search con lang del idioma del proyecto + offline
            · use_directory_urls: false y extra.polyfills:
              [assets/vendor/iframe-worker/iframe-worker-shim-1.0.4.min.js] — sin unpkg: el ZIP se
              abre con doble clic en index.html, con búsqueda, sin servidor ni red
            · Generador = zensical: plugins soportados y `hooks:` (ver § Reglas por generador: Zensical)
         c. Assets: si alguno de los seis recursos de docs/assets/ (js/sidebar-toggle.js,
            css/mermaid.css, css/nav.css, vendor/mermaid/ con la librería, LICENSE y SOURCE.txt,
            js/mermaid-theme.js, vendor/iframe-worker/ con el shim, LICENSE y SOURCE.txt) no existe
            en el destino, o su librería Mermaid o su shim es de otra versión,
            indicarlo explícitamente en RESUMEN con la acción: "Copiar desde doc_ia/docs/assets/"
            (una versión distinta se sustituye: borrar la antigua y actualizar extra_javascript).
Fase 6 — Revisión final: Markdown, enlaces relativos, sintaxis y conformidad Mermaid (§3.17 del
          estándar), secciones de arquetipo completas.
         Trazabilidad (§3.16): frontmatter `fuentes` en páginas con Evidencia; si existe
         scripts/doc_trace.py → `stamp` + `drift` + `matrix` + `llms` (todos con exit 0).
Fase 7 — Verificación de build (solo con --verify-build): build --strict del generador + lectura del HTML.
         Generador = zensical: comando según § Reglas por generador: Zensical.
Fase 7b — downloads.md (SIEMPRE obligatorio — no condicional)
         Crear o actualizar `docs/downloads.md` en el destino según la variante:

         VARIANTE A — Al menos TIENE_ZIP_SCRIPT=true o TIENE_MKDOCS_PLUGIN=true:
           ⚠️  Guarda de orden: si Fase 7 no fue activada, advertir que site/ puede no estar
               sincronizado con los últimos cambios y recomendar ejecutar el build antes del ZIP.
           1. Si TIENE_ZIP_SCRIPT = true:
                Proponer ejecutar en el directorio del ORIGEN:
                  python scripts/build_docs_zip.py
                Si el script fue ejecutado (o existe un ZIP reciente en dist/):
                  a. Leer dist/{project}-docs-{version}.zip.sha256 para obtener el hash.
                  b. Calcular tamaño del ZIP en MB.
                  c. Actualizar la fila de la tabla en docs/downloads.md:
                       | versión | ~X MB | [.sha256](<enlace release>) | YYYY-MM-DD |
                     Regla: reemplazar la fila existente — no acumular filas.
                Si el script no se ejecutó: marcar la fila como pendiente de verificación manual.
              Si TIENE_ZIP_SCRIPT = false (Gap A1):
                Reportar en RESUMEN: "⚠️ Falta `scripts/build_docs_zip.py`. Crear siguiendo el
                patrón de `doc_ia/scripts/build_docs_zip.py` para generar artefactos versionados en dist/."
           2. Verificar TIENE_MKDOCS_PLUGIN:
                · true  → reportar en RESUMEN: "✅ Hook MkDocs presente — ZIP generado
                    automáticamente en site/ en cada `mkdocs build`. Sin instalación requerida."
                  Verificar que el hook se ejecuta después del plugin `offline`
                  (`on_post_build.mkdocs_priority = -200`, como `doc_ia/mkdocs_hooks.py`); si no
                  (Gap V3), añadirlo: sin él, el ZIP latest sale sin índice de búsqueda en JS.
                  Verificar que `docs/downloads.md` usa la estructura normalizada con enlace HTML:
                    `<a href="{nombre}-docs-latest.zip">{nombre}-docs-latest.zip</a>`
                    `<a href="{nombre}-docs-latest.zip.sha256">.sha256</a>`
                  Si la tabla no tiene estos enlaces → actualizar siguiendo la estructura del Paso B3.
                · false (Gap A2) → ⚠️ ACCIÓN OBLIGATORIA: CREAR el hook antes de cerrar sesión.

                  **Paso A2-0 — Crear `scripts/start-server.py`** (obligatorio):
                    Adaptar `doc_ia/scripts/start-server.py` cambiando solo el nombre del proyecto
                    en los mensajes `print`. Este script se incluirá dentro del ZIP para que los
                    usuarios puedan lanzar un servidor local con un solo comando.

                  **Paso A2-1 — Crear `mkdocs_hooks.py`** en la raíz del destino:
                    Adaptar `doc_ia/mkdocs_hooks.py` cambiando solo:
                      `zip_path = site_dir / "{nombre}-docs-latest.zip"`
                    El hook ya añade a la raíz del ZIP `start-server.py` y las instrucciones de
                    la Fase 7c (con idioma `en`, cambiar `VER_DOCUMENTACION.md` por `VIEW_DOCS.md`):
                      ```python
                      EXTRA_FILES = ("scripts/start-server.py", "VER_DOCUMENTACION.md")
                      ```
                    Mantener `on_post_build.mkdocs_priority = -200`: el hook debe ir después del
                    plugin `offline`, que escribe el índice de búsqueda en JS.
                    Hook existente sin `EXTRA_FILES` (Gap V2) → actualizarlo siguiendo
                    `doc_ia/mkdocs_hooks.py`; igual con `EXTRA_FILES` en `build_docs_zip.py`.
                    No crear `{nombre}_docs/` ni `pyproject.toml` — el hook no requiere instalación.

                  **Paso A2-2 — Registrar en `mkdocs.yml`**:
                    Añadir antes de `plugins:`:
                    ```yaml
                    hooks:
                      - mkdocs_hooks.py
                    ```
                    Verificar el build: `python -m mkdocs build --strict` desde el directorio del destino.
           3. Verificar TIENE_WORKFLOW_GITHUB:
                · true  → reportar en RESUMEN: "✅ Workflow GitHub presente".
                · false (Gap A3) → reportar Gap en RESUMEN:
                    "⚠️ Falta `.github/workflows/docs-zip-release.yml`. El ZIP se genera localmente
                     pero no se publica automáticamente en GitHub Releases. Crear siguiendo el
                     patrón de `doc_ia/.github/workflows/docs-zip-release.yml`."
                  Añadir a pendientes de verificación humana.

         VARIANTE B — Las tres señales = false:
           ⚠️  ACCIÓN OBLIGATORIA: CREAR `scripts/build_docs_zip.py` antes de escribir
               downloads.md. No documentar solo el gap — resolverlo.

           **Paso B1 — CREAR `scripts/build_docs_zip.py` en el proyecto destino:**
             Si no existe el directorio `scripts/` → crearlo.
             Detectar fuente de versión según tipo de proyecto:
               · `pyproject.toml` presente (Python)  → `tomllib.load(f)["project"]["version"]`
               · `pom.xml` presente (Java/Maven)      → `xml.etree.ElementTree` + strip `-SNAPSHOT`
                  Ejemplo: `re.sub(r"-(SNAPSHOT|RC\d*|BETA\d*)$", "", ver.text, flags=re.IGNORECASE)`
               · `package.json` presente (Node.js)    → `json.load(f)["version"]`
               · Ninguno                              → argumento `--version` requerido en CLI
             Crear el script adaptando `doc_ia/scripts/build_docs_zip.py`:
               · Cambiar `ZIP_PREFIX = "{nombre_proyecto}-docs"`
               · Cambiar `_version()` según la fuente detectada arriba
               · Mantener el resto del cuerpo sin cambios
             Añadir `dist/` y `site/` al `.gitignore` del proyecto si no están ya.

           **Paso B2 — Ejecutar el script y capturar valores:**
             `python scripts/build_docs_zip.py`
             Leer `dist/{nombre}-docs-{version}.zip.sha256` → hash SHA256.
             Calcular tamaño del ZIP en MB.
             Si termina con «cannot be opened without a server», falta la configuración de la
             Fase 0b (offline, use_directory_urls: false, shim local): corregirla y repetir.
             Si el script falla (dependencias, build error) → indicarlo en RESUMEN y
             dejar la tabla con valores reales hasta donde sea posible, marcando el resto
             como "Pendiente de verificación manual".

           **Paso B3 — Crear/actualizar `docs/downloads.md` con la estructura normalizada:**
             Estructura canónica (idéntica en todos los proyectos):
             1. **"Descarga Actual"** — tabla con enlace HTML directo al ZIP del plugin:
                ```
                | <a href="{nombre}-docs-latest.zip">{nombre}-docs-latest.zip</a> | ~X MB | <a href="{nombre}-docs-latest.zip.sha256">.sha256</a> | YYYY-MM-DD |
                ```
                Sin `../`: con `use_directory_urls: false` (plugin `offline`), `downloads.md` →
                `site/downloads.html`, junto al ZIP en `site/`.
                Línea de versión bajo la tabla: `**{Proyecto} {versión}** — descripción breve`.
             2. **"Cómo usar el ZIP"** — extraer el ZIP **completo** (Windows: «Extraer todo…»;
                Linux/macOS: `unzip`) + visualizar con **doble clic en `index.html`**: sin Python,
                sin servidor y sin red (plugin `offline` + shim local, Fase 0b). Avisar de que el
                doble clic dentro del ZIP sin extraer abre la página sin estilos. Alternativa:
                `python start-server.py` (incluido en el ZIP; `http://127.0.0.1:8000`).
                **Prohibido** indicar flags del navegador como `--allow-file-access-from-files`:
                no hacen falta y desactivan protecciones.
                Remitir a `VER_DOCUMENTACION.md` (incluido en el ZIP) para empezar desde cero.
             3. **"Validar Integridad (SHA256)"** — comandos Windows (PowerShell) + Linux/macOS.
             4. **"Para Desarrolladores"** — `python scripts/build_docs_zip.py` + info CI.
             5. **"Información de versión"** — generador, fecha.
             Eliminar nota "*Pendiente*". Si B2 falló, usar `—` en tamaño/fecha con nota de error.
             · Sección "Enlaces relacionados": quick start, instalación, onboarding.
             Añadir entrada `- Descargas: downloads.md` en el nav de mkdocs.yml (tras "Inicio rápido"
             si existe, o tras "Instalación").

           **Paso B4 — CREAR plugin MkDocs** (ejecutar pasos A2-1 a A2-4 del Gap A2).
             El plugin genera `{nombre}-docs-latest.zip` automáticamente en `site/`
             en cada `mkdocs build` o `mkdocs serve`.

           **Paso B5 — Reportar en RESUMEN:**
             ✅ `scripts/build_docs_zip.py` creado y ejecutado.
             ✅ Plugin MkDocs creado e instalado (ZIP en site/ automático).
             Si el repositorio usa GitHub Actions y falta workflow:
               "⚠️ Falta `.github/workflows/docs-zip-release.yml`. Crear siguiendo el
                patrón de `doc_ia/.github/workflows/docs-zip-release.yml`."
             Si el repositorio usa GitLab CI (`.gitlab-ci.yml` presente) y falta job:
               "⚠️ Falta job GitLab CI. Añadir en `.gitlab-ci.yml` un job que ejecute
                `python scripts/build_docs_zip.py` en cada push a la rama principal
                y adjunte `dist/*.zip` como artefacto."
             Añadir pendiente: "[ ] Publicación automática de ZIP en CI no implementada."
Fase 7c — Instrucciones de visualización (SIEMPRE obligatorio — no condicional)
         Crear o actualizar `VER_DOCUMENTACION.md` (idioma `en`: `VIEW_DOCS.md`) en la RAÍZ del
         destino (carpeta con mkdocs.yml/zensical.toml; fuera de `docs/`), a partir de
         `doc_ia/.github/templates/VER_DOCUMENTACION.template.md`: requisitos y pasos para ver
         la documentación desde cero en Windows, macOS y Linux, aunque no haya Python instalado.
         1. Extraer del destino los valores de los marcadores (nunca inventarlos):
              · generador → `{generador}` (mkdocs | zensical)
              · `requires-python` (pyproject.toml) → `{python_min}`; si no hay, el mínimo del generador
              · fichero de dependencias de docs → `{deps_file}`
                Falta (Gap V1) → CREAR `requirements-docs.txt` con versiones fijadas siguiendo
                `doc_ia/requirements-docs.txt` y los plugins/extensiones reales del mkdocs.yml
                del destino. Prohibido escribir un `pip install` sin fichero que lo respalde.
              · nombre del ZIP (Fase 7b) → `{zip_nombre}`; dónde se publica → `{zip_origen}`
              · `git remote get-url origin` → `{repo_url}`
              · Ruta A: solo si existen `site_url` Y un workflow/servicio que lo publique
                (Pages, gh-deploy, servidor interno documentado); si no → "No aplica" + motivo.
         2. Secciones fijas 0-7 de la plantilla: no omitir ni renumerar; vacías → "No aplica".
         3. Incluirlo en el ZIP: `EXTRA_FILES` de `mkdocs_hooks.py` y de `build_docs_zip.py`
            (Gap V2 si el hook/script del destino no lo incluye → actualizarlo).
         4. No enlazarlo desde `docs/` (está fuera de `docs_dir`: rompe `--strict`): en
            `docs/downloads.md` citarlo como `código inline`.
         5. Estado: A si no existe; B si algún valor (versión de Python, dependencias, nombre
            del ZIP, generador, URL) no coincide con el destino; C si coincide.
```

### Reglas por generador: Zensical

Aplican cuando **Generador = `zensical`**. Con `mkdocs-material` no cambia nada de lo anterior.
Patrón de referencia: el propio doc_ia (`scripts/build_docs_zip.py`, `tests/test_zensical_compat.py`,
ADR-003).

- **Configuración**: Zensical lee el `mkdocs.yml` del destino de forma nativa. **No crear
  `zensical.toml`** (fuente única) y aplicar la misma configuración estándar y los mismos assets
  (Fase 0b / Fase 5): el DOM generado es el de Material.
- **`hooks:` no se ejecuta, y Zensical no avisa** (`.claude/EDGE_CASES.md` § Zensical). Todo lo
  que el destino haga en hooks (sincronizar ficheros raíz, ZIP `latest`) debe ejecutarlo el
  script de build. Por eso, con Zensical:
  - **Fase 1** — señal adicional `TIENE_PIPELINE_SIN_HOOKS = true` si el
    `scripts/build_docs_zip.py` del origen define `HOOKLESS_BUILDERS` (o ejecuta los hooks antes y
    después del build). `TIENE_MKDOCS_PLUGIN` se sigue detectando, pero **no basta**: sin el
    pipeline, el ZIP `latest` no se genera.
  - **Gap A4** (`TIENE_ZIP_SCRIPT = true` y `TIENE_PIPELINE_SIN_HOOKS = false`) → actualizar el
    script siguiendo `doc_ia/scripts/build_docs_zip.py`: `HOOKLESS_BUILDERS`, `_load_hook`,
    `_pre_build` (hooks de pre-build del destino), `_post_build` (`mkdocs_hooks.on_post_build`, solo
    si el build termina con 0) e invocación `python -m <builder>`.
  - **Gap A2 / Paso B4** — `mkdocs_hooks.py` se crea igual: es la plantilla que invoca el script.
    Registrarlo en `hooks:` (Paso A2-2) solo si el destino también construye con MkDocs.
  - **Paso B1** — al adaptar `build_docs_zip.py`, poner `default="zensical"` en `--builder`.
- **Fase 5 — plugins**: cada plugin de `mkdocs.yml` debe figurar en
  `https://zensical.org/compatibility/plugins/`; los demás **se ignoran en silencio** → reportarlos
  en RESUMEN como hallazgo, nunca darlos por funcionando. `hooks:` presente sin pipeline → mismo
  tratamiento.
- **Fase 7 — build**:
  - Con pipeline: `python scripts/build_docs_zip.py --builder zensical`.
  - Sin pipeline: `python -m zensical build --strict`, advirtiendo de que no se ejecutan los hooks.
  - Serve: `python -m zensical serve` (no ejecuta hooks: los ficheros sincronizados pueden estar
    desfasados).
- **Fase 7b — `downloads.md`**: "Para Desarrolladores" usa `python scripts/build_docs_zip.py
  --builder zensical`; "Información de versión" indica Zensical. Los enlaces son
  `{nombre}-docs-latest.zip`, sin `../` (Paso B3): Zensical también aplica `offline` y
  `use_directory_urls: false`. Su índice JS es `search.js` en la raíz de `site/` (MkDocs:
  `search/search_index.js`); `build_docs_zip.py` acepta los dos.
- **Dependencias del destino**: `zensical` con **versión exacta** (está en alfa); en DOWNLOADS y
  RESUMEN, recordar que el workflow de release debe llamar a `build_docs_zip.py --builder zensical`.
- **Salida 8b DOWNLOADS**: añadir el estado de `TIENE_PIPELINE_SIN_HOOKS` y, si aplica, el Gap A4.

**Protocolo ACTUALIZAR (estado B) — obligatorio en Fases 2-4:**
1. Leer el documento existente completo antes de escribir cualquier línea.
2. Comparar sección a sección con el código actual del origen.
3. Actualizar solo las secciones afectadas; copiar verbatim las que siguen vigentes.
4. Nunca eliminar una sección "Pendiente de verificación" sin haberla verificado en el código.
5. Si un símbolo documentado ya no existe en el módulo: retirar su sección y documentar el reemplazo si lo hay.

Reglas transversales: idioma indicado en todo el contenido generado; no inventar módulos,
APIs ni capacidades; secciones vacías → `*No aplica para este módulo.*`; reglas operativas de
`.github/instructions/docs.instructions.md`.
**Mermaid — reglas completas en `DOCUMENTATION_STANDARD.md` §3.17; las que rompen el render:**
- `accTitle:` y `accDescr:` en todo bloque; máximo 12 nodos (8 en el Arquetipo 6).
- Labels de nodo con `@`, `#`, `(`, `)`, `{`, `}`: escribir la label **entre comillas dobles**
  (`A["Cl@ve (firma)"]`). Una `"` dentro de la label se escribe `#quot;`. **Prohibidas las
  entidades HTML** (`&#64;`, `&#40;`…): Mermaid no las decodifica y pinta un `&` sobrante.
- **`/` al inicio de `[...]` sin comillas — PROHIBIDO**: `[/texto/]` es nodo paralelogramo en Mermaid.
  Sin `/` de cierre → lexical error en la línea siguiente. Sustituir rutas UNIX/Windows por
  nombres descriptivos o usar `·` como separador. `<br/>` dentro de labels es seguro.
- `subgraph`: usar `subgraph id[título]` con ID alfanumérico sin hifens. Si el título contiene
  `/` o `-`, usar `·` o guión bajo. Prohibido `subgraph id[(título)]` — parse error.
- Estas reglas aplican solo dentro de bloques ` ```mermaid ``` `; fuera de ellos no hay restricción.

## Devuelve en este orden

1. **VALIDACIÓN DE INPUTS** — tabla: | Parámetro | Valor | Estado (✅/❌) | — si hay ❌, detenerse aquí.
2. **CLASIFICACIÓN DE ORÍGENES** (Fase 0a) — solo con ≥2 orígenes o si el único no es CÓDIGO:
   - Tabla: | Origen | Tipo detectado | Señales | Rol |
   - Si hay ≥2 orígenes CÓDIGO: indicar estrategia elegida por el usuario.
   - ⚠️ Confirmar con el usuario antes de continuar.
3. **INVENTARIO** (Fase 0+0b+0c+1) — indicar el modo (`incremental` desde `<base>` o `completo` + motivo); en incremental, incluir el informe de `doc_trace changes` por origen; tabla: | Módulo / Página | Estado (A/B/C) | Acción (CREAR/ACTUALIZAR/OMITIR) | Arquetipos / Secciones afectadas |
   - Con múltiples orígenes CÓDIGO: un sub-inventario por proyecto.
   - Si Fase 0c activa: incluir resultado de la validación previa (motor instalado, integridad) e indicar qué ficheros se convirtieron (motor usado: docling, markitdown o pandoc), cuáles quedan pendientes y motivo (motor no instalado, fichero inválido, etc.).
   - Si hay documentos convertidos: añadir sub-sección "Fuentes convertidas (`_fuentes/`)" con tabla | Origen | Carpeta `md/` | Copiados / Sin cambios / Huérfanos | Fases donde aplica |, la migración desde un nombre no canónico si la hay, y el aviso de que su texto se versiona en el destino. Sin estado A/B/C — son fuentes de contexto, no destinos de documentación.
4. **PLAN_DOC** — orden de generación con columnas CREAR / ACTUALIZAR (indicar secciones) / OMITIR; impacto en navegación.
5. **GENERACIÓN** (Fases 2-4) — por fases e iterando módulo a módulo; nunca un único prompt masivo.
   - Orígenes MATERIAL: usar como fuente de enriquecimiento de las secciones mapeadas (ver Fase 0a); no crear páginas propias para ellos.
6. **SYNC NAV** (Fase 5) — diff de `mkdocs.yml` (o config del generador) del destino.
7. **REVISIÓN** (Fase 6) — checklist de validación + hallazgos.
8. **BUILD** (Fase 7, solo opt-in) — resultado de `--verify-build`.
8b. **DOWNLOADS** (Fase 7b, siempre) — `downloads.md` creado/actualizado; indicar variante A o B; estado de las tres señales (TIENE_ZIP_SCRIPT, TIENE_MKDOCS_PLUGIN, TIENE_WORKFLOW_GITHUB) y, con Zensical, TIENE_PIPELINE_SIN_HOOKS; huecos (Gaps A1/A2/A3 y, con Zensical, A4) reportados si alguna falta; entrada añadida al nav.
8c. **VISUALIZACIÓN** (Fase 7c, siempre) — `VER_DOCUMENTACION.md` (o `VIEW_DOCS.md`) creado/actualizado/vigente; tabla | Marcador | Valor | Fuente verificada |; Ruta A aplicada o "No aplica" con motivo; Gaps V1/V2 resueltos o pendientes.
9. **RESUMEN** — archivos generados/actualizados, entradas de nav, pendientes de verificación humana.
10. **CIERRE DE SESIÓN** (siempre obligatorio) — crear artefacto `.ai/sessions/YYYY-MM-DD/` en el
    destino (`00_REQUEST.md`, `00_CONTEXT_SNAPSHOT.md`, `TRACEABILITY.md`) y proponer commit
    `docs(<scope>): <resumen>` con recuento de páginas creadas/actualizadas/omitidas; el commit
    incluye `_fuentes/` si la Fase 0c la creó o cambió.
    **Baseline** (siempre, en ambos modos, antes del commit): por cada origen CÓDIGO,
    `python <doc_ia>/scripts/doc_trace.py --root <raíz destino> baseline --origin <origen> [--name <nombre_origen>]`
    → `<raíz destino>/.ai/doc_state.json` (lo escribe la herramienta; nunca a mano) entra en el
    commit. Si avisa de cambios sin confirmar en el origen, indicarlo en RESUMEN: se volverán a
    revisar en la próxima sesión. Registrar el commit de cada origen en `00_CONTEXT_SNAPSHOT.md`.

## Ejemplo de entrada

```
Origen(es): c:\Desarrollo\python\libs\doc_ia
Destino: c:\Desarrollo\python\libs\doc_ia\docs
Generador: mkdocs-material
Idioma: es
Alcance: scripts/ completo (check_env.py, build_docs_zip.py)
Arquetipos: funcional, técnica, ejemplos
Verificación: --verify-build
```

## Invocación por plataforma

- **Claude Code**: `/document-project` (slash command) o "Lee y aplica `.github/prompts/document_project.prompt.md`"
- **Copilot Chat**: `/runSubagent Documentation Generator` proporcionando los 4 parámetros obligatorios
- **Gemini / Cursor / Codex**: "Lee y aplica `.github/prompts/document_project.prompt.md` con [parámetros]"
