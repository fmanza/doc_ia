# Instrucciones Compartidas: Copilot Chat + Claude Code + Gemini + Codex + Cursor

Configuración unificada para trabajar en `doc_ia` con asistentes de código.
Las reglas de cada plataforma solo deben añadir especialización; esta página es la
fuente común para arquitectura, calidad, pruebas y documentación.

---

## Rol esperado

Actúa como senior de ingeniería especializado en:
- Sistemas de instrucciones IA multiplataforma (Claude Code, Gemini, Copilot Chat, Cursor, Codex).
- Documentación técnica de proyectos de desarrollo: arquetipos formales, MkDocs Material, Mermaid.
- Tooling Python determinista: scripts de build, validación de entorno, empaquetado de docs.
- Testing determinista con `pytest` sin servicios externos.

---

## Proyecto: doc_ia

`doc_ia` es un proyecto IA para **documentar cualquier proyecto de desarrollo** mediante
instrucciones IA ejecutadas en los chats de los servicios contratados. Los **orígenes a
documentar** y el **destino de la documentación** son parámetros obligatorios de cada ejecución.

**Versión canónica**: consultar `pyproject.toml` antes de cerrar releases.
**Python**: `>=3.12` según `pyproject.toml`.

### Principios innegociables

1. **Sin API keys**: prohibido incrustar credenciales de servicios IA — no se configuran,
   no se versionan ni se incrustan en código, prompts o workflows de este proyecto.
2. **Sin componentes programáticos IA**: el código Python es exclusivamente tooling determinista
   (build de documentación, ZIP offline, validaciones). **Nunca invoca servicios IA.**
3. **Ejecución en chat**: la generación documental ocurre **siempre en el chat de la plataforma IA**,
   guiada por las instrucciones de `.github/` y `.claude/` — nunca en componentes programáticos.

Estos tres principios aplican a toda ejecución de `document_project` y de los arquetipos:
si una fase parece requerir generación vía API externa, la respuesta es no — se genera en el chat.

### Capacidades principales

- **Punto de entrada único para documentar**: `.github/prompts/document_project.prompt.md`
  (en Claude Code: `/document-project`). Valida inputs obligatorios — **origen(es) a documentar,
  destino de la documentación, generador e idioma** — y se detiene si faltan; después orquesta
  el flujo por fases del Documentation Generator y los arquetipos. **Cierre obligatorio**: crea
  artefacto `.ai/sessions/YYYY-MM-DD/` en el destino y propone commit `docs(<scope>):` antes
  de concluir la sesión.
- **Arquetipos documentales**: prompts formales en `.github/prompts/` (funcional, técnica, how-to,
  tutorial, ejemplos, ADR/MADR 4.0, navegación principal, onboarding, changelog, config IA,
  contribución, referencia del sistema) parametrizables por proyecto.
- **Flujo de trabajo canónico**: `PLAN → AUDIT_PLAN → IMPLEMENT → AUDIT_CODE → VERSION` con
  agentes (`.github/agents/`) y slash commands (`.claude/commands/`).
- **Bootstrap multiplataforma**: `.github/prompts/bootstrap_ai_config.prompt.md` replica este
  sistema en otros proyectos (modelo PULL).
- **Tooling determinista**: `scripts/check_env.py` (verificación de entorno) y
  `scripts/build_docs_zip.py` (ZIP offline con SHA256).

---

## Arquitectura real

```text
doc_ia/
  scripts/              # Tooling determinista: check_env.py, build_docs_zip.py, convert_to_md.py
  hooks/                # Hooks MkDocs + PostToolUse: sync_root_docs.py
  tests/                # Tests pytest del tooling
  docs/                 # Sitio MkDocs Material (es): index, downloads, guides/
                        #   ⚠️  docs/changelog.md y docs/contributing.md son ARTEFACTOS GENERADOS
                        #       por hooks/sync_root_docs.py — editar solo los ficheros raíz
  mkdocs.yml            # Fuente única de configuración del sitio
  CHANGELOG.md          # Fuente de verdad → docs/changelog.md (sync automático)
  CONTRIBUTING.md       # Fuente de verdad → docs/contributing.md (sync automático)
  .github/
    SHARED_INSTRUCTIONS.md   # Este fichero (canónico)
    agents/                  # 12 agentes del flujo de trabajo
    prompts/                 # Prompts de método + arquetipos documentales (12 activos)
    instructions/            # Reglas por tipo de archivo (python, sync, docs)
    workflows/               # CI: build y release del ZIP de docs
  .claude/              # Slash commands, hooks, plantillas Claude Code
  .ai/                  # Contexto persistente: product, architecture, runtime, glossary, standards
  .ai/sessions/TEMPLATE/  # Plantilla canónica de artefactos de sesión
```

### Responsabilidades por módulo

