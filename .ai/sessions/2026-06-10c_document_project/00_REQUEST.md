# REQUEST

## Session metadata
- id: 2026-06-10c
- fecha: 2026-06-10
- rama: main
- skill: new_feature (Fase 5 — pieza específica de doc_ia)
- fase solicitada: completa

## Solicitud original saneada
Fase 5 — Pieza nueva específica de doc_ia (no existe en el origen util_bbdd):

1. `.github/prompts/document_project.prompt.md` + `.claude/commands/document-project.md`:
   comando de entrada único con validación obligatoria de inputs — Origen(es) a documentar
   (rutas), Destino de la documentación (ruta), generador, idioma. Si faltan, DETENERSE
   (mismo patrón de validación que new_feature). Internamente orquesta el flujo de 7 fases
   del Documentation Generator y los arquetipos.
2. Política explícita en SHARED_INSTRUCTIONS: prohibido incrustar API keys; la ejecución IA
   ocurre siempre en el chat de la plataforma; el código Python nunca invoca servicios IA.

## Restricciones explícitas
- DRY: el comando orquesta el flujo existente del Documentation Generator, no lo duplica.
- Sincronizar gobernanza (CLAUDE.md, AGENTS.md, INTEGRATION_MAP) según checklist del canónico.
