# Ejemplo: Origen Base de Datos con db_trace

## 1. Contexto del Ejemplo

El módulo de pedidos de un proyecto guarda sus datos en las tablas `PED_*` de una base de datos
MariaDB. Quien lo documenta ha exportado el esquema del entorno de calidad con `util_bbdd` y
quiere incorporar a la documentación del módulo solo sus tablas, saber en qué difiere el modelo
del código (`entities.xml`) de lo desplegado y devolver a `util_bbdd` el mapa de qué páginas y
qué código corresponden a cada tabla. Este ejemplo usa `db_trace` desde Python con una
exportación mínima inventada (mismo patrón por ruta que `kit_usage.py`); la sección 4 añade la
CLI con sus códigos de salida.

## 2. Implementación de Referencia

```python
--8<-- "examples/db_trace_usage.py"
```

## 3. Explicación del Código

- El `sys.path.insert` apunta a `scripts/` porque doc_ia no es un paquete instalable; los
  scripts se importan por ruta.
- Todo ocurre en una carpeta temporal: `export_calidad` imita la exportación de `util_bbdd`
  (`manifest.json`, `docs/catalog.json` y una página por tabla) y `ventas_docs` es la raíz del
  destino. No hay base de datos, red ni rutas reales: la salida es siempre la misma.
- Paso 1: `import_pages` importa, para el entorno `Calidad`, `PED_PEDIDO` y `PED_LINEA` en `docs/bd/`; `CLIENTE` queda
  fuera del alcance, así que el enlace a su página pasa a texto y aparece en la frontera del
  índice. El catálogo del subconjunto y la cabecera del manifiesto se guardan en
  `_fuentes/bd_calidad/`.
- Paso 2: repetir la importación no cambia nada.
- Paso 3: `compare` encuentra tres discrepancias: la relación `PED_LINEA.IDPEDIDO` del código no
  tiene clave ajena en la base de datos, la columna `OBSERVACIONES` no está en el código y
  `FECHA` es obligatoria en el código pero admite nulos en la base de datos. En una sesión de
  documentación, cada una se convierte en una ficha `COB-DATOS-…`.
- Paso 4: la exportación siguiente, completa y con otra huella para `PED_PEDIDO`, se compara
  con el subconjunto guardado. Sin alcance, `CLIENTE` aparece como `alta` porque no estaba en el
  subconjunto; con el alcance `PED_*`, solo queda el `modificado` de `PED_PEDIDO`.
- Paso 5: el `trace_map` enlaza `PED_PEDIDO` con la página funcional que cita la tabla y
  `PED_LINEA` con la página técnica que cita la clase `PedLineaWnd` de su entidad `PedLinea`.

## 4. Ejecución y Pruebas

Desde código propio:

```bash
python docs/examples/db_trace_usage.py
# 1. Importación del alcance PED_*:
#   creado       docs/bd/tables/ped-pedido.md
#   creado       docs/bd/tables/ped-linea.md
#   creado       docs/bd/index.md
#   creado       _fuentes/bd_calidad/catalog.json
#   creado       _fuentes/bd_calidad/manifest.json
#    FK: `CLIENTE` · [PED_LINEA](ped-linea.md)
#    Frontera: `CLIENTE`
# 2. Segunda importación: sin cambios
# 3. Contraste código ↔ BD:
#   fk           PED_LINEA.IDPEDIDO         relación PED_PEDIDO en el código sin FK en la BD
#   columna      PED_PEDIDO.OBSERVACIONES   en la BD y no en el código
#   nulabilidad  PED_PEDIDO.FECHA           código nullable=false, BD NULL
# 4. Cambios sin alcance: [('alta', 'table:VENTAS.CLIENTE'), ('modificado', 'table:VENTAS.PED_PEDIDO')]
#    Cambios del alcance PED_*: [('modificado', 'table:VENTAS.PED_PEDIDO')]
# 5. trace_map.toml:
# # trace_map de util_bbdd (markdown.trace_map) — generado por doc_ia scripts/db_trace.py
# # tracemap desde la evidencia de la documentación. No editar a mano: se regenera.
#
# [tables."PED_PEDIDO"]
# functional = ["docs/functional/pedidos.md"]
#
# [tables."PED_LINEA"]
# technical = ["docs/api/lineas.md"]

python -m py_compile docs/examples/db_trace_usage.py   # validación sintáctica
```

Desde la CLI, con la misma exportación y el mismo `entities.xml` guardados en disco (rutas
inventadas). `info` comprueba el contrato:

```bash
python <doc_ia>/scripts/db_trace.py info --export export_calidad
# [db_trace] VENTAS · mariadb · util_bbdd 5.4.0 · 2026-11-07T08:00:00+00:00
# [db_trace] objetos: table 3
```

