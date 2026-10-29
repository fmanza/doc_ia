---
arquetipo: "2"
fuentes:
  scripts/doc_trace.py: 9b1c4d981f6a
  tests/test_doc_trace.py: f8c5c5a612ab
revisado: 2026-10-29
---
# doc_trace

Trazabilidad determinista entre la documentación y el código: sella huellas SHA256 de las fuentes en el frontmatter de cada página, detecta páginas desactualizadas (drift), cruza criterios de aceptación con tests reales y genera `llms.txt` desde el `nav` de `mkdocs.yml`.

## 1. Arquitectura y Diseño

```mermaid
flowchart TD
    accTitle: Subcomandos de doc_trace y sus funciones
    accDescr: main despacha a cuatro subcomandos; drift y stamp comparten la lectura del frontmatter y el cálculo de huellas, matrix cruza criterios con los IDs de test y llms recorre el nav; la lectura YAML es común a frontmatter y llms.
    CLI[main · argparse] --> sdrift & sstamp & smatrix & sllms
    subgraph sdrift[drift]
        DR[check_drift]
    end
    subgraph sstamp[stamp]
        ST[stamp_page] --> FF[format_frontmatter]
    end
    subgraph smatrix[matrix]
        CC[collect_criteria] --> BM[build_matrix]
        CT[collect_test_ids · ast] --> BM
    end
    subgraph sllms[llms]
        BL[build_llms_txt] --> NV[_nav_entries + _page_url]
    end
    DR & ST --> RM[read_page_meta]
    DR & ST --> FP[fingerprint]
    RM & BL --> Y[_load_yaml · PyYAML]
```

Script standalone sin dependencias de otros módulos del proyecto. Cada subcomando es una
función `_cmd_*` que delega en funciones puras sobre `Path`, de modo que los tests las
ejercitan con repositorios temporales sin red; `baseline` y `changes` usan además git local.

### Modo incremental (`baseline` y `changes`)

```mermaid
flowchart TD
    accTitle: Modo incremental de doc_trace
    accDescr: baseline guarda el commit del origen en el estado del destino; changes lo lee, pide a git los ficheros cambiados desde ese commit, descarta los artefactos de la documentación y cruza cada ruta con las citas de las páginas; sin baseline utilizable termina con código 3.
    B[_cmd_baseline] --> TB["take_baseline · git rev-parse"]
    TB --> WB[write_baseline]
    WB --> ST[(".ai/doc_state.json")]
    C[_cmd_changes] --> CC[check_changes]
    ST --> CC
    CC -- "sin baseline utilizable" --> X[código 3 · modo completo]
    CC --> CF["changed_files · git diff -z"]
    CF --> DP[documentation_paths excluye artefactos]
    DP --> PC["pages_citing · cita o mención"]
    PC --> LE[linked_examples]
    LE --> FC[format_changes · código 0 o 1]
```

`baseline` se ejecuta en el CIERRE de `/document-project` y `changes` al empezar la Fase 1.
Las rutas de git y las citas se comparan en POSIX y relativas a la raíz del origen
(`git diff --relative`), aunque el origen sea una subcarpeta de un repositorio.

## 2. Modelo de Datos / Contratos

### API pública

