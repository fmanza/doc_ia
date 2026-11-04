# TRACEABILITY — 2026-11-04b Pendientes del registro de decisiones

## Session metadata
- id: 2026-11-04b
- fecha: 2026-11-04
- rama: develop
- skill: new_feature (P2) + fix (P1)
- fase: PLAN + AUDIT_PLAN + IMPLEMENT + verificación

## Prompt issued
«PLAN y AUDIT_PLAN de lo pendiente» → «IMPLEMENT con tus recomendaciones, pregunta lo que
necesites». Recomendaciones aplicadas: 9 registros por módulo; P1 y P2 en commits separados.

## AI output summary
- **P1** (`aca7ffa`, `fix(bootstrap)`): `.github/templates/` en la Capa A del bootstrap y en
  `CLAUDE.md`; `test_bootstrap_copies_every_referenced_template`; AC-05 del bootstrap; mapa
  funcional 75/101.
- **P2** (`docs`): 9 registros `docs/decisiones/*_decisiones.md`, 28 fichas `Pendiente` para 30
  filas (dos hechos compartidos entre la página funcional y la técnica: `COB-BUILDZIP-002`,
  `COB-BOOTSTRAP-004`); ID enlazado en cada fila; registro añadido a `fuentes:` de 13 páginas
  (`architecture.md` recibe frontmatter `arquetipo: "6C"` con el registro como única fuente);
  nav «Decisiones de Cobertura»; `test_unverified_evidence_rows_have_coverage_id` (27 filas de
  Evidencia comprobadas); regla de marcas en el cuerpo en §3.18 y en `coverage_decisions`;
  §3.18 (nota doc_ia), ADR-004, glosario, ejemplo, CHANGELOG.
- Verificación: ruff, mypy strict, pytest 301 passed, `mkdocs build --strict`, `drift` 0,
  `matrix` 75/101, `llms --check`, `decisions` 28 pendientes / 0 hallazgos, 28 anclas `id="cob-…"`
  en `site/decisiones/` y enlaces correctos desde las páginas.
- Ningún campo de persona rellenado: todas las fichas en `Pendiente` con `—`.

## Artefactos generados
| Artefacto | Ruta | Estado |
|---|---|---|
| PLAN + AUDIT_PLAN | `.ai/sessions/2026-11-04b_pendientes_registro/01_PLAN_AUDIT.md` | emitido |
| Registros | `docs/decisiones/*_decisiones.md` (9) | nuevo |
| Tests | `tests/test_docs_conformance.py` | modificado |
| Docs | 13 páginas con IDs + 5 páginas re-selladas, `mkdocs.yml`, `llms.txt` | modificado |

## Directrices para Futuras IAs
- **[decisiones de doc_ia]**: las 28 fichas esperan la decisión de la persona usuaria. La
  siguiente sesión es el **modo aplicación** de `coverage_decisions.prompt.md`; las fichas
  «Remediar» con tests o código pendientes se ejecutan como `/new-feature` o `/hotfix` aparte.
- **[stamp]**: `--source` sustituye la lista; para añadir una fuente, leer `read_page_meta` y
  pasar todas. Las páginas sin frontmatter (ejemplos) no se sellan.
- **[COB-ORIGINS-001]**: §3.10 ya usa la numeración v2; la marca ⚠️ probablemente está desfasada.
- **[COB-DOCPROJ-001]**: el cuerpo marca ⚠️ y la fila de Evidencia ✅ para la misma regla.
- **[marcas en el cuerpo]**: las ⚠️ / 🔍 al final de frases no llevan ID; al aplicar una decisión
  hay que cambiarlas a mano (`decisions` no las ve).

## Aplicación de decisiones (misma fecha)
- La persona usuaria aceptó las propuestas del agente para las 29 fichas (BOOTSTRAP-004: opción a).
  Responsable en cada ficha: Paco Manzano; el contexto indica que la propuesta fue del agente.
- Commits: `00f9440` (ORIGINS-001..004), `f2ffdfe` (remediación ORIGINS-004 + ficha ORIGINS-005),
  y el commit final con las 26 restantes.
- Remediaciones: 7 tests (`check_env` ×4, `convert_to_md`, `doc_trace`, sesiones); regla de la
  Capa D en el bootstrap. El test de CHECKENV-001 reveló un defecto real: con todo instalado,
  `check_env` decía «completo (Python).» por la nota de docling; corregido (nota `ℹ`).
- Resultado: 29 fichas decididas (28 + ORIGINS-005), 0 pendientes, 0 hallazgos; 19 ✅ y 10 ⚠️ aceptados
  conscientemente. El mensaje del commit `718de97` dice «11 ⚠️» por error; son 10.
- Verificación: ruff, mypy, pytest 310 passed, `mkdocs build --strict`, drift 0, matrix 76/101.

## Directrices para Futuras IAs (aplicación)
- **[⚠️ aceptados]**: BUILDZIP-001..004 se revisan al actualizar MkDocs o Zensical; DOCPROJ-002..005,
  ARCHETYPES-001 y CONVERT-001 dependen del chat o de motores externos: no reabrir sin un cambio de
  contexto.
- **[Remediar]**: un test pedido por una decisión puede revelar un defecto (CHECKENV-001): corregir
  el código antes de marcar ✅, nunca ajustar el criterio al defecto.

## Veredicto final
CLOSED (P1, P2 y aplicación de las 29 decisiones)