`select` importa el alcance (código `1` con cambios, `0` sin ellos) y retira lo que sale de él.
`--env` es obligatorio: sin él, o en blanco, termina con código `2` sin escribir nada:

```bash
python <doc_ia>/scripts/db_trace.py select --export export_calidad --root ventas_docs \
    --name bd_calidad --env Calidad --include "PED_*"
# [db_trace] 5 cambio(s) en ventas_docs
#   CREADO       docs/bd/tables/ped-pedido.md
#   …

python <doc_ia>/scripts/db_trace.py select --export export_calidad --root ventas_docs \
    --name bd_calidad --env Calidad --include "PED_PEDIDO"
# [db_trace] 4 cambio(s) en ventas_docs
#   ACTUALIZADO  docs/bd/tables/ped-pedido.md
#   RETIRADO     docs/bd/tables/ped-linea.md
#   ACTUALIZADO  docs/bd/index.md
#   ACTUALIZADO  _fuentes/bd_calidad/catalog.json
```

El índice generado (`docs/bd/index.md`) tras la segunda orden:

```markdown
| Dato | Valor |
|---|---|
| Entorno | **Calidad** |
| Base de datos | `VENTAS` (esquema `VENTAS`) |
| Motor | mariadb |
| Generada | 2026-11-07T08:00:00+00:00 |
| Generador | util_bbdd 5.4.0 |

## Objetos del alcance (1)

| Objeto | Tipo | Comentario |
|---|---|---|
| [PED_PEDIDO](tables/ped-pedido.md) | table | Pedido |

## Frontera (objetos relacionados por FK, no importados: 1)

`CLIENTE`
```

`compare` termina con código `1` si hay discrepancias y `0` si no; `--output` guarda además el
informe:

```bash
python <doc_ia>/scripts/db_trace.py compare --catalog export_calidad/docs/catalog.json \
    --entities entities.xml --include "PED_*"
# # Contraste código ↔ base de datos
#
# Discrepancias: 3
#
# | Tipo | Objeto | Detalle |
# |---|---|---|
# | fk | `PED_LINEA.IDPEDIDO` | relación PED_PEDIDO en el código sin FK en la BD |
# | columna | `PED_PEDIDO.OBSERVACIONES` | en la BD y no en el código |
# | nulabilidad | `PED_PEDIDO.FECHA` | código nullable=false, BD NULL |

python <doc_ia>/scripts/db_trace.py compare --catalog export_calidad/docs/catalog.json \
    --entities entities.xml --include "CLIENTE"
# # Contraste código ↔ base de datos
#
# Discrepancias: 0
```

`tracemap` escribe el mapa (código `0`):

```bash
python <doc_ia>/scripts/db_trace.py tracemap --catalog ventas_docs/_fuentes/bd_calidad/catalog.json \
    --docs ventas_docs/docs --entities entities.xml --output ventas_docs/.ai/trace_map.toml
# [db_trace] trace_map escrito en ventas_docs\.ai\trace_map.toml
```

`changes` se ejecuta **antes** de `select` (que sustituye el subconjunto guardado): compara el
catálogo completo de la exportación nueva con el de `_fuentes/`. Con `--include` solo cuenta el
alcance; sin él, lo que está fuera sale como `alta` (aquí, tras importar `PED_*` con la misma
exportación):

```bash
python <doc_ia>/scripts/db_trace.py changes --catalog export_calidad/docs/catalog.json \
    --previous ventas_docs/_fuentes/bd_calidad/catalog.json --docs ventas_docs/docs \
    --include "PED_*"
# # Cambios de esquema (0)

python <doc_ia>/scripts/db_trace.py changes --catalog export_calidad/docs/catalog.json \
    --previous ventas_docs/_fuentes/bd_calidad/catalog.json --docs ventas_docs/docs
# # Cambios de esquema (1)
#
# - alta: `CLIENTE` → —
```

Errores de contrato o de alcance terminan con código `2`:

```bash
python <doc_ia>/scripts/db_trace.py select --export export_calidad --root ventas_docs \
    --name bd_calidad --env Calidad --include "NADA_*"
# [db_trace] ERROR: ningún objeto encaja con ['NADA_*']

python <doc_ia>/scripts/db_trace.py select --export export_calidad --root ventas_docs \
    --name bd_calidad --env " " --include "PED_*"
# [db_trace] ERROR: indica el entorno que representa la exportación (--env)
```

Ver los demás casos en
[Errores y casos especiales](../api/db_trace.md#errores-y-casos-especiales).

## 5. Referencias Relacionadas

- Documentación funcional: [Trazabilidad con la Base de Datos](../functional/db_trace.md)
- Referencia técnica: [db_trace](../api/db_trace.md)
- Ejemplos relacionados: [Documentar un Proyecto](document_project_usage.md),
  [Kit de Documentación en un Destino](kit_usage.md)
