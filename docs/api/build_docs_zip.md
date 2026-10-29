---
arquetipo: "2"
fuentes:
  mkdocs.yml: 5dd76a635c78
  mkdocs_hooks.py: 31259b7911a3
  pyproject.toml: 751e3d861fb1
  scripts/build_docs_zip.py: 5f972ee674c8
  tests/test_build_docs_zip.py: 82a1d595e6f4
  tests/test_offline_assets.py: 7e632c37987d
revisado: 2026-10-29
---
# build_docs_zip

Distribución offline del sitio de documentación mediante dos mecanismos complementarios: el script `scripts/build_docs_zip.py` (ZIP versionado manual) y el hook `mkdocs_hooks.py` (ZIP automático "latest" en cada build).

## 1. Arquitectura y Diseño

### Script (`scripts/build_docs_zip.py`)

```mermaid
flowchart TD
    accTitle: Flujo de build_docs_zip.py
    accDescr: Sin --no-build ejecuta el pre-build si el generador no admite hooks, construye el sitio en modo estricto y, con Zensical, el post-build. Con --no-build reutiliza site/ o falla si no existe. Después comprueba que site/ se abre sin servidor, lee la versión, crea el ZIP y los ficheros de checksum.
    A[CLI: argparse] --> B{--no-build}
    B -- No --> P{builder sin hooks?<br/>zensical}
    P -- Sí --> PRE[_pre_build:<br/>hooks/sync_root_docs.py]
    PRE --> C[_build: python -m builder build<br/>con --strict por defecto]
    P -- "No, mkdocs" --> C
    C -- "exit != 0" --> X[sys.exit con código del builder]
    C -- "OK, zensical" --> POST[_post_build:<br/>mkdocs_hooks.on_post_build]
    POST --> K
    B -- "Sí, sin site/" --> Y[ERROR a stderr + exit 1]
    C -- "OK, mkdocs" --> K{"_check_offline:<br/>¿se abre sin servidor?"}
    B -- "Sí, con site/" --> K
    K -- "No: problemas" --> Y
    K -- Sí --> D[_version: lee pyproject.toml]
    D --> E["_zip: zipfile sobre site/<br/>excluye .zip y .sha256 + EXTRA_FILES"]
    E --> F[_create_checksum_files:<br/>.sha256 + CHECKSUMS.txt]
```

Pipeline secuencial de funciones privadas orquestadas por `main()`; cada etapa
falla rápido con código de salida explícito. Zensical ignora la clave `hooks:` de `mkdocs.yml`,
así que para los generadores de `HOOKLESS_BUILDERS` el script ejecuta él mismo los dos hooks:
`hooks/sync_root_docs.py` antes del build y `mkdocs_hooks.py` después, **solo si el build
termina con `0`**. Ambos módulos se cargan por ruta desde la raíz del repositorio
(`_load_hook`), porque al ejecutar `python scripts/build_docs_zip.py` la raíz no está en
`sys.path`.

Antes de empaquetar, `_check_offline` exige que `site/` se pueda abrir desde `file://` (doble
clic en `index.html`). `_offline_problems` devuelve la lista de motivos, vacía si está listo:
falta `index.html`; no existe ninguno de `OFFLINE_SEARCH_INDEXES` (`search/search_index.js` de
MkDocs, `search.js` de Zensical), que escribe el plugin `offline`; alguna página tiene un
`<script src>` remoto (con esquema o `//`), como el shim de unpkg que añaden los temas sin la
copia local; o algún `href`/`src` relativo termina en `/` (ignorando `?` y `#`), es decir, enlaza
a una carpeta. Se informan hasta `MAX_REPORTED_PROBLEMS` (20) y el número de los restantes.

### Hook (`mkdocs_hooks.py`)

