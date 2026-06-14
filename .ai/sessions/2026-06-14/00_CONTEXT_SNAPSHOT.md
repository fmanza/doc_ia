# CONTEXT SNAPSHOT

## Contexto del repositorio revisado

- `scripts/convert_to_md.py` — script de conversión (estado anterior: pandoc-only)
- `scripts/check_env.py` — verificación de entorno
- `docs/functional/convert_to_md.md` — arquetipo funcional
- `docs/api/convert_to_md.md` — arquetipo técnico (incompleto al inicio de sesión)
- `docs/installation.md` — instrucciones de instalación
- `.github/SHARED_INSTRUCTIONS.md` — instrucciones canónicas para todos los agentes IA
- `.github/prompts/document_project.prompt.md` — prompt de documentación (Fase 0b)
- `CLAUDE.md` — especialización Claude Code

## Estado actual observado

- **Tests**: pytest --collect-only limpio (validación sintaxis).
- **Lint / mypy**: limpio al cierre (ruff E501 corregido en check_env.py durante la sesión).
- **Bug detectado**: `convert_to_md.py` listaba `.pdf` en `CONVERTIBLE_EXTENSIONS` pero llamaba a pandoc, que devuelve EXIT:21 para PDF ("Unknown input format 'pdf'"). Bug silencioso: fallaba por fichero sin detener el script.
- **markitdown**: paquete Python de Microsoft; cubre PDF, DOCX, PPTX, HTML, EPUB, CSV, JSON y más con una sola instalación pip. No requiere binario externo.
- **pandoc**: incapaz de leer PDF por diseño; sigue siendo la opción de mayor calidad para DOCX complejos, ODT y RST.

## Estado Git relevante

- Rama activa: develop
- Cambios locales pre-existentes: ninguno al inicio de sesión
- Último commit al inicio: `68c7521 docs(tooling): elevar sincronización visual MkDocs a requisito obligatorio`
- Cambios acumulados en la sesión: 9 ficheros (252 ins / 106 del)

## Clasificación metodológica

- Tipo principal: bug fix + refactor (convert_to_md.py) + docs update (instrucciones IA y arquetipo técnico)
- Estado real de alcance: acotado — todos los cambios giran en torno a la integración markitdown
- Consecuencia: commit único `feat(tooling):` con fix embebido

## Gate G0 · Context Ready

Veredicto: GO
Condiciones pendientes: ninguna
