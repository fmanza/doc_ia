# CONTEXT SNAPSHOT

## Contexto del repositorio revisado

- `.github/SHARED_INSTRUCTIONS.md` — fuente canónica de reglas
- `.github/prompts/document_project.prompt.md` — prompt principal afectado
- `.github/prompts/bootstrap_ai_config.prompt.md` — revisado (sin cambios; ya cubre Capa B)
- `CLAUDE.md` — entry point Claude Code afectado (DRY)
- `util_bbdd/scripts/build_docs_zip.py` — script de referencia del patrón a reconocer
- `util_bbdd/dist/CHECKSUMS.txt` — evidencia de uso real del patrón
- `util_bbdd/docs/downloads.md` — página de descargas de referencia
- `util_bbdd/.github/SHARED_INSTRUCTIONS.md` — confirmado: el patrón no está documentado aquí como instrucción IA

## Estado actual observado

- Sin cambios previos pendientes en la rama `develop` antes de esta sesión.
- `mkdocs serve` activo en terminal `mkdocs`.
- `util_bbdd` versión `0.10.0`; `dist/CHECKSUMS.txt` con 5 entradas históricas.
- El patrón ZIP offline está completamente implantado en `util_bbdd` pero invisible para las instrucciones IA de `doc_ia`.

## Estado Git relevante

- Rama activa: develop
- Cambios locales pre-existentes: ninguno relevante a esta sesión
- Último tag / versión publicada: consultar `pyproject.toml`

## Clasificación metodológica

- Tipo principal: new_feature (extensión de capacidad de detección del flujo documental)
- Estado real de alcance: acotado — 3 ficheros, sin código Python, sin tests
- Consecuencia: IMPLEMENT directo tras AUDIT_PLAN aprobado

## Gate G0 · Context Ready

Veredicto: GO
Condiciones pendientes (si aplica):
- Ninguna
