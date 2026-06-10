# REQUEST

## Session metadata
- id: 2026-06-10
- fecha: 2026-06-10
- rama: main
- skill: new_feature (bootstrap_ai_config)
- fase solicitada: completa (ANÁLISIS → PLAN → AUDIT_PLAN → IMPLEMENT → AUDIT_CODE → VERSION)

## Solicitud original saneada
Aplicar `.github/prompts/bootstrap_ai_config.prompt.md` con:
- Origen (solo lectura): `c:\Desarrollo\python\libs\util_bbdd`
- Destino: `C:\Desarrollo\Proyectos\doc_ia`
- Lenguaje/arquitectura destino: Python tooling (scripts + docs, sin librería de negocio)
- Plataformas IA activas: Claude Code, Gemini, Copilot, Cursor, Codex
- Generador de documentación destino: Zensical/MkDocs Material
- Fase: completa

## Objetivo operativo de esta sesión
- Replicar el sistema de instrucciones IA multiplataforma de util_bbdd en doc_ia (modelo PULL).
- Clasificar cada activo del origen en capas A/B/C/D y actuar según la capa.
- Dejar las puertas de calidad en verde (ruff, mypy, pytest, mkdocs --strict).

## Restricciones explícitas
- Origen de solo lectura (no modificar util_bbdd).
- Principios de doc_ia: sin API keys, sin componentes programáticos IA, ejecución en chat.
- No copiar capa D (sesiones, changelog, caches, settings.local.json, workflows con APIs IA).

## Resultado esperado
- Canónico + 5 entry points reescritos para doc_ia.
- Método completo (agentes, prompts, commands, TEMPLATE) con comandos del destino.
- `.ai/*` regenerado desde el árbol real; sistema ZIP offline adaptado.
