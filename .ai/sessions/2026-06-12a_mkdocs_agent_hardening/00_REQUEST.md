# REQUEST

## Session metadata
- id: 2026-06-12a_mkdocs_agent_hardening
- fecha: 2026-06-12
- rama: develop
- skill: hotfix
- fase solicitada: RCA + FIX — agentes de documentación no aplican estándar mkdocs.yml

## Solicitud original saneada

Errores detectados en la documentación generada para `C:\Desarrollo\Proyectos\socyalpro\docs\`:
1. Diagramas Mermaid no se renderizan (p.ej. `docs/index.md` § Módulos principales)
2. Dark mode no disponible
3. Menú lateral izquierdo no agrupa las páginas por sección
4. El estándar de documentación definido en doc_ia no se está siguiendo

Identificar causa raíz y actualizar los agentes IA para que no vuelva a ocurrir.

## Objetivo operativo de esta sesión

1. Diagnosticar los tres defectos visuales en el `mkdocs.yml` de socyalpro.
2. Corregir `mkdocs.yml` de socyalpro y añadir los assets custom (js/css) faltantes.
3. Blindar `document_project.prompt.md` y `documentation-generator.agent.md`
   para que la Fase 5 verifique y corrija la configuración estándar en cualquier destino futuro.
4. Actualizar `DOCUMENTATION_STANDARD.md §4.1` con los ítems ausentes.

## Restricciones explícitas

- No modificar código fuente de socyalpro.
- No crear artefactos de sesión en socyalpro (solo en doc_ia).
- Los assets de socyalpro son copias directas de `doc_ia/docs/assets/` sin modificación.

## Resultado esperado

- `C:\Desarrollo\Proyectos\socyalpro\mkdocs.yml` corregido (dark mode, Mermaid CDN, nav indentado)
- `C:\Desarrollo\Proyectos\socyalpro\docs\assets\` — 4 assets copiados
- `doc_ia/.github/prompts/document_project.prompt.md` — Fase 5 con verificación estándar
- `doc_ia/.github/agents/documentation-generator.agent.md` — Fase 5 con verificación estándar
- `doc_ia/.github/DOCUMENTATION_STANDARD.md` — §4.1 actualizado
- `.ai/sessions/2026-06-12a_mkdocs_agent_hardening/` — artefactos de trazabilidad
