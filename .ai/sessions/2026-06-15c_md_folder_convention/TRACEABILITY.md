# TRACEABILITY

## Session metadata
- id: 2026-06-15c_md_folder_convention
- fecha: 2026-06-15
- rama: develop
- skill: new_feature (instrucciones IA) + PLAN + AUDIT_PLAN + IMPLEMENT
- fase: PLAN → AUDIT_PLAN → IMPLEMENT

## Prompt issued

"Convertir documentos a Markdown de C:\Desarrollo\documentation\SOCYALPRO\doc_referencia\Legales"
"Actualizar la documentación IA para que se contemple que los documentos de referencia se conviertan
a formato Markdown, los ficheros generados están ubicados en una carpeta 'md' que deben ser usados
por la IA. PLAN - AUDIT PLAN"

## Context supplied

- `scripts/convert_to_md.py` — script determinista de conversión PDF → markitdown, DOCX → pandoc
- `.github/prompts/document_project.prompt.md` — Fase 0b original (sin detección de md/ pre-existente)
- `.claude/commands/document-project.md` — INVENTARIO sin sub-sección md/
- `.github/SHARED_INSTRUCTIONS.md` — tabla de módulos sin patrón md/
- `C:\Desarrollo\documentation\SOCYALPRO\doc_referencia\Legales\` — 20 PDFs en CA/ (17), ES/ (2), LC/ (1)

## AI output summary

- Dry-run de conversión: 20 PDFs detectados en CA/, ES/, LC/. `LC/md/` ya existía (1 fichero).
- Conversión ejecutada: 20/20 OK en `Legales/md/` (estructura CA/, ES/, LC/ reflejada). Un PDF de Baleares tenía restricción de extracción; markitdown la ignoró y procedió.
- PLAN emitido: 3 ficheros a modificar, 5 casos de cobertura, ajustes A2/A4/A5 identificados en AUDIT.
- AUDIT_PLAN: veredicto favorable con 3 ajustes menores (A2 confirmación usuario, A4 interacción Fase 0a, A5 Fase 1).
- IMPLEMENT — `document_project.prompt.md`: Fase 0b reescrita con Paso 0 (detección pre-existente), Pasos 1-5 renumerados; Nota final actualizada; Fase 1 ampliada; sección INVENTARIO de salida con sub-sección md/.
- IMPLEMENT — `document-project.md`: sub-sección "Documentos de referencia pre-convertidos" añadida en paso 3 (INVENTARIO).
- IMPLEMENT — `SHARED_INSTRUCTIONS.md`: fila `Patrón <origen>/md/` añadida en tabla de módulos.

## Artefactos generados

| Artefacto | Ruta | Estado |
|---|---|---|
| PDFs convertidos a Markdown (20 ficheros) | `C:\Desarrollo\documentation\SOCYALPRO\doc_referencia\Legales\md\` | CREADO |
| Fase 0b reestructurada (Pasos 0-5 + Nota + Fase 1) | `.github/prompts/document_project.prompt.md` | ACTUALIZADO |
| Sub-sección INVENTARIO md/ | `.claude/commands/document-project.md` | ACTUALIZADO |
| Fila patrón md/ en tabla de módulos | `.github/SHARED_INSTRUCTIONS.md` | ACTUALIZADO |
| Session 00_REQUEST | `.ai/sessions/2026-06-15c_md_folder_convention/00_REQUEST.md` | CREADO |
| Session TRACEABILITY | `.ai/sessions/2026-06-15c_md_folder_convention/TRACEABILITY.md` | CREADO |

## Directrices para Futuras IAs

- **[Fase 0b]**: La detección de `md/` pre-existente (Paso 0) es OBLIGATORIA antes de proponer conversión. Cubre 5 casos: md/ completo, md/ parcial, sin md/ con binarios, sin md/ sin binarios, md/ sin binarios visibles (requiere confirmación usuario).
- **[REFERENCIA/NORMATIVA]**: Orígenes clasificados como REFERENCIA o NORMATIVA en Fase 0a deben pasar por Paso 0 de Fase 0b con prioridad, aunque no haya binarios visibles.
- **[md/ sin binarios]**: Si `md/` existe pero los binarios originales no están, confirmar con el usuario antes de usar esos ficheros como contexto — podrían ser de otro proyecto o estar desactualizados.
- **[convert_to_md.py]**: El script ya excluye la carpeta `md/` de su búsqueda recursiva (evita re-procesar artefactos). No hay riesgo de conversión circular.

## Veredicto final

Veredicto: GO
Pendientes al cierre:
- Los 20 Markdown de Legales están en `C:\Desarrollo\documentation\SOCYALPRO\doc_referencia\Legales\md\` fuera del repo doc_ia — no se versionan aquí.