```mermaid
flowchart TD
    accTitle: Hook on_post_build de MkDocs
    accDescr: Tras mkdocs build, el hook empaqueta site/ con start-server.py y VER_DOCUMENTACION.md, sin ZIP ni checksums previos, y escribe la huella SHA256 de doc_ia-docs-latest.zip.
    MK[mkdocs build] --> H["on_post_build(config)"]
    H --> Z[zipfile.ZipFile sobre site/<br/>excluye .zip y .sha256]
    Z --> S["EXTRA_FILES: start-server.py<br/>y VER_DOCUMENTACION.md"]
    S --> C2[hashlib.sha256 → .zip.sha256]
    C2 --> OUT[site/doc_ia-docs-latest.zip]
```

Función `on_post_build` invocada por MkDocs tras cada build exitoso. Sin instalación ni
entry points; cargado directamente por MkDocs mediante la clave `hooks:` de `mkdocs.yml`.

## 2. Modelo de Datos / Contratos

### API pública

| Función | Fichero | Firma simplificada | Descripción | Retorna |
|---|---|---|---|---|
| `main` | `scripts/build_docs_zip.py` | `main() -> None` | Punto de entrada CLI: parsea argumentos y ejecuta el pipeline | — (termina con `sys.exit` en error) |
| `on_post_build` | `mkdocs_hooks.py` | `on_post_build(config, **kwargs) -> None` | Callback MkDocs: genera ZIP+SHA256 "latest" tras cada build exitoso | — |

Las funciones `_version`, `_load_hook`, `_pre_build`, `_build`, `_post_build`, `_is_remote`,
`_offline_problems`, `_check_offline`, `_zip`,
`_sha256_file` y `_create_checksum_files` del script son privadas (prefijo `_`) y no forman parte del contrato público. La función `_sha256`
del hook también es privada.

### Contrato de entrada — Script (argumentos CLI)

| Parámetro | Tipo | Descripción | Restricciones |
|---|---|---|---|
| `--builder` | `mkdocs` \| `zensical` | Generador a usar; se invoca como `python -m <builder> build` con el mismo intérprete | Por defecto `mkdocs`; `zensical` debe estar instalado y además ejecuta los hooks pre/post |
| `--no-strict` | flag | Omite `--strict` en el build | Por defecto el build es estricto |
| `--no-build` | flag | Empaqueta `site/` existente sin reconstruir | Requiere que `site/` exista |
| `--output-dir` | ruta | Carpeta de salida del ZIP | Por defecto `dist/`; relativa se resuelve contra la raíz del repo; se crea si no existe |

### Contrato de entrada — Hook (callback MkDocs)

| Parámetro | Tipo | Descripción |
|---|---|---|
| `config` | `dict` | Configuración MkDocs; se usa `config["site_dir"]` para localizar el sitio generado |
| `**kwargs` | — | Argumentos adicionales de MkDocs; ignorados |

### Contrato de salida

**Script**:
- `dist/doc_ia-docs-<versión>.zip` — sitio completo (sin `.zip`/`.sha256` anidados) más
  `EXTRA_FILES` en la raíz, igual que el ZIP "latest"; versión leída de `pyproject.toml`.
- `dist/doc_ia-docs-<versión>.zip.sha256` — línea `<hash>  <nombre_zip>`.
- `dist/CHECKSUMS.txt` — registro acumulativo `<hash>  <nombre>  (<timestamp ISO>)`.
- stdout: progreso con prefijo `[build_docs_zip]` (comando de build, ruta del ZIP, tamaño en MB, hash).

**Hook**:
- `site/doc_ia-docs-latest.zip` — sitio completo; incluye `EXTRA_FILES` (`start-server.py`,
  `VER_DOCUMENTACION.md`) en la raíz del ZIP. `on_post_build.mkdocs_priority = -200`: MkDocs lo
  ejecuta después del `on_post_build` del plugin `offline` (-100), que escribe
  `search/search_index.js`; así el ZIP lo incluye. Es el atributo que fija
  `mkdocs.plugins.event_priority`, asignado sin importar mkdocs (Zensical carga el hook sin él).
