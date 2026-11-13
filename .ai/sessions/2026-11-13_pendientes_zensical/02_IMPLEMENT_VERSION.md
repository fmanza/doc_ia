# IMPLEMENT + VERSION CLOSURE — v0.13.0

Prompt: «si» (2026-11-13) al PLAN y AUDIT_PLAN.

## Commits (rama `develop`)

| Fase | Commit | Contenido |
|---|---|---|
| Q1 | `de170f5` | `feat(build)`: ZIP reproducible en `build_docs_zip.py::_zip` y `mkdocs_hooks.py` (entradas ordenadas, `ZipInfo` con fecha fija `SOURCE_DATE_EPOCH` → último commit → 1980-01-01, permisos `0o644`); 4 tests; AC-17; EDGE_CASES |
| Q2 | `a857c6c` | `ci(release)`: `docs-release.yml` adjunta también el `.sha256`; `downloads.md` |
| Q3 | `5eb0dc2` | `feat(build)!`: fuera `--builder` y `LEGACY_BUILDER_FLAG`; `test_builder_option_was_removed`; AC-16 reescrito; referencia, troubleshooting, ADR-003, bootstrap |
| Q4 | `ee047be` | `docs(contributing)`: § «Actualizar Zensical» + `test_zensical_pinned_to_the_same_version_everywhere`; restos del doble generador en CONTRIBUTING y el estándar |
| VERSION | (este commit) | `release: v0.13.0` |

## Verificación

- Q1 en real: dos pipelines completos con un minuto de diferencia → ZIP versionado y `latest`
  idénticos byte a byte (misma huella).
- Guarda de Q4 probada en negativo (versión distinta en `requirements.txt` → falla con el detalle)
  y restaurada.
- ruff, `ruff format --check`, mypy strict y pytest en verde tras cada fase; `drift`, `decisions`,
  `llms --check` y `matrix` sin hallazgos.
- Hallazgo de paso: el post-build recorría `site/` con `os.walk` sin ordenar (orden no
  determinista); corregido en Q1.

## VERSION v0.13.0

- **Impacto en API**: `build_docs_zip.py` sin `--builder` (BREAKING, código 2 «unrecognized
  arguments»). Nuevas funciones privadas `_zip_date_time` y `_add_entry` (script y post-build).
- **Migraciones**: quitar `--builder` de llamadas propias y de las copias del script en destinos
  (UFV la tiene desde 0.12.0; se corrige en su próxima Fase 0b).
- **Compatibilidad**: Python 3.12–3.14; Zensical 0.1.1 + zensical-ui 0.0.42.
- **Rollback**: `git revert` del merge en `main`; las releases publicadas no se retiran.
- **Comprobación tras publicar**: huella de `v0.13.0` = huella de `docs-v0.13.0` (A1 del AUDIT).
- Merge, tag y push por separado y con confirmación.
