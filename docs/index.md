# doc_ia

## 1. Identidad y Propósito

doc_ia es un proyecto IA para **documentar cualquier proyecto de desarrollo** mediante
instrucciones IA ejecutadas en los chats de los servicios contratados. Los **orígenes a
documentar** y el **destino de la documentación** son parámetros obligatorios de cada
ejecución: doc_ia no documenta un producto concreto, es la fábrica de documentación.

Audiencia: desarrolladores y technical writers que documentan proyectos con asistentes
IA (Claude Code, Gemini Code Assist, GitHub Copilot Chat, Cursor, Codex).

Principios innegociables: **sin API keys**, **sin componentes programáticos IA** (el
código Python es tooling determinista) y **ejecución siempre en el chat** de la plataforma.

## 2. Capacidades Principales

- ✅ **Punto de entrada único para documentar**: `document_project.prompt.md`
  (`/document-project` en Claude Code) — valida origen(es), destino, generador e idioma.
- ✅ **8 arquetipos documentales formales** (funcional, técnica, guía, ejemplos, ADR,
  navegación, onboarding, normativa condicional) en `.github/prompts/`.
- ✅ **Flujo de método** `PLAN → AUDIT_PLAN → IMPLEMENT → AUDIT_CODE → VERSION` con
  12 agentes y 9 slash commands.
- ✅ **Bootstrap multiplataforma**: replica este sistema de instrucciones en otro
  proyecto (modelo PULL).
- ✅ **Tooling determinista**: `scripts/check_env.py` (verificación de entorno) y
  `scripts/build_docs_zip.py` (ZIP offline con SHA256).

| Plataforma IA | Entry point |
|---|---|
| Claude Code | `CLAUDE.md` + `.claude/commands/` |
| Gemini Code Assist | `GEMINI.md` |
| GitHub Copilot Chat | `.github/copilot-instructions.md` + agentes |
| Cursor | `.cursorrules` |
| Codex (OpenAI) | sin fichero propio — ver [Guía de Codex](guides/codex_guide.md) |

## 3. Quick Start

```bash
git clone https://github.com/fmanza/doc_ia.git && cd doc_ia
python -m venv .venv && .venv\Scripts\activate
python -m pip install -r requirements.txt
python scripts/check_env.py
# Entorno de tooling documental completo.
```

Para documentar un proyecto, en el chat de tu plataforma IA:

```text
/document-project

Origen(es): c:\repos\mi_proyecto
Destino: c:\repos\mi_proyecto\docs
Generador: mkdocs-material
Idioma: es
```

## 4. Mapa de la Documentación

| Sección | Contenido |
|---|---|
| [Instalación](installation.md) | Entorno de tooling y configuración por plataforma IA |
| Documentación Funcional | Qué hace cada módulo y por qué ([entorno](functional/check_env.md), [ZIP offline](functional/build_docs_zip.md)) |
| Referencia Técnica | Contratos y diagramas ([check_env](api/check_env.md), [build_docs_zip](api/build_docs_zip.md)) |
| Ejemplos | Casos ejecutables verificables ([verificar entorno](examples/check_env_usage.md), [ZIP offline](examples/build_docs_zip_offline.md)) |
| Guías | [Onboarding](guides/onboarding_dev.md), [troubleshooting](guides/troubleshooting.md), [Codex](guides/codex_guide.md) |
| [Arquitectura](architecture.md) | Vista panorámica del sistema + [ADR](adr/ADR-001-mkdocs-material-por-defecto.md) |
| [Descargas](downloads.md) | Documentación offline (ZIP + SHA256) |

## 5. Compatibilidad y Soporte

- **Python**: ≥ 3.12 (`pyproject.toml`).
- **Generador de docs**: MkDocs + Material (por defecto); Zensical recíprocamente
  compatible sobre el mismo `mkdocs.yml` (no es dependencia).
- **Plataformas IA**: las cinco de la tabla de §2; la generación documental ocurre en el
  chat, nunca en CI ni en código.
- **Repositorio**: [github.com/fmanza/doc_ia](https://github.com/fmanza/doc_ia) —
  releases `docs-vX.Y.Z` con ZIP offline adjunto.
