# Arquitectura — doc_ia

> Contexto persistente para agentes IA. Actualizado: 2026-06-18.
> Describe solo lo que existe.

## Estilo

Proyecto de **tooling plano** (sin librería de negocio, sin `src/`, sin servidor):
scripts deterministas + documentación + sistema de instrucciones IA multiplataforma.

## Árbol real

```text
doc_ia/
  pyproject.toml          # Versión, ruff, mypy strict, pytest
  requirements.txt        # mkdocs-material, ruff, mypy, pytest
  mkdocs.yml              # Config del sitio (Material, idioma es) — fuente única
  mkdocs_hooks.py         # Hook MkDocs: genera ZIP offline en site/ en cada build
  README.md
  CHANGELOG.md            # Fuente de verdad → docs/changelog.md (sync automático)
  CONTRIBUTING.md         # Fuente de verdad → docs/contributing.md (sync automático)
  scripts/
    check_env.py          # Verifica herramientas instaladas (mkdocs, ruff, mypy, pytest, markitdown, pandoc)
    build_docs_zip.py     # Build (mkdocs|zensical) + ZIP + SHA256 en dist/
    convert_to_md.py      # Convierte documentos binarios a Markdown (PDF→markitdown, DOCX/PPTX/…→pandoc)
    start-server.py       # Servidor HTTP local para navegación offline (incluido en el ZIP)
  hooks/
    sync_root_docs.py     # Copia CHANGELOG.md y CONTRIBUTING.md a docs/ (hook MkDocs + PostToolUse)
  tests/
    test_check_env.py     # Tests unitarios del tooling
  docs/                   # Sitio MkDocs Material (31 páginas, 11 arquetipos aplicados — dogfooding)
    functional/           # Arquetipos 1 — 7 páginas funcionales
    api/                  # Arquetipos 2 — 6 páginas técnicas
    examples/             # Arquetipos 4 — 6 páginas de ejemplos
    guides/               # Arquetipos 3a/7 — onboarding, troubleshooting, guías de plataforma
    ai-config/            # Arquetipo 10 — configuración de Claude Code
    adr/                  # Arquetipo 5 — ADR-001 (MADR 4.0)
    assets/css/           # nav.css, mermaid.css
    assets/js/            # mermaid.js, sidebar-toggle.js
  .github/
    SHARED_INSTRUCTIONS.md      # Canónico multiplataforma
    copilot-instructions.md     # Entry point Copilot Chat
    AGENTS.md                   # Registro de agentes
    DOCUMENTATION_STANDARD.md   # Estándar de 11 arquetipos documentales
    INTEGRATION_MAP.md          # Mapa de gobernanza IA
    agents/*.agent.md           # 12 agentes
    prompts/*.prompt.md         # 25 prompts (12 de método + 13 de arquetipo)
    instructions/               # python.instructions.md, docs.instructions.md, sync.instructions.md
    workflows/                  # docs-zip-release.yml, docs-release.yml
  .claude/
    settings.json(.example)     # Hooks PostToolUse: sync_root_docs, ruff, mypy, pytest collect
    commands/*.md               # 9 slash commands
    COMMAND_TEMPLATE.md, EDGE_CASES.md, TESTING_GUIDE.md
  .ai/
    product.md, architecture.md, runtime.md, glossary.md, standards.md
    sessions/TEMPLATE/          # Plantilla canónica de artefactos de sesión
    sessions/INDEX.md           # Registro de sesiones completadas
  .vscode/                      # tasks.json (docs build/serve, calidad)
```

## Reglas de dependencia

- `scripts/` no importa nada de `docs/` ni de `.github/`; cada script es standalone.
- `hooks/` no importa de `scripts/`; `sync_root_docs.py` opera solo con `pathlib`/`shutil`.
- `mkdocs_hooks.py` es independiente de `scripts/build_docs_zip.py` (mecanismo dual complementario).
- `tests/` importa funciones de `scripts/` vía `sys.path` (no hay paquete instalable).
- Los entry points de plataforma (`CLAUDE.md`, `GEMINI.md`, …) dependen del canónico
  `.github/SHARED_INSTRUCTIONS.md`; nunca entre sí.
- Los prompts de arquetipo no dependen de un proyecto concreto: origen/destino son parámetros.

## Flujo runtime típico (documentar un proyecto)

```text
Usuario (chat IA) → /document-project (o document_project.prompt.md)
  → VALIDACIÓN de 4 parámetros obligatorios
  → Fase 0a: clasificación de orígenes (si ≥2 o no CÓDIGO)
  → Fase 0b: sincronización visual (assets, mkdocs.yml, .gitignore)
  → Fase 1: inventario (estado A/B/C) + detección señales ZIP offline
  → Fases 2-4: generación por arquetipos (funcional → técnica → ejemplos/guías)
  → Fase 5: sincronización de mkdocs.yml
  → Fase 6: revisión (Markdown, enlaces, Mermaid)
  → Fase 7: build estricto (opt-in) + downloads.md
  → Cierre: .ai/sessions/YYYY-MM-DD/ + commit docs(<scope>):
```

## Decisiones de diseño vigentes

- **MkDocs Material por defecto**; Zensical compatible sobre el mismo `mkdocs.yml`
  (no es dependencia; `--builder zensical` disponible en `build_docs_zip.py`).
- **Hook MkDocs nativo** (`mkdocs_hooks.py`) para ZIP automático en cada build; sin
  instalación (no requiere `pyproject.toml` ni `pip install -e .`).
- **Sin workflows CI con APIs de IA**: prohibido por el principio "sin API keys".
- **`pip + requirements.txt`** como gestión de dependencias (no hay paquete publicable).
- **Sincronización automática raíz→docs/**: `CHANGELOG.md` y `CONTRIBUTING.md` se copian
  a `docs/` vía `hooks/sync_root_docs.py` (hook MkDocs + PostToolUse).
