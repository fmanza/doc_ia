# GITHUB COMMIT MESSAGE

## Commit propuesto

```
feat(tooling): plugin MkDocs ZIP automático + start-server.py para distribución offline

- doc_ia_docs/: plugin on_post_build que genera doc_ia-docs-latest.zip en site/
  en cada mkdocs build; incluye start-server.py en el ZIP automáticamente
- pyproject.toml: [build-system] + entry point doc_ia_documentation_zip
- mkdocs.yml: plugin doc_ia_documentation_zip registrado
- scripts/start-server.py: servidor HTTP local (abre navegador automáticamente)
- docs/downloads.md: estructura normalizada — tabla con enlaces HTML directos
  (<a href="../doc_ia-docs-latest.zip">), Opción A python start-server.py
- .gitignore: excluir *.egg-info/
- .claude/EDGE_CASES.md: caso "plugin vinculado al venv" documentado
- .github/SHARED_INSTRUCTIONS.md: distribución offline → 4 piezas obligatorias
- .github/prompts/document_project.prompt.md: Gap A2 crea plugin (A2-0..A2-4);
  B3 estructura canónica con enlaces HTML; B4 crea plugin; Paso A2-0 start-server.py

Sesión: .ai/sessions/2026-06-12f_mkdocs_plugin_distribution/

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

## Ficheros a incluir en el commit

```
git add doc_ia_docs/ \
        scripts/start-server.py \
        pyproject.toml \
        mkdocs.yml \
        docs/downloads.md \
        .gitignore \
        .claude/EDGE_CASES.md \
        .github/SHARED_INSTRUCTIONS.md \
        .github/prompts/document_project.prompt.md \
        .ai/sessions/2026-06-12f_mkdocs_plugin_distribution/
```

## Ficheros a excluir del commit

- `.claude/settings.json` — configuración local del entorno (no versionar)
