# TRACEABILITY

## Session metadata
- id: 2026-10-28e
- fecha: 2026-10-28
- rama: develop
- skill: new_feature
- fase: ANÁLISIS + PLAN + AUDIT_PLAN + IMPLEMENT (M0, M1, M3, M2, M4, M5) + cierre

## Prompt issued
1. "Analizar si lo gráficos mermaid son los adecuados para la documentación que se genera. Puedes
   comprobar información en internet y en https://mermaid.js.org/. Puedes recomendar cambios.
   Solo información, no se implementa nada."
2. "PLAN y AUDIT_PLAN de lo propuesto, pregunta lo que necesites"
3. "GO entero"

## Context supplied
- `.github/DOCUMENTATION_STANDARD.md`, `.github/instructions/docs.instructions.md`, agentes y
  prompts de arquetipo, `.claude/EDGE_CASES.md`, `tests/test_docs_conformance.py`, `ci.yml`.
- mermaid.js.org (flowchart, syntax reference, accessibility), Material for MkDocs (diagrams),
  README de mermaid-cli, registro npm.
- Bundles instalados de mkdocs-material 9.8.0 y zensical 0.0.73.

## AI output summary
- Análisis: 23 diagramas extraídos; render real con mermaid@11 y @12 en Edge headless
  (harness en el scratchpad de la sesión, fuera del repo). Hallazgos: entidades HTML pintan `&`,
  8 diagramas > 12 nodos, flujos duplicados, 0 diagramas accesibles, versión 11/12 flotante.
- Decisiones del usuario: alcance completo por fases; fijar Mermaid dentro de F10; test estático
  + CI con mermaid-cli; mantener 12 nodos con test.
- D1: `docs.instructions.md` es Capa C en el bootstrap → fuente única en el estándar §3.17.
- M0 `a9cd2af`: regla de comillas, fix `build_docs_zip.md`, tests de entidades y comillas
  (detector calibrado con fixtures renderizadas), AC-11, EDGE_CASES.
- M1 `75481a6`: §3.17; agentes, prompts, `docs.instructions.md` y `CLAUDE.md` remiten a ella.
  C1 verificada antes (accTitle/accDescr en 5 tipos, v11 y v12).
- M3 `827a9cb` (adelantada a M2 para no anotar diagramas que se sustituían): 9 diagramas
  rediseñados, contador de nodos con fixtures, AC-12. C2: `convert_to_md` y `doc_trace`
  contrastados con el código (el diagrama técnico anterior de convert_to_md no reflejaba que
  `validate_only` reúne ficheros ni que `_detect_device` solo aplica a docling sin dry-run).
  C3: render v11/v12 sin errores y captura del sitio real de Zensical.
- M2 `2752cb1`: accTitle/accDescr en los 14 restantes y en `INTEGRATION_MAP.md`, `\n` →
  `<br/>`, flechas etiquetadas en el contexto, AC-13. Un primer script sustituyó saltos de línea
  reales por un fallo de escapado en el heredoc; se detectó en el diff, se restauraron los 3
  ficheros con `git checkout` y se rehízo con un script en fichero.
- M4 `14e153c`: job `mermaid` en `ci.yml`. C4: mmdc devuelve 1 ante parse error; las 18
  páginas pasan con cli 11.17.0 + mermaid 11.17.2 y cli 12.0.0 + mermaid 12.2.0.
- M5 `8777901`: F10 incluye Mermaid fijado y local + condición C9; EDGE_CASES 11/12. En el cierre
  se rebaja a hipótesis la afirmación de que `privacy` no intercepta la carga dinámica (no
  verificada; el mensaje del commit M5 la da por hecha).
- DoD en cada fase: ruff, format, mypy, pytest, drift 0, matrix, llms --check, build strict
  MkDocs y Zensical; páginas re-selladas solo tras revisarlas.

## Artefactos generados

| Artefacto | Ruta | Estado |
|---|---|---|
| PLAN + AUDIT_PLAN | `.ai/sessions/2026-10-28e_mermaid_diagrams/01_PLAN_AUDIT.md` | emitido |
| Norma de diagramas | `.github/DOCUMENTATION_STANDARD.md` §3.17 | completado |
| Tests | `tests/test_docs_conformance.py::test_mermaid_*` | completado |
| Diagramas | `docs/**` (24 bloques) | completado |
| CI | `.github/workflows/ci.yml` job `mermaid` | pendiente de primera ejecución en GitHub |
| Anexo F10 | `.ai/sessions/2026-10-28d_zensical_migration/02_PLAN_FASES.md` | planificado |

## Directrices para Futuras IAs
- **[Mermaid]**: Mermaid no decodifica entidades HTML (`&#64;` → `&@`); su sintaxis es `#64;`.
  La forma limpia es la label entre comillas. Sin comillas, `@ ( ) { }` en `[...]`/`{...}` son
  parse error en v11 y v12; `#` y `A@{ shape }` no.
- **[Mermaid]**: `\n` y `<br/>` funcionan en v11 y v12; la norma usa `<br/>`.
- **[Mermaid]**: `--strict` no valida diagramas. Para comprobar de verdad, `mermaid.render()`
  diagrama a diagrama o `mmdc -i página.md`; una galería con `startOnLoad` y mermaid@12
  superpone los diagramas y da falsos positivos visuales.
- **[Bootstrap]**: `docs.instructions.md` no viaja a los destinos (Capa C); las reglas que deban
  viajar van en `DOCUMENTATION_STANDARD.md` (Capa B) o en los agentes/prompts (Capa A).
- **[Shell]**: no reemplazar `\n` literales desde un heredoc de bash con Python; usar un script
  en fichero con `chr(92) + "n"`.

## Veredicto final
Veredicto: CLOSED
Pendientes al cierre:
- Primera ejecución del job `mermaid` en GitHub (requiere push; no se ha hecho push ni tag).
- Hotfix en socyalpro (y otros destinos) que aplicaron la regla `&#64;`.
- F10: Mermaid fijado y local, condicionado a F8.
- Versión: proponer 0.3.0 (feat) en el próximo `/version-closure`.
