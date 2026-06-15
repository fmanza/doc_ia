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

- **Tipo de cada origen**: `CÓDIGO` | `NORMATIVA` | `ESPECIFICACIÓN` | `UI/PANTALLAS` | `REFERENCIA` | `CONTRATO` | `INFRAESTRUCTURA` | `MANUAL` — autodetectado si se omite; se confirma con el usuario antes de continuar
- **Estrategia** (solo con ≥2 orígenes CÓDIGO): `federado` | `hub+satélite` | `monorepo` — siempre preguntar al usuario, nunca autodetectar
- **Alcance**: módulos o subconjunto a documentar (por defecto: proyecto completo)
- **Arquetipos**: subconjunto a aplicar (por defecto: todos los aplicables según inventario)
- **Verificación**: `--verify-tools` y/o `--verify-build [--serve]` (opt-in, nunca automáticos)

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
         1. Para cada origen, detectar tipo por señales del sistema de ficheros:
            - CÓDIGO         : archivos fuente (.py, .js, .ts, .cs, .java, .go, .rs, …),
                               pyproject.toml, package.json, pom.xml, Cargo.toml, go.mod,
                               src/, tests/ presentes
            - NORMATIVA      : PDFs/docs con palabras clave en nombre o carpeta:
                               ley, decreto, directiva, rgpd, gdpr, une, iso, reglamento, compliance
            - ESPECIFICACIÓN : Word/PDF de requisitos, user stories, pliego, ficheros .feature (BDD);
                               carpetas specs/, requirements/, ux/, user-stories/
            - UI/PANTALLAS   : wireframes, mockups, capturas (.png, .jpg, .pdf de diseño);
                               carpetas mockups/, screens/, wireframes/, figma-exports/
            - REFERENCIA     : manuales de TERCEROS, RFCs, especificaciones de protocolo AJENAS al proyecto
            - CONTRATO       : especificaciones machine-readable del PROPIO proyecto:
                               .yaml/.json con clave openapi: o asyncapi:; .graphql/.gql; .proto; .avsc;
                               .sql DDL en db//migrations/; .dbml; carpetas api/, contracts/, schemas/, proto/
            - INFRAESTRUCTURA: IaC y despliegue: .tf (Terraform); Dockerfile, docker-compose.yml;
                               YAML en k8s/, deploy/, manifests/, helm/; playbooks Ansible en roles//ansible/
            - MANUAL         : documentación narrativa del PROPIO proyecto: .pdf/.docx/.md con manual/
                               guide/runbook/ayuda/help en nombre; carpetas manuals/, help/, user-docs/; .chm
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
            NORMATIVA        → Arquetipo 8 + enriquece §2 (Reglas de Negocio) del Arquetipo 1
            ESPECIFICACIÓN   → enriquece Arquetipo 1 §2+§3+§4 del proyecto principal
            UI/PANTALLAS     → enriquece Arquetipo 1 §3 (Casos de Uso) y Arquetipo 3
            REFERENCIA       → enriquece Arquetipo 2 §4 (Dependencias) o Arquetipo 5 (ADR)
            CONTRATO         → enriquece Arquetipo 2 §1 (Arquitectura/interfaces) y §2 (Modelo de Datos/Contratos)
            INFRAESTRUCTURA  → enriquece Arquetipo 2 §4 (Dependencias) y Arquetipo 6D §3 (vista despliegue)
            MANUAL           → enriquece Arq. 3a §3, Arq. 3b §3, Arq. 6A/B §1 (Descripción), Arq. 7 §3 y §5

Fase 0 — Detección de normativa: si el origen referencia normativa de obligado cumplimiento,
         ofrecer Arquetipo 8 (normative_traceability.prompt.md). Si no hay, omitir.
         Nota: si la Fase 0a ya clasificó un origen como NORMATIVA, este paso está cubierto.
