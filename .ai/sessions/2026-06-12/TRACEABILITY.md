# TRACEABILITY

## Session metadata

- id: 2026-06-12
- fecha: 2026-06-12
- rama: develop
- skill: refactor
- fase: IMPLEMENT

## Prompt issued

> Disponemos de una funcionalidad en util_bbdd para la generación de ficheros ZIP y Checksum
> SHA256 en el apartado "Descargas" de la documentación. Esta funcionalidad tiene que ser
> implementada siempre en la generación de documentación en formato offline y disponer de
> otra en GitHub; las dos deben existir. Se necesita actualizar las instrucciones IA de
> generación de documentación para que se tenga en cuenta, tanto en la creación como en la revisión.

## Context supplied

- Exploración completa de `util_bbdd` (script, workflows, `docs/downloads.md`)
- Exploración completa de `doc_ia` (script, workflows, `SHARED_INSTRUCTIONS.md`,
  `document_project.prompt.md`, `CLAUDE.md`, `docs/downloads.md`)

## AI output summary

- Identificada la regla de negocio: script local (`scripts/build_docs_zip.py`) y workflow
  GitHub (`.github/workflows/docs-zip-release.yml`) son siempre obligatorios y complementarios.
- `SHARED_INSTRUCTIONS.md` actualizado:
  - §Distribución de documentación offline: reescrito con regla explícita "complementarios,
    no alternativos"; lista de las 3 piezas obligatorias con propósito diferenciado.
  - §Patrón de distribución offline (renombrado): describe las dos señales del patrón y que
    Fase 1 + Fase 7b las detectan de forma independiente.
- `document_project.prompt.md` actualizado:
  - Fase 1: añadida detección de `TIENE_WORKFLOW_GITHUB`; tabla de 4 combinaciones con
    variante aplicable en Fase 7b.
  - Fase 7b VARIANTE A: añadido paso 4 (verificar workflow; reportar gap si falta).
  - Fase 7b VARIANTE B: ampliada con reporte de gap completo y patrones de referencia.
  - §Devuelve 8b: actualizado para reflejar estado de las dos señales y huecos reportados.
- `CLAUDE.md` actualizado:
  - §Descarga de Documentación Offline: reescrito párrafo introductorio; nombra ambos
    mecanismos con la regla "deben existir siempre".
  - Referencia de sección corregida: "patrón build_docs_zip.py" → "Patrón de distribución offline".

## Artefactos generados

| Artefacto              | Ruta                                                      | Estado     |
|------------------------|-----------------------------------------------------------|------------|
| SHARED_INSTRUCTIONS.md | `.github/SHARED_INSTRUCTIONS.md`                          | modificado |
| document_project       | `.github/prompts/document_project.prompt.md`              | modificado |
| CLAUDE.md              | `CLAUDE.md`                                               | modificado |
| REQUEST                | `.ai/sessions/2026-06-12/00_REQUEST.md`                   | creado     |
| CONTEXT_SNAPSHOT       | `.ai/sessions/2026-06-12/00_CONTEXT_SNAPSHOT.md`          | creado     |
| TRACEABILITY           | `.ai/sessions/2026-06-12/TRACEABILITY.md`                 | creado     |

## Directrices para Futuras IAs

- **[distribución offline]**: el patrón completo requiere SIEMPRE dos señales en el origen:
  `scripts/build_docs_zip.py` (build local) y `.github/workflows/docs-zip-release.yml`
  (auto-publicación GitHub Releases). Si solo existe una, hay un gap que reportar.
- **[document_project Fase 1]**: la detección ZIP usa ahora dos flags independientes
  (`TIENE_ZIP_SCRIPT`, `TIENE_WORKFLOW_GITHUB`); la tabla de combinaciones está en Fase 1,
  no en Fase 7b — consultar ahí para la variante aplicable.
- **[patrones de referencia]**: la implementación canónica vive en `doc_ia/scripts/build_docs_zip.py`
  y `doc_ia/.github/workflows/docs-zip-release.yml`. `util_bbdd` tiene la misma estructura
  pero con `zensical` como builder por defecto.

## Veredicto final

Veredicto: CLOSED
Pendientes al cierre:
- Commit + push a develop (preparado en esta sesión).
