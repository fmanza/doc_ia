# /document-project

Documentar un proyecto (origen → destino) orquestando los arquetipos formales. Comando de entrada único del producto doc_ia.

## Cuándo usar

- Documentar un proyecto origen externo completo aplicando los arquetipos (funcional, técnica, ejemplos, guías, ADR, landing, onboarding, normativa)
- Regenerar o actualizar la documentación propia de doc_ia (dogfooding)
- Documentar un subconjunto de módulos de un origen manteniendo `mkdocs.yml` sincronizado
- Antipatrón: NO usar para una única página suelta — aplica directamente el prompt de arquetipo correspondiente (`functional_doc`, `technical_doc`, etc.)
- Antipatrón: NO usar para cambios de código o tooling — usa `/new-feature`, `/hotfix` o `/refactor`

## Inputs requeridos (OBLIGATORIO completar TODOS)

- [ ] **Origen(es) a documentar**: Ruta(s) raíz del/los proyecto(s) (ej. `c:\repos\mi_api`)
- [ ] **Destino de la documentación**: Ruta donde se escribe (ej. `c:\repos\mi_api\docs`)
- [ ] **Generador**: `mkdocs-material` (por defecto) | `zensical` — con `zensical` aplicar
  `.github/prompts/document_project.prompt.md` § *Reglas por generador: Zensical* (no ejecuta
  `hooks:`; señal `TIENE_PIPELINE_SIN_HOOKS`, Gap A4, plugins soportados, build vía script)
- [ ] **Idioma**: `es` | `en` | otro
- [ ] **Tipo de cada origen** (opcional): `CÓDIGO` | `NORMATIVA` | `ESPECIFICACIÓN` | `UI/PANTALLAS` | `CONTRATO` | `INFRAESTRUCTURA` | `MANUAL` | `REFERENCIA` — autodetectado si se omite; el usuario confirma antes de continuar
- [ ] **Estrategia** (solo con ≥2 orígenes CÓDIGO): `federado` | `hub+satélite` | `monorepo` — preguntar al usuario, nunca autodetectar
- [ ] **Alcance** (opcional): módulos o subconjunto; por defecto proyecto completo
- [ ] **Arquetipos** (opcional): subconjunto; por defecto todos los aplicables **excepto 9 (Changelog) y 11 (Contribución)**, que son opt-in explícito
- [ ] **Verificación** (opcional): `--verify-tools` y/o `--verify-build [--serve]`
- [ ] **Modo** (opcional): `incremental` | `completo` — por defecto `incremental` si el destino
  tiene `.ai/doc_state.json` con baseline del origen. En incremental, la Fase 1 parte de
  `doc_trace.py changes` (cambios del origen desde el último CIERRE y páginas que los citan) y
  solo lee esos ficheros y páginas; el CIERRE siempre ejecuta `doc_trace.py baseline`
  (ver `document_project.prompt.md` § Fase 1 y § CIERRE)

### ⚠️ VALIDACIÓN

Si **alguno** de los 4 campos obligatorios (Origen, Destino, Generador, Idioma) está vacío,
es ambiguo o no es verificable en disco, **DETENTE AHORA**. Pide los datos al usuario antes
de continuar. No inventes rutas ni elijas generador o idioma por el usuario. No emitas
INVENTARIO hasta que los 4 estén completos (mismo patrón de validación que `/new-feature`).

Ejemplo de detención: "Campo 'Destino' vacío → preguntar: ¿escribo en `docs/` del origen o en un repositorio aparte?"

## Política de cambios para este comando

**Obligatorio**:
- Ejecutar el flujo por fases del Documentation Generator (Fases 0-6; Fase 7 solo opt-in)
- Actualizar la navegación del generador (`mkdocs.yml`) por cada página creada, movida o retirada
- Fase 7c: crear o actualizar `VER_DOCUMENTACION.md` (idioma `en`: `VIEW_DOCS.md`) en la raíz
  del destino desde `.github/templates/VER_DOCUMENTACION.template.md`, con valores verificados
  en el destino (ver `document_project.prompt.md` § Fase 7c)
- Secciones de arquetipo completas; vacías → `*No aplica para este módulo.*`
- **Al actualizar (estado B)**: leer el documento existente antes de escribir; conservar verbatim
  las secciones que siguen vigentes; actualizar solo las afectadas por cambios en el código

