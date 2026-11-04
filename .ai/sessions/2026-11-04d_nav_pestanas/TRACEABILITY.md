# TRACEABILITY — 2026-11-04d Barra superior en 9 pestañas («Inicio» y «Proyecto»)

## Session metadata
- id: 2026-11-04d
- fecha: 2026-11-04
- rama: develop
- skill: new_feature
- fase: PLAN + AUDIT_PLAN (GO_CONDICIONAL, opción B) + IMPLEMENT + verificación

## Prompt issued
«El menú superior tiene muchos elementos y se corta la visualización del último elemento;
queremos incluir en el menú "Inicio" un submenú con el menú "Descargas"». Alternativas
P0, A-F; elegida **B**.

## AI output summary
- Diagnóstico: 14 pestañas; Material y Zensical no tienen desplegables en las pestañas (una
  sección es pestaña y sus páginas van a la barra lateral). Mover solo Descargas (P0) dejaba 13.
- Opción B: sección «Inicio» (Inicio, Quick Start, Instalación, Descargas) con
  `navigation.indexes` + sección «Proyecto» (Configuración IA, Changelog, Contribuir) → 9
  pestañas. URLs sin cambios (`downloads.html`).
- Condiciones del AUDIT_PLAN: Zensical admite `navigation.indexes` (sus plantillas
  `tabs-item.html` / `nav-item.html` lo leen) ✅; entrada índice con título (`- Inicio: index.md`)
  para que `llms.txt` no muestre «index.md» ✅; regla de migración «mover, nunca duplicar» en
  prompt, agente y estándar ✅.
- Producto: §4.1 del estándar (plantilla nav, `navigation.indexes`, notas: máx. 9 pestañas,
  «Inicio», «Proyecto»), §3.12-3.14 (Changelog/Config IA/Contribuir bajo «Proyecto»), §3.18
  (Decisiones dentro de «Normativa» si existe, para no pasar de 9), §4.2; prompt Fase 5 + Paso
  B3 + RESUMEN 8b; agente Fase 4; comando (tabla de features + checklist Fase 0b);
  `docs.instructions.md`.
- Dogfooding: `mkdocs.yml`, `docs/llms.txt` regenerado; Arq. 1 de arquetipos (regla «Barra
  superior legible», AC-15, Evidencia); postcondición de `document_project` y SYNC NAV de su API.
- Tests: `test_top_navigation_fits_in_nine_tabs`, `test_standard_nav_template_groups_home_and_project`,
  `test_nine_tabs_rule_everywhere` (×4).
- Verificación: ruff, mypy strict, pytest, `mkdocs build --strict` (9 pestañas en `site/index.html`),
  drift 0 tras revisar y sellar 9 páginas, `decisions` sin hallazgos, `llms --check`.

## Directrices para Futuras IAs
- **[pestañas]**: no añadir entradas de primer nivel al nav sin contar; si se supera 9, agrupar
  (nunca un desplegable propio con `custom_dir`: rompe la compatibilidad con Zensical).
- **[Decisiones + Normativa]**: con Arquetipo 8, «Decisiones» va dentro de «Normativa».
- **[pendiente]**: comprobación visual manual de la barra a 1366 px en `site/` (no automatizable
  sin navegador).

## Veredicto final
CLOSED
