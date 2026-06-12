# REQUEST

## Session metadata
- id: 2026-06-12f
- fecha: 2026-06-12
- rama: develop
- skill: mejora tooling + normalización instrucciones IA

## Solicitud original saneada

Revisar por qué no se genera el fichero offline del ZIP en descargas (`downloads.md`) de los
proyectos socyalpro y doc_ia al ejecutar `mkdocs serve`, cuando en dpss sí se genera.
Actualizar lo necesario para que las instrucciones IA lo tengan en cuenta y lo hagan.
Normalizar `downloads.md` entre proyectos (estructura común con enlaces HTML directos).
Incluir siempre `start-server.py` en el ZIP de cualquier proyecto.

## Objetivo operativo de esta sesión

1. Diagnosticar el mecanismo de dpss (plugin MkDocs con `on_post_build` + egg-info en CWD)
2. Crear plugin MkDocs para doc_ia (`doc_ia_docs/`) vía `pyproject.toml` + `pip install -e .`
3. Adaptar el mismo patrón para socyalpro (`socyalpro_docs/` + `pyproject.toml`)
4. Documentar causa del error "plugin not installed" (entry point vinculado al venv)
5. Crear `scripts/start-server.py` en ambos proyectos (incluido en el ZIP)
6. Normalizar `docs/downloads.md` con estructura canónica + tabla HTML con enlaces directos
7. Actualizar instrucciones IA: SHARED_INSTRUCTIONS, document_project.prompt.md, EDGE_CASES

## Restricciones explícitas

- Cambios en doc_ia commiteados en rama `develop`
- Cambios en socyalpro gestionados de forma independiente (sin commit desde esta sesión)
- Mantener compatibilidad con venv compartido (`doc_ia/.venv`)
