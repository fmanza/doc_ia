# REQUEST

## Session metadata
- id: 2026-06-10i_example_document_project
- fecha: 2026-06-10
- rama: develop
- skill: new_feature (Arquetipo 4)
- fase solicitada: IMPLEMENT (ejemplo de uso)

## Solicitud original saneada

Crear un ejemplo de uso del proyecto.

## Objetivo operativo de esta sesión

- Crear `docs/examples/document_project_usage.md` siguiendo el Arquetipo 4 (Ejemplos de Código)
- Documentar los 3 escenarios principales del comando `/document-project`
- Sincronizar `mkdocs.yml` añadiendo la nueva entrada bajo una subsección "Flujos IA"
- Verificar build estricto sin errores

## Restricciones explícitas

- No inventar comportamiento: todo el contenido se basa en el código y documentación real del proyecto
- Seguir Arquetipo 4 exacto (5 secciones numeradas obligatorias)
- No crear archivos `.py` de soporte: el flujo `/document-project` ocurre en el chat, no en Python

## Resultado esperado

- `docs/examples/document_project_usage.md` con 3 escenarios y output esperado por fase
- `mkdocs.yml` actualizado con subsección "Flujos IA" en "Ejemplos"
- `python -m mkdocs build --strict` sin errores
