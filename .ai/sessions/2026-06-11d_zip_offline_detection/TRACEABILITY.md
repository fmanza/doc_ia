# TRACEABILITY

## Session metadata

- id: 2026-06-11d_zip_offline_detection
- fecha: 2026-06-11
- rama: develop
- skill: new_feature
- fase: PLAN + AUDIT_PLAN + IMPLEMENT

## Prompt issued

> Actualmente el fichero de versión y el Checksum en el proyecto `util_bbdd` se autogenera en
> local, en las instrucciones IA de doc_ia (este proyecto) no se tiene en cuenta y queremos que
> sea así. PLAN – AUDIT PLAN

## Context supplied

- `util_bbdd/scripts/build_docs_zip.py` — implementación de referencia del patrón
- `util_bbdd/dist/CHECKSUMS.txt` y `util_bbdd/dist/util_bbdd-docs-0.10.0.zip.sha256` — evidencia de artefactos reales
- `util_bbdd/docs/downloads.md` — tabla de descargas de referencia
- `.github/prompts/document_project.prompt.md` — fichero principal a modificar
- `.github/SHARED_INSTRUCTIONS.md` — fuente canónica
- `CLAUDE.md` — entry point con duplicación a resolver

## AI output summary

1. Leídos `SHARED_INSTRUCTIONS.md` (doc_ia y util_bbdd), `document_project.prompt.md`, `bootstrap_ai_config.prompt.md`, `CLAUDE.md`, `util_bbdd/scripts/build_docs_zip.py`, `util_bbdd/dist/CHECKSUMS.txt`, `util_bbdd/docs/downloads.md`.
2. **PLAN emitido**: identificados 3 ficheros candidatos; cambios en Fase 1 + nueva Fase 7b + paso 8b + sección SHARED + DRY en CLAUDE.md.
3. **AUDIT_PLAN ejecutado**: 6 hallazgos; 2 correcciones bloqueantes incorporadas al plan (señales independientes A1; guarda de orden A2); 1 corrección recomendada (DRY A3); veredicto APROBADO.
4. **IMPLEMENT ejecutado** (tras confirmación del usuario):
   - `document_project.prompt.md` — Fase 1 ampliada con detección TIENE_ZIP_SCRIPT / TIENE_DOWNLOADS_PAGE; Fase 7b añadida con 4 casos y guarda de orden; paso 8b añadido en sección "Devuelve".
   - `SHARED_INSTRUCTIONS.md` — sección "Artefactos generados" ampliada con párrafo del patrón `build_docs_zip.py` generalizable.
   - `CLAUDE.md` — sección "Actualizar tabla Descarga Actual" convertida a referencia DRY con comandos específicos de doc_ia conservados.

## Artefactos generados

| Artefacto | Ruta | Estado |
|---|---|---|
| PLAN + AUDIT_PLAN | conversación (chat) | emitido |
| IMPLEMENT — Fase 1 + 7b + 8b | `.github/prompts/document_project.prompt.md` | completado |
| IMPLEMENT — patrón ZIP offline | `.github/SHARED_INSTRUCTIONS.md` | completado |
| IMPLEMENT — DRY | `CLAUDE.md` | completado |
| Artefacto de sesión | `.ai/sessions/2026-06-11d_zip_offline_detection/` | creado |

## Directrices para Futuras IAs

- **[document_project / Fase 7b]**: las señales `TIENE_ZIP_SCRIPT` y `TIENE_DOWNLOADS_PAGE` son independientes; no asumir que siempre aparecen juntas.
- **[document_project / Fase 7b]**: la guarda de orden (Fase 7 → Fase 7b) es obligatoria; si `--verify-build` no se activó, `site/` puede estar desactualizado y el ZIP sería incorrecto.
- **[SHARED_INSTRUCTIONS vs CLAUDE.md]**: la regla del patrón ZIP vive en `SHARED_INSTRUCTIONS.md`; `CLAUDE.md` solo añade comandos específicos de doc_ia. No duplicar la lógica.
- **[bootstrap_ai_config.prompt.md]**: ya cubre el patrón ZIP en la sección "Capa B" correctamente; no modificar en futuras iteraciones relacionadas con este patrón.
- **[util_bbdd]**: ningún archivo de `util_bbdd` fue modificado en esta sesión; el gap era exclusivamente en doc_ia.

## Veredicto final

Veredicto: CLOSED
Pendientes al cierre:
- Ninguno
