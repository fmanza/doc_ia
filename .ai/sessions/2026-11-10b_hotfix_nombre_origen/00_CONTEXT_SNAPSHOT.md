# CONTEXT SNAPSHOT

## Contexto del repositorio revisado
- `scripts/snapshot_sources.py` (`NAME_RE`, `declare`, `read_manifest`, `_cmd_replace` con `shutil.rmtree`, `sync_source`)
- `tests/test_snapshot_sources.py`
- `.ai/sessions/2026-11-10_web_pre_manual/04_AUDIT_CODE.md` (C1 y propuesta)

## Estado actual observado
- `develop` = `main` = `15fdea4` (release 0.11.0 subida; el tag `v0.11.0` está creado en local y sin subir).
- 491 tests en verde antes del fix.
- Nombres de origen reales en UFV: todos válidos con la regla nueva.

## Estado Git relevante
- Rama activa: develop
- Cambios locales pre-existentes: ninguno
- Último tag / versión publicada: v0.10.0 (v0.11.0 creado en local)

## Clasificación metodológica
- Tipo principal: hotfix
- Estado real de alcance: acotado
- Consecuencia: fix en un fichero + tests

## Gate G0 · Context Ready
Veredicto: GO
Condiciones pendientes (si aplica):
- Ninguna