| Módulo | Responsabilidad |
|---|---|
| `scripts/` | Tooling determinista sin dependencias IA: validación de entorno, build + ZIP de docs, conversión de documentos binarios a Markdown con validación previa y motor elegido con `--engine` (`docling` por defecto: PDF/DOCX/PPTX/XLSX/CSV/HTML/EPUB, imágenes, email, LaTeX, audio, con OCR; `markitdown` alternativa ligera, necesaria solo para XLS; `pandoc` complemento: DOC/ODT/RST) |
| Patrón `<origen>/md/` → `_fuentes/` | Artefactos generados por `scripts/convert_to_md.py`: versiones `.md` de documentos binarios del origen (PDF, DOCX, PPTX, …). El destino recibe **siempre** una copia en `<raíz del destino>/_fuentes/<nombre_origen>/<ruta relativa al origen>` (nombre único, fuera de `docs/`, versionada); el agente la usa como contexto de primera clase en Fases 2-4 sin re-conversión. Nunca editarlos directamente. Ver Fase 0c de `document_project.prompt.md`. |
| `hooks/` | `sync_root_docs.py`: copia `CHANGELOG.md`/`CONTRIBUTING.md` a `docs/` antes del build y tras cada Edit/Write |
| `tests/` | Tests unitarios del tooling (sin red, sin servicios externos) |
| `docs/` | Documentación pública del propio proyecto (dogfooding de los arquetipos); `docs/changelog.md` y `docs/contributing.md` son artefactos generados |
| `.github/prompts/` | Instrucciones ejecutables en chat: método + arquetipos documentales |
| `.github/agents/` | Definición de agentes especializados por fase del flujo |
| `.claude/commands/` | Slash commands de Claude Code equivalentes a los prompts de método |
| `.ai/` | Contexto que los agentes leen antes de planificar |

---

## Principios de diseño

### Tooling determinista
- Cada script de `scripts/` debe ser ejecutable standalone (`python scripts/<nombre>.py`).
- Salida por código de retorno (`0` éxito, `≠0` fallo) para integrarse en CI y hooks.
- Prohibido: llamadas a APIs de IA, credenciales, estado global mutable, dependencias de red en tests.
- `print()` permitido en scripts CLI (son herramientas de línea de comandos, no librería).

### Instrucciones IA
- Los orígenes a documentar y el destino son **parámetros**, nunca constantes embebidas.
- Los prompts de arquetipo no inventan módulos ni capacidades: leen el árbol real del proyecto objetivo.
- Toda regla común vive aquí; los entry points por plataforma solo añaden especialización (DRY).

### SOLID operativo
- **SRP**: cada script y cada prompt tiene una responsabilidad principal.
- **OCP**: nuevos arquetipos o plataformas se añaden como ficheros nuevos, sin reescribir los existentes.
- **DIP**: los entry points dependen de este canónico, no entre sí.

### Formato de cadenas
- Usa f-strings para strings con parámetros; evita `.format()`, `%` y concatenación.

---

## Calidad y pruebas

### Comandos de desarrollo

```bash
python -m ruff check scripts tests    # Linting
python -m ruff format scripts tests   # Formato
python -m mypy scripts                # Type-checking (strict)
python -m pytest                      # Tests del tooling
python -m mkdocs build --strict       # Build de documentación (por defecto)
python -m mkdocs serve                # Documentación local
python scripts/check_env.py           # Verificación del entorno de tooling
python scripts/build_docs_zip.py      # Build + ZIP offline en dist/doc_ia-docs-{version}.zip
python scripts/convert_to_md.py <ruta>                 # Valida + convierte a Markdown en <ruta>/md/ (docling por defecto; --engine markitdown | pandoc)
python scripts/convert_to_md.py <ruta> --validate-only # Solo validación previa (motor instalado, integridad de ficheros)
# Onboarding: aplicar .github/prompts/onboarding_dev.prompt.md → docs/guides/onboarding_dev.md
```

> **Generador de docs**: MkDocs Material es el builder por defecto (instalado vía
> `requirements.txt`). Zensical es recíprocamente compatible sobre el mismo `mkdocs.yml`
> (`python scripts/build_docs_zip.py --builder zensical`) pero no es una dependencia del proyecto.

### Estrategia de tests
- Tests unitarios deterministas en `tests/`; sin red, sin servicios externos, sin credenciales.
- Los scripts se testean importando sus funciones (ver `tests/test_check_env.py`).
- `mypy` en modo `strict` sobre `scripts/` — todo símbolo tipado.

### Documentación obligatoria

#### Cuándo es CRÍTICA (bloquea PRs)

