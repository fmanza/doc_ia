---
arquetipo: "12"
fuentes:
  .claude/settings.json.example: e1c10842aa20
  .github/workflows/docs-zip-release.yml: 20d18f9f3c59
  CLAUDE.md: a167ad648656
  hooks/sync_root_docs.py: ef5e576436c6
  mkdocs.yml: 417c1a6602da
  mkdocs_hooks.py: 2f510611cb6f
  scripts/build_docs_zip.py: b9a2694d122f
  scripts/check_env.py: a30937ae040f
  scripts/convert_to_md.py: e7e60518d96f
  scripts/doc_trace.py: a1824b159937
  scripts/start-server.py: ec67386821f7
revisado: 2026-10-28
---
# Referencia — doc_ia

Superficie que consulta quien ejecuta u opera el tooling de doc_ia: configuración, comandos de
línea de comandos, códigos de salida y eventos de build. La API interna de cada script está en
[Referencia Técnica](../api/check_env.md).

## 1. Configuración

| Clave | Origen | Tipo | Por defecto | Descripción |
|---|---|---|---|---|
| `CUDA_VISIBLE_DEVICES` | `env` | cadena | `""` (lo fija `convert_to_md.py` al importarse si no existe) | Visibilidad de GPU para docling. `--device cpu` la fija a `""`; `--device cuda` la elimina; `--device auto` respeta un valor exportado por el usuario e ignora el que fija el propio módulo |
| `project.version` | fichero `pyproject.toml` | cadena SemVer | `0.1.0` (valor actual) | Versión usada en el nombre del ZIP (`doc_ia-docs-{versión}.zip`) y en la release `docs-v{versión}` |
| `site_dir` | fichero `mkdocs.yml` | ruta | `site` | Directorio de salida del build; `mkdocs_hooks.py` lo lee de la configuración. `build_docs_zip.py` usa `site/` fijo |
| `hooks` | fichero `mkdocs.yml` | lista de rutas | `hooks/sync_root_docs.py`, `mkdocs_hooks.py` | Hooks MkDocs cargados en cada build (ver §4). Zensical los ignora: con `--builder zensical`, `build_docs_zip.py` los ejecuta él mismo |
| `hooks.PostToolUse` | fichero `.claude/settings.json` (no versionado; plantilla en `.claude/settings.json.example`) | objeto JSON | `sync_root_docs.py` + ruff + mypy + pytest `--collect-only` sobre `Edit\|Write` | Sincronización y validaciones automáticas tras cada edición en Claude Code |

!!! note "Sin secretos"
    doc_ia no lee credenciales ni API keys. `.gitignore` excluye `.env`, `.env.*` y `*.key`.

## 2. CLI y Comandos

### build_docs_zip.py

```bash
python scripts/build_docs_zip.py [--builder {mkdocs,zensical}] [--no-strict] [--no-build] [--output-dir DIR]
```

| Opción / Argumento | Tipo | Por defecto | Descripción |
|---|---|---|---|
| `--builder` | `mkdocs` \| `zensical` | `mkdocs` | Generador usado en el build (`python -m <builder> build`). Con `zensical` ejecuta antes `hooks/sync_root_docs.py` y, si el build termina con `0`, `mkdocs_hooks.py` |
| `--no-strict` | flag | desactivado (build con `--strict`) | Construye sin `--strict` |
| `--no-build` | flag | desactivado | Omite el build y empaqueta el `site/` existente |
| `--output-dir` | ruta | `dist` | Directorio del ZIP; relativo a la raíz del repositorio si no es absoluto |

Salida: `{output-dir}/doc_ia-docs-{versión}.zip`, `.zip.sha256` y una línea añadida a `CHECKSUMS.txt`.

### check_env.py

```bash
python scripts/check_env.py
```

Sin opciones. Comprueba las herramientas obligatorias (`mkdocs`, `ruff`, `mypy`, `pytest`) y
avisa de las opcionales (`zensical`, `docling`, `markitdown` y sus plugins, `pandoc`).

### convert_to_md.py

```bash
python scripts/convert_to_md.py <source> [opciones]
```

