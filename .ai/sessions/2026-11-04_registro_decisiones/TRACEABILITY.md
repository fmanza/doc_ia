# TRACEABILITY — 2026-11-04 Registro de Decisiones de Cobertura

## Session metadata
- id: 2026-11-04
- fecha: 2026-11-04
- rama: develop
- skill: new_feature
- fase: OPCIONES + PLAN + AUDIT_PLAN + IMPLEMENT (L1-L3) + AUDIT_CODE + VERSION

## Prompt issued
Leyenda de cobertura (✅ ⚠️ ❌ 🔍) aportada por la persona usuaria; actualizar las instrucciones
para generar un documento Markdown de decisión que revisan y editan personas, y para que las
revisiones lo lean y actualicen la documentación citándolo. «Dame opciones. PLAN y AUDIT_PLAN».
Después: «Adelante, pregunta lo que necesites».

## Context supplied
- `CLAUDE.md`, `DOCUMENTATION_STANDARD.md` §3.8 y §3.16, `normative_traceability.prompt.md`,
  `scripts/doc_trace.py`, `tests/test_doc_trace.py`, `tests/test_docs_conformance.py`.

## AI output summary
- Opciones A (columnas en Arq. 8), B (registro por norma), C (Arquetipo 13 transversal),
  D (tooling). La persona usuaria eligió **C + D**, registro dentro de `docs/`, IDs
  `COB-<ÁMBITO>-<NNN>` y commit directo en `develop`.
- L1: `doc_trace.py decisions` (7 tipos de hallazgo; pendientes informativas; ignora código).
- L2: 15 tests unitarios/CLI en `test_doc_trace.py`; 4 tests de conformidad (12 casos).
- L3: estándar §3.8 (leyenda canónica + columna ID), §3.16, §3.18 nuevo, §4.3, checklist;
  prompt `coverage_decisions` y plantilla; prompt normativo, flujo `/document-project`, agentes,
  prompt de revisión, entry points; docs de `doc_trace`, arquetipos, `document_project`,
  referencia, mapa funcional (total corregido), ejemplo con salida real; ADR-004; CHANGELOG.
- 11 páginas revisadas y re-selladas; `llms.txt` regenerado.

## Artefactos generados
| Artefacto | Ruta | Estado |
|---|---|---|
| PLAN + AUDIT_PLAN | `.ai/sessions/2026-11-04_registro_decisiones/01_PLAN_AUDIT.md` | emitido |
| AUDIT_CODE + VERSION | `.ai/sessions/2026-11-04_registro_decisiones/02_AUDIT_VERSION.md` | emitido |
| Tooling | `scripts/doc_trace.py` | modificado |
| Tests | `tests/test_doc_trace.py`, `tests/test_docs_conformance.py` | modificado |
| Producto | `.github/prompts/coverage_decisions.prompt.md`, `.github/templates/DECISIONES_COBERTURA.template.md` | nuevo |
| Producto | estándar, prompts, comando, agentes, entry points | modificado |
| Docs | `docs/adr/ADR-004-registro-decisiones-cobertura.md` | nuevo |
| Docs | 13 páginas + `mkdocs.yml` + `llms.txt` + CHANGELOG | modificado |

## Directrices para Futuras IAs
- **[decisions]**: los IDs `COB-…` escritos entre comillas invertidas o en bloques de código no
  cuentan; úsalos así al documentar el formato en doc_ia, o `test_doc_ia_coverage_decisions_are_consistent`
  fallará con `orphan_ref`.
- **[decisions]**: una fila cuenta como cobertura solo si es fila de tabla con símbolo de la
  leyenda o «No aplica»; el estado es el **último** símbolo de la fila.
- **[Arquetipo 13]**: el agente nunca escribe Decisión, Contexto aportado, Responsable, Fecha ni
  Estado resultante. Si el código contradice una decisión, se informa; no se cambia.
- **[bash heredoc]**: en esta máquina, heredocs largos con comillas o acentos fallan en el tool
  Bash («unexpected EOF»); escribir el script con Write en el scratchpad y ejecutarlo.
- **[mapa funcional]**: el total de §1 debe ser la suma de las filas (= `doc_trace matrix`).

## Veredicto final
CLOSED