Fase 0b — Conversión de documentos no legibles y uso de documentos pre-convertidos:
         Paso 0 — Detectar carpeta md/ pre-existente (ejecutar SIEMPRE, antes del Paso 1):
           · Buscar en todo el árbol del origen subcarpetas llamadas `md/` que contengan
             ficheros `.md`. Criterio de carpeta válida de pre-convertidos: la carpeta `md/`
             existe junto a ficheros binarios en el directorio padre, O sus ficheros `.md`
             tienen nombres que corresponden a binarios del directorio padre (sin extensión).
             Si no se cumplen estos criterios, descartar esa carpeta `md/` para este paso.
           · Para orígenes clasificados como REFERENCIA o NORMATIVA en Fase 0a, ejecutar
             este paso con prioridad aunque no haya ficheros binarios visibles.
           · Para cada fichero binario encontrado, comprobar si ya tiene equivalente en `md/`
             (mismo nombre relativo, extensión cambiada a `.md`):
               TIENE_MD = true  → marcar OMITIR_CONVERSIÓN
               TIENE_MD = false → añadir a lista de pendientes de conversión (Paso 1)
           · Si TODOS los binarios tienen TIENE_MD = true, O si no hay binarios pero `md/`
             tiene contenido → omitir Pasos 1-3 y pasar directamente al Paso 4.
           · Si `md/` parcial (algunos binarios sin equivalente) → ejecutar Pasos 1-3 solo
             para los pendientes; incluir ya los pre-existentes en Paso 4.
           · Si no existe ninguna `md/` válida NI ficheros binarios → omitir esta fase.
           · Cuando `md/` existe sin binarios visibles (binarios eliminados tras conversión),
             reportar en INVENTARIO con nota "Documentos pre-convertidos sin binario original"
             y confirmar con el usuario antes de usarlos en Fases 2-4.
         Paso 1 — Detectar binarios pendientes de conversión (solo si Paso 0 identifica pendientes):
           Extensiones no legibles directamente: .pdf, .docx, .doc, .pptx, .odt, .epub, .rst, .html, .htm
         Paso 2 — Proponer conversión de los pendientes:
           → proponer al usuario ejecutar en el directorio del ORIGEN:
                python scripts/convert_to_md.py <ruta_origen>
            Crea una carpeta `md/` dentro del origen con las versiones Markdown convertidas,
            reflejando la estructura de subdirectorios para evitar colisiones de nombres.
            El script usa la herramienta correcta según la extensión:
              - PDF                     → markitdown  (pip install markitdown)
              - DOCX, DOC, PPTX, ODT,
                EPUB, RST, HTML, HTM   → pandoc       (winget/brew/apt install pandoc)
            IMPORTANTE: pandoc NO puede leer PDF. Para PDF usar siempre markitdown.
            Si el origen no dispone del script (proyecto externo), usar directamente:
                markitdown <fichero.pdf> -o <fichero_sin_ext>.md     ← para PDF
                pandoc <fichero> -o <fichero_sin_ext>.md --wrap=none  ← para DOCX/PPTX/…
         Paso 3 — Resolver herramientas faltantes (si aplica):
              markitdown (PDF):  pip install markitdown
              pandoc (DOCX/…):   Windows: winget install JohnMacFarlane.Pandoc
                                 macOS:   brew install pandoc
                                 Linux:   sudo apt install pandoc | sudo dnf install pandoc
         Paso 4 — Incluir ficheros md/ como contexto (siempre que md/ tenga contenido):
           · Incluir en las Fases 2-4 todos los ficheros `.md` de carpetas `md/` del origen,
             tanto los recién convertidos como los pre-existentes.
           · Tratamiento idéntico a ficheros `.md` nativos del origen.
           · Estos ficheros son artefactos generados — nunca editarlos directamente.
         Paso 5 — Registrar en INVENTARIO los pendientes no resueltos:
           Si el usuario no instala la herramienta o decide omitir → registrar en INVENTARIO
           (Fase 1) los ficheros no convertidos con estado A y nota:
           "Pendiente: requiere markitdown para convertir [nombre.pdf]" (PDF)
           "Pendiente: requiere pandoc para convertir [nombre.docx]" (DOCX/PPTX/…)
         Nota: omitir esta fase solo si no existen ficheros binarios NI carpeta `md/` con
         contenido válido en el origen.
