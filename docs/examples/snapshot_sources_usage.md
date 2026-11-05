# Ejemplo: Adquirir Orígenes Documentales

## 1. Contexto del Ejemplo

Un módulo funcional se documenta con dos materiales que no viven en su repositorio: el manual
de usuario, publicado en una carpeta compartida con la versión en el nombre
(`Manual_Modulo_v1.2.50.docx`), y una carpeta de normativa con PDF, notas y vídeos. Ninguno
de los dos se puede tocar. Este ejemplo muestra cómo `snapshot_sources` los copia a la zona de
trabajo `_staging/` del destino, cómo se refleja la publicación de una versión nueva del
manual y cómo usar `declare` y `sync_source` desde código propio (mismo patrón por ruta que
`doc_trace_usage.py`).

## 2. Implementación de Referencia

```python
--8<-- "examples/snapshot_sources_usage.py"
```

## 3. Explicación del Código

- El `sys.path.insert` apunta a `scripts/` porque doc_ia no es un paquete instalable; los
  scripts se importan por ruta.
- Todo ocurre en una carpeta temporal: `Modulos` hace de carpeta compartida y
  `mi_modulo_docs` de raíz del destino. No hay red ni rutas reales, así que la salida es
  siempre la misma.
- `declare` solo anota el origen en el manifiesto en memoria; `sync_source` resuelve el
  patrón (gana `1.2.50` frente a `1.2.9`, y el `.pdf` no encaja), copia con el nombre estable
  `Manual_Modulo.docx` y devuelve los cambios. El manifiesto se escribe solo si hubo cambios,
  igual que hace la CLI.
- Al aparecer `v1.2.51`, la copia conserva su ruta, la conversión `md/Manual_Modulo.md` se
  borra para que `convert_to_md.py` la rehaga y el historial guarda `version_anterior`.

## 4. Ejecución y Pruebas

Desde código propio:

```bash
python docs/examples/snapshot_sources_usage.py
# 2026-11-02: 1 cambio(s)
#   ALTA       manual/Manual_Modulo.docx (v1.2.50)
# 2026-11-03: 0 cambio(s)
# 2026-11-05: 1 cambio(s)
#   MODIFICADO manual/Manual_Modulo.docx (v1.2.50 → v1.2.51)
# Ficheros en el destino: .ai/sources.json, _staging/manual/Manual_Modulo.docx
#   2026-11-02 alta: v1.2.50 (antes —)
#   2026-11-05 modificado: v1.2.51 (antes 1.2.50)

python -m py_compile docs/examples/snapshot_sources_usage.py   # validación sintáctica
```

Desde la CLI, sobre un destino `mi_modulo_docs` (rutas inventadas; en una carpeta de red se
escribiría `\\servidor\recurso\Modulos\…`). Primero se declaran los dos orígenes; la carpeta
de normativa se filtra a PDF:

```bash
python <doc_ia>/scripts/snapshot_sources.py --root mi_modulo_docs add manual "Modulos/Manual_Modulo_v{ver}.docx"
# [snapshot] Origen «manual» declarado en …\mi_modulo_docs\.ai\sources.json. Ejecuta `sync` para copiarlo.

python <doc_ia>/scripts/snapshot_sources.py --root mi_modulo_docs add normativa Normativa --include "*.pdf"
```

`--dry-run` informa sin copiar (código `1`: habría cambios); `sync` copia y registra:

```bash
python <doc_ia>/scripts/snapshot_sources.py --root mi_modulo_docs sync --date 2026-11-02
# [snapshot] manual: 1 cambio(s)
#   ALTA       manual/Manual_Modulo.docx (v1.2.50)
# [snapshot] normativa: 2 cambio(s)
#   ALTA       normativa/ley_proteccion.pdf
#   ALTA       normativa/sub/plan_igualdad.pdf
# [snapshot] Manifiesto actualizado: …\mi_modulo_docs\.ai\sources.json
```

Una segunda ejecución sin cambios en los orígenes termina con código `0`
(`[snapshot] manual: sin cambios`). Después se publica `Manual_Modulo_v1.2.51.docx`, cambia
`ley_proteccion.pdf` y se elimina `sub/plan_igualdad.pdf` (código `1`):

```bash
python <doc_ia>/scripts/snapshot_sources.py --root mi_modulo_docs sync --date 2026-11-05
# [snapshot] manual: 1 cambio(s)
#   MODIFICADO manual/Manual_Modulo.docx (v1.2.50 → v1.2.51)
# [snapshot] normativa: 2 cambio(s)
#   MODIFICADO normativa/ley_proteccion.pdf
#   BAJA       normativa/sub/plan_igualdad.pdf
# [snapshot] Manifiesto actualizado: …\mi_modulo_docs\.ai\sources.json

python <doc_ia>/scripts/snapshot_sources.py --root mi_modulo_docs list
# manual: Modulos/Manual_Modulo_v{ver}.docx · 1 fichero(s)
#   Manual_Modulo.docx v1.2.51 · 12d736fd61cc
# normativa: Normativa · 1 fichero(s)
#   ley_proteccion.pdf · 92912776951e
```

En una consola Windows que no es UTF-8 (cp1252) la salida se reconfigura a UTF-8, así que la
flecha del cambio de versión se escribe sin errores (ver
[Errores y casos especiales](../api/snapshot_sources.md#errores-y-casos-especiales)).

Entrada `manual` de `.ai/sources.json` tras las dos sincronizaciones (huellas reales del
contenido de prueba; con un manual real cambian):

```json
{
  "ficheros": {
    "Manual_Modulo.docx": {
      "sha256": "12d736fd61cc6abbe9442ade6750cfb07a131bfa1827e9030dc1a8d8227b3029",
      "bytes": 3,
      "origen": "Modulos\\Manual_Modulo_v1.2.51.docx",
      "version": "1.2.51"
    }
  },
  "historial": [
    {
      "fecha": "2026-11-02",
      "fichero": "Manual_Modulo.docx",
      "cambio": "alta",
      "sha256": "e93c533dd53026c9c6f8e53c91f82de2557f469313e246136cdf6a5bfb18e4d7",
      "version": "1.2.50"
    },
    {
      "fecha": "2026-11-05",
      "fichero": "Manual_Modulo.docx",
      "cambio": "modificado",
      "sha256": "12d736fd61cc6abbe9442ade6750cfb07a131bfa1827e9030dc1a8d8227b3029",
      "version": "1.2.51",
      "version_anterior": "1.2.50"
    }
  ],
  "origen": "Modulos/Manual_Modulo_v{ver}.docx",
  "sincronizado": "2026-11-05"
}
```

Un origen no declarado, o declarado con un nombre o un filtro inválidos, termina con código
`2`:

```bash
python <doc_ia>/scripts/snapshot_sources.py --root mi_modulo_docs sync otro
# [snapshot] ERROR: orígenes no declarados: otro (usa `add`)
```

## 5. Referencias Relacionadas

- Documentación funcional: [Adquisición de Orígenes Documentales](../functional/snapshot_sources.md)
- Referencia técnica: [snapshot_sources](../api/snapshot_sources.md)
- Ejemplos relacionados: [Convertir Documentos a Markdown](convert_to_md_usage.md),
  [Auditar la Trazabilidad](doc_trace_usage.md)
