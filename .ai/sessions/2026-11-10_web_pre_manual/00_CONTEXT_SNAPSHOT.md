# CONTEXT SNAPSHOT

## Contexto del repositorio revisado
- `.claude/commands/document-project.md` — inputs, tipos de origen, caso degenerado sin CÓDIGO
- `.github/prompts/document_project.prompt.md` — § Origen BASE DE DATOS, Fase 0-pre,
  prioridad entre fuentes, datos personales
- `docs/functional/origin_types.md` — `UI/PANTALLAS`, `MANUAL`, `BASE DE DATOS`
- `docs/adr/ADR-002-arquetipos-con-evidencia.md` — arquetipos nuevos aplazados hasta destino real
- `.ai/sessions/2026-10-28_archetypes_v2/02_AUDIT_PLAN.md` — precedente S3 (Arq. 15/16 NO_GO temporal)
- `.github/kit/MANIFEST.txt` — kit multiplataforma
- `scripts/redact_secrets.py`, `scripts/snapshot_sources.py`, `scripts/doc_trace.py`,
  `scripts/convert_to_md.py` (OCR de imágenes con docling)
- `tests/test_docs_conformance.py` — 9 pestañas, páginas por script, registro de arquetipos

## Orígenes externos consultados
- `C:\Desarrollo\documentacion\UFV\` — destino real (solo lectura): `mkdocs.yml` con 9 pestañas
  (Inicio, Funcional, Técnica, Integraciones, Referencia, Ejemplos, Guías, Decisiones, Base de
  datos); `.ai/product.md` (kuniv 1.8.8 `master` 64c8f2ae, survey 1.2.29, BD PRE, roles).
- Web desplegada de kuniv en **PRE** — URL declarada por el usuario, no versionada. No se ha
  accedido a ella en esta sesión.

## Estado actual observado
- Sin cambios locales al inicio. No se han ejecutado tests (sesión de solo análisis).

## Estado Git relevante
- Rama activa: develop
- Cambios locales pre-existentes: ninguno
- Último tag / versión publicada: v0.10.0

## Clasificación metodológica
- Tipo principal: new_feature
- Estado real de alcance: acotado tras AUDIT_PLAN (plan reducido)
- Consecuencia: IMPLEMENT en una sesión `/new-feature` posterior

## Gate G0 · Context Ready
Veredicto: GO
Condiciones pendientes (si aplica):
- Ninguna para el análisis; las de implementación están en `02_AUDIT_PLAN.md`.
