# PLAN + AUDIT_PLAN — Pendientes tras P3

## Solicitud
"PLAN y AUDIT_PLAN de lo que queda pendiente" → "Adelante, si necesitas preguntar por algo hazlo".

## Decisiones del usuario (2026-10-28)
- **D1 GitHub Pages**: B — no publicar; `site_url` solo para sitemap y enlaces de `llms.txt`; documentarlo.
- **D2 ZIP latest con build fallido**: aceptar y documentar en `EDGE_CASES.md`.
- **C3 drift en CI**: bloqueante.

## Entregas (orden)
1. **H — `/hotfix`**: `.md` en `DOCLING_EXTENSIONS` → `convert_to_md` reconvierte Markdown ya legible.
2. **R1 — `/refactor` coherencia**: Fase 0b/0c; bootstrap (ruta Codex, Capa B con Arq. 7/8/10/12 y
   `doc_trace.py`); hook `sync_root_docs` en `settings.json.example`; §4.2 de la norma → referencia a
   `mkdocs.yml`; D1 y D2 documentados.
3. **Q2 — `/new-feature` calidad automatizada**: mypy limpio con/sin docling; `requirements-docs.txt` +
   `requirements-dev.txt`; `.github/workflows/ci.yml` (ruff, format, mypy, pytest, doc_trace drift/matrix/
   llms --check, mkdocs build --strict); `tests/test_build_docs_zip.py`; `tests/test_docs_conformance.py`.

## AUDIT_PLAN — condiciones
- C1: verificar el orden real de fases en `document_project.prompt.md` antes de renombrar.
- C2: mypy limpio con y sin docling.
- C3: drift bloqueante (decidido).
- C4: CI en verde en el primer push (no se hace push en esta sesión; se valida en local con los
  mismos comandos y Python ≥ 3.12).
- S1: `permissions: contents: read` en `ci.yml`.

Veredicto: GO_CONDICIONAL → GO tras decisiones D1/D2/C3.
