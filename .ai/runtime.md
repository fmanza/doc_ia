# Runtime — doc_ia

> Contexto persistente para agentes IA. Regenerado en el bootstrap (2026-06-10).

## Entorno

- **Python**: >= 3.12 (`pyproject.toml`)
- **SO de desarrollo**: Windows 11 (rutas con `\`, venv en `.venv\Scripts\`); CI en ubuntu-latest
- **Instalación**:
  ```bash
  python -m venv .venv
  .venv\Scripts\python -m pip install -r requirements.txt
  ```

## Comandos de ejecución

| Comando | Propósito | Salida |
|---|---|---|
| `python scripts/check_env.py` | Verificar herramientas del entorno | exit 0 si completo; exit 1 + lista de faltantes |
| `python scripts/build_docs_zip.py` | Build mkdocs + ZIP + SHA256 | `dist/doc_ia-docs-{version}.zip` + `.sha256` + `CHECKSUMS.txt` |
| `python scripts/build_docs_zip.py --no-build` | Solo ZIP de `site/` existente | ídem |
| `python scripts/build_docs_zip.py --builder zensical` | Build con Zensical (si está instalado) | ídem |
| `python -m mkdocs serve` | Sitio docs en local | http://127.0.0.1:8000 |
| `python -m mkdocs build --strict` | Build con validación estricta | `site/` |

## Calidad (hooks y CI)

| Herramienta | Comando | Configuración |
|---|---|---|
| ruff (lint) | `python -m ruff check scripts tests` | `pyproject.toml` `[tool.ruff]` (line-length 100, E/F/W/I/UP/B) |
| ruff (formato) | `python -m ruff format scripts tests` | ídem |
| mypy | `python -m mypy scripts` | `[tool.mypy]` strict, files=scripts |
| pytest | `python -m pytest` | `[tool.pytest.ini_options]` testpaths=tests, `-q` |

Hooks PostToolUse de Claude Code (`.claude/settings.json`): ruff check + mypy + pytest collect
tras cada Edit/Write.

## VS Code Tasks (`.vscode/tasks.json`)

- `docs: build` — mkdocs build --strict con el venv del workspace
- `docs: serve` — mkdocs serve en background
- `calidad: ruff + mypy + pytest` — cadena completa de calidad

## CI/CD (GitHub Actions)

| Workflow | Trigger | Efecto |
|---|---|---|
| `docs-zip-release.yml` | push a `main` con cambios en docs/ (o manual) | Release `docs-vX.Y.Z` con ZIP + checksums |
| `docs-release.yml` | tag `v*` (o manual) | ZIP adjunto a la release del tag |

Ningún workflow usa API keys de servicios IA (principio del proyecto).
