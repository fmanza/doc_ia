# Ejemplo: Kit de Documentación en un Destino

## 1. Contexto del Ejemplo

Un módulo funcional se documenta en un repositorio aparte, `mi_modulo_docs`, que se entregará
a otro equipo. Ese equipo debe poder relanzar la documentación con `/documentar` sin tener
doc_ia abierto. Este ejemplo muestra cómo `kit` instala en el destino la copia de la
metodología, los lanzadores y la guía, cómo se comprueba esa copia, cómo se actualiza cuando
doc_ia cambia y qué ocurre si alguien ha editado un fichero del kit en el destino. El código
usa `sync` y `check` desde Python con un doc_ia mínimo inventado (mismo patrón por ruta que
`snapshot_sources_usage.py`); la sección 4 añade la instalación del kit real desde la CLI.

## 2. Implementación de Referencia

```python
--8<-- "examples/kit_usage.py"
```

## 3. Explicación del Código

- El `sys.path.insert` apunta a `scripts/` porque doc_ia no es un paquete instalable; los
  scripts se importan por ruta.
- Todo ocurre en una carpeta temporal: `doc_ia` es un doc_ia mínimo con una lista blanca de
  tres ficheros de metodología, un lanzador y la guía; `mi_modulo_docs` es la raíz del
  destino. Sin red ni rutas reales, la salida es siempre la misma.
- Paso 1: la instalación copia la metodología a `.doc_ia/`, el lanzador a la raíz y crea
  `DOCUMENTAR.md` sin el comentario de la plantilla y con el `site_name` de `mkdocs.yml`.
- Paso 2: la comprobación señala que falta el prompt de instancia, que no crea `kit` sino
  `/documentar` o el cierre de la sesión de documentación.
- Pasos 3 y 4: con el prompt de instancia ya escrito y un cambio publicado en doc_ia,
  `check(dest, doc_ia)` informa del fichero desfasado y `sync` lo actualiza.
- Paso 5: un parche local en `.doc_ia/scripts/doc_trace.py` es un conflicto; `sync` no lo
  pisa aunque doc_ia tenga una versión nueva (con `force=True` sí lo haría).

## 4. Ejecución y Pruebas

Desde código propio:

```bash
python docs/examples/kit_usage.py
# 1. Instalación:
#   creado           .doc_ia/pyproject.toml
#   creado           .doc_ia/.github/prompts/document_project.prompt.md
#   creado           .doc_ia/scripts/doc_trace.py
#   creado           .claude/commands/documentar.md
#   creado           DOCUMENTAR.md
#    DOCUMENTAR.md: # Cómo documentar Mi Módulo
# 2. Comprobación:
#   conflicto        .ai/prompts/documentar.prompt.md — falta (lo crea /documentar o el CIERRE)
# 3. Comprobación contra doc_ia:
#   desfasado        .doc_ia/scripts/doc_trace.py
# 4. Actualización:
#   actualizado      .doc_ia/scripts/doc_trace.py
# 5. Actualización con un fichero editado en el destino:
#   conflicto        .doc_ia/scripts/doc_trace.py — editado en el destino
#    Contenido conservado: print('parche local')

python -m py_compile docs/examples/kit_usage.py   # validación sintáctica
```

Desde la CLI, con el kit real de doc_ia sobre un destino `mi_modulo_docs` (ruta inventada; la
salida se abrevia y el número de ficheros depende de la lista blanca de la versión de doc_ia).
`--dry-run` informa sin escribir (código `1`: habría cambios):

```bash
python <doc_ia>/scripts/kit.py sync --root mi_modulo_docs --dry-run
# [kit] doc_ia 0.13.0 → …\mi_modulo_docs: 53 cambio(s)
#   CREADO           .doc_ia/pyproject.toml
#   …
#   CREADO           .doc_ia/scripts/kit.py
#   …
#   CREADO           .claude/commands/documentar.md
#   CREADO           .github/prompts/documentar.prompt.md
#   CREADO           AGENTS.md
#   CREADO           GEMINI.md
#   CREADO           DOCUMENTAR.md
# [kit] --dry-run: no se ha escrito nada.
```

La misma orden sin `--dry-run` instala el kit (código `1`); repetida, termina con código `0`
(`[kit] doc_ia 0.13.0 → …\mi_modulo_docs: sin cambios`). El registro queda así (huellas
abreviadas):

```json
{
  "doc_ia": "0.13.0",
  "fecha": "2026-11-07",
  "ficheros": {
    ".claude/commands/documentar.md": "44364ebb0ca8…",
    ".doc_ia/.claude/EDGE_CASES.md": "89b996b192fe…",
    "…": "…"
  }
}
```

Desde el destino, la copia del kit comprueba la integridad (código `1` hasta que el cierre de
la primera sesión escribe el prompt de instancia):

```bash
python mi_modulo_docs/.doc_ia/scripts/kit.py check --root mi_modulo_docs
# [kit] kit doc_ia 0.13.0 en …\mi_modulo_docs
#   CONFLICTO        .ai/prompts/documentar.prompt.md — falta (lo crea /documentar o el CIERRE)
```

La copia no se actualiza a sí misma: sin `--from` termina con código `2`; con `--from` compara
con doc_ia y, con `sync`, actualiza:

```bash
python mi_modulo_docs/.doc_ia/scripts/kit.py sync --root mi_modulo_docs
# [kit] ERROR: este kit.py es la copia de un destino: indica el doc_ia con --from

python mi_modulo_docs/.doc_ia/scripts/kit.py --from <doc_ia> check --root mi_modulo_docs
python mi_modulo_docs/.doc_ia/scripts/kit.py --from <doc_ia> sync --root mi_modulo_docs
```

Ver los demás casos en
[Errores y casos especiales](../api/kit.md#errores-y-casos-especiales).

## 5. Referencias Relacionadas

- Documentación funcional: [Kit de Documentación en el Destino](../functional/kit.md)
- Referencia técnica: [kit](../api/kit.md)
- Ejemplos relacionados: [Documentar un Proyecto](document_project_usage.md),
  [Adquirir Orígenes Documentales](snapshot_sources_usage.md)
