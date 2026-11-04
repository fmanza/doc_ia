# PLAN + AUDIT_PLAN — Pendientes de 2026-11-04 (registro de decisiones)

Origen: `02_AUDIT_VERSION.md` de `2026-11-04_registro_decisiones` (dos deudas técnicas Media).

## P1 — El bootstrap no copia `.github/templates/` (fix, pequeño)

**Problema verificado**: la Capa A de `bootstrap_ai_config.prompt.md` copia `.github/prompts/`
verbatim, pero no `.github/templates/`. Los prompts copiados la referencian:
`coverage_decisions.prompt.md` (`DECISIONES_COBERTURA.template.md`) y `document-project.md`
(`VER_DOCUMENTACION.template.md`). En el destino, esas rutas no existen.

| Fichero | Cambio |
|---|---|
| `.github/prompts/bootstrap_ai_config.prompt.md` | Fila `.github/templates/` → verbatim en la tabla de dirección y en la lista de Capa A |
| `CLAUDE.md` (tabla de capas del bootstrap) | Añadir `.github/templates/` a la Capa A |
| `docs/{functional,api}/bootstrap.md` | Capa A con plantillas; criterio nuevo AC-05 |
| `tests/test_docs_conformance.py` | `test_bootstrap_copies_every_referenced_template`: cada `.github/templates/<f>` citado en `.github/prompts/` o `.claude/commands/` existe y la Capa A incluye `.github/templates/` |
| `CHANGELOG.md` | `Fixed` |

## P2 — doc_ia adopta su propio registro de decisiones (dogfooding del Arquetipo 13)

**Inventario verificado** (filas de tabla con ⚠️/❌/🔍 como último símbolo, fuera de código):
30 filas en 13 páginas → 9 ámbitos.

| Ámbito | Páginas | Filas |
|---|---|---|
| `ARCHETYPES` | `api/archetypes.md`, `functional/archetypes.md` | 2 |
| `BOOTSTRAP` | `api/bootstrap.md`, `functional/bootstrap.md` | 5 |
| `BUILDZIP` | `api/build_docs_zip.md`, `functional/build_docs_zip.md` | 5 |
| `CHECKENV` | `functional/check_env.md` | 4 |
| `CONVERT` | `functional/convert_to_md.md` | 2 |
| `DOCTRACE` | `functional/doc_trace.md` | 1 |
| `DOCPROJ` | `functional/document_project.md` | 5 |
| `ORIGINS` | `functional/origin_types.md` | 4 |
| `SISTEMA` | `architecture.md` (6C), `functional/index.md` (1-I) | 2 |

Además hay 6 marcas en prosa (cuerpo de Arq. 1/2) que repiten una fila de Evidencia; no llevan
ID (§3.16) y se actualizan al aplicar la decisión de su fila.

**Fases** (las decisiones las toma la persona usuaria, no el agente):
1. **Generación** (esta sesión): 9 registros desde la plantilla, 30 fichas `Pendiente` con
   «Evidencia» precisa (qué falta: test, prueba manual, fuente externa); ID enlazado en cada fila;
   registro añadido a `fuentes:` de cada página (sellado con todas las fuentes actuales + el
   registro, porque `--source` sustituye la lista); nav «Decisiones»; `llms.txt`.
2. **Decisión** (persona usuaria): rellena las fichas.
3. **Aplicación** (sesión posterior): modo aplicación; las fichas «Remediar» con tests o código
   pendientes se ejecutan como `/new-feature` o `/hotfix` aparte.

| Fichero | Cambio |
|---|---|
| `docs/decisiones/*_decisiones.md` (9, nuevos) | Registros con frontmatter `arquetipo: "13"` |
| 13 páginas del inventario | ID enlazado en la celda «Elemento» (Evidencia) o primera celda (tablas de cuerpo); re-sellado |
| `mkdocs.yml`, `docs/llms.txt` | Sección `Decisiones` tras `Funcional` |
| `.github/DOCUMENTATION_STANDARD.md` §3.18 | Nota «Este proyecto (doc_ia)»: adoptado |
| `docs/adr/ADR-004-…` | Estado y Revisión: deuda cerrada |
| `tests/test_docs_conformance.py` | `test_unverified_evidence_rows_have_coverage_id`: toda fila ⚠️/❌/🔍 de un bloque Evidencia de doc_ia lleva ID `COB-…` |
| `.ai/glossary.md` (Dogfooding: 13 arquetipos), `CHANGELOG.md` | Actualizar |

## AUDIT_PLAN

### Riesgos funcionales
| ID | Riesgo | Mitigación |
|---|---|---|
| F1 | El agente rellena por error un campo de persona | Las 30 fichas salen con `—`; `decisions` lista 30 pendientes; revisión del diff |
| F2 | Las marcas en prosa divergen de la fila tras aplicar una decisión | Regla en el prompt (ya existe «en todas las filas»); se amplía a «y sus marcas en el cuerpo»; revisión manual |
| F3 | Muchas fichas «Remediar» que en realidad son tests pendientes | Es el resultado esperado: el registro hace visible la deuda de tests y la prioriza la persona usuaria |
| F4 | P1: copiar `TEMPLATE_mkdocs.yml` a un destino que no publica docs | Inocuo (solo plantilla); se indica igual que `DOCUMENTATION_STANDARD.md` (Capa B condicional) |

### Riesgos técnicos (incluye LSP/ISP)
| ID | Riesgo | Mitigación |
|---|---|---|
| T1 | `stamp --source` sustituye la lista: perder fuentes al añadir el registro | Script de un solo uso que lee `read_page_meta` y pasa fuentes actuales + registro; `drift` y diff de frontmatter |
| T2 | El prefijo de ID en la celda «Elemento» rompe `matrix` | `AC_ROW_RE` solo casa filas de §7 sin sangría; las de Evidencia van sangradas → sin efecto (verificar con `matrix` antes/después: 74/100) |
| T3 | Las tablas de cuerpo (`api/bootstrap.md` §2, `architecture.md`, `document_project.md` §5) tienen el estado en otra columna | El ID va en la primera celda; `decisions` toma el último símbolo de la fila |
| T4 | Anclas `{ #cob-… }` en el build | `mkdocs build --strict` + comprobar en `site/` que existen los `id` |
| T5 | LSP/ISP | Sin cambios de código en `scripts/` (solo tests y docs) |

### Riesgos de seguridad
- El registro se publica (decisión de ADR-004). Las fichas de doc_ia solo citan rutas del repo.

### Simplificaciones
- P1 y P2 en commits separados (P1 es un `fix`, P2 `docs`).
- Un registro por ámbito → 9 ficheros. Alternativa: un único ámbito `DOCIA` (1 fichero, 30
  fichas), que contradice «un registro por módulo» de §3.18 y exigiría cambiar el estándar.

**Veredicto: GO_CONDICIONAL**
- C1: la persona usuaria confirma la granularidad (9 registros por módulo o uno `DOCIA`).
- C2: `matrix` sigue en 74/100 y `drift`, `decisions` (30 pendientes, 0 hallazgos), ruff, mypy,
  pytest y `mkdocs build --strict` en verde antes de cada commit.
- C3: ningún campo de persona rellenado por el agente.
