# 00_REQUEST — 2026-06-12c

## Solicitud

`downloads.md` ausente en `C:\Desarrollo\Proyectos\socyalpro\docs\` al ejecutar `/document-project`.
Actualizar documentación IA para que no vuelva a ocurrir.

## RCA

`DOCUMENTATION_STANDARD.md §4.1` marcaba `downloads.md` como condicional:
`# si el proyecto genera artefactos descargables`

Y la fila en §3.9 "Guías adicionales según tipo de proyecto" incluía `downloads.md` solo bajo
la fila "Tooling de documentación (doc_ia)", implicitando que es específico de ese tipo de proyecto.

Los agentes interpretaron la señal condicional y omitieron `downloads.md` en proyectos sin
`build_docs_zip.py`. Corrección: la página es **siempre obligatoria** con dos variantes de contenido:
- **Variante A**: proyecto tiene `scripts/build_docs_zip.py` — página completa con tabla artefacto
- **Variante B**: sin script — build local + placeholder tabla pendiente

## Restricciones

- No crear artefactos `.ai/sessions/` en el repositorio socyalpro (restricción de usuario)
- Cambios aplicados únicamente en doc_ia (instrucciones IA canónicas) y en socyalpro/docs/ (contenido)

## Ficheros origen

- `C:\Desarrollo\Proyectos\socyalpro\docs\` (defecto observado: faltaba downloads.md en el nav)
