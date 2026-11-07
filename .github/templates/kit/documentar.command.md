# /documentar

Documentar (o actualizar la documentación de) este proyecto con la metodología de doc_ia que
vive en `.doc_ia/`. Comando del **kit de documentación**: lo instala y lo actualiza
`kit.py sync`; no editarlo a mano.

## Qué hace

1. Lee el prompt de instancia `.ai/prompts/documentar.prompt.md` (parámetros y decisiones de
   ESTE proyecto: orígenes, alcance, generador, idioma, prioridades).
2. Aplica `.doc_ia/.github/prompts/document_project.prompt.md` con esos parámetros, siguiendo
   `.doc_ia/.claude/commands/document-project.md` y el agente
   `.doc_ia/.github/agents/documentation-generator.agent.md`.
3. `<doc_ia>` en esas instrucciones es la carpeta `.doc_ia/` de este destino (scripts en
   `.doc_ia/scripts/`).

## Argumentos (opcionales)

- **Modo**: `incremental` (por defecto si hay `.ai/doc_state.json`) | `completo` |
  `verificar` (solo `kit.py check`, `drift`, `decisions` y build) | `aplicar-decisiones`
  (fichas `COB-…` decididas, `coverage_decisions.prompt.md`) | `zip` (solo build y ZIP).
- **Alcance** o **arquetipos**: si se indican, prevalecen sobre el prompt de instancia en esta
  sesión.

Sin argumentos: modo por defecto con los parámetros del prompt de instancia, de principio a fin.

## Reglas

- Si falta `.ai/prompts/documentar.prompt.md`, crearlo desde
  `.doc_ia/.github/templates/kit/documentar.prompt.template.md` con los parámetros que dé el
  usuario (orígenes, destino, generador e idioma son obligatorios) y continuar.
- Plantillas y decisiones solo de `.doc_ia/` y de los orígenes de este proyecto: otros destinos
  documentados con doc_ia no son plantilla ni fuente de decisiones.
- Guía para personas: `DOCUMENTAR.md` en la raíz.
