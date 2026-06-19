# CONTEXT SNAPSHOT

## Contexto del repositorio revisado
- `scripts/convert_to_md.py` — script de conversión (antes: markitdown solo para PDF, pandoc para todo lo demás)
- `scripts/check_env.py` — verificación de entorno (antes: markitdown como opcional sin detalle de plugins)
- `.github/SHARED_INSTRUCTIONS.md` — fuente canónica de instrucciones IA
- `CLAUDE.md` — especialización Claude Code
- `.github/prompts/document_project.prompt.md` — prompt de documentación (Fase 0b)
- `.claude/commands/document-project.md` — slash command (delega al prompt, sin cambios necesarios)
- `pyproject.toml` — configuración del proyecto (Python >=3.12, ruff, mypy strict)

## Estado actual observado
- Tests: 4/4 en verde (test_check_env.py)
- Lint (ruff): limpio
- mypy strict: limpio
- markitdown 0.1.6 instalado en .venv con converters registrados para PDF, DOCX, PPTX, XLSX, XLS, HTML, CSV, EPUB, IPYNB, ZIP
- Plugins opcionales faltantes al inicio: python-docx, python-pptx, openpyxl, xlrd, mammoth

## Estado Git relevante
- Rama activa: develop
- Cambios locales pre-existentes: ninguno (working tree clean)
- Último tag / versión publicada: docs-v0.1.0

## Clasificación metodológica
- Tipo principal: refactor
- Estado real de alcance: acotado
- Consecuencia: proceder directamente

## Gate G0 · Context Ready
Veredicto: GO
Condiciones pendientes (si aplica):
- Ninguna
