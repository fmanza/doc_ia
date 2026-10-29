# Instrucciones para Claude Code — doc_ia

Este fichero proporciona especialización a Claude Code cuando trabaja con doc_ia,
incluyendo slash commands, hooks de desarrollo y configuración integrada.

---

## ⚠️ Contexto previo obligatorio

Lee **primero**:
- **`.github/SHARED_INSTRUCTIONS.md`** — Fuente canónica: principios del proyecto (sin API keys,
  tooling determinista, ejecución en chat), arquitectura, calidad, comandos, documentación,
  flujo de trabajo, Conventional Commits. **Esta es la base.**
- **Este fichero** — Especialización para Claude Code únicamente.

---

## Slash commands de Claude Code

Usa estos comandos para activar flujos estructurados con automatización integrada:

| Comando | Propósito | Entrada | Salida |
|---|---|---|---|
| `/document-project` | **Documentar un proyecto (producto doc_ia)** | Origen(es) + destino + generador + idioma (obligatorios; si faltan, se detiene) | VALIDACIÓN → INVENTARIO → PLAN_DOC → GENERACIÓN → SYNC NAV → REVISIÓN → RESUMEN → CIERRE (sesión `.ai/` + commit) |
| `/new-feature` | Nueva funcionalidad | Descripción + módulos | PLAN → AUDIT_PLAN → IMPLEMENT → AUDIT_CODE → VERSION |
| `/hotfix` | Bug P1/P2 mínimo | Descripción + impacto | RCA → FIX → AUDIT_CODE → VERSION |
| `/refactor` | Refactor sin cambios funcionales | Área + objetivo | PLAN → AUDIT_PLAN → IMPLEMENT → AUDIT_CODE |
| `/audit-code` | Auditoría técnica independiente | Rutas o cambios | Scope → Findings → Verdict |
| `/security-review` | Auditoría de seguridad | Áreas críticas | Findings by severity → Remediation |
| `/tech-debt` | Deuda técnica priorizada | Área o módulo | Findings por severidad → Plan de remediación |
| `/maturity-assessment` | Evaluación de madurez del repo | Área o evaluación completa | Executive summary → Findings → Maturity verdict |
| `/version-closure` | Cierre de versión | Sesión completada | Release notes → Changelog → Rollback → Handoff |

**Ejemplo de uso**:

```
/new-feature

Objetivo: Añadir validación de enlaces rotos al tooling de docs

Alcance: scripts/check_links.py (nuevo), tests/test_check_links.py (nuevo)

Restricciones:
  - Tooling determinista: sin red en tests, sin servicios IA
  - mypy strict + ruff sin errores
  - Documentación en docstrings + entrada en README
```

---

## Trasladar esta configuración IA a otro proyecto (bootstrap)

Para replicar este sistema de instrucciones IA (Claude / Gemini / Copilot / Cursor / Codex) en **otro
proyecto**, incluso de **otro lenguaje y arquitectura**, usa el prompt
[`.github/prompts/bootstrap_ai_config.prompt.md`](./.github/prompts/bootstrap_ai_config.prompt.md).
La auditoría posterior la hace el agente **Config Reviewer**.

**Modelo PULL — se invoca desde el proyecto DESTINO**, apuntando a este repo como plantilla de
solo lectura. El lenguaje y la arquitectura del destino son **parámetros de entrada**, no constantes.

| Capa | Acción | Ejemplos |
|---|---|---|
| **A — Metodología** | Copiar verbatim (revisar comandos embebidos) | `.github/agents/`, `.github/prompts/`, `.claude/commands/`, `.ai/sessions/TEMPLATE/` |
| **B — Especialización** | Copiar + reescribir dominio | `SHARED_INSTRUCTIONS.md`, `CLAUDE.md`, `GEMINI.md`, `copilot-instructions.md`, `.cursorrules` |
| **C — Contexto** | Regenerar analizando el destino | `.ai/{product,architecture,runtime,glossary,standards}.md` |
| **D — No copiar** | Excluir | `.ai/sessions/<fechas>/`, `CHANGELOG.md`, caches, `settings.local.json` |

---

## Configuración: Hooks y PostToolUse

