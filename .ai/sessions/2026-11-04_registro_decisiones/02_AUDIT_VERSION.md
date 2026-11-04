# AUDIT_CODE + VERSION — Registro de Decisiones de Cobertura

## AUDIT_CODE

| Área | Hallazgo | Severidad | Estado |
|---|---|---|---|
| Bugs | Una ficha inválida o incompleta no se comprueba contra la página: evita hallazgos encadenados (una decisión mal escrita no produce además `unreflected`) | — | Diseño intencionado; documentado en `docs/api/doc_trace.md` §2 |
| Edge cases | `⚠` con y sin U+FE0F; IDs en bloques de código y código en línea; tablas sangradas de admonición; transición `🔍 → ✅`; «No aplica» | — | Cubiertos por tests |
| Edge cases | Una fila de «Resumen de gaps» (Arq. 8 §N) que cita el ID sin símbolo cuenta como mención, no como cobertura: no se exige reflejo | Baja | Aceptado; la regla de §3.18 pide retirar el gap al cerrarlo |
| Edge cases | Una decisión que mantiene el estado («Aceptar riesgo» sobre ⚠️) cuenta como reflejada en cuanto la fila enlaza la ficha | Baja | Riesgo aceptado en ADR-004 |
| Performance | Cruce entradas × filas O(n·m); registros de decenas o cientos de fichas | — | Sin impacto |
| Seguridad | Solo lectura de `docs/**/*.md`; sin red, sin ejecución, sin escritura en registros | — | OK |
| Tipado | mypy strict sin errores; `DecisionIssue` como `Literal`; dataclasses congeladas | — | OK |
| Deuda técnica | `_reflection_problem` usa `entry.result or '✅'` solo para el tipo (el resultado ya está validado) | Baja | Aceptado |
| Deuda técnica | El bootstrap (`bootstrap_ai_config.prompt.md`, Capa A) no enumera `.github/templates/`; ya afectaba a `VER_DOCUMENTACION.template.md` | Media | Preexistente; fuera de alcance (prohibido refactorizar). Propuesta para otra sesión |
| Deuda técnica | La documentación de doc_ia no adopta el registro (22 filas ⚠️/🔍 sin ficha) | Media | Decisión D7; siguiente sesión si se desea |

**Verificación**: ruff + format OK · mypy strict OK · pytest 290 passed · `mkdocs build --strict`
OK · `doc_trace drift` / `matrix` / `llms --check` / `decisions` con código 0 · ejemplo ejecutado
· salida de `decisions` del ejemplo obtenida de una ejecución real sobre un destino de prueba.

**Veredicto**: GO. Condiciones C1–C3 del AUDIT_PLAN cumplidas.

## VERSION

**Commit**: `feat(docs): arquetipo 13 registro de decisiones de cobertura y doc_trace decisions`

**Changelog** (`[Unreleased]`): Added — Arquetipo 13 y `doc_trace.py decisions`; Changed —
leyenda canónica, columna `ID` del Arquetipo 8, total del mapa funcional.

**Impacto en API pública**: aditivo. Nuevo subcomando `decisions [--docs] [--output]` (códigos
0/1); nuevos símbolos públicos en `scripts/doc_trace.py` (`DecisionEntry`, `CoverageRow`,
`DecisionFinding`, `DecisionReport`, `parse_registers`, `collect_coverage_rows`,
`check_decisions`, `format_decisions`). Ningún subcomando existente cambia de firma ni de salida.
Versión sugerida al publicar: minor (0.5.0).

**Rollback**: `git revert <commit>`; no hay datos migrados ni estado persistente nuevo.

**Pruebas sugeridas** (manuales, en un destino real con Arquetipo 8):
1. `/document-project` genera `docs/decisiones/<norma>_decisiones.md` con fichas `Pendiente`.
2. Una persona decide dos fichas; la siguiente ejecución las aplica sin tocar los campos de
   persona y `doc_trace decisions` termina con 0.
3. `mkdocs build --strict` resuelve las anclas `#cob-…` del registro.