- `site/doc_ia-docs-latest.zip.sha256` — línea `<hash>  <nombre_zip>`.
- stdout: progreso con prefijo `[ZIP]` / `[OK]`.

### Errores y casos especiales

- **Script** — build fallido: proceso termina con el código de salida del builder (`sys.exit`).
  Con `zensical`, el pre-build ya se ha ejecutado (copias de `docs/` actualizadas) pero el
  post-build no: el ZIP "latest" de un build anterior no se sobrescribe.
- **Script** — `--no-build` sin `site/` existente: mensaje `ERROR` por stderr y código `1`.
- **Script** — `site/` que no se abre sin servidor: `ERROR` por stderr con la configuración
  esperada (`use_directory_urls: false`, plugin `offline`, iframe-worker local en
  `extra.polyfills`), una línea `- <página>: <problema>` por problema (máximo 20) y código `1`,
  sin crear `dist/`. Con `zensical`, el ZIP "latest" ya se ha generado en `site/`.
- **Script** — `CHECKSUMS.txt` es acumulativo (modo append): conserva el histórico.
- **Hook** — si el build lanza una excepción, MkDocs no invoca `on_post_build` y el ZIP "latest"
  no se sobreescribe. Con `--strict`, en cambio, MkDocs ejecuta `on_post_build` **antes** de
  abortar por avisos: el ZIP "latest" se regenera aunque el build termine con error ⚠️.
- **Hook** — si `site_dir` no existe en el momento de `on_post_build`: se imprime WARN y se retorna sin error fatal.

## 3. Componentes y Clases

| Componente | Ruta | Responsabilidad |
|---|---|---|
| `main` | `scripts/build_docs_zip.py` | CLI: parsea argumentos y orquesta el pipeline de build+ZIP |
| `on_post_build` | `mkdocs_hooks.py` | Hook MkDocs: genera `site/doc_ia-docs-latest.zip` tras cada build |
| `_sha256` | `mkdocs_hooks.py` | Calcula la huella SHA256 del ZIP (el `.sha256` lo escribe `on_post_build`) |

El script (`build_docs_zip.py`) contiene solo funciones privadas (`_version`, `_load_hook`,
`_pre_build`, `_build`, `_post_build`, `_is_remote`, `_offline_problems`, `_check_offline`,
`_zip`, `_sha256_file`, `_create_checksum_files`) y las constantes `HOOKLESS_BUILDERS`,
`OFFLINE_SEARCH_INDEXES`, `MAX_REPORTED_PROBLEMS` y `EXTRA_FILES` (esta, también en el hook), sin clases. El hook (`mkdocs_hooks.py`) es el patrón
canónico de referencia para otros proyectos: copiar y cambiar únicamente `zip_path`.

## 4. Dependencias y Requisitos

| Dependencia | Propósito | Componente | Comportamiento sin ella |
|---|---|---|---|
| `argparse`, `hashlib`, `importlib`, `re`, `zipfile`, `subprocess`, `tomllib`, `pathlib`, `datetime` (stdlib) | CLI, SHA256, comprobación del HTML, ZIP, builder, carga de hooks, versión | script | — (stdlib Python ≥ 3.11) |
| Plugin `offline` + `docs/assets/vendor/iframe-worker/` en `extra.polyfills` | Índice de búsqueda en JS y shim local: el sitio se abre sin servidor | sitio | El script termina con código `1` (sin índice JS, o con el shim de unpkg) |
| `hashlib`, `os`, `zipfile`, `pathlib` (stdlib) | ZIP + SHA256 | hook | — (stdlib Python ≥ 3.11) |
| `mkdocs` + `mkdocs-material` | Builder por defecto; invocador del hook | ambos | Script: falla con su código de error. Hook: sin mkdocs no hay `on_post_build` |
| `zensical` | Builder alternativo | script | Solo con `--builder zensical`; falla si no está instalado en el intérprete que ejecuta el script |
| `hooks/sync_root_docs.py`, `mkdocs_hooks.py` | Pre/post-build para generadores sin hooks | script | Con `zensical`: error al cargarlos si faltan |
| `scripts/start-server.py`, `VER_DOCUMENTACION.md` | Servidor HTTP local e instrucciones de visualización incluidos en el ZIP (`EXTRA_FILES`) | ambos | ZIP válido, sin el fichero que falte |