| Opción / Argumento | Tipo | Por defecto | Descripción |
|---|---|---|---|
| `source` | ruta (obligatorio) | — | Fichero o directorio a convertir; la salida va a `<origen>/md/` |
| `--engine` | `docling` \| `markitdown` \| `pandoc` | `docling` | Motor de conversión |
| `--dry-run` | flag | desactivado | Muestra qué se convertiría sin convertir |
| `--validate-only` | flag | desactivado | Solo validación previa (tamaño, integridad ZIP, cabeceras) |
| `--force` | flag | desactivado | Re-convierte aunque exista el `.md` de salida |
| `--metadata` | flag | desactivado | Añade frontmatter YAML con metadatos |
| `--chunk` | flag | desactivado | Genera chunks para RAG (solo `docling`) |
| `--chunk-max-tokens` | entero | `512` | Tamaño máximo de chunk |
| `--ocr` / `--no-ocr` | flag | `--ocr` | Habilita o deshabilita OCR |
| `--ocr-engine` | `auto` \| `easyocr` \| `tesseract` \| `rapidocr` | `auto` | Motor OCR de docling |
| `--ocr-lang` | lista separada por comas | `es,en` | Idiomas OCR |
| `--table-mode` | `accurate` \| `fast` | `accurate` | Extracción de tablas (docling) |
| `--image-export` | `placeholder` \| `embedded` \| `referenced` | `placeholder` | Exportación de imágenes |
| `--pdf-backend` | `docling-parse` \| `pypdfium2` | `docling-parse` | Backend PDF de docling |
| `--timeout` | entero (segundos) | `300` | Timeout por documento |
| `--device` | `cpu` \| `cuda` \| `auto` | `cpu` | Dispositivo de cómputo; `auto` usa GPU si `nvidia-smi` la detecta, salvo que el usuario haya exportado `CUDA_VISIBLE_DEVICES=""` |
| `--num-threads` | entero | `4` | Hilos CPU de docling |
| `--flash-attention` | flag | desactivado | Flash Attention 2; requiere `--device cuda` o `auto` |
| `--batch-size` | entero | `1` | Documentos por lote; `>1` solo con `docling` |
| `--workers` | entero | `1` | Concurrencia por lote; `>1` solo con `docling` |

### doc_trace.py

```bash
python scripts/doc_trace.py [--root DIR] {drift,stamp,matrix,llms} [opciones]
```

| Opción / Argumento | Tipo | Por defecto | Descripción |
|---|---|---|---|
| `--root` | ruta | raíz del repositorio | Base para resolver las fuentes del frontmatter (global, antes del subcomando) |
| `drift --docs` | ruta | `docs` | Carpeta donde buscar páginas con frontmatter `fuentes` |
| `stamp <páginas…>` | rutas (obligatorio) | — | Páginas a sellar |
| `stamp --source` | ruta (repetible) | fuentes actuales del frontmatter | Ficheros de los que deriva la página |
| `stamp --archetype` | cadena | el actual del frontmatter | Arquetipo de la página (`1`, `1-I`, `2`, `12`…) |
| `stamp --date` | `YYYY-MM-DD` | hoy | Fecha `revisado` |
| `matrix --docs` | ruta | `docs` | Se leen los `AC-xx` de `<docs>/functional/*.md` |
| `matrix --tests` | ruta | `tests` | Carpeta con `test_*.py` |
| `matrix --output` | ruta | stdout | Fichero Markdown de la matriz |
| `llms --config` | ruta | `mkdocs.yml` | Configuración con `site_name`, `site_url` y `nav` |
| `llms --output` | ruta | `docs/llms.txt` | Fichero generado |
| `llms --site-url` | URL | `site_url` de `mkdocs.yml` | Base de los enlaces |
| `llms --check` | flag | desactivado | Solo comprueba que el fichero está al día |

### start-server.py

```bash
python start-server.py [--port PORT] [--no-browser]
```

Se distribuye dentro del ZIP offline (lo añade `mkdocs_hooks.py`) y sirve el directorio donde está.

| Opción / Argumento | Tipo | Por defecto | Descripción |
|---|---|---|---|
| `--port` | entero | `8000` | Puerto HTTP local |
| `--no-browser` | flag | desactivado | No abre el navegador automáticamente |