```
.claude/
  settings.json           ← Configuración: hooks PostToolUse (sync + ruff + mypy + pytest)
  settings.json.example   ← Plantilla de ejemplo
  settings.local.json     ← Personalización local (no versionado, git-ignored)
  commands/               ← Slash commands personalizados
  EDGE_CASES.md           ← Casos límite conocidos en el proyecto (se puebla con el tiempo)
  TESTING_GUIDE.md        ← Guía de testing con PostToolUse
hooks/
  sync_root_docs.py       ← Copia CHANGELOG.md y CONTRIBUTING.md a docs/ (y cualquier PAIRS)
```

**Orden de ejecución automático** (hooks PostToolUse sobre Edit|Write):

1. `python hooks/sync_root_docs.py` — sincroniza ficheros raíz → `docs/` (**va primero**)
2. `python -m ruff check scripts tests hooks --quiet` (linting)
3. `python -m mypy scripts --no-error-summary` (type-checking strict)
4. `python -m pytest --collect-only -q tests` (validación de sintaxis de tests)

**Regla crítica de sync**: `docs/changelog.md` y `docs/contributing.md` son **artefactos
generados** — nunca los edites directamente. Edita siempre `CHANGELOG.md` o `CONTRIBUTING.md`
en la raíz; el hook propaga los cambios automáticamente. Para añadir un nuevo fichero raíz
al sync, añadir su tupla a `PAIRS` en `hooks/sync_root_docs.py` y su entrada en `mkdocs.yml`.

---

## 📐 Arquetipos Formales de Documentación

Toda documentación sigue los **arquetipos formales** definidos en
[`.github/DOCUMENTATION_STANDARD.md`](./.github/DOCUMENTATION_STANDARD.md).
Los arquetipos 1–8 son la base; 3b y 9–11 son las adiciones 2024-2025; 12 y la regla transversal
de evidencia (§3.16) son las adiciones 2026.

| Arquetipo | Propósito | Ubicación | Prompt |
|---|---|---|---|
| **1. Funcional** | ¿Qué hace y por qué? | `docs/functional/` | `functional_doc.prompt.md` |
| **2. Técnica/API** | ¿Cómo funciona internamente? | `docs/api/` | `technical_doc.prompt.md` |
| **3a. How-to** | ¿Cómo resuelvo esta tarea concreta? | `docs/guides/*_howto.md` | `howto_doc.prompt.md` |
| **3b. Tutorial** | ¿Cómo aprendo esto paso a paso? | `docs/guides/*_tutorial.md` | `tutorial_doc.prompt.md` |
| **4. Ejemplos de Código** | ¿Cómo se implementa? | `docs/examples/` | `example_doc.prompt.md` |
| **5. ADR / MADR 4.0** | ¿Por qué se decidió así? | `docs/adr/` | `architecture_doc.prompt.md` |
| **6. Navegación Principal** *(variante A/B/C/D)* | Intro + instalación + visión + quick start | `docs/index.md`, `installation.md`, `architecture.md`, `quickstart.md` | `landing_doc.prompt.md` |
| **7. Onboarding Desarrolladores** | ¿Cómo me incorporo? | `docs/guides/onboarding_dev.md` | `onboarding_dev.prompt.md` |
| **8. Trazabilidad Normativa** *(condicional)* | ¿Qué normativa cubre el sistema? | `docs/normativa/` | `normative_traceability.prompt.md` |
| **9. Changelog** *(opt-in)* | ¿Qué cambió en cada versión? | `CHANGELOG.md` | `changelog.prompt.md` |
| **10. Config Agente IA** | ¿Cómo está configurado el agente IA? | `docs/ai-config/` | `ai_config_doc.prompt.md` |
| **11. Guía de Contribución** *(opt-in)* | ¿Cómo contribuyo al proyecto? | `CONTRIBUTING.md` | `contributing_doc.prompt.md` |
| **12. Referencia del Sistema** *(condicional)* | ¿Qué configuración, comandos y códigos expone? | `docs/reference/` | `reference_doc.prompt.md` |

