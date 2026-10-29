# VERSION CLOSURE — v0.3.0

- Fecha: 2026-10-29
- Rama: `develop` → `main` (merge `--no-ff`) + tag `v0.3.0`
- Alcance: todo `[Unreleased]` desde `v0.2.0`. Sesiones incluidas: 2026-10-28e (diagramas
  Mermaid), 2026-10-28f (Mermaid local), commit `c8a6265` (orden de tipos de origen) y
  2026-10-29 (`_fuentes/` en el destino + docling en la Fase 0c).

## Commit message

```
release: v0.3.0 - Mermaid local, regla de diagramas y fuentes convertidas en _fuentes/
```

## Release notes (resumen)

- **Diagramas**: regla única §3.17; 9 diagramas rediseñados; `accTitle`/`accDescr` en todos;
  tests de conformidad (entidades HTML, comillas, accesibilidad, ≤12 nodos); job `mermaid` en CI
  con el parser real.
- **Mermaid 12.2.0 servido en local**: el sitio y el ZIP offline dibujan sin conexión, igual con
  MkDocs Material y Zensical.
- **Producto `/document-project`**: Fase 0b con 5 recursos (Mermaid local); los documentos
  convertidos llegan siempre al destino en `_fuentes/<nombre_origen>/<ruta relativa al origen>`;
  Fase 0c con docling como motor por defecto; REFERENCIA como último tipo de origen.
- **Fixes**: entidades HTML en labels Mermaid; nombres improvisados `.fuentes/`/`_fuentes/`;
  Fase 0c que describía markitdown como principal.

Detalle completo: `CHANGELOG.md` § `[0.3.0] — 2026-10-29`.

## Impacto en API pública

- Scripts sin cambios de firma ni de comportamiento (`check_env.py` solo cambia textos de avisos).
- Sin deprecaciones.

## Migraciones (para proyectos destino de doc_ia)

- Fase 0b: de 3 a 5 recursos (`vendor/mermaid/mermaid-12.2.0.min.js` + `js/mermaid-theme.js`, en
  ese orden en `extra_javascript`); retirar CDN de Mermaid y `mermaid.js` propio.
- Fuentes convertidas: `.fuentes/` o `fuentes/` en la raíz del destino se migran a `_fuentes/`
  (el flujo lo propone y pide confirmación); `_fuentes/` no va en `.gitignore`.

## Compatibilidad

- Python 3.12–3.14 (CI en 3.12 y 3.14).
- Generadores: MkDocs + Material 9.x (por defecto); Zensical 0.0.73 en paridad no bloqueante.
- Motores de conversión: docling (por defecto), markitdown, pandoc — sin cambios de contrato.
- ZIP «latest» ~2,7 MB (antes ~1,1 MB) por la librería Mermaid local.

## Rollback

1. Borrar las releases `v0.3.0` y `docs-v0.3.0` en GitHub y el tag (`git push origin :v0.3.0`;
   lo hace el usuario: el borrado de tags remotos está denegado al agente).
2. `git revert -m 1 <merge en main>` y push a `main` (vuelve a publicar la documentación anterior).
3. Riesgo: bajo. Sin datos ni esquemas persistentes; los destinos que ya tengan Mermaid local o
   `_fuentes/` siguen funcionando con la versión anterior de las instrucciones.

## Checklist final

- [x] `ruff check scripts tests hooks` y `ruff format --check` sin errores
- [x] `mypy scripts` (strict) sin errores
- [x] `pytest` verde
- [x] `python -m build` (sdist + wheel `doc_ia-0.3.0`) exitoso en venv aislado
- [x] `pyproject.toml` → `0.3.0`
- [x] `CHANGELOG.md` → `[0.3.0] — 2026-10-29` con enlaces (+ `docs/changelog.md` sincronizado)
- [x] `doc_trace drift` sin drift y `llms --check` al día
- [x] `mkdocs build --strict` + ZIP `dist/doc_ia-docs-0.3.0.zip`; tabla de `docs/downloads.md`
- [x] CI de `develop` y de `main`, merge a `main` (`6ceb437`) y tag `v0.3.0` → release `v0.3.0` correcta
- [x] Release `docs-v0.3.0` con ZIP, `.sha256` y `CHECKSUMS.txt` (run 40862075101)

## Handoff

- Mejora menor pendiente (desde v0.2.0): el ZIP versionado incluye el ZIP «latest» de `site/`
  (5,33 MB frente a 2,7 MB).
- C2 de ADR-003: F8 no antes del 2026-11-11; F7 al publicarse Zensical 0.1.