## 5. Ejemplos Relacionados

- [Ejemplo: Generar ZIP Offline](../examples/build_docs_zip_offline.md) — invocaciones CLI
  típicas, validación del checksum y output esperado.

## 6. Verificación y Tests

| Test | Qué verifica | Tipo |
|---|---|---|
| `test_main_builds_strict_and_packages_versioned_zip` | Build con `--strict`, ZIP versionado, `.sha256` y `CHECKSUMS.txt` | integración (CLI, build simulado) |
| `test_versioned_zip_matches_latest_layout` | ZIP versionado sin `.zip`/`.sha256` anidados y con `start-server.py` + `VER_DOCUMENTACION.md` en la raíz | integración (CLI) |
| `test_main_no_strict_omits_flag` | `--no-strict` no pasa `--strict` al generador | unitario |
| `test_main_no_build_without_site_exits_1` | `--no-build` sin `site/` termina con `1` sin crear `dist/` | integración (CLI) |
| `test_main_build_failure_propagates_exit_code` | El código de error del generador se propaga y no se crea ZIP | integración (CLI) |
| `test_main_no_build_relative_output_dir` | `--output-dir` relativo se resuelve contra la raíz | integración (CLI) |
| `test_sha256_file_matches_archive` | El `.sha256` coincide con el hash real del ZIP | unitario |
| `test_checksums_txt_is_append_only` | `CHECKSUMS.txt` acumula una línea por build | unitario |
| `test_zensical_runs_hooks_around_build` | Con `zensical`: comando `python -m zensical build --strict` y orden pre → build → post | integración (CLI, build simulado) |
| `test_zensical_build_failure_skips_post_build` | Con `zensical` y build fallido: sin post-build ni ZIP | integración (CLI) |
| `test_mkdocs_builder_leaves_hooks_to_mkdocs` | Con `mkdocs`: el script no ejecuta los hooks (lo hace MkDocs) | integración (CLI) |
| `test_zensical_with_real_hooks_syncs_and_creates_latest_zip` | Con los hooks reales: copia `CHANGELOG.md` a `docs/` y genera el ZIP `latest` + `.sha256` | integración (CLI, build simulado) |
| `test_post_build_hook_creates_latest_zip` | `mkdocs_hooks.on_post_build`: ZIP `latest` + `.sha256`, incluye `start-server.py` y `VER_DOCUMENTACION.md`, excluye `.zip`/`.sha256` | unitario |
| `test_zensical_search_index_layout_is_accepted` | Índice `search.js` en la raíz (Zensical) válido | integración (CLI) |
| `test_external_and_file_links_are_not_folder_links` | Enlaces externos, `mailto:`, a ficheros con `#…/` y anclas no son enlaces a carpeta | integración (CLI) |
| `test_site_not_browsable_from_file_exits_1` | Enlace a carpeta (`api/x/`, `../#a`, `./`) o script remoto (`https:`, `//`) → código `1`, página y problema en stderr, sin `dist/` | integración (CLI, 5 casos) |
| `test_missing_search_index_js_exits_1` | Sin índice JS → código `1` y aviso del plugin `offline` | integración (CLI) |
| `test_offline_check_runs_after_build` | La comprobación va después del build que crea el índice | integración (CLI, build simulado) |
| `test_problem_report_is_truncated` | 25 problemas → 20 líneas + «... and 5 more» | integración (CLI) |
| `test_offline_assets.py::test_zip_hook_runs_after_offline_plugin` | Prioridad del hook menor que la del `on_post_build` del plugin `offline` instalado | unitario |