**Prohibido**:
- Incrustar API keys o invocar servicios IA desde código (la generación ocurre en este chat)
- Inventar módulos, APIs, salidas, errores o dependencias no presentes en el origen
- Modificar código fuente del origen (solo se escribe documentación y navegación)

**Recomendado**:
- Iterar módulo a módulo dentro de cada fase; nunca un único prompt masivo
- Cerrar con `python -m mkdocs build --strict` (o `--verify-build`) antes de publicar; con
  Zensical, `python scripts/build_docs_zip.py --builder zensical` (ejecuta los hooks que Zensical ignora)

## Sincronización de Configuración Visual (Fase 0b) ← OBLIGATORIO

> ⚠️ **Este paso es OBLIGATORIO en toda sesión `/document-project`**, tanto en la creación inicial
> de un destino como en cualquier actualización posterior. No omitir aunque el objetivo sea solo
> actualizar contenido: los assets y `mkdocs.yml` pueden haberse desincronizado desde la última sesión.
>
> Caso real documentado: proyecto `dpss` tenía `navigation.sections` activo y carecía de
> `nav.css` / `sidebar-toggle.js` → el menú lateral no era colapsable y los márgenes eran
> excesivamente anchos. Detectado en sesión `.ai/sessions/2026-06-12/`.

**Cuándo aplica**: En toda sesión `/document-project`, independientemente de si el destino ya tiene `mkdocs.yml`.

**Checklist obligatorio** (ejecutar al inicio de CADA sesión, antes de cualquier otra fase):

- [ ] `.gitignore` presente en la raíz del destino con los patrones estándar (primera sesión: crear si no existe; ver tabla abajo), sin ignorar `_fuentes/`
- [ ] `theme.features` verificado — sin `navigation.sections` si `nav.css` presente
- [ ] `extra_css` incluye `assets/css/nav.css` y `assets/css/mermaid.css`
- [ ] `extra_javascript` incluye, en este orden, `assets/js/sidebar-toggle.js`, `assets/vendor/mermaid/mermaid-12.2.0.min.js` y `assets/js/mermaid-theme.js`, y **no** incluye el CDN de Mermaid ni `assets/js/mermaid.js` (si están, retirarlos: duplican el render — ver `.claude/EDGE_CASES.md § Mermaid`)
- [ ] Los archivos `docs/assets/css/nav.css`, `docs/assets/css/mermaid.css`, `docs/assets/js/sidebar-toggle.js`, `docs/assets/js/mermaid-theme.js` y `docs/assets/vendor/mermaid/` (librería de la misma versión que doc_ia, `LICENSE`, `SOURCE.txt`) existen en disco; una librería de otra versión se sustituye
- [ ] `pymdownx.superfences` con `custom_fences` para `mermaid` (`format: !!python/name:pymdownx.superfences.fence_code_format`): sin él los diagramas salen como código
- [ ] `markdown_extensions` incluye los universales (ver tabla abajo)

**Qué sincronizar** (universal, aplicable a todos los proyectos MkDocs):
- `theme.features` — Ver tabla de compatibilidad más abajo; algunas requieren decisión
- `markdown_extensions` críticas — `pymdownx.snippets` (para `--8<--`), `pymdownx.superfences` (Mermaid), `pymdownx.emoji`, `pymdownx.highlight`, `pymdownx.inlinehilite`, `attr_list`, `md_in_html`
- `extra_javascript` y `extra_css` — Assets personalizados (`sidebar-toggle.js`, `nav.css`, `mermaid.css`, Mermaid local y `mermaid-theme.js`); el tema renderiza con la copia local de Mermaid
- `extra.social` — Enlaces de redes sociales (si aplica)

**Tabla de `theme.features` — copiables vs decisión**:

| Feature | Acción | Razón |
|---|---|---|
| `navigation.tabs`, `navigation.tabs.sticky` | ✅ Copiar | Universal |
| `navigation.top`, `navigation.footer` | ✅ Copiar | Universal |
| `search.suggest`, `search.highlight` | ✅ Copiar | Universal |
| `content.code.copy`, `content.code.annotate`, `content.tabs.link` | ✅ Copiar | Universal |
| `toc.follow` | ✅ Copiar | Universal |
| **`navigation.sections`** | ⚠️ **NO copiar si `nav.css` presente** | Activa grupos estáticos: desactiva `.md-nav__item--nested` → sidebar sin colapso |
| `navigation.expand` | ⚠️ Decisión | Expande todo por defecto; puede no ser deseado |
| `navigation.prune` | ⚠️ Decisión | Solo recomendado en navs muy grandes |

