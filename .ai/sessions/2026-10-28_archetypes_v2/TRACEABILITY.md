# TRACEABILITY

## Session metadata
- id: 2026-10-28
- fecha: 2026-10-28
- rama: develop
- skill: new_feature
- fase: PLAN + AUDIT_PLAN (P1/P2/P3) + IMPLEMENT P1 + AUDIT_CODE P1 + IMPLEMENT P2 + AUDIT_CODE P2 + IMPLEMENT P3 + AUDIT_CODE P3

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

## P2 (tras commit 51b6b57 de P1)
- Norma/prompts: roles condicionales, columna `Test`, Variante 1-I, Arq. 2 §6, Arq. 12 §6.
- Dogfooding con 3 forks en paralelo (ficheros disjuntos): 7 funcionales, 6 técnicas; el hilo
  principal hizo `docs/reference/` §6, Mapa Funcional, nav y la renumeración v2 en la orquestación.
- Verificación independiente: 25/25 tests citados existen; build estricto, ruff y pytest OK.

## P3 (tras commits 4c03178 de P2 y 16f9f4b del hotfix)
- `scripts/doc_trace.py` + 20 tests; frontmatter de trazabilidad en 17 páginas; `docs/llms.txt`.
- Detalle y hallazgos corregidos en `05_IMPLEMENT_P3.md`.

## AUDIT_CODE (P3)
- **Bugs corregidos**: cascada de drift en fuentes `.md`; `UnicodeEncodeError` en consola cp1252;
  trazas no controladas en `stamp`/`llms`.
- **Edge cases**: `--date` omitido → fecha del día (sello no determinista entre días, ⚠️ documentado);
  cambios triviales en fuentes alteran la huella (EDGE_CASES.md).
- **Seguridad**: rutas del frontmatter resueltas y limitadas a la raíz (`outside_repo`, sin lectura).
- **Tipado**: `mypy --strict` limpio en `doc_trace.py`; yaml sin stubs aislado en `_load_yaml`.
- **Deuda**: sin paso en CI (opcional en el PLAN); 37/66 criterios sin test (flujos IA y ZIP).

## AUDIT_CODE (P2)
- **Hechos falsos corregidos por los forks** en páginas existentes: ruta de chunks (`chunks/<doc>/`
  junto al `.md`, no `md/chunks/`); `check_env` emite avisos además de la línea de estado;
  `mkdocs_hooks.py::on_post_build` regenera el ZIP latest aunque `--strict` aborte (⚠️);
  bootstrap exige 8 parámetros, no 4/5; capa D "credenciales" → "caches".
- **Hallazgos colaterales (no corregidos)**:
  - "Fase 0b" significa cosas distintas en `document_project.prompt.md` (conversión `md/`) y en
    `.claude/commands/document-project.md` / `CLAUDE.md` (sincronización visual).
  - `bootstrap_ai_config.prompt.md` cita `docs/codex_guide.md` (real: `docs/guides/codex_guide.md`)
    y su lista de prompts de Capa B omite `ai_config_doc`, `reference_doc` y `normative_traceability`.
  - `convert_to_md`: docling incluye `.md` en sus extensiones; `.md` del origen fuera de `md/` se
    recogen como convertibles (por verificar).
  - Cobertura: 15/52 criterios con test; `build_docs_zip.py` sin tests.

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
- **[Arq. 1]**: desde P2 todas las páginas `docs/functional/` de doc_ia siguen la estructura v2
  (8 secciones + columna `Test` + Evidencia); una página v1 nueva ya es incumplimiento.
- **[trazabilidad]**: para validar la columna `Test`, extraer los ids con `def test_` de `tests/`;
  `pytest --collect-only -q` en este repo solo imprime recuentos por fichero.
- **[tooling]**: en ediciones vía heredoc de Bash, `\n` dentro de cadenas Python se convierte en
  salto real; para etiquetas Mermaid con `\n` literal usar Edit o un script en el scratchpad.

## Veredicto final
Veredicto: CLOSED — P1 (51b6b57) · P2 (4c03178) · P3 (este commit)
Pendientes al cierre:
- Opcional: añadir `doc_trace.py drift` / `matrix` / `llms --check` a `.github/workflows/`.
- Hallazgos colaterales de P2 (Fase 0b, ruta y lista de prompts en `bootstrap_ai_config`, `.md` en docling).
