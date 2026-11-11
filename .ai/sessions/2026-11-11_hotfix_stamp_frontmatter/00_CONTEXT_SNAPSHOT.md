# CONTEXT SNAPSHOT

## Contexto del repositorio revisado
- `scripts/doc_trace.py` (`stamp_page`, `format_frontmatter`, `read_page_meta`, `FRONTMATTER_RE`)
- `tests/test_doc_trace.py` (`_register_repo`, tests de sellado)
- Destino UFV: `docs/decisiones/web_decisiones.md` (caso real)

## Estado actual observado
- `develop` = `main` = `515b3a5` (0.11.2 publicada). 502 tests en verde.
- Claves de frontmatter fuera de las que gestiona `stamp`: `ambito` (registros), metadatos MADR
  (ADR) y JSON generado de `docs/bd/` (UFV, no se sella).

## Estado Git relevante
- Rama activa: develop
- Cambios locales pre-existentes: ninguno
- Último tag / versión publicada: v0.11.2

## Clasificación metodológica
- Tipo principal: hotfix
- Estado real de alcance: acotado
- Consecuencia: fix en una función + test

## Gate G0 · Context Ready
Veredicto: GO
Condiciones pendientes (si aplica):
- Ninguna