**Regla crítica**: Si `nav.css` está en `extra_css` → `navigation.sections` debe estar **ausente** de `theme.features`.

**Qué NO sincronizar** (específico del proyecto, nunca copiar ciegamente):
- `plugins` — Solo sincronizar si el destino lo necesita (ej: `mkdocstrings` es para proyectos con código; no para doc_ia)
- `site_name`, `site_description`, `site_author`, `site_url`, `repo_url` — Específicos del proyecto
- `site_dir`, `docs_dir` — Usar defaults o configuración destino

**Proceso**:
1. Si destino NO tiene `mkdocs.yml` → copiar completo de origen
2. Si destino tiene `mkdocs.yml` incompleto → sincronizar secciones "universal" del origen
3. Si destino tiene `mkdocs.yml` personalizado → verificar assets personalizados existen en disco

**Validación de Assets**:
```bash
# Verificar que los archivos referenciados en extra_javascript y extra_css existen
ls {destino}/docs/assets/js/*.js
ls {destino}/docs/assets/css/*.css

# Si faltan, copiar desde origen (si es proyecto hermano) o crear vacíos
cp -r {origen}/docs/assets/* {destino}/docs/assets/
```

**Commit de referencia**: En doc_ia → origin, origen de la configuración visual

**Inicialización de `.gitignore`** (primera sesión de un destino nuevo):

Si la raíz del destino no tiene `.gitignore`, crearlo con los patrones estándar. Si ya existe,
verificar que contiene al menos `site/`; añadir los que falten sin borrar los existentes.

```gitignore
site/
__pycache__/
*.pyc
*.egg-info/
.venv/
*.pdf
*.doc
*.docx
```

> **Por qué `*.pdf` / `*.doc` / `*.docx`**: los proyectos origen pueden incluir binarios de
> documentación fuente (especificaciones, manuales). Los binarios nunca entran en el repositorio
> de documentación; su **texto convertido** sí, en `_fuentes/` (ver *Fuentes convertidas* abajo),
> para que la evidencia y `doc_trace` apunten a rutas del propio repositorio. Nunca añadir
> `_fuentes/` al `.gitignore`.
>
> **Por qué `site/`**: MkDocs regenera `site/` en cada build. Si se versiona, genera ruido en
> cada `git status` y conflictos innecesarios. La página de descargas documenta cómo obtener
> el ZIP; no hace falta que `site/` esté en git.
>
> Si `site/` ya estaba rastreado (error de sesión anterior): ejecutar
> `git rm -r --cached site/` para retirarlo del índice sin borrar del disco.

---

## Devuelve en este orden

1. **VALIDACIÓN DE INPUTS**
   - Tabla: | Parámetro | Valor | Estado (✅/❌) |
   - Si hay ❌ → detenerse y preguntar

