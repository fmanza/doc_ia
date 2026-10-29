# Ejemplo: Auditar la Trazabilidad

## 1. Contexto del Ejemplo

Tras modificar código o instrucciones conviene saber qué páginas de documentación han
quedado desactualizadas y si los criterios de aceptación citan tests reales. Este ejemplo
muestra las dos formas de hacerlo con `doc_trace`: importar `check_drift` y `build_matrix`
desde código propio (mismo patrón por ruta que `check_env_usage.py`), o usar los subcomandos
de la CLI: `stamp`, `drift`, `matrix` y `llms`, y para relanzar `/document-project` solo sobre lo
cambiado, `baseline` y `changes`.

## 2. Implementación de Referencia

```python
--8<-- "examples/doc_trace_usage.py"
```

## 3. Explicación del Código

- El `sys.path.insert` apunta a `scripts/` porque doc_ia no es un paquete instalable; los
  scripts se importan por ruta.
- `check_drift` solo lee las páginas con frontmatter `fuentes`; las demás se ignoran. Cada
  hallazgo indica la página, la fuente y su estado (`stale`, `missing` u `outside_repo`).
- `collect_test_ids` analiza los tests con `ast`: no los importa ni los ejecuta, así que el
  ejemplo es determinista y no tiene efectos secundarios.
- `build_matrix` devuelve el Markdown de la matriz y la lista de tests citados que no
  existen; el ejemplo solo usa los recuentos.

## 4. Ejecución y Pruebas

Sellar una página con sus fuentes (reescribe solo el frontmatter):

```bash
python scripts/doc_trace.py stamp docs/api/doc_trace.md --archetype 2 --date 2026-10-28 \
  --source scripts/doc_trace.py --source tests/test_doc_trace.py
# [doc_trace] docs/api/doc_trace.md: 2 fuente(s) sellada(s)
```

Comprobar desactualizaciones (código `0` sin hallazgos, `1` con ellos):

```bash
python scripts/doc_trace.py drift
# [doc_trace] Sin drift: todas las huellas coinciden.

# Tras editar una fuente sin volver a sellar las páginas que la citan:
# [doc_trace] stale        docs/functional/origin_types.md ← .github/prompts/document_project.prompt.md
# [doc_trace] 1 fuente(s) desactualizada(s). Revisa y ejecuta `stamp`.
```

Matriz de criterios ↔ tests (salida recortada; código `1` si se cita un test inexistente):

```bash
python scripts/doc_trace.py matrix
# # Matriz de Trazabilidad — Criterios ↔ Tests
#
# | Página | Criterios | Con test | Tests citados |
# |---|---|---|---|
# | `docs/functional/check_env.md` | 4 | 4 | 4 |
# | `docs/functional/convert_to_md.md` | 12 | 11 | 21 |
# | `docs/functional/doc_trace.md` | 14 | 14 | 17 |
# ...
# **Total**: 29/66 criterios con test.
```

Índice para agentes IA (`--check` no escribe; código `1` si está desactualizado):

```bash
python scripts/doc_trace.py llms --check
# [doc_trace] C:\...\doc_ia\docs\llms.txt al día.
```

Modo incremental sobre un destino aparte (`mi_api_docs`) que documenta `mi_api`. Al cerrar la
sesión se guarda el baseline; en la siguiente, `changes` lista lo cambiado desde él (salida real
tras añadir un parámetro a `pagar` y crear `src/facturas.py`):

```bash
cd mi_api_docs
python <doc_ia>/scripts/doc_trace.py --root . baseline --origin ../mi_api
# [doc_trace] mi_api: baseline 7e7518596fde (main) → …\mi_api_docs\.ai\doc_state.json

python <doc_ia>/scripts/doc_trace.py --root . changes --origin ../mi_api   # código 1: hay cambios
# # Cambios en el origen «mi_api» desde 7e7518596fde
#
# | Cambio | Fichero | Lo citan (Evidencia) | Lo mencionan |
# |---|---|---|---|
# | A | `src/facturas.py` | *Sin página* | — |
# | M | `src/pagos.py` | `docs/api/pagos.md` | — |
#
# ## Páginas a revisar (1)
# - `docs/api/pagos.md`
# ...
# ## Ejemplos enlazados desde páginas técnicas (1)
# - `docs/examples/pagos.md`
#
# ## Ficheros sin página (1) — clasificar en el INVENTARIO
# - `src/facturas.py`
```

`.ai/doc_state.json` escrito por `baseline`:

```json
{
  "doc_ia": "0.3.0",
  "origenes": {
    "mi_api": {
      "commit": "7e7518596fde23819458cc2426cf18f64aac6f89",
      "rama": "main",
      "sucio": false,
      "fecha": "2026-10-29"
    }
  }
}
```

Sin cambios, `changes` termina con código `0`; sin baseline utilizable, con código `3` y el
motivo (la sesión de `/document-project` se hace entonces completa).

Ejemplo desde código propio (los recuentos dependen del estado del repositorio):

```bash
python docs/examples/doc_trace_usage.py
# Fuentes desactualizadas: 0
# Criterios con test: 29/66
# Tests citados inexistentes: 0

python -m py_compile docs/examples/doc_trace_usage.py   # validación sintáctica
```

## 5. Referencias Relacionadas

- Documentación funcional: [Trazabilidad entre Documentación y Código](../functional/doc_trace.md)
- Referencia técnica: [doc_trace](../api/doc_trace.md)
- Ejemplos relacionados: [Verificar Entorno](check_env_usage.md)
