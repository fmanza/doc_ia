# VERSION CLOSURE — v0.4.0

- Fecha: 2026-10-29
- Rama: `develop` → `main` (merge `--no-ff`) + tag `v0.4.0`
- Alcance: todo `[Unreleased]` desde `v0.3.0`. Sesiones incluidas: 2026-10-29b (instrucciones de
  visualización, `dd343ba`), 2026-10-29c (modo incremental, `fc18349`) y 2026-10-29d (ZIP
  navegable sin servidor, `a43ebcc`).

## Commit message

```
release: v0.4.0 - ZIP navegable sin servidor, modo incremental e instrucciones de visualización
```

## Release notes (resumen)

- **ZIP con doble clic**: tras extraerlo, `index.html` se abre con navegación, búsqueda y
  diagramas, sin Python, servidor ni red, con MkDocs Material y Zensical (plugin `offline` +
  shim iframe-worker 1.0.4 local). Probado sin red en Edge, Chrome y Firefox.
- **Modo incremental de `/document-project`**: `doc_trace.py baseline` en el CIERRE y
  `doc_trace.py changes` en la Fase 1; solo se revisa lo cambiado en el origen.
- **Instrucciones de visualización** (Fase 7c): `VER_DOCUMENTACION.md` siempre en la raíz del
  destino, para Windows, macOS y Linux.
- **`start-server.py`**: solo `127.0.0.1`, con hilos y puerto ocupado detectado (también en
  Windows); queda como alternativa al doble clic.
- **Fixes**: ZIP `latest` sin índice de búsqueda en JS (orden de `on_post_build`); ZIP versionado
  con el `latest` anidado y sin `start-server.py`; mapa funcional desfasado.

Detalle completo: `CHANGELOG.md` § `[0.4.0] — 2026-10-29`.

## Impacto en API pública

- `build_docs_zip.py`: mismos argumentos; nueva postcondición: termina con código 1 si `site/`
  no se abre sin servidor (índice de búsqueda en JS, ningún script remoto, ningún enlace a carpeta).
- `mkdocs_hooks.py`: `on_post_build.mkdocs_priority = -200`.
- `start-server.py`: escucha solo en `127.0.0.1`; código 1 con el puerto ocupado.
- `doc_trace.py`: subcomandos nuevos `baseline` y `changes` (código 3 → modo completo).
- URLs del sitio: `x.html` en lugar de `x/`.
- Sin deprecaciones.

## Migraciones (para proyectos destino de doc_ia)

- Fase 0b: de 5 a 6 recursos (`vendor/iframe-worker/`), `use_directory_urls: false`, plugin
  `offline` y `extra.polyfills` con el shim local. Un destino que copie `build_docs_zip.py` sin esta
  configuración verá el código 1 con la lista de problemas.
- Hook propio sin `mkdocs_priority = -200` → Gap V3 (el ZIP `latest` saldría sin búsqueda).
- `docs/downloads.md`: enlaces `{nombre}-docs-latest.zip` sin `../`.
- Destinos con web publicada: los enlaces profundos pasan a `*.html` (el RESUMEN lo avisa).
- `VER_DOCUMENTACION.md` se genera en la siguiente sesión; el modo incremental empieza tras el
  primer CIERRE con `baseline`.

## Compatibilidad

- Python 3.12–3.14 (CI en 3.12 y 3.14). Abrir el ZIP no requiere Python; el servidor local, 3.7+.
- Generadores: MkDocs 1.6.1 + Material 9.8.0 (por defecto); Zensical 0.0.73 en paridad no
  bloqueante. El índice JS difiere (`search/search_index.js` / `search.js`); se aceptan los dos.
- Navegadores verificados por `file://` sin red: Edge, Chrome y Firefox (Firefox con ⚠️: la prueba
  sin ventana abre la búsqueda como el icono).
- ZIP «latest» y versionado: 2,81 MB (antes ~2,7 MB) por el índice en JS.

## Rollback

1. Borrar las releases `v0.4.0` y `docs-v0.4.0` en GitHub y el tag (`git push origin :v0.4.0`;
   lo hace el usuario: el borrado de tags remotos está denegado al agente).
2. `git revert -m 1 <merge en main>` y push a `main` (vuelve a publicar la documentación anterior).
3. Riesgo: bajo. Sin datos persistentes. Los destinos ya migrados (offline, `doc_state.json`,
   `VER_DOCUMENTACION.md`) siguen funcionando; con las instrucciones anteriores, la Fase 0b no
   retiraría el plugin `offline`, pero el Paso B3 volvería a enlazar `../{nombre}-docs-latest.zip`.

## Checklist final

- [x] `ruff check scripts tests hooks` y `ruff format --check` sin errores
- [x] `mypy scripts` (strict) sin errores
- [x] `pytest` verde (263)
- [x] `python -m build` (sdist + wheel `doc_ia-0.4.0`) exitoso en venv aislado
- [x] `pyproject.toml` → `0.4.0`
- [x] `CHANGELOG.md` → `[0.4.0] — 2026-10-29` con enlaces (+ `docs/changelog.md` sincronizado)
- [x] `doc_trace drift` sin drift, `matrix` y `llms --check` al día
- [x] `mkdocs build --strict` + ZIP `dist/doc_ia-docs-0.4.0.zip` (2,81 MB, validado sin servidor); tabla de `docs/downloads.md`
- [x] CI de `develop` (run 40898388352) y de `main` (run 40898770989), merge a `main` (`520835c`) y tag `v0.4.0` → release `v0.4.0` (run 40899582347)
- [x] Release `docs-v0.4.0` con ZIP, `.sha256` y `CHECKSUMS.txt` (run 40898770937). ZIP publicado descargado: `sha256sum -c` OK, `_offline_problems` = 0 y prueba de humo en Edge sin red OK

## Handoff

- La prueba de humo de Chromium escribe ahora tecla a tecla (`Input.dispatchKeyEvent`): con
  `Input.insertText` Material no procesa la consulta si el índice ya está listo, y fallaba de forma
  intermitente (3/3 en el ZIP publicado y en el local, antes de corregirla).
- Comprobar con Firefox con ventana que un clic en la búsqueda la abre (K5 de AUDIT_CODE).
- C2 de ADR-003: F8 no antes del 2026-11-11; F7 al publicarse Zensical 0.1.
- Las fuentes de Google y la API de GitHub (`repo_url`) se piden al abrir el sitio con red (D4).
