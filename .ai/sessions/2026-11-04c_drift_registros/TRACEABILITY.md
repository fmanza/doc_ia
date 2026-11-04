# TRACEABILITY — 2026-11-04c `drift` vigila los registros de decisiones

## Session metadata
- id: 2026-11-04c
- fecha: 2026-11-04
- rama: develop
- skill: new_feature
- fase: PLAN (en el chat) + IMPLEMENT + AUDIT_CODE + verificación

## Prompt issued
«Quiero que drift también lo cubra en doc_ia» — tras la sesión de APDI, donde los registros no
podían declararse en `fuentes:` porque la documentación vive en otro repositorio que el código.

## AI output summary
- Diseño: clave nueva `decisiones:` en el frontmatter (ruta del registro tal como la enlaza la
  página, relativa a ella → huella). `stamp` la rellena desde los enlaces `COB-…` fuera de código;
  `drift` la compara desde la página (no desde `--root`) y añade el estado `unsealed`.
- `scripts/doc_trace.py`: `PageMeta.registers`, `linked_registers`, `REGISTER_LINK_RE`;
  `read_page_meta`, `format_frontmatter`, `stamp_page` y `check_drift` ampliados.
- 5 tests nuevos (sellado y `stale`, `unsealed`, página solo con registros, destino externo,
  enlaces en código). Migradas 13 páginas de doc_ia de `fuentes:` a `decisiones:`.
- Docs: §3.16 y §3.18 del estándar, `coverage_decisions`, prompt normativo, ADR-004, páginas
  de `doc_trace` (AC-29, AC-30), referencia, mapa funcional (79/104), CHANGELOG.
- Comprobación real (solo lectura): sobre APDI, `drift` informa 32 relaciones `unsealed`
  (11 registros desde la normativa + 21 páginas con Evidencia).
- Verificación: ruff, mypy strict, pytest 317 passed, `mkdocs build --strict`, drift 0,
  `decisions` 0/0, `llms --check`.

## Directrices para Futuras IAs
- **[decisiones:]**: nunca se escribe a mano; `stamp` la recalcula en cada sellado. Un registro
  ya no va en `fuentes:`.
- **[destinos existentes]**: al actualizar a doc_ia ≥ 0.6, cada página que enlaza registros sale
  `unsealed` hasta sellarla; las páginas sin frontmatter (p. ej. la normativa de APDI) se sellan con
  `--archetype`.

## Veredicto final
CLOSED
