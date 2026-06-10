# doc_ia

Proyecto IA para **documentar cualquier proyecto de desarrollo** mediante instrucciones IA
ejecutadas en los chats de los servicios contratados (Claude Code, Gemini, Copilot Chat,
Cursor, Codex). Los **orígenes a documentar** y el **destino de la documentación** son
parámetros obligatorios de cada ejecución.

## Principios

- **Sin API keys**: ninguna credencial de servicios IA se configura ni se versiona en este proyecto.
- **Sin componentes programáticos IA**: el código Python es exclusivamente tooling determinista
  (build de documentación, ZIP offline, validaciones). Nunca invoca servicios IA.
- **Ejecución en chat**: la generación documental ocurre siempre en el chat de la plataforma IA,
  guiada por las instrucciones de `.github/` y `.claude/`.

## Estado

**Bootstrap de configuración IA completado** (2026-06-10, modelo PULL desde
`util_bbdd`). El sistema multiplataforma está operativo:

- **Canónico**: `.github/SHARED_INSTRUCTIONS.md`
- **Entry points**: `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`,
  `.cursorrules`, `docs/guides/codex_guide.md` (Codex)
- **Método**: 12 agentes (`.github/agents/`), 19 prompts (`.github/prompts/`),
  8 slash commands (`.claude/commands/`)
- **Arquetipos documentales**: 7 formales (`.github/DOCUMENTATION_STANDARD.md`)
- **Contexto IA**: `.ai/{product,architecture,runtime,glossary,standards}.md`
- **Distribución offline**: `scripts/build_docs_zip.py` + workflows de release

Pendiente (dogfooding): generar `docs/` completo con los propios arquetipos
(installation, architecture, functional, api, examples, onboarding, troubleshooting).

## Entorno

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

## Comandos

```bash
python -m ruff check scripts tests   # Linting
python -m ruff format scripts tests  # Formato
python -m mypy scripts               # Type-checking
python -m pytest                     # Tests del tooling
python -m mkdocs build --strict      # Build de documentación
python -m mkdocs serve               # Documentación local
```
