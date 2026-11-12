# IMPLEMENT — Paridad Zensical, F7 y Zensical como generador único

Prompt: «IMPLEMENT» (2026-11-12). D5, D6 y B6 no se respondieron explícitamente: se aplicaron
las opciones recomendadas en el plan (nombres heredados `mkdocs.yml`/`mkdocs_hooks.py`;
migración explícita de destinos con guarda de plugins; `--builder zensical` aceptado una versión
y `--builder mkdocs` → código 2).

## Commits (rama `develop`, sin push)

| Fase | Commit | Contenido |
|---|---|---|
| P1 | `7199613` | `fix(docs)`: `extra.homepage: index.html` (mkdocs.yml, plantilla, estándar, Fase 0b); `_is_folder` detecta `.` y `..`; tests y EDGE_CASES |
| P2 (F7) | `b63cf2d` | `build(deps)`: Zensical 0.1.1 + zensical-ui 0.0.42; test de Mermaid sobre `zensical_ui`; plugins `optimize` y `meta-descriptions`; evidencias COB-BUILDZIP-002/003 re-verificadas |
| VERSION | `1599b04` | `release: v0.11.4` |
| Z1 | `b6ee093` | `feat(build)!`: pipeline solo Zensical, `--builder mkdocs` → 2, check_env exige zensical, requisitos sin MkDocs, mkdocs.yml sin `hooks:`, CI bloqueante sin paridad, workflows de release, ADR-003 ACEPTADO / ADR-001 REEMPLAZADO, docs de build_docs_zip y check_env (AC-14 reescrito, AC-16 nuevo), EDGE_CASES «Histórico (MkDocs)» |
| Z2 | `4c6e3cb` | `docs`: instrucciones de las plataformas IA, `.github/instructions`, `.ai/`, README, CONTRIBUTING, VER_DOCUMENTACION y documentación propia |
| Z3 | `5fd6ce0` | `feat(prompts)!`: `/document-project` sin campo generador, migración de destinos MkDocs con guarda de plugins, agentes, estándar, plantillas, kit, páginas de producto; tests de conformidad y guarda `test_no_mkdocs.py` |
| Z5 | (este commit) | CHANGELOG, trazabilidad de esta sesión y de `2026-10-28d_zensical_migration` |

Z2 y Z3 los redactaron dos subagentes en paralelo sobre ficheros disjuntos; la revisión, la
coherencia entre ambos (se quitaron las líneas `Generador: zensical` que Z2 dejó en los ejemplos),
los re-sellados y los commits se hicieron en el hilo principal.

## Condiciones del plan

- **C-a** (notas de versión 0.0.74-0.1.1): leídas; sin breaking changes; `hooks:` sigue sin
  soporte; `privacy` soportado desde 0.0.72; `mkdocs.yml` se sigue leyendo; 0.1.0 abre una beta de
  3 meses.
- **C-b** (Mermaid sin conexión con 0.1.1): **verificada por muestra**. Edge headless por
  `file://` con unpkg y jsDelivr bloqueados: 3 diagramas de `architecture` en claro y 3 de
  `api/doc_trace` en oscuro dibujados, sin iconos de error. `--dump-dom` no da salida en este
  entorno, así que no se repitió el recuento 24/24 de la sesión 2026-10-28f.
- **C3** (revisión visual Zensical 0.1.1): portada (claro), descargas (oscuro, admonitions,
  bloques de código, pie «Made with Zensical»), mapa funcional (oscuro, tablas, pestañas, barra
  lateral, TOC) y móvil (400 px). En móvil la captura sale cortada a la derecha **igual con MkDocs**
  (artefacto del navegador sin ventana). **Pendiente de revisión humana**: búsqueda por `file://`
  y móvil en un dispositivo real, antes de publicar v0.12.0.
- **C10** (0 enlaces a carpeta): garantizada por `_is_folder` en cada build.

## Verificación (DoD)

- ruff, `ruff format --check`, mypy strict y pytest en verde tras cada fase.
- `.venv` sin MkDocs (desinstalado: `mkdocs`, `mkdocs-material`, `mkdocs-material-extensions`,
  `mkdocs-get-deps`, `ghp-import`, `mergedeep`, `pyyaml_env_tag`, `paginate`): el pipeline real
  `python scripts/build_docs_zip.py` termina con 0 y genera el ZIP `latest`.
- `doc_trace.py drift` sin drift, `decisions` sin hallazgos, `llms --check` al día, `matrix` sin
  criterios sin test.
- `test_no_mkdocs.py`: sin comandos ni paquetes MkDocs fuera del histórico.

## Z4 (F10 reducida) — no implementada

`use_directory_urls: false`, `offline` y el shim local ya están desde `a43ebcc`; el texto de la
release ya describe el uso sin conexión. Queda una **decisión del usuario**: añadir el plugin
`privacy` (Zensical lo soporta) para que también las fuentes tipográficas vayan en el ZIP, a
cambio de descargas de terceros durante el build en CI. Sin decisión no se toca.

## Pendientes para el usuario

1. COB-BUILDZIP-001 («hook ejecutado antes del aborto por `--strict`», solo MkDocs): la evidencia
   ya indica que el caso no se da desde ADR-003; **decidir** si se reclasifica (p. ej. `No aplica`).
2. Revisión humana de C3 (búsqueda por `file://`, móvil real).
3. Decisión Z4 (`privacy`).
4. VERSION v0.12.0 (`/version-closure`): commit `release`, merge a `main`, tag y push por
   separado y con confirmación.
5. Tras el push, comprobar que la CI (ahora con build Zensical bloqueante) pasa en 3.12 y 3.14.
