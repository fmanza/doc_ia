# TRACEABILITY

## Session metadata
- id: 2026-06-12f
- fecha: 2026-06-12
- rama: develop
- skill: mejora tooling + normalización instrucciones IA

## Resumen cronológico

1. **DIAGNÓSTICO** — dpss genera ZIP porque tiene `dpss_docs/docs_build_plugin.py` (MkDocs `BasePlugin`
   con `on_post_build`) + `dpss_docs.egg-info/` en la raíz del proyecto. Python descubre el entry point
   vía `''` (CWD) en `sys.path`. doc_ia y socyalpro no tenían plugin equivalente.
2. **PLUGIN doc_ia** — Creado `doc_ia_docs/__init__.py` + `doc_ia_docs/docs_build_plugin.py`.
   Actualizado `pyproject.toml` con `[build-system]` + `[project.entry-points."mkdocs.plugins"]`.
   Añadido `- doc_ia_documentation_zip:` en `mkdocs.yml`. Instalado con `python -m pip install -e .`.
3. **PLUGIN socyalpro** — Mismos pasos: `socyalpro_docs/`, `pyproject.toml` nuevo, `mkdocs.yml` actualizado.
4. **EDGE CASE documentado** — Error "plugin is not installed" si el venv no está activo.
   Registrado en `.claude/EDGE_CASES.md`. Diferencia con dpss: dpss usa egg-info en CWD (no requiere
   venv activo); enfoque moderno via dist-info requiere el venv correcto.
5. **start-server.py** — Creado `scripts/start-server.py` en doc_ia y socyalpro. Plugin actualizado
   en ambos para incluir el script en el ZIP (`arcname="start-server.py"`).
6. **downloads.md normalizado** — Estructura canónica aplicada en dpss (referencia), socyalpro y doc_ia:
   tabla con `<a href="../{nombre}-docs-latest.zip">` + `<a href="../...sha256">` + Cómo usar
   (Opción A `python start-server.py` ⭐ / Opción B sin servidor) + Validar integridad + Desarrolladores.
7. **INSTRUCCIONES IA actualizadas** — Ver tabla de artefactos abajo.

## Artefactos generados / modificados

| Artefacto | Ruta | Estado |
|---|---|---|
| Plugin package | `doc_ia_docs/__init__.py` | CREADO |
| Plugin MkDocs | `doc_ia_docs/docs_build_plugin.py` | CREADO — on_post_build; incluye start-server.py en ZIP |
| Metadatos Python | `pyproject.toml` | ACTUALIZADO — [build-system] + entry point doc_ia_documentation_zip |
| Navegación | `mkdocs.yml` | ACTUALIZADO — plugin doc_ia_documentation_zip bajo plugins: |
| Servidor offline | `scripts/start-server.py` | CREADO — servidor HTTP local, abre navegador automáticamente |
| Página descargas | `docs/downloads.md` | ACTUALIZADO — estructura normalizada; enlaces HTML directos; python start-server.py |
| .gitignore | `.gitignore` | ACTUALIZADO — añadido *.egg-info/ |
| Casos límite | `.claude/EDGE_CASES.md` | ACTUALIZADO — caso "plugin vinculado al venv" |
| Instrucciones IA | `.github/SHARED_INSTRUCTIONS.md` | ACTUALIZADO — 4 piezas obligatorias; ref. start-server.py en plugin |
| Instrucciones IA | `.github/prompts/document_project.prompt.md` | ACTUALIZADO — Paso A2-0 (start-server.py obligatorio); Gap A2 crea plugin; B3 estructura canónica con enlaces HTML; B4 crea plugin; B5 reportar |

## Build verificado

```
[ZIP] Generando descarga: doc_ia-docs-latest.zip
[ZIP] Incluyendo servidor local: start-server.py
[OK] ZIP creado: doc_ia-docs-latest.zip (0.96 MB)
exit=0
```

## Directrices para futuras IAs

- **Plugin vinculado al venv**: si `mkdocs build` falla con "plugin is not installed", el venv
  no está activo. Activar `doc_ia/.venv/Scripts/Activate.ps1` o usar `python -m mkdocs build`.
  Ver `.claude/EDGE_CASES.md` § *Plugin ZIP no encontrado*.
- **start-server.py**: siempre en `scripts/start-server.py` de cualquier proyecto con docs offline.
  El plugin lo incluye en el ZIP si el fichero existe (condición `if server_script.exists()`).
- **downloads.md**: la tabla "Descarga Actual" usa `<a href="../{nombre}-docs-latest.zip">`.
  El path `../` funciona con `use_directory_urls: true` (la página está en `downloads/index.html`
  y el ZIP en la raíz de `site/`).
- **Reinstalar el plugin**: si el entorno cambia (nuevo venv, nuevo desarrollador), ejecutar
  `python -m pip install -e .` desde la raíz del proyecto para registrar el entry point.

## Veredicto final

Veredicto: CLOSED
Build: OK — `doc_ia-docs-latest.zip` generado con `start-server.py` incluido.