Fase 1 — Inventariar y clasificar:
         Leer árbol real del origen (README, código, docs/, mkdocs.yml del destino,
         y carpetas `md/` de documentos de referencia pre-convertidos si existen).
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
Fase 3 — Documentación técnica con Mermaid (technical_doc.prompt.md) → [destino]/api/
Fase 4 — Ejemplos verificables (example_doc.prompt.md) → [destino]/examples/
         Guías y landing según inventario: guide_doc, landing_doc, onboarding_dev, architecture_doc.
Fase 5 — Sincronizar navegación y verificar configuración estándar del generador (mkdocs.yml del destino):
         a. Navegación: añadir/mover/retirar entradas de nav; indentación de 4 espacios extra por nivel.
         b. Configuración estándar (DOCUMENTATION_STANDARD.md §4.1) — verificar y corregir si falta:
            · palette: dos entradas (light con media+toggle, dark con scheme:slate+media+toggle)
            · extra_javascript: CDN mermaid@11 + assets/js/mermaid.js + assets/js/sidebar-toggle.js
            · extra_css: assets/css/mermaid.css + assets/css/nav.css
            · markdown_extensions: attr_list, md_in_html, pymdownx.snippets (base_path:[docs]),
              line_spans:__span y pygments_lang_class:true en pymdownx.highlight
            · plugins: search con lang del idioma del proyecto
         c. Assets: si alguno de los cuatro ficheros de docs/assets/ (js/mermaid.js,
            js/sidebar-toggle.js, css/mermaid.css, css/nav.css) no existe en el destino,
            indicarlo explícitamente en RESUMEN con la acción: "Copiar desde doc_ia/docs/assets/".
Fase 6 — Revisión final: Markdown, enlaces relativos, sintaxis Mermaid, secciones de arquetipo completas.
Fase 7 — Verificación de build (solo con --verify-build): build --strict del generador + lectura del HTML.
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
                  Verificar que `docs/downloads.md` usa la estructura normalizada con enlace HTML:
                    `<a href="../{nombre}-docs-latest.zip">{nombre}-docs-latest.zip</a>`
                    `<a href="../{nombre}-docs-latest.zip.sha256">.sha256</a>`
                  Si la tabla no tiene estos enlaces → actualizar siguiendo la estructura del Paso B3.
                · false (Gap A2) → ⚠️ ACCIÓN OBLIGATORIA: CREAR el hook antes de cerrar sesión.

                  **Paso A2-0 — Crear `scripts/start-server.py`** (obligatorio):
                    Adaptar `doc_ia/scripts/start-server.py` cambiando solo el nombre del proyecto
                    en los mensajes `print`. Este script se incluirá dentro del ZIP para que los
                    usuarios puedan lanzar un servidor local con un solo comando.

                  **Paso A2-1 — Crear `mkdocs_hooks.py`** en la raíz del destino:
                    Adaptar `doc_ia/mkdocs_hooks.py` cambiando solo:
                      `zip_path = site_dir / "{nombre}-docs-latest.zip"`
                    El hook ya incluye el bloque que añade `start-server.py` al ZIP:
                      ```python
                      server_script = Path(__file__).parent / "scripts" / "start-server.py"
                      if server_script.exists():
                          zipf.write(server_script, arcname="start-server.py")
                      ```
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
             Si el script falla (dependencias, build error) → indicarlo en RESUMEN y
             dejar la tabla con valores reales hasta donde sea posible, marcando el resto
             como "Pendiente de verificación manual".

           **Paso B3 — Crear/actualizar `docs/downloads.md` con la estructura normalizada:**
             Estructura canónica (idéntica en todos los proyectos):
             1. **"Descarga Actual"** — tabla con enlace HTML directo al ZIP del plugin:
                ```
                | <a href="../{nombre}-docs-latest.zip">{nombre}-docs-latest.zip</a> | ~X MB | <a href="../{nombre}-docs-latest.zip.sha256">.sha256</a> | YYYY-MM-DD |
                ```
                El path `../` funciona porque con `use_directory_urls: true`,
                `downloads.md` → `site/downloads/index.html` y el ZIP está en `site/`.
                Línea de versión bajo la tabla: `**{Proyecto} {versión}** — descripción breve`.
             2. **"Cómo usar el ZIP"** — extraer (Windows + Linux/macOS) + visualizar:
                Opción A ⭐ (recomendada): `python start-server.py` — el script está incluido
                en el ZIP y abre el navegador automáticamente en `http://localhost:8000`.
                Opción B: abrir `index.html` directamente (sin búsqueda).
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
```

**Protocolo ACTUALIZAR (estado B) — obligatorio en Fases 2-4:**
1. Leer el documento existente completo antes de escribir cualquier línea.
2. Comparar sección a sección con el código actual del origen.
3. Actualizar solo las secciones afectadas; copiar verbatim las que siguen vigentes.
4. Nunca eliminar una sección "Pendiente de verificación" sin haberla verificado en el código.
5. Si un símbolo documentado ya no existe en el módulo: retirar su sección y documentar el reemplazo si lo hay.

Reglas transversales: idioma indicado en todo el contenido generado; no inventar módulos,
APIs ni capacidades; secciones vacías → `*No aplica para este módulo.*`; reglas operativas de
`.github/instructions/docs.instructions.md`.
**Mermaid — sintaxis de nodos y subgrafos:**
- Caracteres prohibidos en labels de nodo (`[...]`, `(...)`, `{...}`): `@`, `#`, `"`.
  Sustituir con entidad HTML: `@` → `&#64;`, `#` → `&#35;`.
