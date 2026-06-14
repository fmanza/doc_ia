# REQUEST

## Session metadata
- id: 2026-06-14
- fecha: 2026-06-14 / 2026-06-15
- rama: develop
- skill: ad-hoc (bug fix + instrucciones IA)
- fase solicitada: corrección bug pandoc/PDF → integración markitdown → posicionamiento como herramienta principal

## Solicitud original saneada

1. Actualizar las instrucciones IA para recomendar markitdown a la hora de convertir archivos a Markdown.
2. Analizar si conviene unificar el proceso usando solo markitdown en lugar del esquema dual markitdown+pandoc.
3. "Lo que sí tiene sentido es hacer pandoc completamente opcional (ya lo es) y documentar que markitdown es la dependencia principal."

## Objetivo operativo de esta sesión

- Corregir bug silencioso: `scripts/convert_to_md.py` enviaba ficheros PDF a pandoc, que no puede leer PDF (EXIT:21).
- Introducir markitdown como herramienta de conversión PDF y establecer routing explícito por extensión.
- Actualizar todas las instrucciones IA y documentación del producto para reflejar la arquitectura dual y posicionar markitdown como dependencia principal.
- Completar arquetipo técnico `docs/api/convert_to_md.md` pendiente de sesión anterior.

## Restricciones explícitas

- Sin API keys ni servicios IA externos.
- Tooling determinista: ruff + mypy limpios en cada cambio.
- No crear nuevas páginas de documentación: solo actualizar las existentes.

## Resultado esperado

- `scripts/convert_to_md.py` con routing PDF→markitdown / DOCX+…→pandoc.
- `scripts/check_env.py` con markitdown como advertencia primaria.
- `docs/api/convert_to_md.md` reflejando arquitectura dual.
- `docs/installation.md` con markitdown como dependencia principal.
- Instrucciones IA actualizadas: `SHARED_INSTRUCTIONS.md`, `CLAUDE.md`, `document_project.prompt.md`.
- Artefactos `.ai/sessions/2026-06-14/` creados.