2. **CLASIFICACIÓN DE ORÍGENES** (solo con ≥2 orígenes, o si el único origen no es CÓDIGO)
   - Tabla: | Origen | Tipo detectado | Señales | Rol |
   - Tipos posibles:
     - `CÓDIGO` — archivos fuente (`.py`, `.js`, `.ts`, `.cs`, `.java`, `.go`, `.rs`, …), `pyproject.toml`, `package.json`, `pom.xml`, `src/`, `tests/` presentes → documentar como proyecto (arquetipos 1–7, y 12 si hay señales de configuración/CLI/códigos de salida)
     - `NORMATIVA` — PDFs/docs con nombres que contienen `ley`, `decreto`, `directiva`, `rgpd`, `gdpr`, `une`, `iso`, `reglamento` → activar Arquetipo 8; enriquece §2 Arquetipo 1 del proyecto principal
     - `ESPECIFICACIÓN` — Word/PDF de requisitos, user stories, pliego, ficheros `.feature`; carpetas `specs/`, `requirements/`, `ux/` → enriquece Arquetipo 1 §3+§5+§6+§7 del proyecto principal
     - `UI/PANTALLAS` — wireframes, mockups, capturas (`.png`, `.jpg`, `.pdf` de diseño); carpetas `mockups/`, `figma-exports/` → enriquece Arquetipo 1 §3 y Arquetipo 3
     - `REFERENCIA` — manuales de **terceros**, RFCs, especificaciones de protocolo **ajenas al proyecto** → enriquece Arquetipo 2 §4 o Arquetipo 5
     - `CONTRATO` — especificaciones machine-readable del **propio proyecto**: `openapi:` / `asyncapi:` YAML, `.graphql`, `.proto`, `.sql` DDL, `.dbml`; carpetas `api/`, `schemas/`, `proto/` → enriquece Arquetipo 2 §1 (interfaces) y §2 (contratos/datos) y Arquetipo 12 §5 (interfaces publicadas)
     - `INFRAESTRUCTURA` — IaC y despliegue: `.tf`, `Dockerfile`, `docker-compose.yml`, K8s YAML en `k8s/`/`deploy/`/`helm/`, Ansible → enriquece Arquetipo 2 §4 y Arquetipo 6C §3 › Despliegue
     - `MANUAL` — documentación narrativa del **propio proyecto**: `.pdf`/`.docx`/`.md` con `manual`/`guide`/`runbook`/`ayuda`/`help` en nombre; carpetas `manuals/`, `help/`, `user-docs/` → enriquece Arquetipos 3a §3, 3b §3, 6A/B §1 y 7 §3+§5
   - Si hay ≥2 orígenes `CÓDIGO` → preguntar estrategia (nunca autodetectar):
     - `federado`: cada proyecto documenta de forma independiente (docs/ propio, mkdocs.yml propio)
     - `hub+satélite`: un proyecto "hub" es el destino; los demás se documentan como secciones dentro de él
     - `monorepo`: un mkdocs.yml raíz agrupa secciones por proyecto
   - **Caso degenerado**: si no hay ningún origen `CÓDIGO` → **DETENER**: "No se detecta ningún proyecto de desarrollo. `/document-project` requiere al menos un origen de tipo CÓDIGO. Para documentar solo normativa o especificación, usa directamente `normative_traceability.prompt.md` o `functional_doc.prompt.md`."
   - ⚠️ **Confirmar clasificación con el usuario antes de continuar al INVENTARIO.**

3. **INVENTARIO** (Fases 0-1)
   - Normativa de referencia (Arquetipo 8) si aplica
   - Tabla con 4 columnas: | Módulo / Página | Estado | Acción | Arquetipos / Secciones |
     - Estado A — sin doc → CREAR
     - Estado B — desactualizado → ACTUALIZAR (indicar qué secciones)
     - Estado C — vigente → OMITIR
   - Criterios estado B: firma cambiada · símbolo nuevo no documentado · símbolo retirado
     del módulo · tests contradicen docs · sección "Pendiente de verificación" verificable ya
   - **Fuentes convertidas (`_fuentes/`)** — si el origen contiene carpetas `md/`
     (generadas por `scripts/convert_to_md.py`) o el destino ya tiene `_fuentes/`, añadir
     sub-sección separada:
     | Origen | Carpeta `md/` | Copiados / Sin cambios / Huérfanos | Fases donde aplica como contexto |
     No asignar estado A/B/C: son fuentes de contexto, no destinos de documentación.
     Regla única (Fase 0c, Paso 5, de `document_project.prompt.md`): el destino recibe **siempre**
     una copia en `<raíz del destino>/_fuentes/<nombre_origen>/<ruta relativa al origen>`, fuera
     de `docs/`, aunque origen y destino sean el mismo repositorio. Ningún otro nombre: si el
     destino tiene `.fuentes/` o `fuentes/` en su raíz, proponer la migración a `_fuentes/`
     y esperar confirmación. Huérfanos: listar y borrar solo con confirmación. Avisar de que el
     texto de los documentos se versiona en el destino.
     Enriquecen Fases 2-4 (leídos desde `_fuentes/`) con el mismo tratamiento que ficheros `.md`
     nativos del origen. Si `md/` existe sin binarios originales visibles: confirmar con el
     usuario antes de usar.

4. **PLAN_DOC**
   - Orden de ejecución: CREAR (A) antes que ACTUALIZAR (B); OMITIR (C) no se toca
   - Por cada página: acción + secciones afectadas + impacto en navegación
   - Con múltiples orígenes CÓDIGO: indicar estrategia elegida y qué proyecto es el hub (si aplica)

5. **GENERACIÓN** (Fases 2-4)
   - Funcional → técnica → ejemplos → guías/landing según inventario
   - Para estado B: leer página existente completa → actualizar solo secciones afectadas
     → conservar verbatim las vigentes → nunca borrar "Pendiente de verificación" sin verificar
   - Orígenes MATERIAL: usar como fuente de enriquecimiento de las secciones mapeadas (ver CLASIFICACIÓN); no crear páginas propias para ellos

