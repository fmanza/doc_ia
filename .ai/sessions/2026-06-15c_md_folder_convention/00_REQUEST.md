# REQUEST

## Session metadata
- id: 2026-06-15c_md_folder_convention
- fecha: 2026-06-15
- rama: develop
- skill: new_feature (instrucciones IA) + PLAN + AUDIT_PLAN + IMPLEMENT
- fase solicitada: PLAN → AUDIT_PLAN → IMPLEMENT

## Solicitud original saneada

1. Convertir documentos a Markdown de `C:\Desarrollo\documentation\SOCYALPRO\doc_referencia\Legales`.
2. Actualizar la documentación IA para que contemple que los documentos de referencia se convierten
   a formato Markdown y que los ficheros generados, ubicados en una carpeta `md/`, deben ser usados
   por la IA como fuente de contexto.

## Objetivo operativo de esta sesión

- Ejecutar `scripts/convert_to_md.py` sobre los 20 PDFs de `Legales/` (subcarpetas CA/, ES/, LC/).
- Actualizar Fase 0b de `document_project.prompt.md` para detectar carpetas `md/` pre-existentes
  y usarlas directamente sin proponer conversión redundante.
- Actualizar el INVENTARIO del command file `.claude/commands/document-project.md`.
- Añadir la convención `<origen>/md/` a la tabla de módulos de `SHARED_INSTRUCTIONS.md`.

## Restricciones explícitas

- Solo modificar instrucciones IA y documentación; no tocar código fuente Python.
- Los ficheros `md/` son artefactos generados — no editarlos directamente.
- Aplicar PLAN → AUDIT_PLAN antes de IMPLEMENT.

## Resultado esperado

- 20 PDFs convertidos en `Legales/md/` con estructura CA/, ES/, LC/ reflejada.
- `document_project.prompt.md` con Fase 0b reestructurada (Pasos 0-5 + Nota actualizada + Fase 1 ampliada).
- `.claude/commands/document-project.md` con sub-sección "Documentos de referencia" en INVENTARIO.
- `SHARED_INSTRUCTIONS.md` con fila `Patrón <origen>/md/` en tabla de módulos.
- Artefactos de sesión en `.ai/sessions/2026-06-15c_md_folder_convention/`.