| Función/Clase | Firma simplificada | Descripción | Retorna |
|---|---|---|---|
| `PageMeta` | `dataclass(frozen)`: `page`, `archetype`, `sources: dict[str, str]`, `reviewed` | Frontmatter de trazabilidad de una página | — |
| `DriftFinding` | `dataclass(frozen)`: `page`, `source`, `status` | Fuente desactualizada; `status` ∈ `stale` \| `missing` \| `outside_repo` | — |
| `CriterionRow` | `dataclass(frozen)`: `page`, `criterion`, `tests: tuple[str, ...]` | Fila `AC-xx` de una página funcional | — |
| `fingerprint` | `fingerprint(path) -> str` | SHA256 truncado a `HASH_LENGTH` (12) con CRLF→LF; en `.md` excluye el frontmatter | Huella hex |
| `read_page_meta` | `read_page_meta(page) -> PageMeta \| None` | Lee el frontmatter; `None` si no hay o no declara `fuentes` | `PageMeta` o `None` |
| `format_frontmatter` | `format_frontmatter(meta) -> str` | Serializa el frontmatter con fuentes ordenadas | Bloque `---…---\n` |
| `stamp_page` | `stamp_page(page, repo_root, *, sources=None, archetype=None, reviewed=None) -> PageMeta` | Recalcula huellas y reescribe el frontmatter conservando el cuerpo | `PageMeta` escrito |
| `check_drift` | `check_drift(docs_dir, repo_root) -> list[DriftFinding]` | Recorre `docs_dir/**/*.md` sellados y compara huellas | Hallazgos en orden estable |
| `collect_test_ids` | `collect_test_ids(tests_dir, repo_root) -> set[str]` | Ids `tests/x.py::test_y` y `::Clase::test_y` vía `ast` (sin importar los tests) | Conjunto de ids |
| `collect_criteria` | `collect_criteria(functional_dir) -> list[CriterionRow]` | Filas `\| AC-xx \|` de `functional_dir/*.md`; tests de la última celda si la fila tiene ≥5 celdas | Filas |
| `build_matrix` | `build_matrix(criteria, test_ids, repo_root) -> tuple[str, list[str]]` | Matriz Markdown por página, totales, tests inexistentes y tests sin criterio | `(markdown, inexistentes)` |
| `build_llms_txt` | `build_llms_txt(mkdocs_yml, site_url=None) -> str` | `llms.txt` con `site_name`, `site_description` y una sección `##` por grupo del `nav` | Contenido |
| `OriginChange` | `dataclass(frozen)`: `kind`, `path`, `old_path` | Fichero cambiado; `kind` ∈ `A` \| `M` \| `D` \| `R` (`old_path` solo en `R`; las copias cuentan como `A`) | — |
| `OriginBaseline` | `dataclass(frozen)`: `commit`, `branch`, `dirty`, `date` | Estado del origen al cerrar la sesión; `commit=None` si no hay git | — |
| `ChangeReport` | `dataclass(frozen)`: `status`, `reason`, `base`, `changes`, `pages`, `mentions`, `examples` | Resultado de `changes`; `status` ∈ `ok` \| `fallback` | — |
| `take_baseline` | `take_baseline(origin, excluded=(), today=None) -> OriginBaseline` | `HEAD`, rama y cambios pendientes fuera de `excluded` | `OriginBaseline` |
| `write_baseline` | `write_baseline(state_path, name, baseline) -> None` | Escribe la entrada del origen y la versión de doc_ia; conserva los demás orígenes | — |
| `read_state` | `read_state(state_path) -> dict[str, Any]` | Lee `.ai/doc_state.json` | `{}` si no existe |
| `changed_files` | `changed_files(origin, base, excluded=()) -> list[OriginChange] \| None` | `git diff --name-status -z -M --relative <base>` + ficheros sin seguimiento | Cambios ordenados o `None` si git falla |
| `documentation_paths` | `documentation_paths(origin, docs_dir) -> tuple[str, ...]` | Artefactos de la documentación dentro del origen (`docs/`, `DOC_ARTIFACTS`) | Rutas POSIX relativas al origen |
| `pages_citing` | `pages_citing(docs_dir, paths, name) -> tuple[dict, dict]` | Por ruta: páginas que la citan (frontmatter o bloque «Evidencia») y páginas que solo la mencionan | `(citas, menciones)` |
| `linked_examples` | `linked_examples(pages, docs_dir) -> tuple[Path, ...]` | Ejemplos enlazados desde las páginas de `api/` afectadas | Rutas de ejemplos |
| `check_changes` | `check_changes(origin, docs_dir, state_path, name) -> ChangeReport` | Valida el baseline y compone el informe | `ChangeReport` |
| `format_changes` | `format_changes(report, name, root) -> str` | Informe Markdown para el INVENTARIO | Markdown |
| `main` | `main(argv=None) -> int` | CLI con subcomandos `drift`, `stamp`, `matrix`, `llms`, `baseline`, `changes` | Código de salida |

### Contrato de entrada

