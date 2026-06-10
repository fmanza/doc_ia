# Producto — doc_ia

> Contexto persistente para agentes IA. Regenerado en el bootstrap (2026-06-10)
> analizando el árbol real del proyecto. No describe capacidades no verificadas.

## Qué es

`doc_ia` es un proyecto IA para **documentar cualquier proyecto de desarrollo** mediante
instrucciones IA ejecutadas en los chats de los servicios contratados (Claude Code, Gemini
Code Assist, GitHub Copilot Chat, Cursor, Codex). Los **orígenes a documentar** y el
**destino de la documentación** son parámetros obligatorios de cada ejecución.

## Para quién

- Desarrolladores y equipos que documentan sus proyectos con asistentes IA en chat.
- Mantenedores de doc_ia que evolucionan los arquetipos, agentes y el tooling.

## Principios innegociables

1. **Sin API keys**: ninguna credencial de servicios IA se configura ni se versiona.
2. **Sin componentes programáticos IA**: el código Python es exclusivamente tooling
   determinista (build de documentación, ZIP offline, validaciones). Nunca invoca servicios IA.
3. **Ejecución en chat**: la generación documental ocurre siempre en el chat de la plataforma
   IA, guiada por las instrucciones de `.github/` y `.claude/`.

## Capacidades verificadas (estado actual)

| Capacidad | Soporte | Evidencia |
|---|---|---|
| Arquetipos documentales (7) | ✅ | `.github/prompts/{functional,technical,guide,example,architecture,landing}_doc.prompt.md`, `onboarding_dev.prompt.md` |
| Flujo PLAN→AUDIT_PLAN→IMPLEMENT→AUDIT_CODE→VERSION | ✅ | `.github/agents/` (12), `.claude/commands/` (8) |
| Bootstrap multiplataforma (modelo PULL) | ✅ | `.github/prompts/bootstrap_ai_config.prompt.md` |
| Verificación de entorno | ✅ | `scripts/check_env.py` + `tests/test_check_env.py` |
| ZIP offline de docs con SHA256 | ✅ | `scripts/build_docs_zip.py`, `.github/workflows/docs-zip-release.yml` |
| Sitio de documentación propio | ✅ (mínimo) | `mkdocs.yml` + `docs/` (index, downloads, guides/codex_guide) |
| Documentación de proyectos externos parametrizada | 🔜 Pendiente | objetivo del producto; los arquetipos están listos, falta la guía de invocación parametrizada |

## Plataformas IA activas

Claude Code (`CLAUDE.md`), Gemini (`GEMINI.md`), Copilot Chat
(`.github/copilot-instructions.md`), Cursor (`.cursorrules`), Codex
(`docs/guides/codex_guide.md` — sin fichero de instrucciones propio).

## Versión

`0.1.0` según `pyproject.toml` (verificar antes de cerrar releases).
