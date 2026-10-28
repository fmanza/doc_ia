# Incorporación para Desarrolladores

Guía para poner en marcha el entorno de desarrollo de doc_ia desde cero (Arquetipo 7).

## 1. Prerequisitos del Entorno

| Herramienta | Versión mínima | Verificar con | Notas |
|---|---|---|---|
| Python | 3.12 | `python --version` | Declarado en `pyproject.toml` (`requires-python`) |
| pip | reciente | `python -m pip --version` | Actualizar con `python -m pip install -U pip` |
| Git | 2.x | `git --version` | — |

## 2. Obtener el Código

```bash
git clone https://github.com/fmanza/doc_ia.git
cd doc_ia
```

Rama principal de trabajo: `main`. No hay submódulos ni dependencias privadas.

## 3. Configurar el Entorno

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/Mac
python -m pip install -r requirements.txt
```

No se configuran credenciales: el proyecto **no usa API keys** (principio innegociable).
Personalización local opcional de Claude Code en `.claude/settings.local.json` (git-ignored).

## 4. Primera Compilación/Instalación

```bash
python -m mkdocs build --strict
```

| Error frecuente | Causa probable | Solución |
|---|---|---|
| `No module named mkdocs` | venv sin activar o dependencias sin instalar | Activar venv y repetir `pip install -r requirements.txt` |
| Warning con `--strict` | Página huérfana o enlace roto en `docs/` | Revisar `nav:` en `mkdocs.yml` y los enlaces relativos |

## 5. Infraestructura Local

*No aplica para este proyecto.* Los tests son unitarios y deterministas; no se requiere
base de datos, contenedores ni servicios externos.

## 6. Ejecutar la Aplicación

doc_ia no tiene servidor propio; lo ejecutable es el tooling y el sitio de documentación:

```bash
python scripts/check_env.py     # verificación del entorno
python -m mkdocs serve          # sitio de docs en http://127.0.0.1:8000/
python scripts/convert_to_md.py <ruta>  # convertir documentos binarios a Markdown
```

## 7. Mapa del Código

```text
doc_ia/
  scripts/          # Tooling determinista: check_env.py, build_docs_zip.py, convert_to_md.py, start-server.py
  hooks/            # sync_root_docs.py: copia CHANGELOG.md/CONTRIBUTING.md a docs/
  mkdocs_hooks.py   # Hook MkDocs: genera ZIP offline en site/ en cada build
  tests/            # Tests pytest (importan scripts/ vía sys.path)
  docs/             # Sitio MkDocs Material (este sitio, 33 páginas)
  .github/          # Canónico, 12 agentes, 25 prompts, 3 instructions, 2 workflows
  .claude/          # 9 slash commands, hooks PostToolUse, plantillas
  .ai/              # Contexto persistente para agentes IA + sesiones trazadas
```

Regla de capas: `scripts/` no importa de `docs/` ni `.github/`; `hooks/` no importa de
`scripts/`; cada script es standalone.

## 8. Convenciones y Herramientas

| Herramienta | Comando | Regla |
|---|---|---|
| ruff | `python -m ruff check scripts tests hooks` | Lint sin errores |
| ruff format | `python -m ruff format scripts tests hooks` | Formato canónico |
| mypy | `python -m mypy scripts` | Modo `strict`: todo símbolo tipado |
| pytest | `python -m pytest` | Tests deterministas, sin red |

Estilo: f-strings para cadenas con parámetros; sin estado global mutable; sin llamadas a
APIs de IA desde código. Fuente completa: `.github/SHARED_INSTRUCTIONS.md`.

## 9. Flujo de Trabajo Git

- Rama principal: `main`.
- Commits con [Conventional Commits](https://www.conventionalcommits.org/): `feat:`,
  `fix:`, `refactor:`, `test:`, `docs:`, `chore:`.
- Cambios no triviales siguen el flujo `PLAN → AUDIT_PLAN → IMPLEMENT → AUDIT_CODE → VERSION`
  con sesión trazada en `.ai/sessions/`.

## 10. Verificación del Entorno

| Verificación | Comando | Output esperado |
|---|---|---|
| Tooling completo | `python scripts/check_env.py` | `Entorno de tooling documental completo.` |
| Lint | `python -m ruff check scripts tests hooks` | `All checks passed!` |
| Tipos | `python -m mypy scripts` | `Success: no issues found` |
| Tests | `python -m pytest -q` | Todos los tests en verde |
| Docs | `python -m mkdocs build --strict` | `Documentation built` sin warnings |

## 11. Recursos y Referencias

- `.github/SHARED_INSTRUCTIONS.md` — canónico del proyecto (leer primero)
- `.ai/product.md`, `.ai/architecture.md`, `.ai/runtime.md` — contexto persistente
- [Arquitectura del sistema](../architecture.md) — vista panorámica
- [Troubleshooting](troubleshooting.md) — errores conocidos y diagnóstico
- [Descargas](../downloads.md) — documentación offline
