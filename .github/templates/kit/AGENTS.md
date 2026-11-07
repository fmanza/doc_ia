# Instrucciones para agentes — repositorio de documentación

Este repositorio es un **destino de documentación** generado con doc_ia. Fichero del kit de
documentación (lo instala y actualiza `kit.py sync`; no editar a mano).

Para documentar o actualizar la documentación («documentar», «actualiza la documentación»):

1. Lee `.ai/prompts/documentar.prompt.md` (parámetros y decisiones de este proyecto).
2. Aplica `.doc_ia/.github/prompts/document_project.prompt.md` con esos parámetros y el agente
   `.doc_ia/.github/agents/documentation-generator.agent.md`. `<doc_ia>` = `.doc_ia/`.
3. Modo opcional: `incremental` (por defecto) | `completo` | `verificar` |
   `aplicar-decisiones` | `zip`.

Reglas: la generación ocurre en el chat (sin API keys ni servicios IA desde código); plantillas
y decisiones solo de `.doc_ia/` y de los orígenes de este proyecto. Guía: `DOCUMENTAR.md`.
