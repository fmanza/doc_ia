# convert_to_md

Convierte ficheros en formatos no legibles directamente por el agente IA (PDF, DOCX, PPTX…) a Markdown, depositando el resultado en `<origen>/md/` con la estructura de subdirectorios reflejada. Usa `markitdown` para PDF y `pandoc` para el resto de formatos.

## 1. Arquitectura y Diseño

```mermaid
flowchart TD
    CLI["CLI: argparse\n(source, --dry-run)"] --> SE{source existe?}
    SE -- No --> ERR2["ERROR: origen no existe → exit 1"]
    SE -- Sí --> CF["collect_files(source)\nfiltrar CONVERTIBLE_EXTENSIONS\nexcluir carpeta md/"]
    CF --> WARN["Advertir si falta\nmarkitdown o pandoc"]
    WARN --> EMPTY{¿Sin ficheros?}
    EMPTY -- Sí --> OK0["Mensaje informativo → exit 0"]
    EMPTY -- No --> LOOP["Para cada fichero:\noutput_path(file, root, md_root)"]
    LOOP --> EXISTS{¿Ya existe en md/?}
    EXISTS -- Sí --> SKIP["OMITIR — idempotente"]
    EXISTS -- No --> DRY{--dry-run?}
    DRY -- Sí --> DRYOUT["DRY-RUN — listar sin convertir"]
    DRY -- No --> EXT{¿Extensión PDF?}
    EXT -- Sí --> MIT["markitdown.convert(file)"]
    EXT -- No --> PAN["pandoc file -o out.md --wrap=none"]
    MIT --> RES{¿Éxito?}
    PAN --> RES
    RES -- Sí --> OKFILE["OK — imprimir ruta salida"]
    RES -- No --> ERRFILE["ERROR — eliminar parcial\n+ imprimir mensaje"]
    SKIP & DRYOUT & OKFILE & ERRFILE --> MORE{¿Más ficheros?}
    MORE -- Sí --> LOOP
    MORE -- No --> FINAL{¿Hubo errores?}
    FINAL -- Sí --> EXIT1["exit 1"]
    FINAL -- No --> EXIT0["exit 0"]
```

Pipeline determinista: cada fichero se procesa de forma independiente; un error en un fichero no detiene los restantes. La función `main` acumula contadores y devuelve el código de salida agregado.

## 2. Modelo de Datos / Contratos

### API pública

| Función | Firma | Descripción | Retorna |
|---|---|---|---|
| `pandoc_available` | `() -> bool` | Comprueba si `pandoc` está en el PATH del sistema mediante `shutil.which` | `True` si disponible |
| `markitdown_available` | `() -> bool` | Comprueba si el paquete `markitdown` está instalado mediante `importlib.util.find_spec` | `True` si disponible |
| `collect_files` | `(source: Path) -> list[Path]` | Recopila ficheros convertibles bajo `source`; excluye `md/` para evitar recursión | Lista ordenada de `Path` |
| `output_path` | `(source_file: Path, source_root: Path, md_root: Path) -> Path` | Calcula la ruta de salida reflejando la estructura relativa del origen | `Path` bajo `md_root` |
| `convert_file` | `(source_file: Path, source_root: Path, md_root: Path, *, dry_run: bool = False) -> bool` | Convierte un fichero con markitdown (PDF) o pandoc (resto); idempotente si ya existe | `True` si éxito u omisión |
| `main` | `() -> int` | Punto de entrada CLI: parsea args, verifica herramientas, itera ficheros, devuelve código de salida | `0` ok · `1` error |

### CLI

```
python scripts/convert_to_md.py <source> [--dry-run]
```

| Argumento | Tipo | Descripción | Restricciones |
|---|---|---|---|
| `source` | `Path` | Fichero o directorio a convertir | Obligatorio; debe existir |
| `--dry-run` | flag | Lista qué se convertiría sin ejecutar conversión | Opcional |

### Constantes

