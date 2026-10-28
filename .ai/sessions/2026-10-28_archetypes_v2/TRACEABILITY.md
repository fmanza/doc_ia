# TRACEABILITY

## Session metadata
- id: 2026-10-28
- fecha: 2026-10-28
- rama: develop
- skill: new_feature
- fase: PLAN + AUDIT_PLAN (P1/P2/P3) + IMPLEMENT P1 + AUDIT_CODE P1

## Prompt issued
"Analizar si se puede o se recomienda actualizar los arquetipos actuales, el objetivo es obtener
la máxima información funcional y técnica sobre el repositorio de código…" → "PLAN y AUDIT_PLAN
con lo propuesto" → "Adelante con las dos opciones" (guardar sesión + IMPLEMENT P1).

## Context supplied
- `.github/DOCUMENTATION_STANDARD.md`, prompts de arquetipo, agentes de documentación
- Búsqueda web: arc42, Diátaxis, llms.txt, AGENTS.md, Reversa 2026, traceability-check

## AI output summary
- Análisis de huecos y propuesta priorizada P1/P2/P3 (chat).
- `01_PLAN.md` y `02_AUDIT_PLAN.md` emitidos; veredicto GO_CONDICIONAL; S1–S4 aceptadas.
- IMPLEMENT P1 (ver `03_IMPLEMENT_P1.md`): 31 ficheros modificados, 4 nuevos.
- Verificación: `python -m mkdocs build --strict` OK; bloque "Evidencia" renderizado como
  `<details>` con tabla (19 filas); `ruff` OK; `pytest` 76 OK. Sin cambios en código Python.

## AUDIT_CODE (P1)
- **Bugs**: un heredoc convirtió `\n` de etiquetas Mermaid en saltos reales en
  `docs/functional/archetypes.md` (nodos Q12/A12); detectado y corregido antes del build.
- **Edge cases**: tablas dentro de admonition plegable verificadas en HTML; `Edit\|Write`
  escapado en tablas.
- **Hallazgos colaterales (no corregidos, fuera de alcance)**:
  - `scripts/convert_to_md.py`: el módulo fija `CUDA_VISIBLE_DEVICES=""` al importarse, por lo
    que `--device auto` siempre resuelve a CPU salvo valor previo no vacío. Candidato `/hotfix`.
  - `.claude/settings.json.example` no incluye el hook `sync_root_docs.py` que `CLAUDE.md`
    describe como primer PostToolUse.
  - `mkdocs.yml::site_url` apunta a GitHub Pages pero ningún workflow publica en Pages.
  - mypy: 11 errores preexistentes en `convert_to_md.py` por docling no instalado.
  - `DOCUMENTATION_STANDARD.md` §4.2 (nav "implementación actual") está desactualizado.
- **Deuda técnica**: 7 páginas funcionales con estructura v1 (migración en P2); páginas de
  Arq. 1/2 existentes sin bloque "Evidencia" (se añade al migrar en P2).

## Artefactos generados

| Artefacto | Ruta | Estado |
|---|---|---|
| REQUEST | `.ai/sessions/2026-10-28_archetypes_v2/00_REQUEST.md` | emitido |
| CONTEXT_SNAPSHOT | `.ai/sessions/2026-10-28_archetypes_v2/00_CONTEXT_SNAPSHOT.md` | emitido |
| PLAN | `.ai/sessions/2026-10-28_archetypes_v2/01_PLAN.md` | emitido |
| AUDIT_PLAN | `.ai/sessions/2026-10-28_archetypes_v2/02_AUDIT_PLAN.md` | emitido |
| IMPLEMENT P1 | `.ai/sessions/2026-10-28_archetypes_v2/03_IMPLEMENT_P1.md` | completado |
| Prompt Arq. 12 | `.github/prompts/reference_doc.prompt.md` | nuevo |
| Referencia doc_ia | `docs/reference/index.md` | nuevo |
| ADR-002 | `docs/adr/ADR-002-arquetipos-con-evidencia.md` | nuevo |

## Directrices para Futuras IAs
- **[arquetipos]**: el bloque "Evidencia" va al final, plegable (`??? note "Evidencia"`) y SIN
  número de sección; añadirlo nunca renumera.
- **[arquetipos]**: las citas de evidencia son código inline `ruta::símbolo`; un enlace Markdown a
  código fuera de `docs/` rompe `mkdocs build --strict`.
- **[Arq. 2]**: doc_ia no tiene mkdocstrings; no emitir directivas `:::` en `docs/api/`.
- **[Arq. 1]**: las páginas `docs/functional/` de doc_ia siguen la estructura v1 (5 secciones)
  hasta P2; no tratarlas como incumplimiento crítico antes de esa migración.
- **[tooling]**: en ediciones vía heredoc de Bash, `\n` dentro de cadenas Python se convierte en
  salto real; para etiquetas Mermaid con `\n` literal usar Edit o un script en el scratchpad.

## Veredicto final
Veredicto: GO (P1)
Pendientes al cierre:
- Commit de P1 (pendiente de confirmación del usuario).
- P2 y P3 según `01_PLAN.md`.
