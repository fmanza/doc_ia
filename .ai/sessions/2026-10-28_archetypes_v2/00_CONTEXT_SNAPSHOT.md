# CONTEXT SNAPSHOT

## Contexto del repositorio revisado
- `.github/DOCUMENTATION_STANDARD.md` (§1–§3.14)
- `.github/prompts/functional_doc.prompt.md`, `technical_doc.prompt.md`, `landing_doc.prompt.md`,
  `document_project.prompt.md`, `onboarding_dev.prompt.md`
- `.claude/commands/document-project.md`, `.github/agents/documentation-generator.agent.md`
- `docs/functional/archetypes.md`, `docs/api/archetypes.md`, `docs/examples/archetypes_usage.md`,
  `docs/functional/origin_types.md`, `docs/adr/ADR-001-mkdocs-material-por-defecto.md`
- `.ai/sessions/TEMPLATE/`, `.ai/sessions/INDEX.md`

## Orígenes externos consultados
Buenas prácticas (búsqueda web, 2026-10-28): arc42 (docs.arc42.org — §7 despliegue, §8
conceptos transversales, §10 calidad; secciones opcionales, 3–5 objetivos de calidad),
Diátaxis (cuadrante Reference), llms.txt (llmstxt.org), AGENTS.md, Reversa 2026 (modelo de
confianza y gaps en documentación inversa), skills `traceability-check` y RFC de drift.

## Estado actual observado
- Tests: 76 en verde (`python -m pytest -q`).
- Ruff: limpio (`scripts tests hooks`).
- Mypy: **11 errores preexistentes** en `scripts/convert_to_md.py` (docling no instalado en el
  venv → `import-not-found`, `unused-ignore`, `no-any-return`). Fuera de alcance de esta sesión.
- Discrepancia norma ↔ prompts detectada: la norma define el Arq. 1 con 5 secciones y el prompt
  con 8; la norma llama §2 del Arq. 2 "Modelo de Datos / Contratos" y el prompt "API Reference".

## Estado Git relevante
- Rama activa: develop
- Cambios locales pre-existentes: ninguno
- Último tag / versión publicada: `docs-v0.1.0` (pyproject `0.1.0`)

## Clasificación metodológica
- Tipo principal: new_feature (instrucciones IA + arquetipos)
- Estado real de alcance: pendiente de descomposición → descompuesto en P1/P2/P3
- Consecuencia: solo P1 se implementa en esta sesión

## Gate G0 · Context Ready
Veredicto: GO
Condiciones pendientes (si aplica):
- Los errores de mypy preexistentes no se corrigen aquí (requieren `pip install .[docling]` o
  ajuste de overrides en `pyproject.toml`; candidato a `/tech-debt`).
