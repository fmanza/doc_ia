# REQUEST

## Session metadata
- id: 2026-06-12
- fecha: 2026-06-12
- rama: develop
- skill: refactor
- fase solicitada: IMPLEMENT (actualización de instrucciones IA)

## Solicitud original saneada

Disponemos de una funcionalidad en `util_bbdd` para la generación de ficheros ZIP y Checksum
SHA256 en el apartado "Descargas" de la documentación.
- Esta funcionalidad tiene que ser implementada siempre en la generación de documentación en
  formato offline y disponer de otra en GitHub; las dos deben existir.
- Se necesita actualizar las instrucciones IA de generación de documentación para que se tenga
  en cuenta, tanto en la creación como en la revisión.

## Objetivo operativo de esta sesión

- Establecer la regla "script local + workflow GitHub son obligatorios y complementarios" en
  `SHARED_INSTRUCTIONS.md` como fuente canónica.
- Actualizar la detección en Fase 1 de `document_project.prompt.md` para comprobar las dos
  señales de forma independiente (`TIENE_ZIP_SCRIPT` y `TIENE_WORKFLOW_GITHUB`).
- Actualizar Fase 7b de `document_project.prompt.md` con la tabla de combinaciones y las
  acciones de remediación para cada caso (incluyendo VARIANTE B con gap completo).
- Sincronizar `CLAUDE.md` con la nueva regla y corregir la referencia de sección.

## Restricciones explícitas

- No modificar scripts ni workflows: solo instrucciones IA (`.github/`, `CLAUDE.md`).
- No inventar nuevas capacidades; la referencia de implementación es `doc_ia` y `util_bbdd`.

## Resultado esperado

- `SHARED_INSTRUCTIONS.md` con regla explícita "complementarios, no alternativos".
- `document_project.prompt.md` con Fase 1 y Fase 7b cubriéndolas dos señales y todos los casos.
- `CLAUDE.md` actualizado y referencia de sección corregida.
- Artefacto de sesión `.ai/sessions/2026-06-12/` con los tres ficheros de trazabilidad.
