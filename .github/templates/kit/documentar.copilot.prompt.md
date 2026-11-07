---
mode: agent
description: "Documentar este proyecto con la metodología de doc_ia del kit (.doc_ia/)"
---

# documentar

Kit de documentación de doc_ia (lo instala y actualiza `kit.py sync`; no editar a mano).

1. Lee el prompt de instancia `.ai/prompts/documentar.prompt.md`: parámetros y decisiones de
   ESTE proyecto.
2. Aplica `.doc_ia/.github/prompts/document_project.prompt.md` con esos parámetros y el agente
   `.doc_ia/.github/agents/documentation-generator.agent.md`. `<doc_ia>` = `.doc_ia/`.
3. Modo opcional en el mensaje: `incremental` (por defecto) | `completo` | `verificar` |
   `aplicar-decisiones` | `zip`.

Guía para personas: `DOCUMENTAR.md`. Plantillas y decisiones solo de `.doc_ia/` y de los
orígenes de este proyecto.
