# REQUEST

## Session metadata
- id: 2026-06-19_markitdown_prevalidation
- fecha: 2026-06-19
- rama: develop
- skill: refactor
- fase solicitada: Actualizar documentación IA y script de conversión para validación previa con markitdown

## Solicitud original saneada
Actualizar la documentación IA para contemplar la validación previa antes de convertir con markitdown,
que está instalado y tiene disponible todos los plugins necesarios para realizar la conversión de archivos.
Validación completa: extensiones soportadas + herramientas disponibles + integridad del fichero.

## Objetivo operativo de esta sesión
- Expandir markitdown como conversor principal (no solo PDF) en `scripts/convert_to_md.py`
- Implementar validación previa en 3 dimensiones (extensiones, plugins, integridad) con flag `--validate-only`
- Actualizar `scripts/check_env.py` con validación granular de plugins de markitdown
- Sincronizar toda la documentación IA: SHARED_INSTRUCTIONS.md, CLAUDE.md, document_project.prompt.md

## Restricciones explícitas
- Solo documentación IA y scripts de tooling — no tocar código funcional del producto
- Mantener pandoc como complemento (DOC/ODT/RST) y fallback (DOCX/PPTX/EPUB)
- ruff, mypy strict y pytest deben pasar sin errores

## Resultado esperado
- `scripts/convert_to_md.py` con validación previa y markitdown como conversor principal
- `scripts/check_env.py` con detalle de plugins de markitdown
- Documentación IA actualizada: Fase 0b con paso de validación obligatorio
- Sesión `.ai/sessions/2026-06-19_markitdown_prevalidation/` con artefactos de trazabilidad
