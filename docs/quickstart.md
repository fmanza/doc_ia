# Quick Start

Pon en marcha doc_ia y documenta tu primer proyecto en menos de 5 minutos.

## 1. Prerequisito Mínimo

| Herramienta | Versión mínima | Verificar con |
|---|---|---|
| Python | 3.12 | `python --version` |
| Git | cualquier versión reciente | `git --version` |
| Plataforma IA | Claude Code / Gemini / Copilot / Cursor / Codex | — |

## 2. Primer Comando

Clona el repositorio e instala las dependencias de tooling:

```bash
git clone https://github.com/fmanza/doc_ia.git
cd doc_ia
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/Mac
python -m pip install -r requirements.txt
python scripts/check_env.py
```

## 3. Primer Resultado Visible

Si el entorno está completo verás:

```
Entorno de tooling documental completo.
```

Si alguna herramienta falta, `check_env.py` indica cuál y sale con código 1:

```
Faltan herramientas: ruff, mypy
```

Instala las dependencias que falten con `pip install -r requirements.txt`.

## 4. Siguiente Paso Sugerido

Documenta tu proyecto con el comando `/document-project` en tu plataforma IA:

**Claude Code** (chat o terminal):

```text
/document-project

Origen(es): c:\ruta\a\tu_proyecto
Destino:    c:\ruta\a\tu_proyecto\docs
Generador:  mkdocs-material
Idioma:     es
```

El flujo valida los inputs, inventaría el código, genera la documentación por fases
y sincroniza `mkdocs.yml`. Finaliza con `python -m mkdocs build --strict` para
verificar que el sitio compila sin errores.

Para una instalación detallada del entorno (Python, plataformas IA, variables de
entorno) consulta [Instalación](installation.md).
