# Trazabilidad — 2026-06-12g visual_sync_mandatory

## Cronología

| Acción | Resultado |
|---|---|
| Comparar `mkdocs.yml` doc_ia vs dpss | 3 problemas identificados: `navigation.sections`, sin assets, sin features/extensions |
| Leer `nav.css`, `sidebar-toggle.js`, `mermaid.js`, `mermaid.css` en doc_ia | Contenido verificado para replicar |
| Crear `docs/assets/css/` y `docs/assets/js/` en dpss | 4 archivos creados |
| Actualizar `mkdocs.yml` dpss | `navigation.sections` eliminado; `custom_dir` eliminado; features/extensions/extra_* añadidos |
| Actualizar `CLAUDE.md` doc_ia | Fase 0b añadida al flujo como OBLIGATORIO con nota explicativa |
| Actualizar `.claude/commands/document-project.md` | Sección Fase 0b → OBLIGATORIO + checklist de 5 puntos |
| Actualizar `.claude/EDGE_CASES.md` | Caso límite `navigation.sections` registrado con síntoma/causa/tratamiento |

## Tabla de artefactos

| Artefacto | Ruta | Estado |
|---|---|---|
| nav.css | `dpss/docs/assets/css/nav.css` | ✅ CREADO |
| mermaid.css | `dpss/docs/assets/css/mermaid.css` | ✅ CREADO |
| sidebar-toggle.js | `dpss/docs/assets/js/sidebar-toggle.js` | ✅ CREADO (STORAGE_KEY = `dpss_sidebar_collapsed`) |
| mermaid.js | `dpss/docs/assets/js/mermaid.js` | ✅ CREADO |
| dpss/mkdocs.yml | `dpss/mkdocs.yml` | ✅ ACTUALIZADO |
| CLAUDE.md | `doc_ia/CLAUDE.md` | ✅ ACTUALIZADO |
| document-project.md | `doc_ia/.claude/commands/document-project.md` | ✅ ACTUALIZADO |
| EDGE_CASES.md | `doc_ia/.claude/EDGE_CASES.md` | ✅ ACTUALIZADO |

## Directrices para IAs futuras

1. **Fase 0b es obligatoria**: En toda sesión `/document-project`, verificar antes de cualquier
   otra fase que el destino tiene los 4 assets y que `navigation.sections` está ausente.
2. **`navigation.sections` y `nav.css` son mutuamente excluyentes**: si coexisten, el menú
   no colapsa y el CSS de grupos no tiene efecto.
3. **`STORAGE_KEY` en `sidebar-toggle.js`**: usar el nombre del proyecto como prefijo
   (ej. `dpss_sidebar_collapsed`, `util_sidebar_collapsed`) para evitar conflictos entre proyectos.

## Veredicto

**GO** — Corrección aplicada en dpss. Requisito documentado como obligatorio en doc_ia.
