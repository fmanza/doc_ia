# TRACEABILITY

## Session metadata
- id: 2026-11-12
- fecha: 2026-11-12
- rama: develop
- skill: new_feature (fix + build(deps))
- fase: PLAN + AUDIT_PLAN + IMPLEMENT

## Prompt issued
1. Revisión de lo pendiente de la migración a Zensical (F7, F8, F9, F10, F12): situación actual y
   qué falta.
2. «PLAN y AUDIT_PLAN».
3. Decisión del usuario (D4): Zensical es el generador estándar (doc_ia y destinos) y MkDocs
   queda fuera; añadirla al PLAN y al AUDIT_PLAN.
4. «IMPLEMENT».

## Context supplied
- `2026-10-28d_zensical_migration/{02_PLAN_FASES,TRACEABILITY}.md`, `ci.yml`, anotaciones de CI
  (`gh api …/annotations`), PyPI (`zensical`).

## AI output summary
- Situación: Zensical 0.1.1 publicada. La paridad falla en CI desde v0.7.0 (2026-11-04), oculta
  porque la conclusión del run es `success`. C2 no ha empezado a contar.
- Spike (scratchpad, worktrees eliminados):
  - Causa raíz: `navigation.indexes` (`adb2825`) hace que el logo enlace a una carpeta en las 66
    páginas, con MkDocs y con Zensical.
  - Arreglo `extra.homepage: index.html` verificado.
  - Zensical 0.1.1: build OK, mismas rutas, nueva dependencia `zensical-ui`, un test de Mermaid
    que adaptar y `hooks:` todavía ignorado.
- PLAN P1 (fix + regla de comprobación + plantilla de producto), P2 (F7, Zensical 0.1.1),
  P3 (plan de la migración al día: C2 reiniciada, F10 reducido, C10).
- AUDIT_PLAN inicial: 9 hallazgos (A1-A9). Veredicto: P1 GO, P2 GO_CONDICIONAL (C-a, C-b), P3 GO.
- D4 incorporada:
  - F8, F9, F12 y F13 sustituidas por Z1 (único generador), Z2 (docs), Z3 (destinos),
    Z4 (F10 reducido) y Z5 (plan al día). C2 y C5 retiradas.
  - Propuestas D5 (se mantienen los nombres `mkdocs.yml`/`mkdocs_hooks.py`) y D6 (migración
    explícita de los destinos MkDocs en la Fase 0b, con guarda de plugins).
  - Nuevos hallazgos B1-B10 (sin fallback, C3 obligatoria antes de Z1, cambio de contrato
    para los destinos, CLI `--builder`).
- PLAN y AUDIT_PLAN sin cambios en código.
- IMPLEMENT (detalle en `03_IMPLEMENT.md`): P1 `7199613`, P2 `b63cf2d`, release v0.11.4
  `1599b04`, Z1 `b6ee093`, Z2 `4c6e3cb`, Z3 `5fd6ce0`, Z5 (CHANGELOG y trazabilidad). D5, D6 y B6
  aplicados con la opción recomendada (sin respuesta explícita). C-a cumplida; C-b y C3
  verificadas con capturas por `file://` (búsqueda y móvil real pendientes de revisión humana).
  Z4 queda como decisión (`privacy`). Todo en `develop`, sin push.

## Pendiente
- Decidir COB-BUILDZIP-001 (¿reclasificar a `No aplica`?), Z4 (`privacy`) y revisión humana de C3.
- VERSION v0.12.0 con `/version-closure` (merge, tag y push por separado, con confirmación).