### sync_root_docs.py

```bash
python hooks/sync_root_docs.py
```

Sin opciones. Copia `CHANGELOG.md` → `docs/changelog.md` y `CONTRIBUTING.md` → `docs/contributing.md`.

## 3. Errores y Códigos de Salida

| Código / Error | Origen | Cuándo ocurre | Acción recomendada |
|---|---|---|---|
| `0` | `build_docs_zip.py` | ZIP y checksums generados | — |
| `1` | `build_docs_zip.py` | `--no-build` sin `site/` existente | Ejecutar sin `--no-build` |
| `≠ 0` (propagado) | `build_docs_zip.py` | El build del generador falla (p. ej. enlace roto con `--strict`) | Corregir los avisos del build |
| `2` | `build_docs_zip.py`, `convert_to_md.py`, `start-server.py` | Opción desconocida o valor fuera de `choices` (argparse) | Revisar la sinopsis del §2 |
| `0` | `check_env.py` | Herramientas obligatorias presentes (con o sin avisos de opcionales) | — |
| `1` | `check_env.py` | Falta alguna herramienta obligatoria | Instalar las listadas (`pip install -r requirements.txt`) |
| `0` | `convert_to_md.py` | Conversión completa, validación sin errores o ningún fichero convertible | — |
| `1` | `convert_to_md.py` | Origen inexistente, motor no instalado, errores de validación o de conversión, `--device cuda` sin `nvidia-smi` | Ver el mensaje `ERROR:`; instalar el motor o cambiar `--engine` |
| `2` | `convert_to_md.py` | Combinación inválida: `--chunk`, `--batch-size >1` o `--workers >1` sin `docling`; `--flash-attention` con `--device cpu` | Ajustar las opciones |
| `0` | `start-server.py` | Servidor detenido con Ctrl+C | — |
| `1` | `start-server.py` | Puerto ocupado (excepción no capturada) 🔍 | Usar otro `--port` |
| `0` | `doc_trace.py` | Sin drift, sin tests citados inexistentes, `llms.txt` al día o sellado correcto | — |
| `1` | `doc_trace.py drift` | Alguna fuente `stale`, `missing` u `outside_repo` | Revisar la página contra el cambio y re-sellar con `stamp` |
| `1` | `doc_trace.py stamp` | Página o fuente inexistente, fuente fuera del repositorio o página sin fuentes | Corregir la ruta o `--source` |
| `1` | `doc_trace.py matrix` | La columna `Test` cita un test que no existe | Corregir el criterio o crear el test |
| `1` | `doc_trace.py llms` | `mkdocs.yml` sin `nav` o ilegible; con `--check`, `llms.txt` no coincide con el `nav` actual | Revisar `--config`; ejecutar `llms` sin `--check` |
| `2` | `doc_trace.py` | Sin subcomando u opción desconocida (argparse) | Revisar la sinopsis del §2 |
| `0` | `sync_root_docs.py` | Siempre; un fichero raíz ausente solo genera un aviso | — |

## 4. Eventos y Mensajes

| Evento / Mensaje | Productor | Consumidor | Payload / formato |
|---|---|---|---|
| `on_pre_build` | MkDocs | `hooks/sync_root_docs.py` | Configuración MkDocs (`docs_dir`); copia los ficheros raíz a `docs/` |
| `on_post_build` | MkDocs | `mkdocs_hooks.py` | Configuración MkDocs (`site_dir`); genera `site/doc_ia-docs-latest.zip` + `.sha256` |
| Pre/post-build sin hooks | `build_docs_zip.py --builder zensical` | `sync_root_docs.main()` / `mkdocs_hooks.on_post_build({"site_dir": ...})` | Mismo efecto que los dos eventos anteriores; el post-build solo si el build termina con `0` |
| `PostToolUse` (`Edit\|Write`) | Claude Code | Comandos de `.claude/settings.json` | Ejecuta `sync_root_docs.py`, ruff, mypy y pytest `--collect-only`; salida truncada a 5–15 líneas |
| Prefijos de log `[build_docs_zip]`, `[ZIP]`, `[OK]`, `[sync_root_docs]`, `[doc_ia-docs]` | Scripts y hooks | Usuario / CI | Texto libre por stdout; sin contrato estable más allá del prefijo |

