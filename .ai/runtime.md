# Runtime — doc_ia

> Contexto persistente para agentes IA. Actualizado: 2026-06-18.

## Entorno

- **Python**: >= 3.12 (`pyproject.toml`)
- **SO de desarrollo**: Windows 11 (rutas con `\`, venv en `.venv\Scripts\`); CI en ubuntu-latest
- **Herramientas opcionales**: `docling` (Python, motor por defecto de `convert_to_md.py`), `markitdown` (Python, alternativa ligera; necesaria para XLS), `pandoc` (sistema, para DOC/ODT/RST)
- **Instalación**:
  ```bash
  python -m venv .venv
  .venv\Scripts\python -m pip install -r requirements.txt
  pip install docling              # opcional, motor por defecto de convert_to_md.py
  pip install markitdown           # opcional, alternativa ligera (XLS)
  # pandoc: instalar desde https://pandoc.org/installing.html
  ```

## Comandos de ejecución

| Comando | Propósito | Salida |
|---|---|---|
| `python scripts/check_env.py` | Verificar herramientas del entorno (requeridas + opcionales) | exit 0 si completo; exit 1 + lista de faltantes |
| `python scripts/build_docs_zip.py` | Build mkdocs + ZIP + SHA256 | `dist/doc_ia-docs-{version}.zip` + `.sha256` + `CHECKSUMS.txt` |
| `python scripts/build_docs_zip.py --no-build` | Solo ZIP de `site/` existente | ídem |
| `python scripts/build_docs_zip.py --builder zensical` | Build con Zensical (si está instalado) | ídem |
| `python scripts/convert_to_md.py <ruta>` | Convertir documentos binarios a Markdown | `<ruta>/md/*.md` (estructura espejo) |
| `python scripts/convert_to_md.py <ruta> --dry-run` | Previsualizar conversiones sin ejecutar | Lista de ficheros que se convertirían |
| `python scripts/start-server.py` | Servidor HTTP local desde el directorio del ZIP | http://localhost:8000 (auto-abre navegador) |
| `python -m mkdocs serve` | Sitio docs en local | http://127.0.0.1:8000 |
| `python -m mkdocs build --strict` | Build con validación estricta | `site/` + `site/doc_ia-docs-latest.zip` (vía hook) |

## Hooks

### Hooks MkDocs (en `mkdocs.yml`)

| Hook | Evento | Propósito |
|---|---|---|
| `hooks/sync_root_docs.py` | `on_pre_build` | Copia CHANGELOG.md y CONTRIBUTING.md a docs/ |
| `mkdocs_hooks.py` | `on_post_build` | Genera `doc_ia-docs-latest.zip` + `.sha256` en `site/` |

### Hooks PostToolUse (en `.claude/settings.json`)

Ejecutados automáticamente tras cada Edit/Write sobre código Python:

1. `python hooks/sync_root_docs.py` — sincroniza ficheros raíz → `docs/`
2. `python -m ruff check scripts tests hooks --quiet` — linting
3. `python -m mypy scripts --no-error-summary` — type-checking strict
4. `python -m pytest --collect-only -q tests` — validación de sintaxis de tests

## Calidad

| Herramienta | Comando | Configuración |
|---|---|---|
| ruff (lint) | `python -m ruff check scripts tests hooks` | `pyproject.toml` `[tool.ruff]` (line-length 100, E/F/W/I/UP/B) |
| ruff (formato) | `python -m ruff format scripts tests hooks` | ídem |
| mypy | `python -m mypy scripts` | `[tool.mypy]` strict, files=scripts |
| pytest | `python -m pytest` | `[tool.pytest.ini_options]` testpaths=tests, `-q` |

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
