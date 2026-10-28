# IMPLEMENT — Entrega P3

## Level 1 — Tooling (S4: un único script)

| Fichero | Cambio |
|---|---|
| `scripts/doc_trace.py` | **Nuevo** — subcomandos `stamp`, `drift`, `matrix`, `llms`. API: `PageMeta`, `DriftFinding`, `CriterionRow`, `fingerprint`, `read_page_meta`, `stamp_page`, `check_drift`, `collect_test_ids`, `collect_criteria`, `build_matrix`, `build_llms_txt`, `main`. Códigos 0 / 1 / 2. Sin dependencias nuevas (PyYAML vía mkdocs, aislado en `_load_yaml`) |
| `tests/test_doc_trace.py` | **Nuevo** — 20 tests sin red ni git (`tmp_path`) |

Mitigaciones del AUDIT_PLAN cubiertas por test:
- **T4** `!!python/name:` en `mkdocs.yml` → `test_build_llms_txt_tolerates_python_tags`.
- **S-1** rutas fuera del repo → `test_drift_never_reads_outside_repo`, `test_stamp_rejects_source_outside_repo`.
- **T3** saltos de línea → `test_fingerprint_ignores_line_endings`.
- **T6** fuera del hook PostToolUse: no se añade a `.claude/settings.json*`.

## Level 2 — Norma y orquestación

`DOCUMENTATION_STANDARD.md` §3.16 › Frontmatter de trazabilidad y detección de drift;
`documentation-generator.agent.md` (Fase 6: stamp + drift + matrix + llms);
`documentation-reviewer.agent.md` (stale = Nivel 2, test inexistente = Nivel 1);
`document_project.prompt.md` (Fase 6); `CLAUDE.md` (comandos); `.claude/EDGE_CASES.md` (falso positivo de huellas).

## Level 3 — Dogfooding

- 17 páginas con bloque Evidencia selladas (`arquetipo`, `fuentes`, `revisado`).
- `docs/llms.txt` (38 páginas) publicado en `site/llms.txt`.
- Páginas nuevas del propio script: `docs/functional/doc_trace.md` (14 AC, 14 con test),
  `docs/api/doc_trace.md`, `docs/examples/doc_trace_usage.md` + `.py` (fork).
- Referencia del Sistema: CLI, códigos, interfaces (`llms.txt`, matriz) y datos (frontmatter).
- Mapa Funcional: capacidad nueva; cobertura 29/66.

## Hallazgos durante el dogfooding (corregidos)

1. **Cascada de drift**: sellar una página `.md` que es fuente de otra (Mapa Funcional) la
   marcaba como `stale`. Fix: la huella de fuentes `.md` excluye su frontmatter + test.
2. **Consola cp1252**: `matrix` fallaba al imprimir `↔` en Windows. Fix: reconfiguración UTF-8
   de stdout/stderr en `__main__` (mismo patrón que `convert_to_md.py`).
3. **Trazas no controladas** (detectadas por el fork): `stamp` con página inexistente y `llms`
   sin `nav`. Fix: captura de `ValueError`/`OSError` → mensaje + código 1 + 2 tests.
4. **Drift real tras editar la norma**: 15 fuentes `stale` en 7 páginas; revisadas una a una
   (contenido actualizado en 6, solo resellado en `origin_types.md`).

## Verificación final

`drift` 0 · `matrix` 0 (29/66, ningún test inexistente) · `llms --check` 0 ·
`mkdocs build --strict` OK · pytest 97 OK · ruff OK · mypy sin errores nuevos (10 preexistentes).