6. **SYNC NAV** (Fase 5)
   - Diff de `mkdocs.yml` del destino

7. **REVISIÓN** (Fase 6)
   - Markdown, enlaces, Mermaid, secciones de arquetipo

8. **BUILD** (Fase 7, solo con `--verify-build`)

8c. **VISUALIZACIÓN** (Fase 7c, siempre)
   - `VER_DOCUMENTACION.md` creado / actualizado / vigente, en la raíz del destino (fuera de `docs/`)
   - Tabla: | Marcador | Valor | Fuente verificada | — sin valores inventados
   - Ruta A (web publicada) solo si hay `site_url` y publicación verificada; si no, "No aplica"
   - Gap V1 (falta `requirements-docs.txt` → crearlo) y Gap V2 (`EXTRA_FILES` en hook/script)
   - Prohibido indicar «abrir `index.html` con doble clic»: los enlaces apuntan a carpetas

9. **RESUMEN**
   - Archivos generados/actualizados, entradas de nav, pendientes de verificación humana

10. **CIERRE DE SESIÓN** (siempre obligatorio)

    **a) Archivos de contexto raíz `.ai/*.md`** — en la **primera sesión** de un destino nuevo
    (o si faltan en un destino existente), crear los siguientes archivos de contexto persistente
    sobre el proyecto FUENTE. Una IA futura los leerá en su `00_CONTEXT_SNAPSHOT` antes de empezar.

    | Archivo | Contenido |
    |---|---|
    | `.ai/product.md` | Descripción, versión, dominio funcional, audiencia, capacidades, marco legal |
    | `.ai/architecture.md` | Módulos, stack tecnológico, patrones de diseño, CI/CD |
    | `.ai/glossary.md` | Términos del dominio funcional, capas arquitectónicas, abreviaturas |
    | `.ai/runtime.md` | Prerequisitos, estructura de proyecto, comandos, despliegue, BD |
    | `.ai/standards.md` | Estilo de código, testing, commits, seguridad, API |

    Estos archivos describen el **proyecto fuente**, no doc_ia. No copiar de DPSS o SOCYALPRO —
    escribir a partir de lo observado en el origen durante el INVENTARIO.
    En sesiones posteriores: actualizar solo si el INVENTARIO detecta cambios relevantes en el origen.

    **b) Artefacto `.ai/sessions/`** — crear en el **destino** (no en doc_ia), en la ruta
    `{destino}/../.ai/sessions/YYYY-MM-DD/` con tres ficheros:

    - `00_REQUEST.md` — inputs recibidos (origen, destino, generador, idioma, alcance,
      arquetipos, verificación) + objetivo operativo de la sesión
    - `00_CONTEXT_SNAPSHOT.md` — ficheros leídos antes de la primera fase, estado git
      (rama, cambios pre-existentes, último commit), estado de build (si se ejecutó).
      Si la sesión usa orígenes externos (MANUAL, NORMATIVA, CÓDIGO fuera del destino):
      añadir sección "Orígenes externos consultados" con sus rutas.
    - `TRACEABILITY.md` — resumen cronológico de acciones, tabla de artefactos generados
      (`| Artefacto | Ruta | Estado |`), directrices para IAs futuras, veredicto final
      (`GO` / `GO_CONDICIONAL` / `NO_GO` / `CLOSED`)

    Usar como plantilla los ficheros de `.ai/sessions/TEMPLATE/` de doc_ia (o del propio destino
    si ya los tiene). Si `.ai/sessions/` no existe en el destino, crearlo junto con
    la carpeta `TEMPLATE/` y el archivo `INDEX.md` — es el primer uso del sistema de sesiones
    en ese proyecto. El `INDEX.md` debe listar las sesiones completadas con fecha, objetivo,
    rama, skill y estado.

    **b) Commit** — una vez escritos los artefactos y verificado el build (si aplica), proponer
    el siguiente commit en el repositorio **destino**:

    ```
    docs(<scope>): <resumen de lo documentado>

    Sesión: .ai/sessions/YYYY-MM-DD/
    Arquetipos: <lista de arquetipos generados/actualizados>
    Páginas: <N> creadas · <M> actualizadas · <K> omitidas
    Fuentes: _fuentes/ <N> copiadas · <M> sin cambios     ← solo si hubo Fase 0c
    ```

    - `git add` incluye `_fuentes/` cuando la Fase 0c la creó o cambió
    - Antes del commit, `doc_trace.py --root <raíz destino> baseline --origin <origen>` por cada
      origen CÓDIGO; `git add` incluye `.ai/doc_state.json` (base del próximo modo incremental)

    - `<scope>` = nombre corto del origen (ej. `util_bbdd`, `mi_api`)
    - Conventional Commits: usar `docs:` para sesiones de documentación pura
    - No hacer `git push`: solo proponer el mensaje y ejecutar `git add` + `git commit`
      si el usuario confirma
    - Si el destino es el propio doc_ia, hacer el commit en doc_ia

