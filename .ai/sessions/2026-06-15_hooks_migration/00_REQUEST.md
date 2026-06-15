# REQUEST

## Session metadata
- id: 2026-06-15_hooks_migration
- fecha: 2026-06-15
- rama: develop
- skill: refactor (tooling)
- fase solicitada: IMPLEMENT → DOCS UPDATE

## Solicitud original saneada

Error al ejecutar `python -m mkdocs build --strict` fuera del venv de doc_ia:
```
ERROR - Config value 'plugins': The 'socyalpro_documentation_zip' plugin is not installed
```

El usuario solicita que la ejecución de la documentación sea lo más directa posible
con las mínimas dependencias, y que sea consistente en todos los proyectos (SOCYALPRO, DPSS, doc_ia).

Petición explícita: "Necesito que la ejecución de la documentación sea siempre la misma.
Actualizar la documentación IA para que así sea."

Pregunta clave que desencadenó el dogfooding: "Como sabe C:\Desarrollo\python\libs\doc_ia
que tiene que crear el archivo mkdocs_hooks.py y donde está en este proyecto?" — el patrón
canónico debía residir en doc_ia, no en un proyecto externo.

## Objetivo operativo de esta sesión

- Eliminar la dependencia de `pip install -e .` para la generación del ZIP de documentación.
- Migrar SOCYALPRO, DPSS y doc_ia del sistema de plugins MkDocs al sistema de hooks nativos.
- Crear `doc_ia/mkdocs_hooks.py` como patrón canónico de referencia para futuras IAs.
- Actualizar instrucciones IA (SHARED_INSTRUCTIONS.md, document_project.prompt.md) para reflejar el nuevo enfoque.

## Restricciones explícitas

- Cero instalación: el hook debe funcionar con cualquier Python que tenga `mkdocs` instalado.
- La referencia canónica debe residir dentro de doc_ia (accesible a cualquier agente IA que trabaje desde las instrucciones de doc_ia).
- No cambiar el comportamiento del ZIP resultante (contenido, SHA256, start-server.py incluido).

## Resultado esperado

- `doc_ia/mkdocs_hooks.py` — hook canónico, solo cambia `zip_path` por proyecto.
- `doc_ia/mkdocs.yml` — usa `hooks:` en vez de plugin `doc_ia_documentation_zip`.
- `SHARED_INSTRUCTIONS.md` — distribución offline: plugin → hook.
- `document_project.prompt.md` — detección y pasos A2 simplificados (4 pasos → 2).
- SOCYALPRO y DPSS migrados con sus propios `mkdocs_hooks.py`.
- Artefactos residuales eliminados: `SOCYALPRO/pyproject.toml`, `SOCYALPRO/socyalpro_docs/`, `DPSS/dpss_docs.egg-info/`.
