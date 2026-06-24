# Instalación

## 1. Requisitos Previos

- Python **≥ 3.12** (declarado en `pyproject.toml` → `requires-python`).
- `pip` actualizado (`python -m pip install -U pip`).
- Git y acceso de red a GitHub para clonar el repositorio.

Solo se instalan las dependencias declaradas en `requirements.txt`; el proyecto **no
requiere API keys** de ningún servicio.

### Conversión de documentos binarios a Markdown (opcional)

El script `scripts/convert_to_md.py` convierte ficheros no legibles directamente (PDF, DOCX,
PPTX, imágenes, email, audio…) a Markdown, depositando el resultado en `<origen>/md/`.
Ofrece tres motores seleccionables con `--engine`:

| Motor | Formatos | Rol |
|---|---|---|
| **docling** (default) | PDF, DOCX, PPTX, XLSX, CSV, HTML, EPUB, imágenes, email, LaTeX, audio | Motor principal — OCR, GPU, chunking RAG, metadata |
| **markitdown** | PDF, DOCX, PPTX, XLSX, XLS, CSV, EPUB, HTML, MSG | Alternativa ligera — un solo `pip install` |
| **pandoc** (binario) | DOC, ODT, RST, TEX/LATEX | Complemento — formatos legacy y LaTeX |

#### docling — motor principal (opcional)

Motor avanzado con OCR integrado, aceleración GPU y chunking RAG:

```bash
pip install docling
```

Para aceleración GPU (opcional): NVIDIA driver + `nvidia-smi` en PATH. CPU es el default.

```bash
pip install 'doc_ia[docling]'     # o directamente: pip install docling
```

#### markitdown — alternativa ligera

Cubre PDF, DOCX, PPTX, HTML, EPUB, CSV y más con una sola instalación Python:

```bash
pip install markitdown
pip install 'doc_ia[markitdown]'  # equivalente
```

#### pandoc — complemento para formatos legacy

Necesario solo si el origen contiene `.doc`, `.odt`, `.rst` o `.tex`:

| Sistema operativo | Comando de instalación |
|---|---|
| Windows | `winget install JohnMacFarlane.Pandoc` |
| macOS | `brew install pandoc` |
| Linux (Debian/Ubuntu) | `sudo apt install pandoc` |
| Linux (Fedora/RHEL) | `sudo dnf install pandoc` |

#### Todos los motores

```bash
pip install 'doc_ia[all-engines]'  # docling + markitdown
# pandoc se instala aparte como binario del sistema
```

!!! note "Los tres motores son opcionales e independientes"
    `python scripts/check_env.py` informa del estado de cada motor, pero no falla.
    Solo necesitas el motor que corresponda a los formatos de tu origen.

## 2. Instalación del Entorno

| Paso | Comando | Para qué |
|---|---|---|
| 1 | `git clone https://github.com/fmanza/doc_ia.git && cd doc_ia` | Obtener el código |
| 2 | `python -m venv .venv` | Entorno virtual aislado |
| 3 | `.venv\Scripts\activate` (Windows) / `source .venv/bin/activate` (Linux/Mac) | Activar el venv |
| 4 | `python -m pip install -r requirements.txt` | Dependencias reales: mkdocs-material, ruff, mypy, pytest |

## 3. Configuración por Plataforma IA

Las plataformas leen sus entry points directamente del repositorio; no hay nada que
instalar aparte de abrir el proyecto:

| Plataforma | Entry point | Configuración adicional |
|---|---|---|
| Claude Code | `CLAUDE.md` | Hooks PostToolUse en `.claude/settings.json`; personalización local en `.claude/settings.local.json` (git-ignored) |
| Gemini Code Assist | `GEMINI.md` | — |
| GitHub Copilot Chat | `.github/copilot-instructions.md` | Agentes en `.github/agents/` (`/runSubagent`) |
| Cursor | `.cursorrules` | — |
| Codex (OpenAI) | sin fichero propio | Lee `CLAUDE.md` + canónico; ver [Guía de Codex](guides/codex_guide.md) |

## 4. Verificación

```bash
python scripts/check_env.py
# Entorno de tooling documental completo.

python -m mkdocs build --strict
# INFO    -  Documentation built in X.XX seconds   (sin warnings)
```

## 5. Solución de Problemas

| Escenario/Error | Causa probable | Solución |
|---|---|---|
| `Faltan herramientas: …` | Dependencias sin instalar o venv inactivo | Paso 3 y 4 de §2 |
| `No module named mkdocs` | venv equivocado | Activar el venv del proyecto |
| Warning con `--strict` | Enlace roto o página huérfana en `docs/` | Ver [Troubleshooting](guides/troubleshooting.md) |

Más casos en la guía de [Troubleshooting](guides/troubleshooting.md).