```bash
python -m pytest tests/test_build_docs_zip.py -q
```

Sin cubrir en los tests: el build real con MkDocs o Zensical (se simula `subprocess.run`). La CI
ejecuta el build real y `build_docs_zip.py --no-build` sobre él (paso «ZIP navegable sin servidor»).

??? note "Evidencia"

    | Elemento | Fuente | Confianza |
    |---|---|---|
    | `main` y opciones `--builder`, `--no-strict`, `--no-build`, `--output-dir` | `scripts/build_docs_zip.py::main` | ✅ |
    | `on_post_build` | `mkdocs_hooks.py::on_post_build` | ✅ |
    | Versión desde `pyproject.toml` | `scripts/build_docs_zip.py::_version` | ✅ |
    | Build con `--strict` y salida con el código del builder | `scripts/build_docs_zip.py::_build` | ✅ |
    | ZIP `doc_ia-docs-<versión>.zip` | `scripts/build_docs_zip.py::_zip`, `::ZIP_PREFIX` | ✅ |
    | `.sha256` y `CHECKSUMS.txt` acumulativo | `scripts/build_docs_zip.py::_create_checksum_files` | ✅ |
    | `--no-build` sin `site/` → stderr + código `1` | `scripts/build_docs_zip.py::main` | ✅ |
    | Hook: `site_dir` desde la configuración, WARN si no existe | `mkdocs_hooks.py::on_post_build` | ✅ |
    | Hook: excluye `.zip`/`.sha256` e incluye `EXTRA_FILES` | `mkdocs_hooks.py::on_post_build`, `::EXTRA_FILES` | ✅ |
    | Script: mismo contenido que el ZIP "latest" (sin anidados + `EXTRA_FILES`) | `scripts/build_docs_zip.py::_zip`, `::EXTRA_FILES` | ✅ |
    | Hook ejecutado antes del aborto por `--strict` | `mkdocs.commands.build::build` (MkDocs 1.6.1) | ⚠️ |
    | `_sha256` | `mkdocs_hooks.py::_sha256` | ✅ |
    | Dependencias stdlib del script y del hook | `scripts/build_docs_zip.py`, `mkdocs_hooks.py` (imports) | ✅ |
    | `zensical` como builder alternativo, invocado con `python -m` | `scripts/build_docs_zip.py::_build` | ✅ |
    | Pre/post-build para generadores sin hooks; post solo con build OK | `scripts/build_docs_zip.py::HOOKLESS_BUILDERS`, `::_build`, `::_pre_build`, `::_post_build` | ✅ |
    | Carga de hooks por ruta desde la raíz | `scripts/build_docs_zip.py::_load_hook` | ✅ |
    | Zensical ignora `hooks:` de `mkdocs.yml` | zensical.org/compatibility/configuration (Zensical 0.0.73) | ⚠️ |
    | Comprobación «se abre sin servidor», sus cuatro motivos y el límite de 20 | `scripts/build_docs_zip.py::_offline_problems`, `::_check_offline`, `::_is_remote`, `::OFFLINE_SEARCH_INDEXES`, `::MAX_REPORTED_PROBLEMS` | ✅ |
    | Hook después del plugin `offline` (prioridad -200 frente a -100) | `mkdocs_hooks.py::on_post_build`, `material/plugins/offline/plugin.py::OfflinePlugin.on_post_build` (Material 9.8.0) | ✅ |
    | Índice JS de Zensical en `search.js` | Build real con Zensical 0.0.73 (sesión 2026-10-29d) | ⚠️ |
    | `EXTRA_FILES` opcionales en el ZIP | `mkdocs_hooks.py::on_post_build` (`if extra_path.exists()`), `scripts/build_docs_zip.py::_zip` (`if extra_path.is_file()`) | ✅ |
