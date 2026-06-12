# REQUEST

## Session metadata

- id: 2026-06-12-pandoc
- fecha: 2026-06-12
- rama: develop
- skill: new_feature
- fase solicitada: IMPLEMENT completo (script + docs + instrucciones IA)

## Solicitud original saneada

Actualizar la documentación IA para que cuando se encuentren documentos que no se puedan leer
se use pandoc para convertirlos a formato Markdown. Se creará una carpeta `md/` donde se dejen
los ficheros convertidos. También se actualizará la documentación del proyecto con instrucciones
claras de cómo instalar pandoc. Ejemplo en Windows: `winget install JohnMacFarlane.Pandoc`.

## Objetivo operativo de esta sesión

- Crear `scripts/convert_to_md.py`: script determinista que convierte PDF/DOCX/… a Markdown
  usando pandoc, depositando el resultado en `<origen>/md/` con estructura reflejada.
- Actualizar `scripts/check_env.py`: añadir verificación de pandoc en PATH (`missing_system_tools`).
- Actualizar `docs/installation.md`: sección pandoc con instalación por plataforma
  (Windows/macOS/Linux).
- Actualizar instrucciones IA: Fase 0b de conversión pandoc en flujo `/document-project`.

## Restricciones explícitas

- Sin API keys ni servicios IA en código Python (principio innegociable del proyecto).
- Pandoc es herramienta de sistema (no paquete Python): usar `shutil.which`, no `importlib`.
- Pandoc es opcional: su ausencia advierte pero no falla el entorno (exit 0 en check_env).
- Ruff + mypy strict + pytest deben pasar sin errores.
- `mkdocs build --strict` debe pasar sin links rotos.

## Resultado esperado

- `scripts/convert_to_md.py` creado y funcionando.
- `scripts/check_env.py` con `missing_system_tools()` nueva y tests actualizados.
- `docs/installation.md` con sección pandoc por plataforma.
- `docs/functional/convert_to_md.md` creada y enlazada en `mkdocs.yml`.
- `.github/SHARED_INSTRUCTIONS.md` y `document_project.prompt.md` con Fase 0b.
- `CLAUDE.md` con comando `convert_to_md.py` en tabla de referencia.
- Artefactos de sesión en `.ai/sessions/2026-06-12-pandoc/`.
