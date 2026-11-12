# VERSION CLOSURE — v0.12.0

## Commit message
```
release: v0.12.0 - Zensical como único generador (ADR-003)
```

Incluye la v0.11.4 (`1599b04`), preparada en `develop` y no publicada por separado: el merge a
`main` lleva las dos. La sección `[0.11.4]` del CHANGELOG se mantiene.

## Changelog
- **fix** (0.11.4): logo del ZIP sin servidor (`extra.homepage`); `build_docs_zip.py` detecta
  enlaces `.`/`..` — `mkdocs.yml`, `TEMPLATE_mkdocs.yml`, estándar §4, `scripts/build_docs_zip.py::_is_folder`.
- **build** (0.11.4): Zensical 0.1.1 + `zensical-ui` 0.0.42 — requisitos, `test_mermaid_assets.py`, `test_zensical_compat.py`.
- **feat!**: Zensical único generador — `scripts/build_docs_zip.py` (pipeline; `--builder mkdocs` → 2),
  `scripts/check_env.py` (zensical requerido), requisitos sin MkDocs, `mkdocs.yml` sin `hooks:`,
  `hooks/sync_root_docs.py` sin `on_pre_build`, `mkdocs_hooks.py` sin `mkdocs_priority`, CI y workflows.
- **feat!**: `/document-project` sin campo generador; migración de destinos MkDocs con guarda de
  plugins — prompt, comando, agentes, estándar, plantillas, kit.
- **docs**: instrucciones de las plataformas IA, `.ai/`, documentación propia; ADR-003 ACEPTADO,
  ADR-001 REEMPLAZADO; EDGE_CASES «Histórico (MkDocs)».
- **test**: `test_no_mkdocs.py`, conformidad de `/document-project`, casos nuevos de `build_docs_zip`.

## Impacto en API pública
- `scripts/build_docs_zip.py`: `--builder` obsoleto (`zensical` sin efecto; otro valor → código 2).
  Siempre ejecuta pre-build, `zensical build` y post-build.
- `scripts/check_env.py`: `REQUIRED_TOOLS` = `zensical, ruff, mypy, pytest`;
  `OPTIONAL_DOC_BUILDERS` eliminado.
- `hooks/sync_root_docs.py::on_pre_build` eliminado (queda `main`).
- `/document-project`: tres campos obligatorios (origen(es), destino, idioma).

## Migraciones
- Entornos locales: `pip install -r requirements-dev.txt` (instala Zensical 0.1.1); MkDocs ya no hace falta.
- Llamadas a `build_docs_zip.py --builder mkdocs` → quitar la opción.
- Destinos MkDocs: se migran en la Fase 0b de su próxima ejecución de `/document-project`.

## Compatibilidad
- Python 3.12–3.14 (CI con 3.12 y 3.14).
- Generador: Zensical 0.1.1 (beta). Mermaid 12.2.0 local, iframe-worker 1.0.4 local.

## Rollback
- `git revert` del merge en `main` (o de `b6ee093`, `4c6e3cb`, `5fd6ce0` para volver a MkDocs
  manteniendo 0.11.4); reinstalar `requirements-dev.txt` de la versión revertida.
- Riesgo: los ZIP y releases `v0.12.0`/`docs-v0.12.0` ya publicados no se retiran con el revert;
  los destinos ya migrados conservarían Zensical.

## Checklist final
- [x] `ruff check scripts tests hooks` sin errores
- [x] `mypy scripts` sin errores
- [x] `pytest` verde
- [ ] `python -m build` — no aplica: doc_ia no publica paquete (el módulo `build` no está instalado)
- [x] Versión `0.12.0` en `pyproject.toml` y referencias derivadas
- [x] CHANGELOG.md actualizado (`docs/changelog.md` sincronizado)
- [x] `doc_trace` drift / decisions / llms --check sin hallazgos
- [x] Pipeline real `python scripts/build_docs_zip.py` con exit 0 (ZIP latest ~2,9 MB)

## Pruebas sugeridas tras el push
- CI de `develop` y `main` en 3.12 y 3.14 (build Zensical ahora bloqueante).
- Release `docs-v0.12.0` (push a `main`) y `v0.12.0` (tag): ZIP con `search.js`, abrir con doble clic.
- Revisión humana pendiente de C3: búsqueda por `file://` y móvil real.

## Pendientes de decisión (no bloquean la release)
- COB-BUILDZIP-001: ¿reclasificar a `No aplica`?
- Z4: plugin `privacy`.
