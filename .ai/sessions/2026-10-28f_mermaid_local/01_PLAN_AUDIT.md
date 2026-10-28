# PLAN + AUDIT_PLAN — Mermaid servido en local

## Spike (scratchpad, sin tocar el repo)
- Los bundles de Material 9.8.0 y Zensical 0.0.73 solo descargan de unpkg si
  `typeof mermaid=="undefined"||mermaid instanceof Element`; si existe `window.mermaid`, lo usan y
  siguen llamando a `initialize`/`render` con su `themeCSS`.
- `dist/mermaid.min.js` es un único fichero sin cargas dinámicas (11.17.2: 3,4 MB; 12.2.0: 5,2 MB).
- Inyectado tras el bundle, las 4 combinaciones (Material/Zensical × 11/12) dibujan sin conexión
  (unpkg bloqueado) en secuencia, estados y flowchart con subgrafos; 0 SVG de error en el DOM.
- Material + v12: subgrafos con fondos pastel e ilegibles en oscuro (v12 cambió el tema por
  defecto). Zensical pasa `theme: "default"` y no lo sufre. Arreglo verificado: envolver
  `mermaid.initialize` añadiendo `theme: "default"` y `dropShadow: none`.

## D1
`docs/assets/js/mermaid-theme.js`: `startOnLoad:false` inmediato + envoltorio de `initialize`.

## Fases
| Fase | Contenido |
|---|---|
| L1 | Fichero 12.2.0 + LICENSE + SOURCE en `docs/assets/vendor/mermaid/`, `.gitattributes -text`, `mermaid-theme.js`, `mkdocs.yml`, `tests/test_mermaid_assets.py`, AC en build_docs_zip, matriz CI 12.2.0, downloads.md, §3.17, EDGE_CASES, CONTRIBUTING |
| L2 | Producto: Fase 0b de 3 a 5 recursos (prompt, comando, agente, plantilla, docs.instructions, estándar §4, CLAUDE.md, CONTRIBUTING 5.1, functional/document_project) |
| L3 | F10 sin la parte de Mermaid; CHANGELOG, TRACEABILITY, INDEX |

## AUDIT_PLAN — GO_CONDICIONAL
- L1: C1 24 diagramas legibles sin red (MkDocs y Zensical, claro y oscuro); C2 sin peticiones a
  unpkg; C3 0 SVG de error; C4 el `startOnLoad:false` temprano no pisa la configuración del tema.
- L2, L3: GO.
- Riesgos: carrera `startOnLoad` (mitigada en `mermaid-theme.js`), cambio futuro del cargador del
  tema (test sobre el bundle instalado), tamaño (+5,2 MB), JS de terceros (versión exacta,
  SHA256 fijada, MIT, mismo fichero que valida CI).