- **`/` al inicio de `[...]` — PROHIBIDO**: `[/texto/]` es nodo paralelogramo en Mermaid 11.
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
3. **INVENTARIO** (Fase 0+0b+1) — tabla: | Módulo / Página | Estado (A/B/C) | Acción (CREAR/ACTUALIZAR/OMITIR) | Arquetipos / Secciones afectadas |
   - Con múltiples orígenes CÓDIGO: un sub-inventario por proyecto.
   - Si Fase 0b activa: indicar qué ficheros se convirtieron (con markitdown o pandoc) y cuáles quedan pendientes.
   - Si existen carpetas `md/` de documentos pre-convertidos: añadir sub-sección "Documentos de referencia (md/)" con tabla | Carpeta `md/` | Ficheros disponibles | Fases donde aplica |. Sin estado A/B/C — son fuentes de contexto, no destinos de documentación.
4. **PLAN_DOC** — orden de generación con columnas CREAR / ACTUALIZAR (indicar secciones) / OMITIR; impacto en navegación.
5. **GENERACIÓN** (Fases 2-4) — por fases e iterando módulo a módulo; nunca un único prompt masivo.
   - Orígenes MATERIAL: usar como fuente de enriquecimiento de las secciones mapeadas (ver Fase 0a); no crear páginas propias para ellos.
6. **SYNC NAV** (Fase 5) — diff de `mkdocs.yml` (o config del generador) del destino.
7. **REVISIÓN** (Fase 6) — checklist de validación + hallazgos.
8. **BUILD** (Fase 7, solo opt-in) — resultado de `--verify-build`.
8b. **DOWNLOADS** (Fase 7b, siempre) — `downloads.md` creado/actualizado; indicar variante A o B; estado de las tres señales (TIENE_ZIP_SCRIPT, TIENE_MKDOCS_PLUGIN, TIENE_WORKFLOW_GITHUB); huecos (Gaps A1/A2/A3) reportados si alguna falta; entrada añadida al nav.
9. **RESUMEN** — archivos generados/actualizados, entradas de nav, pendientes de verificación humana.
10. **CIERRE DE SESIÓN** (siempre obligatorio) — crear artefacto `.ai/sessions/YYYY-MM-DD/` en el
    destino (`00_REQUEST.md`, `00_CONTEXT_SNAPSHOT.md`, `TRACEABILITY.md`) y proponer commit
    `docs(<scope>): <resumen>` con recuento de páginas creadas/actualizadas/omitidas.

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
