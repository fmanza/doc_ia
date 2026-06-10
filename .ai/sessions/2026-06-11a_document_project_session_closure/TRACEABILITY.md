# TRACEABILITY

## Session metadata
- id: 2026-06-11a
- fecha: 2026-06-11
- rama: develop
- skill: refactor (instrucciones IA)
- fase: IMPLEMENT directo

## Prompt issued

"Actualizar las instrucciones IA: Cuando se termine con una actualización o creación de
documentación cerrar la sesión con commit y el artefacto .ai/sessions/ del destino"

## Context supplied

- `.claude/commands/document-project.md` — comando existente (9 pasos)
- `.ai/sessions/TEMPLATE/` — plantilla de artefactos de sesión
- `.ai/sessions/INDEX.md` — convención de nomenclatura y registro de sesiones
- `.github/SHARED_INSTRUCTIONS.md` — fuente canónica (descripción de `/document-project`)
- `.github/prompts/document_project.prompt.md` — prompt multiplataforma equivalente
- `CLAUDE.md` — tabla de slash commands

## AI output summary

- Leídos: `document-project.md`, `TEMPLATE/00_REQUEST.md`, `TEMPLATE/TRACEABILITY.md`,
  `TEMPLATE/00_CONTEXT_SNAPSHOT.md`, `SHARED_INSTRUCTIONS.md`, `CLAUDE.md`,
  `document_project.prompt.md`, `INDEX.md`, `version-closure.md`.
- Añadido paso **10. CIERRE DE SESIÓN** a `.claude/commands/document-project.md`:
  sub-paso a (artefacto `.ai/sessions/YYYY-MM-DD/` con 3 ficheros, usando plantilla TEMPLATE)
  y sub-paso b (commit `docs(<scope>):` con recuento páginas, requiere confirmación).
- Añadida línea "Crear siempre el artefacto…" a sección "Recomendado" de la política de cambios.
- Actualizada tabla de slash commands en `CLAUDE.md`: columna Salida añade `→ CIERRE (sesión .ai/ + commit)`.
- Actualizada descripción de `/document-project` en `SHARED_INSTRUCTIONS.md` con nota de cierre obligatorio.
- Añadido paso 10 (forma abreviada) a `.github/prompts/document_project.prompt.md`.
- Creados artefactos de sesión en `.ai/sessions/2026-06-11a_document_project_session_closure/`.
- Actualizado `INDEX.md` con la entrada de esta sesión.

## Artefactos generados

| Artefacto | Ruta | Estado |
|---|---|---|
| Paso 10 (CIERRE) en comando | `.claude/commands/document-project.md` | completado |
| Paso 10 en prompt multiplataforma | `.github/prompts/document_project.prompt.md` | completado |
| Tabla slash commands | `CLAUDE.md` | completado |
| Nota cierre en canónico | `.github/SHARED_INSTRUCTIONS.md` | completado |
| Sesión 00_REQUEST | `.ai/sessions/2026-06-11a_document_project_session_closure/00_REQUEST.md` | completado |
| Sesión TRACEABILITY | `.ai/sessions/2026-06-11a_document_project_session_closure/TRACEABILITY.md` | completado |
| Sesión COMMIT_MSG | `.ai/sessions/2026-06-11a_document_project_session_closure/COMMIT_MSG.txt` | completado |
| INDEX actualizado | `.ai/sessions/INDEX.md` | completado |

## Directrices para Futuras IAs

- **[document-project]**: El paso 10 es parte inmutable del flujo — no omitirlo aunque el
  usuario no lo pida explícitamente. El artefacto va en el **destino**, no en doc_ia,
  salvo que el destino sea el propio doc_ia.
- **[commit]**: El commit del destino siempre requiere confirmación explícita del usuario;
  nunca ejecutarlo de forma automática.
- **[sesión nomenclatura]**: Si en el mismo día ya existe una sesión `YYYY-MM-DD`, usar
  sufijos letra: `YYYY-MM-DDa`, `YYYY-MM-DDb`, etc. (véase INDEX.md para el patrón).

## Veredicto final

Veredicto: CLOSED
Pendientes al cierre:
- Ninguno. Commit pendiente de confirmación del usuario.
