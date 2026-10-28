# TRACEABILITY

## Session metadata
- id: 2026-10-28c
- fecha: 2026-10-28
- rama: develop
- skill: hotfix (H) + refactor (R1) + new_feature (Q2)
- fase: PLAN + AUDIT_PLAN + IMPLEMENT + AUDIT_CODE + VERSION (×3)

## Prompt issued
"PLAN y AUDIT_PLAN de lo que queda pendiente" → "Adelante, si necesitas preguntar por algo hazlo".

## Context supplied
- Pendientes de las sesiones `2026-10-28_archetypes_v2` y `2026-10-28b_cuda_auto_hotfix`.
- Decisiones del usuario: D1 = no publicar en Pages; D2 = aceptar ZIP latest; C3 = drift bloqueante.

## AI output summary
- **H** (`e0965b6` + `70a8dcd`): `.md` fuera de `DOCLING_EXTENSIONS`; test que falla antes y pasa
  después; AC-13 en `functional/convert_to_md.md`; recuento de tests corregido (74).
- **R1** (`a780ab1`): C1 reveló que el prompt multiplataforma **no tenía** la sincronización
  visual; se añade como Fase 0b y la conversión pasa a Fase 0c. Bootstrap: ruta Codex, Capa B
  con Arq. 7/8/10/12 y `doc_trace.py` opcional. `settings.json.example` con `sync_root_docs.py`.
  §4.2 de la norma sin copia del nav. D1 y D2 documentados.
- **Q2**: `style` (`2a00196`, ruff format de `convert_to_md.py`; incluye el `bool(...)` de
  `_is_conversion_success`, sin cambio de comportamiento) + commit Q2:
  - mypy limpio en venv mínimo, global y `.venv` (overrides `docling.*` y `markitdown.*`;
    `warn_unused_ignores=false` solo en `scripts.convert_to_md`).
  - `requirements-docs.txt` / `requirements-dev.txt`; workflows de docs sin docling/torch.
  - `.github/workflows/ci.yml` (3.12 + 3.14, `contents: read`, drift bloqueante).
  - `tests/test_build_docs_zip.py` (8) y `tests/test_docs_conformance.py` (64 casos).
  - Los tests de conformidad detectaron 2 incumplimientos reales, corregidos: enlace §5 sin
    retorno en `examples/document_project_usage.md` y `CONTRIBUTING.md` con 7 secciones.
  - Cobertura de criterios 30/67 → 45/67.
- Verificación: secuencia completa de CI en venv limpio con `requirements-dev.txt` (Python 3.14):
  ruff, format, mypy, pytest 170, drift 0, matrix 0, `llms --check` 0, build `--strict` OK.

## AUDIT_CODE
- **C2 parcial**: "mypy con docling" no verificable en local (ningún entorno tiene docling); se
  mitiga con `warn_unused_ignores=false` acotado a `scripts.convert_to_md`.
- **C4**: CI no ejecutada en GitHub (sin push en esta sesión). Python 3.12 no está instalado en
  local: la matriz de CI lo validará en el primer push.
- **Regresiones**: ninguna en tests; `requirements.txt` intacto (entorno local completo).
- **Riesgo T1**: `requirements-docs.txt` debe mantenerse alineado con `requirements.txt`
  (comentario en el fichero; la CI construye con él).

## Directrices para Futuras IAs
- **[entorno]**: `.venv` y el Python global de esta máquina son 3.14 y no tienen docling; para
  reproducir la CI usar un venv limpio con `requirements-dev.txt`.
- **[docs]**: `tests/test_docs_conformance.py` es la verificación automática de los arquetipos
  sobre `docs/`; una página nueva que no cumpla la estructura rompe la CI.
- **[doc_trace]**: al citar un fichero de tests nuevo en una página, añadirlo a `fuentes` con
  `stamp --source` (el script de sellado por Evidencia no ve la columna Test).

## Veredicto final
Veredicto: CLOSED
Pendientes al cierre:
- Push a `develop` para validar `ci.yml` en GitHub (C4) y la matriz 3.12.
- 22/67 criterios sin test: flujos IA ejecutados en chat (no automatizables con tests unitarios).
