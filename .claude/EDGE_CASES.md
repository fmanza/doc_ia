# Casos Límite Conocidos — doc_ia

> Plantilla inicial creada en el bootstrap (2026-06-10). Se puebla con el tiempo:
> cada caso límite descubierto en sesiones de trabajo se registra aquí con su contexto.

## Formato de registro

```markdown
## [área] — Título breve

- **Síntoma**: qué se observa
- **Causa**: por qué ocurre (verificado, no especulado)
- **Tratamiento**: cómo lo maneja el código o la instrucción IA
- **Sesión**: .ai/sessions/<fecha>/ donde se descubrió
```

## Casos registrados

## [plugin MkDocs] — Plugin ZIP no encontrado al ejecutar `mkdocs build`

- **Síntoma**: `ERROR - Config value 'plugins': The "{nombre}_documentation_zip" plugin is not installed.`
  El build falla aunque el plugin fue creado e instalado correctamente.
- **Causa**: el entry point del plugin está registrado en un venv específico
  (`doc_ia\.venv\Lib\site-packages\{nombre}_docs-{versión}.dist-info`). Cuando el terminal
  no tiene ese venv activo, `mkdocs` resuelve a otro Python (p. ej.
  `C:\Users\{user}\AppData\Roaming\Python\Python314\Scripts\mkdocs.exe`) que no conoce el plugin.
  Hay múltiples `mkdocs` en el PATH del sistema; el que "gana" depende del orden del PATH
  y del venv activo en el terminal concreto.
- **Contraste con dpss**: dpss usa `egg-info` en la raíz del proyecto. Python lo descubre vía
  `''` (CWD) en `sys.path`, por lo que funciona con cualquier Python ejecutado desde ese
  directorio, sin activar ningún venv.
- **Tratamiento**:
  - Activar el venv antes del build: `doc_ia\.venv\Scripts\Activate.ps1`
  - O invocar explícitamente: `python -m mkdocs build --strict`
    (donde `python` = `doc_ia\.venv\Scripts\python.exe`)
  - Si el proyecto cambia de entorno virtual, repetir `python -m pip install -e .`
    en el nuevo entorno.
- **Sesión**: `.ai/sessions/2026-06-12/` (socyalpro, quinta pasada)
