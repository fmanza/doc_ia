# TRACEABILITY

## Session metadata
- id: 2026-06-15_hooks_migration
- fecha: 2026-06-15
- rama: develop
- skill: refactor (tooling)
- fase: RCA → IMPLEMENT → IA_DOCS_UPDATE → DOGFOODING_DOC_IA → CIERRE

## Prompt issued

"Estoy ejecutando fuera del entorno actual, python -m mkdocs build --strict, da el siguiente error:
ERROR - Config value 'plugins': The 'socyalpro_documentation_zip' plugin is not installed"

"Necesito que la ejecución de la documentación sea siempre la misma. Actualizar la documentación
IA para que así sea. Eliminar C:\Desarrollo\documentation\DPSS\dpss_docs.egg-info"

"Como sabe C:\Desarrollo\python\libs\doc_ia que tiene que crear el archivo mkdocs_hooks.py
y donde está en este proyecto?"

"Actualizar .ai\sessions. Preparar mensaje para subir código a GitHub, solo mensaje."

## Context supplied

- `C:\Desarrollo\documentation\SOCYALPRO\pyproject.toml` — entry points del plugin
- `C:\Desarrollo\documentation\SOCYALPRO\socyalpro_docs\docs_build_plugin.py` — implementación plugin
- `C:\Desarrollo\documentation\DPSS\setup.py` — registro entry points DPSS
- `C:\Desarrollo\documentation\DPSS\dpss_docs.egg-info\` — discovery setuptools sin instalación
- `doc_ia/doc_ia_docs/docs_build_plugin.py` — plugin doc_ia (existente, no migrado aún)
- `doc_ia/.github/prompts/document_project.prompt.md` — instrucciones de generación ZIP
- `doc_ia/.github/SHARED_INSTRUCTIONS.md` — distribución offline

## AI output summary

- **RCA (SOCYALPRO)**: Plugin `socyalpro_documentation_zip` registrado vía `pyproject.toml` en `c:\Desarrollo\python\libs\doc_ia\.venv` → falla en cualquier otro entorno Python.
- **RCA (DPSS)**: `dpss_docs.egg-info/` comprometido en git → setuptools lo descubría desde CWD sin `pip install`. Workaround frágil eliminado.
- **Diseño de la solución**: Hook MkDocs nativo (`hooks:` key) carga el fichero Python directamente; la función `on_post_build(config, **kwargs)` no requiere instalación ni registro.
- **SOCYALPRO migrado**: `mkdocs_hooks.py` creado, `mkdocs.yml` actualizado (plugin→hook), `pyproject.toml` y `socyalpro_docs/` eliminados.
- **DPSS migrado**: `mkdocs_hooks.py` creado, `mkdocs.yml` actualizado (plugin→hook), `dpss_docs.egg-info/` eliminado.
- **Instrucciones IA actualizadas** (primera iteración): `SHARED_INSTRUCTIONS.md` y `document_project.prompt.md` actualizados apuntando a `socyalpro/mkdocs_hooks.py` como referencia.
- **Defecto identificado por el usuario**: La referencia apuntaba a un proyecto externo inaccesible para un agente IA nuevo que solo tiene doc_ia en contexto.
- **Dogfooding doc_ia**: `mkdocs_hooks.py` creado en doc_ia como patrón canónico; `mkdocs.yml` migrado (elimina `doc_ia_documentation_zip`, añade `mkdocs_hooks.py` a `hooks:`).
- **Instrucciones IA corregidas** (segunda iteración): Referencias actualizadas a `doc_ia/mkdocs_hooks.py` en `SHARED_INSTRUCTIONS.md` y `document_project.prompt.md`; pasos A2 reducidos de 4 a 2.

## Artefactos generados

| Artefacto | Ruta | Estado |
|---|---|---|
| Hook canónico doc_ia | `doc_ia/mkdocs_hooks.py` | CREADO |
| mkdocs.yml doc_ia | `doc_ia/mkdocs.yml` | ACTUALIZADO (plugin→hook) |
| SHARED_INSTRUCTIONS.md | `doc_ia/.github/SHARED_INSTRUCTIONS.md` | ACTUALIZADO (§ distribución offline) |
| document_project.prompt.md | `doc_ia/.github/prompts/document_project.prompt.md` | ACTUALIZADO (detección + pasos A2) |
| Hook SOCYALPRO | `SOCYALPRO/mkdocs_hooks.py` | CREADO |
| mkdocs.yml SOCYALPRO | `SOCYALPRO/mkdocs.yml` | ACTUALIZADO |
| socyalpro_docs/ | `SOCYALPRO/socyalpro_docs/` | ELIMINADO |
| pyproject.toml SOCYALPRO | `SOCYALPRO/pyproject.toml` | ELIMINADO |
| Hook DPSS | `DPSS/mkdocs_hooks.py` | CREADO |
| mkdocs.yml DPSS | `DPSS/mkdocs.yml` | ACTUALIZADO |
| dpss_docs.egg-info/ | `DPSS/dpss_docs.egg-info/` | ELIMINADO |

*Nota: Los artefactos de SOCYALPRO y DPSS pertenecen a sus repositorios respectivos.*

## Directrices para Futuras IAs

- **[mkdocs-hooks]**: El patrón canónico para ZIP offline es `doc_ia/mkdocs_hooks.py`. Solo cambiar `zip_path` para otro proyecto. No crear plugins MkDocs ni pyproject.toml.
- **[mkdocs-hooks]**: El hook se activa añadiendo `hooks: [mkdocs_hooks.py]` en `mkdocs.yml`. No requiere ninguna instalación. Funciona con cualquier Python que tenga `mkdocs` instalado, incluso sin activar el venv de doc_ia.
- **[doc_ia_docs/]**: El paquete `doc_ia_docs/` (`__init__.py` + `docs_build_plugin.py`) sigue existiendo en disco pero ya no está referenciado en `mkdocs.yml`. Es código muerto — se puede eliminar en una sesión de limpieza posterior.
- **[document_project.prompt.md]**: La señal de detección de ZIP offline ya no es `{nombre}_docs/docs_build_plugin.py` sino `mkdocs_hooks.py`. El paso A2 ahora tiene solo 2 subesteps (crear hook + añadir a mkdocs.yml), sin pyproject.toml ni pip install.
- **[referencia canónica]**: Las instrucciones IA deben referenciar siempre ficheros dentro de doc_ia. Referencias a proyectos externos (SOCYALPRO, DPSS) son inaccesibles para agentes IA que solo tienen doc_ia en contexto.

## Veredicto final

Veredicto: CLOSED
Pendientes al cierre:
- `doc_ia/doc_ia_docs/` (código muerto) — eliminar en sesión de limpieza posterior si se desea