## Ejemplo de entrada — origen único

```
Origen(es): c:\Desarrollo\python\libs\doc_ia
Destino: c:\Desarrollo\python\libs\doc_ia\docs
Generador: mkdocs-material
Idioma: es
Alcance: scripts/ completo (check_env.py, build_docs_zip.py)
Arquetipos: funcional, técnica, ejemplos
Verificación: --verify-build
```

## Ejemplo de entrada — múltiples orígenes heterogéneos

```
Origen(es):
  - c:\repos\mi_api                  (proyecto principal)
  - c:\docs\normativa\ley_39.pdf     (ley de referencia)
  - c:\docs\pantallas\mockups\       (capturas de pantalla)
Destino: c:\repos\mi_api\docs
Generador: mkdocs-material
Idioma: es
Tipo de cada origen: mi_api=CÓDIGO, ley_39.pdf=NORMATIVA, mockups=UI/PANTALLAS
```

## Ejemplo de entrada — múltiples proyectos de código

```
Origen(es):
  - c:\repos\mi_api    (backend Python)
  - c:\repos\mi_web    (frontend React)
Destino: c:\repos\mi_api\docs
Generador: mkdocs-material
Idioma: es
Estrategia: hub+satélite  (mi_api es el hub)
```

## Ejemplo de salida esperada (VALIDACIÓN + CLASIFICACIÓN + INVENTARIO)

```markdown
## VALIDACIÓN DE INPUTS

| Parámetro | Valor | Estado |
|---|---|---|
| Origen(es) | c:\Desarrollo\python\libs\doc_ia | ✅ existe y es legible |
| Destino | c:\Desarrollo\python\libs\doc_ia\docs | ✅ existe |
| Generador | mkdocs-material | ✅ mkdocs.yml presente |
| Idioma | es | ✅ |

## CLASIFICACIÓN DE ORÍGENES

(origen único — fase omitida; tipo detectado: CÓDIGO)

## INVENTARIO

| Módulo / Página | Estado | Acción | Arquetipos / Secciones |
|---|---|---|---|
| scripts/check_env.py | A — sin doc | CREAR | funcional + técnica + ejemplo |
| scripts/build_docs_zip.py | B — desactualizado | ACTUALIZAR §3 §5 | técnica (firma `--builder` cambiada) |
| docs/index.md | C — vigente | OMITIR | — |

Normativa de referencia: no detectada → Arquetipo 8 omitido.
```

## Qué hacer si falla

- **"Origen no legible o fuera del workspace"** → pedir al usuario que añada el directorio como working dir adicional o confirme la ruta
- **"mkdocs build advierte sobre assets CSS/JS no encontrados"** → Verificar que `extra_javascript` y `extra_css` en `mkdocs.yml` referencian archivos existentes en `docs/assets/`. Si faltan, sincronizarlos desde origen o crearlos vacíos.
- **"mkdocs build --strict falla tras SYNC NAV"** → ver `.claude/TESTING_GUIDE.md`; revisar páginas huérfanas o rotas en `nav:`
- **"Contexto perdido entre fases"** → ver `.claude/EDGE_CASES.md`; retomar desde el RESUMEN parcial de la última fase completada
- **"El usuario pide generar vía API externa"** → rechazar: principio innegociable (SHARED_INSTRUCTIONS § Principios)

## Referencias

- `.github/prompts/document_project.prompt.md` → prompt equivalente multiplataforma
- `.github/agents/documentation-generator.agent.md` → flujo por fases que orquesta este comando
- `.github/DOCUMENTATION_STANDARD.md` → arquetipos formales (estructuras obligatorias)
- `.github/instructions/docs.instructions.md` → reglas operativas (Mermaid, Markdown, snippets)
