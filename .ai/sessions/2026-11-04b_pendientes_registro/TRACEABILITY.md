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

## Veredicto final
CLOSED (P1 y P2 implementados; decisiones pendientes de la persona usuaria)
