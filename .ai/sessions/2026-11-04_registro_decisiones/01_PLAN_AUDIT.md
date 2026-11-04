# PLAN + AUDIT_PLAN — Registro de Decisiones de Cobertura (Arquetipo 13)

## PLAN

**Objetivo**: los apartados ⚠️/❌/🔍 (Arq. 8 siempre; Arq. 1/2/12 cuando el destino adopta el
registro) tienen una ficha `COB-<ÁMBITO>-<NNN>` en `docs/decisiones/<ámbito>_decisiones.md`.
El agente rellena el estado; las personas rellenan la decisión. En cada revisión el agente aplica
las decisiones a la página documentada (símbolo + enlace a la ficha) y `doc_trace decisions`
comprueba de forma determinista que todo está reflejado.

### Decisiones de diseño
| ID | Decisión | Elección |
|---|---|---|
| D1 | Ubicación | `docs/decisiones/<ámbito>_decisiones.md` (publicado; nav `Decisiones`) |
| D2 | ID | `COB-<ÁMBITO>-<NNN>`; ÁMBITO `[A-Z0-9]+` = norma (Arq. 8) o módulo (Arq. 1/2/12); nunca se reutiliza |
| D3 | Dónde va el ID en la página documentada | Arq. 8: primera columna `ID`; Arq. 1/2/12: inicio de la celda «Elemento» del bloque Evidencia |
| D4 | Reflejo de una decisión | La fila lleva el ID enlazado a la ficha (`…/decisiones/<f>.md#cob-…`) y su último símbolo = «Estado resultante» (o el texto «No aplica») |
| D5 | Propiedad de los campos | Agente: Página, Estado detectado, Evidencia. Humano: Decisión, Contexto aportado, Responsable, Fecha, Estado resultante |
| D6 | Vocabulario cerrado de decisiones por estado | ✅ Confirmar/Reabrir · ⚠️ Remediar/Aceptar riesgo/Reclasificar · ❌ Implementar/Medida compensatoria/Aceptar riesgo/No aplica · 🔍 Aportar evidencia/Reclasificar/No aplica · todos: Pendiente |
| D7 | Activación | Condicional: con Arq. 8, si ya existe `docs/decisiones/` o si el usuario lo pide. doc_ia no lo adopta en esta sesión (no tiene Arq. 8) |
| D8 | Drift de decisiones | La página documentada declara su registro en `fuentes:`; editar el registro la marca `stale` en `doc_trace drift` |
| D9 | Leyenda | El texto del usuario pasa a ser la leyenda canónica (§3.8); §3.16 remite a ella con su lectura para Arq. 1/2/12 |

### Capas
| Capa | Ficheros |
|---|---|
| L1 Tooling | `scripts/doc_trace.py`: `DecisionEntry`, `CoverageRow`, `DecisionFinding`, `DecisionReport`, `parse_registers`, `collect_coverage_rows`, `check_decisions`, `format_decisions`, subcomando `decisions [--docs] [--output]` (0 / 1) |
| L2 Tests | `tests/test_doc_trace.py`: un test por tipo de hallazgo, bloque de código ignorado, sangría de admonición, «No aplica», CLI 0/1 y `--output` |
| L3 Producto | `DOCUMENTATION_STANDARD.md` (§3.8 leyenda + columna ID, §3.16, nuevo §3.18 Arq. 13, nav, checklist); `.github/prompts/coverage_decisions.prompt.md` (nuevo); `.github/templates/DECISIONES_COBERTURA.template.md` (nuevo); `normative_traceability.prompt.md`; `document_project.prompt.md` + `.claude/commands/document-project.md`; agentes generator/reviewer; `documentation_review.prompt.md`; entry points (CLAUDE.md, SHARED, copilot-instructions, AGENTS.md, INTEGRATION_MAP, docs.instructions, GEMINI.md, .cursorrules) |
| L3 Docs | `docs/{functional,api}/doc_trace.md`, `docs/examples/doc_trace_usage.md`, `docs/{functional,api}/archetypes.md`, `docs/reference/index.md`, `docs/adr/ADR-004-…`, `mkdocs.yml` (ADR), `llms.txt`, re-sellado; `CHANGELOG.md`; `.ai/glossary.md` |

**Tipos**: `DecisionIssue = Literal["duplicate","orphan_ref","orphan_entry","invalid","incomplete","unreflected","mismatch"]`.

### Criterios de aceptación
- AC-01 `decisions` sin registros ni IDs → exit 0 (compatibilidad hacia atrás).
- AC-02 Detecta los 7 tipos de hallazgo; exit 1 si hay alguno.
- AC-03 Las fichas «Pendiente» no son hallazgo; se listan en el informe.
- AC-04 Ignora IDs dentro de bloques de código y dentro de `docs/decisiones/`.
- AC-05 Lee las tablas sangradas del bloque «Evidencia» (admonición).
- AC-06 `mkdocs build --strict` sin avisos; ruff y mypy strict limpios.

## AUDIT_PLAN

### Riesgos funcionales
| ID | Riesgo | Mitigación |
|---|---|---|
| F1 | La regeneración pisa los campos humanos | Regla D5 en estándar, prompt y agentes; la plantilla marca los campos humanos |
| F2 | IDs renumerados al regenerar | D2: IDs nunca se reutilizan ni reordenan; los nuevos toman el siguiente número libre |
| F3 | Una decisión cuyo resultado coincide con el estado detectado («Aceptar riesgo» ⚠️) queda «reflejada» solo con el enlace | Aceptado: el enlace a la ficha es la referencia exigida; el contexto vive en la ficha |
| F4 | Publicar aceptaciones de riesgo en el sitio y el ZIP | Decisión explícita del usuario (D1); se avisa en el estándar |
| F5 | Leyenda divergente entre §3.8 y §3.16 (❌) | D9 |

### Riesgos técnicos (incluye LSP/ISP)
| ID | Riesgo | Mitigación |
|---|---|---|
| T1 | Parseo frágil de Markdown | Formato fijo (encabezado `### COB-…` + tabla Campo/Valor); campos por nombre normalizado; tests |
| T2 | `⚠️` con o sin selector de variación U+FE0F | Normalizar quitando U+FE0F |
| T3 | Anclas `{ #cob-… }` requieren `attr_list` | Ya presente en `mkdocs.yml` y en `TEMPLATE_mkdocs.yml` |
| T4 | LSP/ISP | Sin interfaces ni async; subcomando nuevo, los existentes no cambian de firma ni de salida |
| T5 | Coste del cambio en instrucciones (≈15 ficheros) | Una única fuente (§3.18); el resto remite |

### Riesgos de seguridad
- Lectura local de Markdown, sin red ni ejecución. Las fichas citan ubicaciones, no secretos (§3.16 regla 3).

### Simplificaciones
- Sin campo «Reflejado en»: la verdad es la página documentada y el informe de `decisions`.
- Sin `--strict` para pendientes: las pendientes se informan, no fallan.
- Retro-adopción en la documentación de doc_ia: fuera de alcance (D7); siguiente sesión si se desea.

**Veredicto: GO_CONDICIONAL**
- C1: §3.18 es la única fuente de la regla; prompts, agentes y entry points remiten.
- C2: `decisions` es aditivo (AC-01) y no cambia ningún subcomando existente.
- C3: build `--strict`, ruff, mypy y pytest en verde antes del commit.
