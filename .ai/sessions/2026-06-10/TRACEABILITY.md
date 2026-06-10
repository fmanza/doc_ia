# TRACEABILITY

## Session metadata
- id: 2026-06-10
- fecha: 2026-06-10
- rama: develop
- skill: refactor
- fase: IMPLEMENT + BUILD_VERIFY

## Prompt issued

> "Los Arquetipos Contribuir y Changelog tienen que ser opcionales y por defecto no generarlos"
> "Actualizar documentación para explicar estas últimas necesidades y poner ejemplos"
> "Solucionar: El build falla por un enlace roto en docs/contributing.md"
> "Actualizar las instrucciones IA para que estos ficheros se actualicen automáticamente, de forma genérica todo lo que quede fuera debe sincronizarse automáticamente con la documentación"

## Context supplied

- `CLAUDE.md` — instrucciones del proyecto
- `.claude/commands/document-project.md` — comando de entrada
- `.github/DOCUMENTATION_STANDARD.md` — estándar de arquetipos
- `.github/instructions/sync.instructions.md` — reglas de sincronización
- `.github/SHARED_INSTRUCTIONS.md` — instrucciones canónicas
- `hooks/sync_root_docs.py` — script de sincronización
- `.claude/settings.json` — hooks PostToolUse configurados
- `docs/functional/archetypes.md`, `docs/api/archetypes.md`, `docs/examples/archetypes_usage.md`, `docs/examples/document_project_usage.md`

## AI output summary

- Marcados arquetipos 9 y 11 como `*(opt-in)*` en `.claude/commands/document-project.md` (input Arquetipos), `.github/DOCUMENTATION_STANDARD.md` (tabla "Conjunto mínimo" + §4.3) y `CLAUDE.md` (tabla de arquetipos).
- `docs/functional/archetypes.md`: nueva regla de negocio "Arquetipos 9 y 11 opt-in", diagrama Mermaid Q9/Q11 reescritos con ramificación opt-in, tabla de arquetipos con `*(opt-in)*`, AC-05/AC-07 actualizados para reflejar que no se generan sin solicitud explícita.
- `docs/api/archetypes.md`: API pública con `*(opt-in)*` en filas 9/11; nuevo caso especial en errores.
- `docs/examples/archetypes_usage.md`: nota opt-in añadida en §3 con referencia cruzada.
- `docs/examples/document_project_usage.md`: Escenario 5 (3 variantes: solo changelog, solo contribución, ambos); parámetro `Arquetipos` explicado en §3.
- Diagnóstico enlace roto: `CONTRIBUTING.md` raíz línea 104 usaba hipervínculo a `.github/templates/TEMPLATE_mkdocs.yml`; el hook `sync_root_docs` lo copiaba a `docs/contributing.md`; MkDocs en modo `--strict` rechaza rutas fuera de `docs_dir`. Fix: hipervínculo → code span. Build limpio verificado.
- `.github/instructions/sync.instructions.md`: `applyTo` ampliado; nueva sección "Patrón de sincronización raíz → docs/": tabla fuente/artefacto, cuándo se ejecuta el sync, cómo añadir ficheros a `PAIRS`, restricciones de hipervínculos; sección 2 del checklist reescrita como "no editar directamente".
- `.github/SHARED_INSTRUCTIONS.md`: `hooks/` añadido al árbol de arquitectura y tabla de responsabilidades; nueva sección "Artefactos generados — nunca editar directamente".
- `CLAUDE.md`: árbol de configuración con `hooks/`; orden real de PostToolUse (sync primero → ruff → mypy → pytest); regla crítica de sync inline.
- Build `python -m mkdocs build --strict` verificado limpio al final de la sesión.

## Artefactos generados

| Artefacto | Ruta | Estado |
|---|---|---|
| Política opt-in arquetipos 9/11 | `.claude/commands/document-project.md` | completado |
| Política opt-in arquetipos 9/11 | `.github/DOCUMENTATION_STANDARD.md` | completado |
| Política opt-in arquetipos 9/11 | `CLAUDE.md` | completado |
| Docs funcional arquetipos | `docs/functional/archetypes.md` | completado |
| Docs API arquetipos | `docs/api/archetypes.md` | completado |
| Ejemplo arquetipos individuales | `docs/examples/archetypes_usage.md` | completado |
| Ejemplo document-project | `docs/examples/document_project_usage.md` | completado |
| Fix enlace roto | `CONTRIBUTING.md` | completado |
| Instrucciones sync raíz→docs/ | `.github/instructions/sync.instructions.md` | completado |
| Arquitectura + regla artefactos | `.github/SHARED_INSTRUCTIONS.md` | completado |
| Hooks + regla artefactos | `CLAUDE.md` | completado |

## Directrices para Futuras IAs

**[arquetipos]**: Los arquetipos 9 (Changelog) y 11 (Contribución) son opt-in explícito en `/document-project`; no se generan por defecto aunque el proyecto tenga releases o acepte contribuciones. Activarlos con `Arquetipos: changelog` o `Arquetipos: contribución`.

**[sync-hook]**: `docs/changelog.md` y `docs/contributing.md` son artefactos generados por `hooks/sync_root_docs.py`. Nunca editarlos directamente — editar siempre `CHANGELOG.md` o `CONTRIBUTING.md` en la raíz. El hook `PostToolUse` los sincroniza automáticamente tras cada Edit/Write.

**[sync-links]**: Los hipervínculos Markdown dentro de `CHANGELOG.md` y `CONTRIBUTING.md` no pueden apuntar a rutas fuera de `docs/` (p.ej. `.github/templates/`). Usar solo `code span` para referenciar esas rutas; de lo contrario `mkdocs build --strict` falla.

**[sync-extensión]**: Para añadir un nuevo fichero raíz al sync: (1) tupla en `PAIRS` en `hooks/sync_root_docs.py`, (2) entrada en `nav:` de `mkdocs.yml`. Ver `.github/instructions/sync.instructions.md`.

**[hooks-orden]**: El orden real de PostToolUse en `settings.json` es: sync_root_docs → ruff → mypy → pytest. CLAUDE.md tenía el orden incorrecto (sin sync, con paths incorrectos); ya corregido en esta sesión.

## Veredicto final

Veredicto: CLOSED
Pendientes al cierre:
- Ninguno. Build limpio. Todos los cambios verificados.
