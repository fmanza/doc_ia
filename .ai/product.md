# Producto — doc_ia

> Contexto persistente para agentes IA. Actualizado: 2026-06-18.
> No describe capacidades no verificadas.

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
   determinista (build de documentación, ZIP offline, validaciones, conversión de documentos).
   Nunca invoca servicios IA.
3. **Ejecución en chat**: la generación documental ocurre siempre en el chat de la plataforma
   IA, guiada por las instrucciones de `.github/` y `.claude/`.

## Capacidades verificadas (estado actual)

| Capacidad | Soporte | Evidencia |
|---|---|---|
| Arquetipos documentales (11) | ✅ | `.github/prompts/` — 13 prompts de arquetipo: funcional, técnica, how-to (3a), tutorial (3b), ejemplos, ADR/MADR 4.0, landing (4 variantes), onboarding, normativa (condicional), changelog (opt-in), config IA, contribución (opt-in) |
| Flujo PLAN→AUDIT_PLAN→IMPLEMENT→AUDIT_CODE→VERSION | ✅ | `.github/agents/` (12 agentes), `.claude/commands/` (9 slash commands) |
| Documentación de proyectos externos parametrizada | ✅ | `/document-project` con 4 parámetros obligatorios, Fase 0a de clasificación (8 tipos de origen), Fase 0b de sincronización visual, cierre de sesión con `.ai/sessions/` |
| Bootstrap multiplataforma (modelo PULL) | ✅ | `.github/prompts/bootstrap_ai_config.prompt.md` (capas A/B/C/D) |
| Verificación de entorno | ✅ | `scripts/check_env.py` + `tests/test_check_env.py` |
| ZIP offline de docs con SHA256 | ✅ | Mecanismo dual: `scripts/build_docs_zip.py` (script) + `mkdocs_hooks.py` (hook nativo MkDocs); `.github/workflows/docs-zip-release.yml` (CI) |
| Conversión de documentos a Markdown | ✅ | `scripts/convert_to_md.py` — docling por defecto (con OCR); markitdown para XLS y pandoc para DOC/ODT/RST con `--engine`; genera carpeta `md/` como contexto IA |
| Sincronización raíz→docs/ | ✅ | `hooks/sync_root_docs.py` — copia CHANGELOG.md y CONTRIBUTING.md a docs/ automáticamente |
| Servidor offline para ZIP | ✅ | `scripts/start-server.py` — servidor HTTP local incluido en el ZIP offline |
| Sitio de documentación propio (dogfooding) | ✅ | `mkdocs.yml` + `docs/` (33 páginas, 12 arquetipos aplicados al propio proyecto) |
| Orígenes heterogéneos | ✅ | 8 tipos: CÓDIGO, NORMATIVA, ESPECIFICACIÓN, UI/PANTALLAS, REFERENCIA, CONTRATO, INFRAESTRUCTURA, MANUAL |

## Instrucciones IA

25 prompts en `.github/prompts/` (13 de arquetipo + 12 de método/flujo), 12 agentes en
`.github/agents/`, 3 instrucciones en `.github/instructions/`, 9 slash commands en
`.claude/commands/`.

## Plataformas IA activas

Claude Code (`CLAUDE.md`), Gemini (`GEMINI.md`), Copilot Chat
(`.github/copilot-instructions.md`), Cursor (`.cursorrules`), Codex
(`docs/guides/codex_guide.md` — sin fichero de instrucciones propio).

## Versión

`0.2.0` según `pyproject.toml` (verificar antes de cerrar releases).
