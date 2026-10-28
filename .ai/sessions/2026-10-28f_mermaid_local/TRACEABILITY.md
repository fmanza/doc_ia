# TRACEABILITY

## Session metadata
- id: 2026-10-28f
- fecha: 2026-10-28
- rama: develop
- skill: new_feature
- fase: SPIKE + PLAN + AUDIT_PLAN + IMPLEMENT (L1, L2, L3) + cierre

## Prompt issued
1. "Dime F10, que sigue esperando a la fase F8, el motivo"
2. "No entiendo, no salen ahora los Mermaid si lo ejecuto"
3. Propuesta del agente aceptada (Mermaid local adelantado a F8) → "PLAN de esa fase"
4. "GO entero"

## Context supplied
- `.ai/sessions/2026-10-28d_zensical_migration/02_PLAN_FASES.md` (F7, F8, F10).
- Bundles instalados de mkdocs-material 9.8.0 y zensical 0.0.73.
- Paquetes npm mermaid 11.17.2 y 12.2.0 (instalados en el scratchpad para el spike de M4).
- Sesión previa `2026-10-28e_mermaid_diagrams`.

## AI output summary
- Explicación de F10 → F8: `offline` + `privacy` con MkDocs en Windows aborta en `--strict`
  (symlinks); F8 depende de F7 (Zensical 0.1, 2026-11-05) y de ≥2 semanas de paridad (C2).
- Demostración: el ZIP con red dibuja los diagramas; con unpkg bloqueado salen como código.
- Spike (scratchpad): ambos bundles usan `window.mermaid` si existe; 4 combinaciones
  generador × versión dibujan sin red; Material + v12 deja subgrafos ilegibles en oscuro y se
  corrige añadiendo `theme: "default"` a `initialize`.
- Decisiones del usuario: 12.2.0, doc_ia + producto, commit + test de versión.
- L1 `698d6bb`: copia local 12.2.0 (+ LICENSE, SOURCE.txt), `.gitattributes -text` (autocrlf
  cambiaba la huella en Windows; huella del blob en Git verificada), `mermaid-theme.js`,
  `mkdocs.yml`, `tests/test_mermaid_assets.py`, AC-10 en build_docs_zip, CI solo 12.2.0,
  downloads.md, §3.17, EDGE_CASES (dos entradas), CONTRIBUTING «Actualizar Mermaid».
  C1–C4: 24/24 diagramas sin conexión, 0 SVG de error, MkDocs y Zensical, claro y oscuro,
  también con `file://`; capturas de subgrafos legibles en ambos esquemas.
- L2 `8ae028d`: Fase 0b de 3 a 5 recursos en prompt, comando, agente, plantilla,
  docs.instructions, estándar §4, CLAUDE.md, CONTRIBUTING 5.1 y functional/document_project;
  el test cubre la plantilla.
- L3: F10 sin la parte de Mermaid (C9 cumplida); CHANGELOG, TRACEABILITY, INDEX.
- DoD en cada fase: ruff, format, mypy, pytest, drift 0, matrix, llms --check, build strict
  MkDocs y Zensical; páginas re-selladas tras revisarlas.

## Artefactos generados

| Artefacto | Ruta | Estado |
|---|---|---|
| PLAN + AUDIT_PLAN | `.ai/sessions/2026-10-28f_mermaid_local/01_PLAN_AUDIT.md` | emitido |
| Mermaid local | `docs/assets/vendor/mermaid/`, `docs/assets/js/mermaid-theme.js` | completado |
| Test | `tests/test_mermaid_assets.py` | completado (7 casos) |
| Producto Fase 0b | prompt, comando, agente, plantilla, estándar | completado |
| CI | `.github/workflows/ci.yml` job `mermaid` (12.2.0) | pendiente de primera ejecución en GitHub |

## Directrices para Futuras IAs
- **[Mermaid]**: Material y Zensical solo descargan Mermaid si `typeof mermaid=="undefined"`;
  la copia local en `extra_javascript` (antes de `mermaid-theme.js`) basta, sin `mermaid.run()`.
- **[Mermaid]**: con Mermaid 12 y Material hay que pasar `theme: "default"`; sin él los subgrafos
  son ilegibles en modo oscuro. Lo hace `mermaid-theme.js`.
- **[Git]**: ficheros de terceros cuya huella se comprueba → `.gitattributes -text`; en este repo
  `core.autocrlf=true`.
- **[Verificación offline]**: `--host-resolver-rules="MAP unpkg.com 0.0.0.0"` en Edge headless y
  contar `<div class="mermaid">` frente a los bloques del Markdown; el render del tema va en un
  shadow root cerrado, pero los SVG de error de un render duplicado quedan en el DOM ligero.
- **[Actualizar Mermaid]**: procedimiento en CONTRIBUTING; el test falla si fichero, `mkdocs.yml`,
  plantilla, CI o huella no coinciden.

## Veredicto final
Veredicto: CLOSED
Pendientes al cierre:
- Push a `develop` para la primera ejecución del job `mermaid` (no se ha hecho push ni tag).
- Los destinos existentes reciben Mermaid local al volver a ejecutar `/document-project`.
- Hotfix `&#64;` en socyalpro (sesión 2026-10-28e).
- F10 (offline/privacy para fuentes y búsqueda), tras F8.
- Versión 0.3.0 en el próximo `/version-closure`.