| Parámetro | Tipo | Descripción | Restricciones |
|---|---|---|---|
| `--root` | `Path` | Raíz del repositorio (opción global, antes del subcomando) | Por defecto, el padre de `scripts/` |
| `drift --docs` | `Path` | Carpeta de documentación | Por defecto `docs/` |
| `stamp pages` | `Path` (1..n) | Páginas a sellar | Deben existir |
| `stamp --source` | `str` (repetible) | Fuente relativa a `--root` | Dentro del repositorio y existente; si se omite, se reutilizan las del frontmatter; si se indica, sustituye la lista completa (no añade) |
| `stamp --archetype` / `--date` | `str` | Arquetipo y fecha `YYYY-MM-DD` | Por defecto, el arquetipo actual y la fecha del día |
| `matrix --docs` / `--tests` / `--output` | `Path` | Carpetas de docs y tests; fichero de salida opcional | Lee `--docs/functional/*.md` (no recursivo) |
| `llms --config` / `--output` / `--site-url` / `--check` | `Path` / `str` / flag | Configuración MkDocs, destino, URL base, modo comprobación | Por defecto `mkdocs.yml`, `docs/llms.txt` y `site_url` del config |
| `baseline` / `changes --origin` | `Path` | Raíz del origen documentado | Obligatorio; puede ser una subcarpeta de un repositorio |
| `baseline` / `changes --name` | `str` | Clave del origen en el estado | Por defecto, el nombre de la carpeta del origen (regla de `_fuentes/`) |
| `baseline` / `changes --docs` / `--state` | `Path` | Docs y estado del destino | Por defecto `<--root>/docs` y `<--root>/.ai/doc_state.json` |
| `changes --output` | `Path` | Fichero Markdown del informe | Por defecto, stdout |

### Contrato de salida

- Frontmatter escrito por `stamp`: `arquetipo` entre comillas, `fuentes` ordenadas
  alfabéticamente, `revisado`, saltos de línea LF.
- `drift`: una línea `[doc_trace] <status> <página> ← <fuente>` por hallazgo.
- `matrix`: Markdown a stdout o a `--output` (crea el directorio padre).
- `baseline`: `.ai/doc_state.json` con `{"doc_ia": <versión>, "origenes": {<nombre>: {"commit",
  "rama", "sucio", "fecha"}}}`, orígenes ordenados, UTF-8 y LF; código `0` (también sin git,
  con `commit: null`).
- `changes`: tabla `| Cambio | Fichero | Lo citan (Evidencia) | Lo mencionan |` y listas de
  páginas a revisar, páginas que solo lo mencionan, ejemplos enlazados y ficheros sin página;
  código `0` sin cambios, `1` con cambios, `3` sin baseline utilizable.
- `llms`: URLs absolutas con `site_url`; con `use_directory_urls: true`, `x.md` → `x/` e
  `index.md` → raíz de su carpeta; sin `site_url`, rutas relativas. Las entradas del `nav`
  que no son `.md` se omiten y las páginas de primer nivel van a "Páginas principales".

### Errores y casos especiales

| Caso | Comportamiento |
|---|---|
| Fuente con `../` fuera de `--root` | `drift`: hallazgo `outside_repo` sin leer el fichero; `stamp`: `ValueError` → código `1` |
| `stamp` sin `--source` ni fuentes previas | `ValueError("sin fuentes")` → código `1` |
| Fuente inexistente al sellar | `ValueError` → código `1` |
| Página inexistente al sellar | `OSError` capturado en `_cmd_stamp` → `[doc_trace] ERROR:` y código `1` |
| Etiquetas `!!python/name:` o `!ENV` en `mkdocs.yml` | Se ignoran (`_load_yaml` con `SafeLoader` derivado) |
| `mkdocs.yml` sin `nav` | `ValueError` capturado en `_cmd_llms` → `[doc_trace] ERROR:` y código `1` |
| Consola no UTF-8 (cp1252) | Solo al ejecutarse como script, stdout/stderr se reconfiguran a UTF-8 |
| `changes`: sin entrada, `commit: null`, commit fuera del historial o versión menor de doc_ia distinta | `ChangeReport("fallback", motivo)` → motivo por stderr y código `3` |
| Destino dentro del origen | `docs/`, `.ai/`, `_fuentes/`, `mkdocs.yml`, `VER_DOCUMENTACION.md` y `VIEW_DOCS.md` no cuentan como cambios ni como cambios pendientes |
| Rutas con caracteres no ASCII | `git … -z` evita el entrecomillado de `core.quotepath` |
| git ausente o con error | `_git` devuelve `None` (sin excepción); `baseline` guarda `commit: null` |

