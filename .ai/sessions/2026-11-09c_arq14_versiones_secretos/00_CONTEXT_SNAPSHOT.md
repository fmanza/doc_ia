# CONTEXT SNAPSHOT

## Contexto del repositorio revisado

`develop` limpio tras `6e268fc` (release v0.9.0). Revisados `scripts/snapshot_sources.py`,
`.github/prompts/document_project.prompt.md`, `.github/DOCUMENTATION_STANDARD.md` (§3.2, §3.15,
§3.18, §4.3), `.claude/commands/document-project.md`, `.github/kit/MANIFEST.txt`, tests de
conformidad y de `snapshot_sources`.

## Orígenes externos consultados

Solo como motivación (no como plantilla): documentos convertidos de un destino para la prueba de
humo de `redact_secrets.py --check` (sin copiar contenido; solo fichero, línea y regla).

## Estado actual observado

- Sin arquetipo de integraciones (solo Arq. 2 §4 y Arq. 12 §5).
- `snapshot_sources.py` sin forma de sustituir un origen declarado.
- Sin regla ni herramienta de secretos para `_fuentes/`.

## Estado Git relevante

`develop`, sin cambios previos.

## Clasificación metodológica

Feature (sin refactor).

## Gate G0 · Context Ready

✅