**Características clave**:
- ✅ Secciones fijas: estructura inmutable (nunca omitir; escribir "No aplica" si vacío)
- ✅ Enlaces bidireccionales: Arquetipo 2 (§5) ↔ Arquetipo 4 (§5) obligatorios
- ✅ Evidencia verificable: Arq. 1, 2 y 12 cierran con bloque plegable "Evidencia" (`ruta::símbolo`
  en código inline + leyenda ✅ ⚠️ 🔍 ❌) — ver `DOCUMENTATION_STANDARD.md` §3.16
- ✅ Parametrizables: en doc_ia los arquetipos son además **producto** — se aplican a proyectos
  origen externos pasando origen y destino como parámetros
- ✅ Arquetipo 5 sigue MADR 4.0 (frontmatter YAML + título "Use X for Y")
- ✅ Arquetipos 3a/3b siguen cuadrantes Diátaxis (How-to / Tutorial claramente separados)

## Documentación con Claude Code

Usa **`/document-project`** como **comando de entrada único** para documentar un proyecto
(origen externo o doc_ia mismo): valida los inputs obligatorios (origen(es), destino, generador,
idioma) y orquesta internamente el flujo de fases del agente **Documentation Generator** y los
arquetipos. No uses un único prompt masivo: trabaja siempre por fases separadas.

### Flujo por fases

```
Fase 0b — Sincronización visual (OBLIGATORIO): verificar/aplicar assets + mkdocs.yml visual
Fase 1  — Inventariar: leer scripts/, README, docs/, mkdocs.yml
Fase 2  — Mapeo funcional (Senior Product Owner): objetivo, precondiciones, flujo, reglas
Fase 3  — Documentación técnica: responsabilidad, Mermaid, API pública, contratos, errores
Fase 4  — Ejemplos verificables: código real, resultado determinista, sin credenciales
Fase 5  — Sincronizar mkdocs.yml: añadir/mover/retirar entradas de navegación
Fase 6  — Revisión final: validar Markdown, enlaces relativos y Mermaid (§3.17 del estándar)
Fase 7  — Verificación de build (opt-in --verify-build): python -m mkdocs build --strict + leer site/
```

> **Fase 0b — Requisito OBLIGATORIO** (creación y actualización):
> Verificar que el destino tiene los 6 recursos (`nav.css`, `mermaid.css`, `sidebar-toggle.js`,
> Mermaid local en `vendor/mermaid/`, `mermaid-theme.js` y el shim local en `vendor/iframe-worker/`)
> en `docs/assets/`, que `mkdocs.yml` los referencia en `extra_css` / `extra_javascript` /
> `extra.polyfills` (la librería antes de `mermaid-theme.js`), que declara `use_directory_urls: false`
> y el plugin `offline` (ZIP con doble clic en `index.html`, sin servidor), que
> `pymdownx.superfences` tiene `custom_fences` para `mermaid` y **no** hay CDN de Mermaid ni
> `mermaid.js` propio (duplican el render), y que **`navigation.sections` está ausente** de `theme.features`
> (su presencia desactiva el colapso del menú lateral e invalida `nav.css`).
> Ver checklist completo en `.claude/commands/document-project.md § Sincronización de Configuración Visual`.
> Ver caso real documentado en `.claude/EDGE_CASES.md § [mkdocs.yml] navigation.sections`.

### Contrato documental obligatorio

1. Revisar documentación existente antes de crear páginas nuevas.
2. Separar siempre **funcional**, **técnico** y **ejemplos** en secciones diferenciadas.
3. MkDocs Material como generador por defecto (Zensical recíprocamente compatible); Mermaid.js para diagramas.
4. Actualizar `mkdocs.yml` cuando se creen, muevan o eliminen páginas en `docs/`.
5. No inventar capacidades, módulos, APIs, salidas, errores ni dependencias.
6. **Prohibido** delegar la generación de contenido a APIs de IA externas (principio del proyecto:
   la generación ocurre en este chat, nunca en componentes programáticos).

---

## 📦 Descarga de Documentación Offline

doc_ia proporciona **documentación en ZIP offline** mediante dos mecanismos complementarios
que **deben existir siempre** (no son alternativos):

