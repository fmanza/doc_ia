# CONTEXT SNAPSHOT

## Contexto del repositorio revisado

- `.github/SHARED_INSTRUCTIONS.md` — fuente canónica; sección §Distribución de documentación offline
- `.github/prompts/document_project.prompt.md` — Fase 1 (detección ZIP), Fase 7b (variantes A/B)
- `CLAUDE.md` — sección §Descarga de Documentación Offline
- `C:\Desarrollo\python\libs\util_bbdd\scripts\build_docs_zip.py` — implementación de referencia
- `C:\Desarrollo\python\libs\util_bbdd\.github\workflows\docs-zip-release.yml` — workflow de referencia
- `C:\Desarrollo\python\libs\doc_ia\scripts\build_docs_zip.py` — implementación local
- `C:\Desarrollo\python\libs\doc_ia\.github\workflows\docs-zip-release.yml` — workflow local

## Estado actual observado

- Rama develop adelantada 4 commits respecto a origin/develop (commits anteriores pendientes de push).
- Sin cambios en tests ni scripts: la sesión solo modifica instrucciones IA.
- `.claude/settings.json` tiene modificaciones previas no relacionadas (allowlist de comandos).

## Estado Git relevante

- Rama activa: develop
- Cambios locales pre-existentes: `.claude/settings.json` (permisos adicionales, no relacionado)
- Último tag / versión publicada: ver `pyproject.toml` (no consultado en esta sesión)

## Clasificación metodológica

- Tipo principal: refactor (instrucciones IA — sin cambio funcional en tooling)
- Estado real de alcance: acotado — solo ficheros de instrucciones IA
- Consecuencia: commit `docs(instructions):` + push a develop

## Gate G0 · Context Ready

Veredicto: GO
Condiciones pendientes (si aplica):
- Ninguna
