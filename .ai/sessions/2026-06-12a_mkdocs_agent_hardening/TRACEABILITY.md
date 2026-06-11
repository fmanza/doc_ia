# TRACEABILITY

## Session metadata
- id: 2026-06-12a_mkdocs_agent_hardening
- fecha: 2026-06-12
- rama: develop
- skill: hotfix
- fase: RCA → FIX (socyalpro) → AGENT UPDATE (doc_ia) → STANDARD UPDATE

## Prompt issued

```
Existen errores en la generación de documentación: en C:\Desarrollo\Proyectos\socyalpro\docs\index.md
→ Módulos principales, no sale mermaid graph, en otras páginas pasa lo mismo. Identificar la causa
y actualizar los agentes IA para que no vuelva a suceder. No se está siguiendo el mismo estándar de
documentación definido en este proyecto, no sale dark, no agrupa menú de la izquierda.
```

## Context supplied

- `C:\Desarrollo\Proyectos\socyalpro\mkdocs.yml` — configuración errónea detectada
- `C:\Desarrollo\Proyectos\socyalpro\docs\index.md` — página con bloque mermaid no renderizado
- `c:\Desarrollo\python\libs\doc_ia\mkdocs.yml` — referencia estándar correcta
- `c:\Desarrollo\python\libs\doc_ia\docs\assets\` — 4 assets fuente (js/css)
- `c:\Desarrollo\python\libs\doc_ia\.github\DOCUMENTATION_STANDARD.md` — §4.1 plantilla canónica
- `c:\Desarrollo\python\libs\doc_ia\.github\prompts\document_project.prompt.md`
- `c:\Desarrollo\python\libs\doc_ia\.github\agents\documentation-generator.agent.md`

## AI output summary

1. **RCA — Tres causas independientes identificadas:**
   - Mermaid no renderiza: faltaba `extra_javascript` con CDN `mermaid@11` y `assets/js/mermaid.js`
   - Dark mode ausente: `palette` con un solo esquema, sin `toggle` ni `scheme: slate`
   - Menú lateral no agrupa: indentación YAML `nav:` a 2 espacios extra en lugar de 4 + falta `assets/css/nav.css`
2. Reescribió `C:\Desarrollo\Proyectos\socyalpro\mkdocs.yml` con la configuración estándar completa:
   palette dual con toggle, `extra_javascript`/`extra_css`, nav con 4-space indent, extensiones
   `attr_list`, `md_in_html`, `pymdownx.snippets`, `line_spans`, `pygments_lang_class`, `plugins: search`
3. Creó los 4 assets en `docs/assets/` de socyalpro (copiados de doc_ia sin modificación):
   `js/mermaid.js`, `js/sidebar-toggle.js`, `css/mermaid.css`, `css/nav.css`
4. Amplió `document_project.prompt.md` Fase 5 con verificación de configuración estándar y assets
5. Amplió `documentation-generator.agent.md` Fase 5 con las mismas reglas de verificación
6. Actualizó `DOCUMENTATION_STANDARD.md §4.1`: añadió `sidebar-toggle.js` a `extra_javascript`
   y nota sobre indentación de 4 espacios en `nav:`

## Artefactos generados

| Artefacto | Ruta | Estado |
|---|---|---|
| mkdocs.yml corregido | `C:\Desarrollo\Proyectos\socyalpro\mkdocs.yml` | actualizado |
| mermaid.js | `C:\Desarrollo\Proyectos\socyalpro\docs\assets\js\mermaid.js` | creado |
| sidebar-toggle.js | `C:\Desarrollo\Proyectos\socyalpro\docs\assets\js\sidebar-toggle.js` | creado |
| mermaid.css | `C:\Desarrollo\Proyectos\socyalpro\docs\assets\css\mermaid.css` | creado |
| nav.css | `C:\Desarrollo\Proyectos\socyalpro\docs\assets\css\nav.css` | creado |
| document_project.prompt.md | `.github/prompts/document_project.prompt.md` | actualizado (Fase 5) |
| documentation-generator.agent.md | `.github/agents/documentation-generator.agent.md` | actualizado (Fase 5) |
| DOCUMENTATION_STANDARD.md | `.github/DOCUMENTATION_STANDARD.md` | actualizado (§4.1) |
| 00_REQUEST.md | `.ai/sessions/2026-06-12a_mkdocs_agent_hardening/00_REQUEST.md` | creado |
| TRACEABILITY.md | `.ai/sessions/2026-06-12a_mkdocs_agent_hardening/TRACEABILITY.md` | creado |

**Total doc_ia:** 3 ficheros actualizados · 2 artefactos sesión creados  
**Total socyalpro (externo):** 1 fichero actualizado · 4 assets creados

## Directrices para Futuras IAs

- **[mkdocs estándar]**: Cuando se crea o actualiza un `mkdocs.yml` en cualquier destino, la Fase 5
  de `/document-project` y del agente `documentation-generator` verifica y corrige la configuración
  estándar (§4.1 de `DOCUMENTATION_STANDARD.md`): palette dual, `extra_javascript` con CDN Mermaid,
  `extra_css` y assets. Si los assets no existen en el destino, indicarlo en RESUMEN.
- **[nav indentación]**: La indentación correcta en `nav:` de MkDocs es 4 espacios extra por nivel
  (no 2). Con 2 espacios el YAML puede parsear mal y los ítems se muestran planos en el sidebar.
- **[mermaid render]**: Sin `extra_javascript` apuntando al CDN de Mermaid Y a `assets/js/mermaid.js`
  (que hace `startOnLoad:false` + `mermaid.run()` explícito), los diagramas ````mermaid` se muestran
  como texto aunque el build `--strict` no emita ningún error.
- **[dark mode]**: La ausencia de toggle en `palette` no es un error de build; solo hay modo claro.
  Siempre generar dos entradas de palette con `media` query, `scheme: slate` para el dark y los
  iconos `material/brightness-7` / `material/brightness-4`.

## Veredicto final

Veredicto: CLOSED  
Pendientes al cierre:
- Ejecutar `python -m mkdocs build --strict` en socyalpro para verificar que los assets se resuelven correctamente (requiere entorno Python con mkdocs-material instalado)
