# REQUEST

## Session metadata
- id: 2026-06-15b_dogfooding_hooks_migration
- fecha: 2026-06-15
- rama: develop
- skill: document_project (dogfooding)
- fase solicitada: INVENTARIO → GENERACIÓN → REVISIÓN

## Solicitud original saneada

Revisar documentación con las instrucciones IA y actualizar lo que falta teniendo en cuenta
las propias instrucciones IA (este proyecto se alimenta de ello). Profundizar para disponer
de la mayor información posible.

Origen: C:\Desarrollo\python\libs\doc_ia
Destino: C:\Desarrollo\python\libs\doc_ia\docs
Generador: mkdocs-material
Idioma: es

## Objetivo operativo de esta sesión

- Reflejar en la documentación la migración de plugin MkDocs → hook MkDocs completada en la sesión anterior (2026-06-15_hooks_migration).
- Actualizar `docs/downloads.md`: ya no hay plugin ni pip install.
- Actualizar `functional/build_docs_zip.md`, `api/build_docs_zip.md` y `examples/build_docs_zip_offline.md`: documentar los dos mecanismos complementarios (hook + script).
- Actualizar `ai-config/claude.md`: EDGE_CASES.md ya no está vacío.
- Actualizar `.claude/EDGE_CASES.md`: añadir solución definitiva (hook) al caso del plugin.

## Restricciones explícitas

- Seguir los arquetipos formales (§1-§5); secciones fijas siempre presentes.
- No inventar comportamientos no presentes en el código fuente (`mkdocs_hooks.py`, `build_docs_zip.py`).
- No modificar código fuente del origen — solo documentación y navegación.
- Prohibido usar APIs externas de IA para generar contenido.

## Resultado esperado

- 6 artefactos actualizados con cobertura del hook `mkdocs_hooks.py`.
- `mkdocs.yml` sin cambios (nav ya correcta).
- Artefactos de sesión en `.ai/sessions/2026-06-15b_dogfooding_hooks_migration/`.
