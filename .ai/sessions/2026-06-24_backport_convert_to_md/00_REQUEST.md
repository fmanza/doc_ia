# REQUEST

## Session metadata
- id: 2026-06-24_backport_convert_to_md
- fecha: 2026-06-24
- rama: develop
- skill: refactor (tooling)
- fase solicitada: IMPLEMENT → DOCS UPDATE

## Solicitud original saneada

Portar la lógica de scripts de `doc_calidad/scripts/` a `doc_ia/scripts/`, con especial
atención en `convert_to_md.py`. doc_calidad ha evolucionado significativamente y ahora
supera a doc_ia en funcionalidad (motor triple docling+markitdown+pandoc, CUDA, OCR,
batch, chunking RAG, metadata frontmatter).

Actualizar también `check_env.py` (añadir verificación de docling), `pyproject.toml`
(dependencias opcionales) y toda la documentación asociada.

## Objetivo operativo de esta sesión

- Reemplazar `convert_to_md.py` con la versión de doc_calidad (900+ líneas, motor triple).
- Preservar `--validate-only` exclusivo de doc_ia (no existe en doc_calidad).
- Portar los 65 tests unitarios de doc_calidad y añadir tests de `--validate-only`.
- Actualizar `check_env.py` con verificación de docling como opcional.
- Actualizar `pyproject.toml` con dependencias opcionales (`docling`, `markitdown`, `all-engines`).
- Actualizar documentación: funcional, API, ejemplos, instalación, troubleshooting, check_env.
- Actualizar `CLAUDE.md` con los nuevos comandos `--engine`.

## Restricciones explícitas

- No romper la CLI existente: `--dry-run` y `--validate-only` deben seguir funcionando.
- Docling es opcional: el script debe funcionar sin docling instalado.
- Python ≥ 3.12; Conventional Commits en español.
- No portar `dedup_docs.py` (QMS-específico).
- Hooks PostToolUse: ruff + mypy + pytest deben pasar.

## Resultado esperado

- `scripts/convert_to_md.py` — versión de doc_calidad + `--validate-only` de doc_ia.
- `scripts/__init__.py` — necesario para imports de tests.
- `tests/test_convert_to_md.py` — 72 tests (65 portados + 5 validate-only + 2 integration).
- `scripts/check_env.py` — verificación de docling y nvidia-smi.
- `pyproject.toml` — dependencias opcionales + pythonpath para pytest.
- 7 ficheros de documentación actualizados.
- `CLAUDE.md` — comandos CLI actualizados.