- ✅ Nuevo script en `scripts/` → docstring de módulo + entrada en README y docs
- ✅ Nuevo arquetipo o prompt → registrar en `.github/AGENTS.md` y `DOCUMENTATION_STANDARD.md`
- ✅ Antes de cerrar versión → `python -m mkdocs build --strict` sin errores ni links rotos
- ✅ Cambios en instrucciones IA → sincronizar todos los ficheros afectados (ver Gobernanza)
- ✅ **Nueva versión (VERSION)** → revisar `.github/instructions/sync.instructions.md`

#### Artefactos generados — nunca editar directamente

`docs/changelog.md` y `docs/contributing.md` son **copias automáticas** generadas por
`hooks/sync_root_docs.py`. Edita siempre los ficheros raíz (`CHANGELOG.md`, `CONTRIBUTING.md`);
el hook propaga los cambios a `docs/` tras cada `Edit`/`Write` y antes de cada `mkdocs build`.

Para añadir un nuevo fichero raíz al sync, registrar la tupla en `hooks/sync_root_docs.py → PAIRS`
y la entrada de navegación en `mkdocs.yml`. Ver `.github/instructions/sync.instructions.md`.

**Patrón de distribución offline (generalizable a proyectos origen externos)**:
El patrón completo consta de **tres señales independientes**; el flujo de
`document_project.prompt.md` (Fase 1 y Fase 7b) las detecta y reporta huecos si alguna falta:

1. `scripts/build_docs_zip.py` — build local + artefacto versionado en `dist/*.zip` + SHA256.
   `dist/*.zip`, `dist/*.sha256` y `dist/CHECKSUMS.txt` son artefactos generados: nunca editarlos
   a mano. La tabla en `docs/downloads.md` refleja estos artefactos: actualizarla tras el script.
2. `mkdocs_hooks.py` en la raíz del proyecto + `hooks: [mkdocs_hooks.py]` en `mkdocs.yml` — hook
   nativo MkDocs que genera automáticamente `{nombre}-docs-latest.zip` en `site/` en cada build.
   **Sin instalación**: funciona con cualquier Python que tenga mkdocs. No requiere `pyproject.toml`,
   `setup.py` ni `pip install -e .`. Patrón de referencia: `socyalpro/mkdocs_hooks.py`.
3. `.github/workflows/docs-zip-release.yml` — auto-publicación en GitHub Releases en cada push
   a `main` con cambios en `docs/`.

Los dos ZIP (latest y versionado) llevan en su raíz `start-server.py` (servidor local, solo
`127.0.0.1`) y `VER_DOCUMENTACION.md` (`EXTRA_FILES`). `VER_DOCUMENTACION.md` vive en la raíz del
destino, fuera de `docs/`, y se genera **siempre** en la Fase 7c desde
`.github/templates/VER_DOCUMENTACION.template.md`: requisitos y pasos para ver la documentación
desde cero (Windows, macOS, Linux; Python incluido). Abrir `index.html` con doble clic **no** es
una opción válida: con `use_directory_urls: true` los enlaces apuntan a carpetas.

#### Configuración de documentación

> **Fuente única**: `mkdocs.yml`. Lo consume MkDocs Material (por defecto) y, recíprocamente,
> Zensical si está instalado. No se usa `zensical.toml`.

- ✅ Página nueva, movida o eliminada en `docs/` → actualizar `mkdocs.yml` bajo `nav:`
- ✅ Ejecutar `python -m mkdocs serve` localmente antes de publicar
- ✅ Verificar que `python -m mkdocs build --strict` pase sin warnings

#### Convención de nombres en `docs/`

- **Todos los ficheros `.md`** en `docs/` usan **minúsculas con guiones bajos**: `installation.md`, `codex_guide.md`.
- **Guías** → siempre en `docs/guides/`, nunca en la raíz de `docs/`.
- **Conjunto mínimo obligatorio en `guides/`**: `onboarding_dev.md` + `troubleshooting.md` (pendientes de generar).

#### Arquetipos documentales

Toda la documentación pública sigue los **arquetipos formales** de
`.github/DOCUMENTATION_STANDARD.md`. Arquetipos activos: funcional, técnica, how-to (3a),
tutorial (3b), ejemplos, ADR/MADR 4.0, navegación + quick start (6), onboarding, trazabilidad
normativa (condicional), changelog (9), config agente IA (10), guía de contribución (11),
referencia del sistema (12, condicional). Regla transversal de evidencia y confianza: §3.16.
Los prompts están en `.github/prompts/*_doc.prompt.md`.

### 📦 Distribución de documentación offline

Las cuatro piezas siguientes son **obligatorias** en todo proyecto con documentación offline —
son complementarias, no alternativas:

1. **Página de descargas** (`docs/downloads.md`) — tabla de versiones + instrucciones SHA256.
2. **Script local** (`scripts/build_docs_zip.py`) — genera ZIP versionado + `.sha256` + `dist/CHECKSUMS.txt`.
   Permite empaquetar localmente sin depender de CI.
