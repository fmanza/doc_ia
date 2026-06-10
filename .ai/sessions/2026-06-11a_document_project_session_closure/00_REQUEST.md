# REQUEST

## Session metadata
- id: 2026-06-11a
- fecha: 2026-06-11
- rama: develop
- skill: refactor (instrucciones IA)
- fase solicitada: IMPLEMENT directo (sin PLAN previo; alcance acotado)

## Solicitud original saneada

1. Actualizar las instrucciones IA para que, al terminar una actualización o creación de
   documentación con `/document-project`, se cierre la sesión con:
   - Artefacto `.ai/sessions/YYYY-MM-DD/` en el **destino** del proyecto documentado.
   - Commit `docs(<scope>):` propuesto antes de concluir.

## Objetivo operativo de esta sesión

- Añadir paso 10 (CIERRE DE SESIÓN) al comando `.claude/commands/document-project.md`
  especificando los tres ficheros del artefacto de sesión y el formato del commit.
- Propagar el cambio al prompt multiplataforma `.github/prompts/document_project.prompt.md`.
- Actualizar la tabla de comandos en `CLAUDE.md` y la descripción en `SHARED_INSTRUCTIONS.md`.

## Restricciones explícitas

- No modificar la lógica de las fases 0-7 existentes.
- No alterar arquetipos ni DOCUMENTATION_STANDARD.md.
- El commit en el destino requiere confirmación del usuario (nunca automático).

## Resultado esperado

- `.claude/commands/document-project.md` con paso 10 completo.
- `.github/prompts/document_project.prompt.md` sincronizado (paso 10).
- `CLAUDE.md` tabla actualizada (columna Salida).
- `.github/SHARED_INSTRUCTIONS.md` nota de cierre en descripción de `/document-project`.