- **Script local** (`scripts/build_docs_zip.py`) — build + ZIP + SHA256 en `dist/`.
- **Workflow GitHub** (`.github/workflows/docs-zip-release.yml`) — auto-publicación de la
  release `docs-vX.Y.Z` en cada push a `main` con cambios en `docs/`.

```bash
python scripts/build_docs_zip.py        # Build (mkdocs) + ZIP en dist/doc_ia-docs-{version}.zip
cat dist/doc_ia-docs-*.zip.sha256       # Ver checksum
sha256sum -c dist/*.sha256              # Validar (Linux/Mac)
```

### Actualizar tabla "Descarga Actual" en docs/downloads.md

> La regla completa (detección de las dos señales, pasos, guarda de orden con build) vive en
> `.github/SHARED_INSTRUCTIONS.md` § *Patrón de distribución offline* y en
> `.github/prompts/document_project.prompt.md` § *Fase 7b*. Esta sección añade solo los
> comandos específicos del proyecto **doc_ia**.

Después de generar el ZIP de doc_ia, actualiza la tabla de `docs/downloads.md` con los valores
reales del artefacto. Reemplaza la fila existente; no acumules filas (el histórico vive en
GitHub Releases y en `dist/CHECKSUMS.txt`).

**Comandos para obtener los valores (doc_ia)**:

```bash
# Versión (desde pyproject.toml)
python -c "import tomllib; f=open('pyproject.toml','rb'); print(tomllib.load(f)['project']['version'])"

# Tamaño del ZIP (PowerShell)
$f = "dist/doc_ia-docs-{version}.zip"; [math]::Round((Get-Item $f).Length/1MB, 1)

# Hash SHA256 (ya en el fichero .sha256)
cat dist/doc_ia-docs-{version}.zip.sha256

# Fecha de generación
(Get-Item dist/doc_ia-docs-{version}.zip).LastWriteTime.ToString("yyyy-MM-dd")
```

---

## Checklist de sincronización

Cuando actualices **`.github/SHARED_INSTRUCTIONS.md`**, verifica:

- [ ] Los entry points (CLAUDE.md, GEMINI.md, copilot-instructions.md, .cursorrules) referencian secciones vigentes
- [ ] No hay duplicación de reglas entre `SHARED_INSTRUCTIONS.md` y especializaciones
- [ ] Rutas de archivos relativas y portables (`./.github/`, no rutas absolutas)
- [ ] Tabla de gobernanza en SHARED_INSTRUCTIONS.md refleja responsabilidad de cada fichero
- [ ] Si cambias slash commands, actualiza la tabla de comandos en este fichero

---

## Comandos útiles referenciados

```bash
python -m ruff check scripts tests   # Linting
python -m ruff format scripts tests  # Formato
python -m mypy scripts               # Type-checking (strict)
python -m pytest                     # Tests
python -m mkdocs build --strict      # Build de documentación
python -m mkdocs serve               # Documentación local
python scripts/check_env.py          # Verificación del entorno (Python + docling + markitdown + plugins + pandoc)
python scripts/build_docs_zip.py     # ZIP offline con SHA256
python scripts/doc_trace.py drift    # Páginas cuyas fuentes de código han cambiado
python scripts/doc_trace.py matrix   # Criterios de aceptación ↔ tests reales
python scripts/doc_trace.py llms     # Regenera docs/llms.txt desde el nav
python scripts/doc_trace.py stamp <página>  # Re-sella las fuentes actuales tras revisar una página
python scripts/doc_trace.py stamp <página> --source <ruta>…  # Primer sellado: --source SUSTITUYE la lista entera
python scripts/convert_to_md.py <ruta>                            # Convierte a Markdown con docling (default) en <ruta>/md/
python scripts/convert_to_md.py <ruta> --engine markitdown        # Convierte con markitdown (sin docling)
python scripts/convert_to_md.py <ruta> --engine pandoc            # Convierte con pandoc (DOC/ODT/RST/TEX)
python scripts/convert_to_md.py <ruta> --validate-only            # Solo validación previa (extensiones, integridad)
python scripts/convert_to_md.py <ruta> --validate-only --engine markitdown  # Validación para motor específico
```

---

*Actualizado: 2026-06-24*