| Nombre | Tipo | Valor |
|---|---|---|
| `MARKITDOWN_EXTENSIONS` | `frozenset[str]` | `{".pdf"}` |
| `PANDOC_EXTENSIONS` | `frozenset[str]` | `{".docx", ".doc", ".pptx", ".odt", ".epub", ".rst", ".html", ".htm"}` |
| `CONVERTIBLE_EXTENSIONS` | `frozenset[str]` | Unión de las dos anteriores |

### Contrato de salida (stdout)

| Situación | Línea impresa |
|---|---|
| Fichero ya convertido | `  OMITIR  <rel_origen> → md/<rel_salida> (ya existe)` |
| Conversión exitosa | `  OK      <rel_origen> → md/<rel_salida>` |
| Error de markitdown | `  ERROR   <rel_origen>: <mensaje markitdown>` |
| Error de pandoc | `  ERROR   <rel_origen>: <mensaje stderr pandoc>` |
| `--dry-run` | `  DRY-RUN <rel_origen> → md/<rel_salida>` |
| Sin ficheros convertibles | `No se encontraron ficheros convertibles en: <source>` |
| markitdown no instalado (aviso previo) | `⚠  markitdown no instalado — los PDF fallarán.` |
| pandoc no encontrado (aviso previo) | `⚠  pandoc no encontrado — los ficheros DOCX/PPTX/… fallarán.` |

### Errores y casos especiales

| Caso | Comportamiento |
|---|---|
| `source` no existe | `exit 1` con mensaje |
| Sin ficheros convertibles | Mensaje informativo + `exit 0` |
| Fichero ya existe en `md/` | `OMITIR` — no re-convierte; comportamiento idempotente |
| `markitdown` no instalado al procesar PDF | `ERROR` en ese fichero; continúa con el resto |
| `pandoc` no en PATH al procesar DOCX/… | `ERROR` en ese fichero; continúa con el resto |
| Al menos un fallo al finalizar | `exit 1`; los ficheros convertidos correctamente se conservan |

## 3. Componentes y Clases

| Componente | Ruta | Responsabilidad |
|---|---|---|
| Script principal | `scripts/convert_to_md.py` | Lógica completa de detección, routing y conversión |
| Constantes de extensiones | `scripts/convert_to_md.py:22-25` | Separación clara PDF (markitdown) vs. otros (pandoc) |
| Dependencia PDF | `markitdown` (paquete Python) | Única herramienta capaz de convertir PDF a Markdown |
| Dependencia DOCX/… | `pandoc` (binario externo) | Conversión de formatos Office/web a Markdown |

## 4. Dependencias y Requisitos

| Dependencia | Propósito | Requerida para | Comportamiento sin ella |
|---|---|---|---|
| `markitdown` (paquete Python) | Convierte PDF a Markdown | Ficheros `.pdf` | `ERROR` por fichero PDF; resto continúa |
| `pandoc` (binario externo) | Convierte DOCX, PPTX, ODT… a Markdown | Ficheros `.docx`, `.pptx`, … | `ERROR` por fichero; resto continúa |
| `pathlib.Path` | Manipulación de rutas | Todos | — (stdlib Python ≥ 3.4) |
| `subprocess` | Invocación de pandoc | Ficheros no-PDF | — (stdlib) |
| `importlib.util` | Detección de markitdown | Todos | — (stdlib) |
| `shutil.which` | Detección de pandoc en PATH | Todos | — (stdlib) |

Verificar entorno antes de usar: `python scripts/check_env.py` (reporta si markitdown y pandoc están instalados).

## 5. Ejemplos Relacionados

- [Ejemplo: Convertir Documentos a Markdown](../examples/convert_to_md_usage.md) — invocaciones
  para directorio completo, fichero individual, `--dry-run` y gestión de errores.
- Integrado en el flujo [Documentar un Proyecto](../functional/document_project.md) § Fase 0b:
  propuesto automáticamente cuando se detectan ficheros binarios en el origen.
