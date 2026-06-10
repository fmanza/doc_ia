# Arquitectura — doc_ia

> Contexto persistente para agentes IA. Regenerado en el bootstrap (2026-06-10)
> desde el árbol real. Describe solo lo que existe.

## Estilo

Proyecto de **tooling plano** (sin librería de negocio, sin `src/`, sin servidor):
scripts deterministas + documentación + sistema de instrucciones IA multiplataforma.

## Árbol real

```text
doc_ia/
  pyproject.toml          # Versión, ruff, mypy strict, pytest
  requirements.txt        # mkdocs-material, ruff, mypy, pytest
  mkdocs.yml              # Config del sitio (Material, idioma es) — fuente única
  README.md
  scripts/
    check_env.py          # Verifica herramientas instaladas (mkdocs, ruff, mypy, pytest)
    build_docs_zip.py     # Build (mkdocs|zensical) + ZIP + SHA256 en dist/
  tests/
    test_check_env.py     # Tests unitarios del tooling
  docs/
    index.md              # Landing (Arquetipo 6, Variante A — pendiente de regenerar)
    downloads.md          # Página de descargas del ZIP offline
    guides/
      codex_guide.md      # Guía de uso de Codex (OpenAI)
  .github/
    SHARED_INSTRUCTIONS.md      # Canónico multiplataforma
    copilot-instructions.md     # Entry point Copilot Chat
    AGENTS.md                   # Registro de agentes
    DOCUMENTATION_STANDARD.md   # Estándar de arquetipos documentales
    INTEGRATION_MAP.md          # Mapa de gobernanza IA
    agents/*.agent.md           # 12 agentes
    prompts/*.prompt.md         # 19 prompts (método + arquetipos + bootstrap)
    instructions/               # python.instructions.md, sync.instructions.md
    workflows/                  # docs-zip-release.yml, docs-release.yml
  .claude/
    settings.json(.example)     # Hooks PostToolUse: ruff, mypy, pytest collect
    commands/*.md               # 8 slash commands
    COMMAND_TEMPLATE.md, EDGE_CASES.md, TESTING_GUIDE.md
  .ai/
    product.md, architecture.md, runtime.md, glossary.md, standards.md
    sessions/TEMPLATE/          # Plantilla de artefactos de sesión
  .vscode/                      # tasks.json (docs build/serve, calidad)
```

## Reglas de dependencia

- `scripts/` no importa nada de `docs/` ni de `.github/`; cada script es standalone.
- `tests/` importa funciones de `scripts/` vía `sys.path` (no hay paquete instalable).
- Los entry points de plataforma (`CLAUDE.md`, `GEMINI.md`, …) dependen del canónico
  `.github/SHARED_INSTRUCTIONS.md`; nunca entre sí.
- Los prompts de arquetipo no dependen de un proyecto concreto: origen/destino son parámetros.

## Flujo runtime típico (documentar un módulo)

```text
Usuario (chat IA) → prompt de arquetipo (.github/prompts/*_doc.prompt.md)
  → lectura del código real del proyecto objetivo
  → generación de docs/<sección>/<página>.md + actualización de mkdocs.yml
  → python -m mkdocs build --strict (validación)
  → opcional: python scripts/build_docs_zip.py (distribución offline)
```

## Decisiones de diseño vigentes

- **MkDocs Material por defecto**; Zensical compatible sobre el mismo `mkdocs.yml`
  (no es dependencia; `--builder zensical` disponible en `build_docs_zip.py`).
- **Sin workflows CI con APIs de IA** (a diferencia del origen del bootstrap): prohibido
  por el principio "sin API keys".
- **`pip + requirements.txt`** como gestión de dependencias (no hay paquete publicable).