## 3. Componentes y Clases

| Componente | Responsabilidad |
|---|---|
| `PageMeta`, `DriftFinding`, `CriterionRow` | Dataclasses inmutables de transporte entre funciones |
| `_load_yaml` | Único punto de importación de PyYAML (import diferido, sin stubs) |
| `_resolve_source` | Guarda de seguridad: resuelve la ruta y exige `is_relative_to(repo_root)` |
| `_nav_entries`, `_page_url` | Aplanado del `nav` («Grupo › Página») y cálculo de URLs publicadas |
| `_cmd_drift`, `_cmd_stamp`, `_cmd_matrix`, `_cmd_llms`, `_cmd_baseline`, `_cmd_changes`, `_parser` | Capa CLI: argumentos, mensajes `[doc_trace]` y códigos de salida |
| `_git` | Único punto de llamada a git: lista de argumentos sin shell, `-C <origen>`, timeout `GIT_TIMEOUT` (60 s) |
| `_split_citations`, `_citation_re` | Zona de citas (frontmatter + bloque «Evidencia») y regex de ruta completa (no sufijo), con o sin prefijo de origen |

## 4. Dependencias y Requisitos

| Dependencia | Propósito | Requerida | Comportamiento sin ella |
|---|---|---|---|
| PyYAML (instalada con `mkdocs`) | Leer frontmatter y `mkdocs.yml` | Para `drift`, `stamp` y `llms` | `ImportError` al ejecutarlos; `matrix` funciona sin ella |
| `ast`, `hashlib`, `re`, `argparse`, `pathlib`, `dataclasses`, `datetime`, `json`, `subprocess`, `tomllib` (stdlib) | Tests vía AST, huellas, regex, CLI, estado y git | Sí | — (siempre disponibles) |
| git (binario) | Historial del origen para `baseline` y `changes` | Solo modo incremental | `baseline` guarda `commit: null`; `changes` → código `3` (modo completo) |

## 5. Ejemplos Relacionados

- [Ejemplo: Auditar la Trazabilidad](../examples/doc_trace_usage.md) — uso de `check_drift`
  y `build_matrix` desde código propio y de los cuatro subcomandos con su salida real.

## 6. Verificación y Tests

| Test | Qué verifica | Tipo |
|---|---|---|
| `test_fingerprint_*` (2) | Huella independiente de CRLF/LF y del frontmatter en `.md` | unitario |
| `test_read_page_meta_*` (3) | Sin frontmatter, sin `fuentes` y lectura de los tres campos | unitario |
| `test_stamp_then_no_drift`, `test_stamp_preserves_existing_sources_and_archetype` (2) | Sellado, conservación del cuerpo y reutilización de fuentes/arquetipo | unitario |
| `test_drift_*` (3) | Hallazgos `stale`, `missing` y `outside_repo` | unitario |
| `test_stamp_rejects_source_outside_repo`, `test_stamp_requires_sources` (2) | Errores de `stamp_page` | unitario |
| `test_collect_test_ids_includes_class_methods`, `test_matrix_reports_unknown_and_uncited` (2) | Ids de tests (incluidos métodos de clase), inexistentes y sin citar | unitario |
| `test_main_matrix_exit_code_on_unknown_test` (1) | `matrix` devuelve `1` con un test inexistente | integración (CLI) |
| `test_build_llms_txt_tolerates_python_tags` (1) | Etiquetas `!!python/name:`, URLs con `site_url` y omisión de enlaces externos | unitario |
| `test_main_llms_check_detects_outdated` (1) | `llms --check` antes y después de generar | integración (CLI) |
| `test_main_llms_without_nav_returns_error`, `test_main_stamp_missing_page_returns_error` (2) | Errores controlados de la CLI con código `1` | integración (CLI) |
| `test_main_requires_subcommand` (1) | Sin subcomando → `SystemExit(2)` | integración (CLI) |
| `test_baseline_records_clean_head`, `test_write_baseline_keeps_other_origins` (2) | Estado escrito: commit, rama, pendiente, versión; conserva otros orígenes | integración (git local) / unitario |
| `test_changes_*` (4 funciones, 7 casos) | Sin cambios (0), citas/menciones/renombrados/ñ/ejemplos (1), prefijo multiorigen y los cuatro motivos de modo completo (3) | integración (git local) |
| `test_baseline_without_git_then_changes_is_full_mode` (1) | Origen sin git → `commit: null` y `changes` con código 3 | integración (CLI) |
| `test_destination_inside_origin_ignores_its_own_artifacts`, `test_origin_in_subfolder_of_repository_uses_origin_relative_paths` (2) | Artefactos propios excluidos; origen en subcarpeta | integración (git local) |

