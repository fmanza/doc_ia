# REQUEST

## Session metadata
- id: 2026-06-10
- fecha: 2026-06-10
- rama: develop
- skill: refactor
- fase solicitada: IMPLEMENT directo (cambios de gobernanza documental, sin PLAN previo)

## Solicitud original saneada

1. Arquetipos Changelog (9) y Contribución (11) deben ser opcionales y no generarse por defecto en `/document-project`.
2. Actualizar la documentación para explicar estas necesidades con ejemplos.
3. Solucionar el build roto: enlace en `docs/contributing.md` apunta a `.github/templates/TEMPLATE_mkdocs.yml` fuera de `docs/`.
4. Actualizar las instrucciones IA para que los ficheros raíz (`CHANGELOG.md`, `CONTRIBUTING.md`, …) se sincronicen automáticamente con la documentación de forma genérica.

## Objetivo operativo de esta sesión

- Marcar arquetipos 9 y 11 como opt-in en todas las fuentes canónicas (comando, estándar, CLAUDE.md, docs/).
- Documentar en los ejemplos cómo activarlos explícitamente.
- Corregir el enlace roto que impedía `mkdocs build --strict`.
- Documentar el patrón `hooks/sync_root_docs.py` en las instrucciones IA: fuente de verdad en raíz, copias en `docs/` son artefactos generados, cómo extender con nuevos ficheros.

## Restricciones explícitas

- No modificar la funcionalidad del script `hooks/sync_root_docs.py`.
- No tocar arquetipos 1–8 ni 10.
- `docs/changelog.md` y `docs/contributing.md` son artefactos generados: no editarlos directamente.

## Resultado esperado

- Build `python -m mkdocs build --strict` sin errores ni warnings.
- Instrucciones IA (SHARED_INSTRUCTIONS, CLAUDE.md, sync.instructions.md) reflejan el patrón de sync.
- Documentación de arquetipos y ejemplos actualizada con política opt-in y Escenario 5.
