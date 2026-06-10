# TRACEABILITY

## Session metadata
- id: 2026-06-10
- fecha: 2026-06-10
- rama: main
- skill: new_feature (bootstrap_ai_config)
- fase: ANÁLISIS + PLAN + AUDIT_PLAN + IMPLEMENT + AUDIT_CODE + VERSION

## Prompt issued
"Lee y aplica .github/prompts/bootstrap_ai_config.prompt.md — Origen: c:\Desarrollo\python\libs\util_bbdd
— Destino: C:\Desarrollo\Proyectos\doc_ia — Python tooling — 5 plataformas — Zensical/MkDocs Material — Fase: completa"

## Context supplied
- Árbol y ficheros reales del destino (Fase 0) y del origen (solo lectura)
- `.github/prompts/bootstrap_ai_config.prompt.md` (clasificación A/B/C/D, matriz de equivalencias)

## AI output summary
- ANÁLISIS: clasificación A/B/C/D + matriz de equivalencias (src→scripts, zensical→mkdocs default).
- Capa A: copiados 12 agentes, 18 prompts, 8 commands, COMMAND_TEMPLATE, sessions/TEMPLATE;
  barrido mecánico de comandos embebidos + parches contextuales de ejemplos.
- Capa B: reescritos SHARED_INSTRUCTIONS, CLAUDE.md, GEMINI.md, copilot-instructions, .cursorrules,
  AGENTS.md, sync.instructions, DOCUMENTATION_STANDARD (parcheado), 7 arquetipos (bloques de dominio),
  codex_guide, downloads.md, build_docs_zip.py (prefijo doc_ia, builder mkdocs), 2 workflows de docs.
- Capa C: regenerados .ai/{product,architecture,runtime,glossary,standards}.md,
  python.instructions.md, INTEGRATION_MAP.md desde el árbol real.
- Capa D: excluidos sesiones fechadas, CHANGELOG/COMPATIBILITY, caches, settings.local.json,
  doc_agents.yml + generate_docs.py (usan API keys — prohibido en doc_ia).
- Integración: mkdocs.yml (nav: Guías/Codex + Descargas), README (estado), EDGE_CASES/TESTING_GUIDE plantilla.
- AUDIT_CODE: grep de huérfanas (restos solo intencionales), ruff=0, mypy=0, pytest=0 (2 passed),
  mkdocs build --strict=0, smoke test ZIP → dist/doc_ia-docs-0.1.0.zip + SHA256. Veredicto: APROBADO.

## Artefactos generados

| Artefacto | Ruta | Estado |
|---|---|---|
| Canónico | .github/SHARED_INSTRUCTIONS.md | reescrito |
| Entry points | CLAUDE.md, GEMINI.md, .github/copilot-instructions.md, .cursorrules, docs/guides/codex_guide.md | reescritos |
| Método | .github/agents/ (12), .github/prompts/ (19), .claude/commands/ (8), .claude/COMMAND_TEMPLATE.md | copiados + adaptados |
| Contexto | .ai/{product,architecture,runtime,glossary,standards}.md | regenerados |
| Gobernanza | .github/AGENTS.md, .github/INTEGRATION_MAP.md, .github/DOCUMENTATION_STANDARD.md | reescritos/adaptados |
| Tooling | scripts/build_docs_zip.py, .github/workflows/docs-zip-release.yml, docs-release.yml | adaptados |
| Docs | docs/downloads.md, docs/guides/codex_guide.md, mkdocs.yml (nav) | creados/actualizados |

## Directrices para Futuras IAs
- **[gobernanza]**: `.github/SHARED_INSTRUCTIONS.md` es el canónico; los entry points (CLAUDE.md,
  GEMINI.md, copilot-instructions.md, .cursorrules) solo especializan — editar el canónico primero.
- **[builder]**: MkDocs Material es el builder por defecto en doc_ia (no Zensical, a diferencia
  del origen util_bbdd); `scripts/build_docs_zip.py --builder zensical` existe pero Zensical no es dependencia.
- **[principio-producto]**: prohibido añadir workflows o código que invoque APIs de IA
  (doc_agents.yml del origen se excluyó deliberadamente por esto).
- **[arquetipos]**: los prompts `*_doc.prompt.md` tienen un único bloque editable
  ("Especialización de dominio"); el resto es núcleo compartido entre proyectos — no modificarlo.
- **[tests]**: los tests importan scripts vía `sys.path.insert` hacia `scripts/` (no hay paquete
  instalable); patrón en tests/test_check_env.py.
- **[bootstrap]**: las menciones a util_bbdd que permanecen en bootstrap_ai_config.prompt.md,
  README (Estado) e INTEGRATION_MAP §5 son intencionales (documentan el origen); no "corregirlas".
- **[pendiente]**: dogfooding de docs/ (installation, architecture, functional, api, examples,
  onboarding_dev, troubleshooting) — generar con los propios arquetipos en sesiones futuras.

## Veredicto final
Veredicto: CLOSED
Pendientes al cierre:
- Generar el sitio docs/ completo con los arquetipos propios (dogfooding).
- Crear CHANGELOG.md en la primera versión que cierre con cambios funcionales.
