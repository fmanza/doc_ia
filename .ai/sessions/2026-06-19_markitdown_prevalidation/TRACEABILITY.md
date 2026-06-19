# TRACEABILITY

## Session metadata
- id: 2026-06-19_markitdown_prevalidation
- fecha: 2026-06-19
- rama: develop
- skill: refactor
- fase: IMPLEMENT + AUDIT_CODE

## Prompt issued
Actualizar la documentación IA para contemplar la validación previa antes de convertir con markitdown,
que está instalado y tiene disponible todos los plugins necesarios para realizar la conversión de archivos.

## Context supplied
- `scripts/convert_to_md.py` (estado anterior)
- `scripts/check_env.py` (estado anterior)
- `.github/SHARED_INSTRUCTIONS.md`
- `CLAUDE.md`
- `.github/prompts/document_project.prompt.md` (Fase 0b completa)
- `.claude/commands/document-project.md`
- `pyproject.toml`
- Listado de converters registrados en markitdown 0.1.6
- Listado de plugins instalados vs faltantes en el venv

## AI output summary
1. Inspeccionó markitdown 0.1.6: 18 converters registrados (PDF, DOCX, PPTX, XLSX, XLS, HTML, CSV, EPUB, IPYNB, ZIP, etc.)
2. Detectó plugins faltantes: python-docx, python-pptx, openpyxl, xlrd (justifica la validación previa)
3. Reescribió `scripts/convert_to_md.py`: markitdown como principal, pandoc como complemento/fallback, validación previa en 3 dimensiones, flag `--validate-only`
4. Refactorizó `validate_conversion_readiness` para reducir complejidad cognitiva (SonarLint S3776)
5. Actualizó `scripts/check_env.py`: validación granular de plugins con `check_markitdown_plugins()`
6. Actualizó `.github/SHARED_INSTRUCTIONS.md`: tabla de módulos y sección de comandos
7. Actualizó `CLAUDE.md`: sección de comandos útiles
8. Reescribió Fase 0b en `document_project.prompt.md`: nuevo Paso 2 (Validación previa obligatorio), extensiones expandidas, routing detallado, pasos renumerados 0-6
9. Verificó: ruff 0 errores, mypy strict 0 errores, pytest 4/4 tests en verde

## Artefactos generados

| Artefacto | Ruta | Estado |
|---|---|---|
| convert_to_md.py | scripts/convert_to_md.py | reescrito |
| check_env.py | scripts/check_env.py | actualizado |
| SHARED_INSTRUCTIONS.md | .github/SHARED_INSTRUCTIONS.md | actualizado |
| CLAUDE.md | CLAUDE.md | actualizado |
| document_project.prompt.md | .github/prompts/document_project.prompt.md | actualizado (Fase 0b) |

## Directrices para Futuras IAs
- **[markitdown]**: markitdown 0.1.6 registra 18 converters pero su funcionamiento real depende de plugins opcionales (python-docx, python-pptx, openpyxl, xlrd). El converter se registra aunque el plugin falte — falla en runtime, no en import. Por eso la validación previa es necesaria.
- **[convert_to_md]**: El routing de conversión sigue la cadena: markitdown (si plugin disponible) → pandoc fallback (solo DOCX/PPTX/EPUB) → pandoc only (DOC/ODT/RST) → error. pandoc NO puede leer PDF.
- **[Fase 0b]**: La validación previa (`--validate-only`) es un paso obligatorio antes de la conversión en el flujo de documentación. El agente debe proponer ejecutarla antes de `convert_to_md.py` sin flag.

## Veredicto final
Veredicto: GO
Pendientes al cierre:
- Instalar plugins opcionales de markitdown cuando se necesiten: `pip install python-docx python-pptx openpyxl xlrd`