3. **Hook MkDocs** (`mkdocs_hooks.py` en la raíz + `hooks: [mkdocs_hooks.py]` en `mkdocs.yml`) —
   genera `{nombre}-docs-latest.zip` en `site/` automáticamente en cada build.
   El ZIP incluye siempre `start-server.py` (desde `scripts/start-server.py` en la raíz del proyecto).
   **Sin instalación**: cargado directamente por MkDocs; funciona con cualquier Python que tenga mkdocs.
   No requiere `pyproject.toml`, `setup.py`, `pip install -e .` ni activar ningún venv.
   Patrón de referencia: `doc_ia/mkdocs_hooks.py` (solo cambiar la línea `zip_path`).
4. **Workflow CI** (`.github/workflows/docs-zip-release.yml` o job en `.gitlab-ci.yml`) —
   auto-publica la release `docs-vX.Y.Z` con los artefactos en cada push a `main`.

**Regla**: las cuatro piezas son complementarias; si falta alguna, la distribución offline
está incompleta. Ver `document_project.prompt.md` §Fase 7b para detección automática y
acciones de remediación (Gap A1, A2, A3).

**Comandos locales**:
```bash
python scripts/build_docs_zip.py            # Build (mkdocs) + ZIP + SHA256
python scripts/build_docs_zip.py --no-build # ZIP sin build
sha256sum -c dist/*.sha256                  # Validar checksums (Linux/Mac)
```

#### Estándar: Validación de Markdown en documentación

- **Listas**: usar `- item` o `1. item`, NUNCA dos espacios al final de línea
  (renderizan `<br />` horizontales en lugar de `<ul><li>`).
- **Enlaces a archivos estáticos**: rutas relativas reales, NO placeholders `#`.
- **Validación**: `python -m mkdocs build --strict` sin errores.

### Formato de commits

Usa [Conventional Commits](https://www.conventionalcommits.org/):

```
feat:     nueva funcionalidad (tooling o instrucciones IA)
fix:      corrección de bug (hotfix, RCA → fix mínimo)
refactor: cambio sin impacto funcional
test:     solo tests, sin cambios de funcionalidad
docs:     solo documentación (README, docs/, arquetipos)
chore:    mantenimiento (deps, config, herramientas)
```

---

## Flujo de trabajo

Para cambios no triviales:

```text
PLAN → AUDIT_PLAN → IMPLEMENT → AUDIT_CODE → VERSION
```

Para auditorías o PR reviews, prioriza hallazgos verificables:
- bug o regresión;
- contrato público roto (CLI de scripts, estructura de arquetipos);
- prueba faltante en comportamiento modificado;
- documentación obsoleta que pueda inducir uso incorrecto.

No mezcles feature, hotfix y refactor salvo que el usuario lo pida explícitamente.
Si detectas instrucciones heredadas de otro proyecto (p.ej. util_bbdd), corrígelas o
márcalas como deuda técnica con ruta exacta.

### Directrices para Futuras IAs — sección obligatoria en VERSION

Cuando cierres una sesión (fase VERSION o `/version-closure`), puebla la sección
`## Directrices para Futuras IAs` del `TRACEABILITY.md` de la sesión con los hechos
descubiertos que una IA futura necesitaría para no repetir análisis. Formato:
`**[área]**: <hecho verificable>`. Template en `.ai/sessions/TEMPLATE/TRACEABILITY.md`.

---

## Gobernanza de plataformas IA

| Archivo | Plataforma | Propósito |
|---|---|---|
| `.github/SHARED_INSTRUCTIONS.md` | Copilot, Claude, Gemini, Codex, Cursor | Fuente canónica: arquitectura, calidad, comandos |
| `CLAUDE.md` | Claude Code | Especialización: slash commands, hooks, settings.json |
| `GEMINI.md` | Gemini Code Assist | Especialización: estándares de código y comandos rápidos |
| `.github/copilot-instructions.md` | GitHub Copilot Chat | Especialización: agentes VS Code, `#file:` |
| `.cursorrules` | Cursor | Especialización: estándar de documentación/ejemplos |
| `docs/guides/codex_guide.md` | Codex (OpenAI) | Guía de uso; Codex lee CLAUDE.md + este canónico + AGENTS.md |
| `.github/AGENTS.md` | Copilot/Claude | Registro de agentes especializados |
| `.github/prompts/bootstrap_ai_config.prompt.md` | Todas | Trasladar esta configuración IA a otro proyecto (modelo PULL) |
| `.ai/*.md` | Todas | Contexto persistente: producto, arquitectura |
| `.ai/sessions/TEMPLATE/` | Todas | Plantilla canónica de artefactos de sesión |

**Regla de oro**: Edita SHARED_INSTRUCTIONS.md primero. Luego sincroniza solo las
especializaciones afectadas.

---

*Actualizado: 2026-06-19*