## 5. Interfaces Publicadas

| Interfaz | Tipo | Contrato fuente | Descripción |
|---|---|---|---|
| ZIP offline `doc_ia-docs-{versión}.zip` | Fichero de salida | `scripts/build_docs_zip.py::_zip` | Sitio HTML completo; nombre estable por versión |
| `doc_ia-docs-{versión}.zip.sha256` | Fichero de salida | `scripts/build_docs_zip.py::_create_checksum_files` | Formato `sha256sum`: `<hash>  <fichero>` |
| `CHECKSUMS.txt` | Fichero de salida (acumulativo) | `scripts/build_docs_zip.py::_create_checksum_files` | Una línea por build: `<hash>  <fichero>  (<ISO-8601>)` |
| Release `docs-v{versión}` | GitHub Release | `.github/workflows/docs-zip-release.yml` | ZIP + `.sha256` + `CHECKSUMS.txt`; se actualiza en cada push a `main` con cambios en `docs/` |
| Ficheros `<origen>/md/**/*.md` | Fichero de salida | `scripts/convert_to_md.py::output_path` | Estructura reflejada del origen; frontmatter opcional con `--metadata` |
| `llms.txt` | Fichero de salida publicado en la raíz del sitio | `scripts/doc_trace.py::build_llms_txt` | Índice para agentes IA ([llmstxt.org](https://llmstxt.org/)): un `##` por sección del `nav` y un enlace por página |
| Matriz de trazabilidad | Fichero de salida (Markdown) | `scripts/doc_trace.py::build_matrix` | Criterios y tests por página, tests citados inexistentes y tests sin criterio |

## 6. Datos

doc_ia no tiene base de datos. Sus datos son los **ficheros con formato propio** que escribe el
tooling.

```mermaid
erDiagram
    DOCUMENTO_ORIGEN ||--|| MARKDOWN : "convert_to_md genera"
    MARKDOWN ||--o| FRONTMATTER : "incluye con --metadata"
    MARKDOWN ||--o{ CHUNK : "se divide con --chunk"
    MANIFIESTO ||--|{ CHUNK : "indexa"
    ZIP_OFFLINE ||--|| SHA256 : "acompañado de"
    ZIP_OFFLINE ||--o{ LINEA_CHECKSUMS : "registrado en"
    PAGINA_DOCS ||--o| TRAZABILIDAD : "declara"
    TRAZABILIDAD ||--|{ FUENTE : "huella por"
```

| Entidad | Campo | Tipo | Restricción | Sensibilidad |
|---|---|---|---|---|
| Frontmatter | `source` | cadena | Nombre del fichero origen (sin ruta) | interna |
| Frontmatter | `engine` | cadena | `docling` \| `markitdown` \| `pandoc` | pública |
| Frontmatter | `converted_at` | fecha-hora UTC | Formato `YYYY-MM-DDTHH:MM:SS` | pública |
| Frontmatter | `engine_version` | cadena | Solo con `docling`: versión del paquete instalado (p. ej. `2.107.0`); `unknown` si no está instalado | pública |
| Frontmatter | `title` | cadena | Solo con `docling`; nombre del documento o del fichero | interna |
| Manifiesto `_manifest.json` | `id` | entero | Correlativo desde 1 | pública |
| Manifiesto `_manifest.json` | `file` | cadena | `NNN.md` (3 dígitos) dentro de `chunks/<documento>/`, junto al `.md` convertido | pública |
| Manifiesto `_manifest.json` | `preview` | cadena | Primeros 80 caracteres del chunk | interna |
| Manifiesto `_manifest.json` | `chars` | entero | Longitud del chunk | pública |
| `.zip.sha256` | línea única | texto | `<sha256>  <nombre.zip>` (formato `sha256sum`) | pública |
| `CHECKSUMS.txt` | una línea por build | texto | `<sha256>  <nombre.zip>  (<ISO-8601 local>)`; solo se añaden líneas | pública |
| Frontmatter de trazabilidad | `arquetipo` | cadena | `1`, `1-I`, `2`, `12`… | pública |
| Frontmatter de trazabilidad | `fuentes` | mapa ruta → huella | Rutas relativas dentro del repositorio; huella = 12 hex de SHA256 con saltos LF (en `.md`, sin su frontmatter) | pública |
| Frontmatter de trazabilidad | `revisado` | fecha | `YYYY-MM-DD` | pública |

La sensibilidad `interna` indica que el campo reproduce contenido o nombres del documento
convertido: hereda la sensibilidad del origen.

??? note "Evidencia"

    | Elemento | Fuente | Confianza |
    |---|---|---|
    | `CUDA_VISIBLE_DEVICES` por defecto `""` | `scripts/convert_to_md.py::_CUDA_ENV_INJECTED` | ✅ |
    | `--device auto` distingue el valor por defecto del valor del usuario | `scripts/convert_to_md.py::_detect_device` | ✅ |
    | `project.version` | `scripts/build_docs_zip.py::_version` | ✅ |
    | `site_dir` fijo en `build_docs_zip.py` | `scripts/build_docs_zip.py::SITE_DIR` | ✅ |
    | `hooks` de MkDocs | `mkdocs.yml::hooks` | ✅ |
    | `hooks.PostToolUse` — `sync_root_docs.py` primero, como describe `CLAUDE.md` | `.claude/settings.json.example` | ✅ |
    | Opciones de `build_docs_zip.py` | `scripts/build_docs_zip.py::main` | ✅ |
    | Herramientas de `check_env.py` | `scripts/check_env.py::REQUIRED_TOOLS` | ✅ |
    | Opciones y restricciones de `convert_to_md.py` | `scripts/convert_to_md.py::_parse_args` | ✅ |
    | Opciones de `start-server.py` | `scripts/start-server.py::main` | ✅ |
    | Código `1` por puerto ocupado | `scripts/start-server.py::main` (sin manejo de `OSError`) | 🔍 |
    | Códigos de `check_env.py` | `scripts/check_env.py::main` | ✅ |
    | Códigos de `convert_to_md.py` | `scripts/convert_to_md.py::main`, `::_detect_device`, `::_parse_args` | ✅ |
    | Código `0` de `sync_root_docs.py` | `hooks/sync_root_docs.py::main` | ✅ |
    | `on_pre_build` | `hooks/sync_root_docs.py::on_pre_build` | ✅ |
    | `on_post_build` + `start-server.py` en el ZIP | `mkdocs_hooks.py::on_post_build` | ✅ |
    | Pre/post-build ejecutados por el script con `zensical` | `scripts/build_docs_zip.py::HOOKLESS_BUILDERS`, `::_pre_build`, `::_post_build` | ✅ |
    | Release `docs-v{versión}` | `.github/workflows/docs-zip-release.yml::build-and-publish` | ✅ |
    | Salida `md/` de `convert_to_md.py` | `scripts/convert_to_md.py::output_path` | ✅ |
    | Campos del frontmatter | `scripts/convert_to_md.py::_build_metadata_basic`, `::_convert_with_docling`, `::_docling_version` | ✅ |
    | Serialización YAML del frontmatter | `scripts/convert_to_md.py::_format_frontmatter` | ✅ |
    | Manifiesto y chunks | `scripts/convert_to_md.py::_run_chunking` | ✅ |
    | Formato `.sha256` y `CHECKSUMS.txt` | `scripts/build_docs_zip.py::_create_checksum_files` | ✅ |
    | Opciones de `doc_trace.py` | `scripts/doc_trace.py::_parser` | ✅ |
    | Códigos de `doc_trace.py` | `scripts/doc_trace.py::_cmd_drift`, `::_cmd_stamp`, `::_cmd_matrix`, `::_cmd_llms` | ✅ |
    | `llms.txt` | `scripts/doc_trace.py::build_llms_txt` | ✅ |
    | Matriz de trazabilidad | `scripts/doc_trace.py::build_matrix` | ✅ |
    | Frontmatter de trazabilidad y huella | `scripts/doc_trace.py::format_frontmatter`, `::fingerprint` | ✅ |