Sin cubrir: los mensajes de `drift` y `stamp` por la CLI, `llms` sin `site_url` y la
reconfiguración UTF-8 de la consola.

```bash
python -m pytest tests/test_doc_trace.py -q
```

??? note "Evidencia"

    | Elemento | Fuente | Confianza |
    |---|---|---|
    | `PageMeta`, `DriftFinding`, `CriterionRow` | `scripts/doc_trace.py::PageMeta`, `::DriftFinding`, `::CriterionRow` | ✅ |
    | Huella de 12 hex, CRLF→LF y sin frontmatter en `.md` | `scripts/doc_trace.py::fingerprint`, `::HASH_LENGTH` | ✅ |
    | Lectura del frontmatter | `scripts/doc_trace.py::read_page_meta`, `::FRONTMATTER_RE` | ✅ |
    | Serialización ordenada | `scripts/doc_trace.py::format_frontmatter` | ✅ |
    | `stamp_page` y sus errores | `scripts/doc_trace.py::stamp_page` | ✅ |
    | Guarda fuera del repositorio | `scripts/doc_trace.py::_resolve_source` | ✅ |
    | `check_drift` y orden estable | `scripts/doc_trace.py::check_drift` | ✅ |
    | Ids de tests vía AST | `scripts/doc_trace.py::collect_test_ids` | ✅ |
    | Filas AC y ≥5 celdas | `scripts/doc_trace.py::collect_criteria`, `::AC_ROW_RE`, `::TEST_ID_RE` | ✅ |
    | Matriz y listas | `scripts/doc_trace.py::build_matrix` | ✅ |
    | `llms.txt`, URLs y omisión de no-`.md` | `scripts/doc_trace.py::build_llms_txt`, `::_page_url`, `::_nav_entries` | ✅ |
    | Etiquetas ignoradas en YAML | `scripts/doc_trace.py::_load_yaml` | ✅ |
    | Errores de `stamp` y `llms` capturados en la CLI | `scripts/doc_trace.py::_cmd_stamp`, `::_cmd_llms`; `tests/test_doc_trace.py::test_main_stamp_missing_page_returns_error`, `::test_main_llms_without_nav_returns_error` | ✅ |
    | Códigos de salida de la CLI | `scripts/doc_trace.py::main`, `::_cmd_drift`, `::_cmd_stamp`, `::_cmd_matrix`, `::_cmd_llms` | ✅ |
    | `matrix` sin PyYAML | `scripts/doc_trace.py::_cmd_matrix` (no llama a `_load_yaml`) | ✅ |
    | Reconfiguración UTF-8 solo en `__main__` | `scripts/doc_trace.py` (bloque `if __name__ == "__main__"`) | ✅ |
    | Modo incremental: estado, diff y cruce con citas | `scripts/doc_trace.py::take_baseline`, `::write_baseline`, `::changed_files`, `::pages_citing`, `::check_changes`, `::format_changes` | ✅ |
    | Exclusión de artefactos de la documentación | `scripts/doc_trace.py::documentation_paths`, `::DOC_ARTIFACTS` | ✅ |
    | Llamada a git sin shell y con timeout | `scripts/doc_trace.py::_git`, `::GIT_TIMEOUT` | ✅ |
    | Código 3 en `changes` | `scripts/doc_trace.py::_cmd_changes` | ✅ |
    | Tests del §6 | `tests/test_doc_trace.py` | ✅ |
