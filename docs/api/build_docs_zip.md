---
arquetipo: "2"
fuentes:
  mkdocs_hooks.py: 2f510611cb6f
  pyproject.toml: b6a2ca1ee162
  scripts/build_docs_zip.py: b9a2694d122f
  tests/test_build_docs_zip.py: 0dad72a78801
revisado: 2026-10-28
---
# build_docs_zip

Distribución offline del sitio de documentación mediante dos mecanismos complementarios: el script `scripts/build_docs_zip.py` (ZIP versionado manual) y el hook `mkdocs_hooks.py` (ZIP automático "latest" en cada build).

## 1. Arquitectura y Diseño

### Script (`scripts/build_docs_zip.py`)

```mermaid
flowchart TD
    A[CLI: argparse] --> B{--no-build}
    B -- No --> P{builder sin hooks?\nzensical}
    P -- Sí --> PRE[_pre_build:\nhooks/sync_root_docs.py]
    PRE --> C[_build: python -m builder build\ncon --strict por defecto]
    P -- "No, mkdocs" --> C
    C -- "exit != 0" --> X[sys.exit con código del builder]
    C -- "OK, zensical" --> POST[_post_build:\nmkdocs_hooks.on_post_build]
    POST --> D
    B -- "Sí, sin site/" --> Y[ERROR a stderr + exit 1]
    C -- "OK, mkdocs" --> D[_version: lee pyproject.toml]
    B -- "Sí, con site/" --> D
    D --> E[_zip: shutil.make_archive sobre site/]
    E --> F[_create_checksum_files:\n.sha256 + CHECKSUMS.txt]
```

Pipeline secuencial de funciones privadas orquestadas por `main()`; cada etapa
falla rápido con código de salida explícito. Zensical ignora la clave `hooks:` de `mkdocs.yml`,
así que para los generadores de `HOOKLESS_BUILDERS` el script ejecuta él mismo los dos hooks:
`hooks/sync_root_docs.py` antes del build y `mkdocs_hooks.py` después, **solo si el build
termina con `0`**. Ambos módulos se cargan por ruta desde la raíz del repositorio
(`_load_hook`), porque al ejecutar `python scripts/build_docs_zip.py` la raíz no está en
`sys.path`.

### Hook (`mkdocs_hooks.py`)

```mermaid
flowchart TD
    MK[mkdocs build] --> H["on_post_build(config)"]
    H --> Z[zipfile.ZipFile sobre site/\nexcluye .zip y .sha256]
    Z --> S[start-server.py incluido en ZIP]
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

Las funciones `_version`, `_load_hook`, `_pre_build`, `_build`, `_post_build`, `_zip`,
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
- `dist/doc_ia-docs-<versión>.zip` — sitio completo; versión leída de `pyproject.toml`.
- `dist/doc_ia-docs-<versión>.zip.sha256` — línea `<hash>  <nombre_zip>`.
- `dist/CHECKSUMS.txt` — registro acumulativo `<hash>  <nombre>  (<timestamp ISO>)`.
- stdout: progreso con prefijo `[build_docs_zip]` (comando de build, ruta del ZIP, tamaño en MB, hash).

**Hook**:
- `site/doc_ia-docs-latest.zip` — sitio completo; incluye `start-server.py` en la raíz del ZIP.
- `site/doc_ia-docs-latest.zip.sha256` — línea `<hash>  <nombre_zip>`.
- stdout: progreso con prefijo `[ZIP]` / `[OK]`.

### Errores y casos especiales

- **Script** — build fallido: proceso termina con el código de salida del builder (`sys.exit`).
  Con `zensical`, el pre-build ya se ha ejecutado (copias de `docs/` actualizadas) pero el
  post-build no: el ZIP "latest" de un build anterior no se sobrescribe.
- **Script** — `--no-build` sin `site/` existente: mensaje `ERROR` por stderr y código `1`.
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
`_pre_build`, `_build`, `_post_build`, `_zip`, `_sha256_file`, `_create_checksum_files`) y la
constante `HOOKLESS_BUILDERS`, sin clases. El hook (`mkdocs_hooks.py`) es el patrón
canónico de referencia para otros proyectos: copiar y cambiar únicamente `zip_path`.

## 4. Dependencias y Requisitos

| Dependencia | Propósito | Componente | Comportamiento sin ella |
|---|---|---|---|
| `argparse`, `hashlib`, `importlib`, `shutil`, `subprocess`, `tomllib`, `pathlib`, `datetime` (stdlib) | CLI, SHA256, ZIP, builder, carga de hooks, versión | script | — (stdlib Python ≥ 3.11) |
| `hashlib`, `os`, `zipfile`, `pathlib` (stdlib) | ZIP + SHA256 | hook | — (stdlib Python ≥ 3.11) |
| `mkdocs` + `mkdocs-material` | Builder por defecto; invocador del hook | ambos | Script: falla con su código de error. Hook: sin mkdocs no hay `on_post_build` |
| `zensical` | Builder alternativo | script | Solo con `--builder zensical`; falla si no está instalado en el intérprete que ejecuta el script |
| `hooks/sync_root_docs.py`, `mkdocs_hooks.py` | Pre/post-build para generadores sin hooks | script | Con `zensical`: error al cargarlos si faltan |
| `scripts/start-server.py` | Servidor HTTP local incluido en el ZIP | hook | ZIP válido, sin el servidor de conveniencia |

## 5. Ejemplos Relacionados

- [Ejemplo: Generar ZIP Offline](../examples/build_docs_zip_offline.md) — invocaciones CLI
  típicas, validación del checksum y output esperado.

## 6. Verificación y Tests

| Test | Qué verifica | Tipo |
|---|---|---|
| `test_main_builds_strict_and_packages_versioned_zip` | Build con `--strict`, ZIP versionado, `.sha256` y `CHECKSUMS.txt` | integración (CLI, build simulado) |
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
| `test_post_build_hook_creates_latest_zip` | `mkdocs_hooks.on_post_build`: ZIP `latest` + `.sha256`, incluye `start-server.py`, excluye `.zip`/`.sha256` | unitario |

```bash
python -m pytest tests/test_build_docs_zip.py -q
```

Sin cubrir: el build real con MkDocs o Zensical (se simula `subprocess.run`).

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
    | Hook: excluye `.zip`/`.sha256` e incluye `start-server.py` | `mkdocs_hooks.py::on_post_build` | ✅ |
    | Hook ejecutado antes del aborto por `--strict` | `mkdocs.commands.build::build` (MkDocs 1.6.1) | ⚠️ |
    | `_sha256` | `mkdocs_hooks.py::_sha256` | ✅ |
    | Dependencias stdlib del script y del hook | `scripts/build_docs_zip.py`, `mkdocs_hooks.py` (imports) | ✅ |
    | `zensical` como builder alternativo, invocado con `python -m` | `scripts/build_docs_zip.py::_build` | ✅ |
    | Pre/post-build para generadores sin hooks; post solo con build OK | `scripts/build_docs_zip.py::HOOKLESS_BUILDERS`, `::_build`, `::_pre_build`, `::_post_build` | ✅ |
    | Carga de hooks por ruta desde la raíz | `scripts/build_docs_zip.py::_load_hook` | ✅ |
    | Zensical ignora `hooks:` de `mkdocs.yml` | zensical.org/compatibility/configuration (Zensical 0.0.73) | ⚠️ |
    | `start-server.py` opcional en el ZIP | `mkdocs_hooks.py::on_post_build` (`if server_script.exists()`) | ✅ |
