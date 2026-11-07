"""Ejemplo: origen BASE DE DATOS con db_trace (exportación de util_bbdd inventada, sin red)."""

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from db_trace import (  # noqa: E402
    build_tracemap,
    catalog_changes,
    compare,
    import_pages,
    load_catalog,
    load_entities,
)

ENTITIES = """<entities>
  <entity name="PedPedido" table="PED_PEDIDO">
    <field column="IDPEDIDO" id="true" name="idpedido" nullable="false"/>
    <field column="FECHA" name="fecha" nullable="false"/>
    <field column="IDCLIENTE" foreignType="Cliente" manyToOne="true" name="idcliente"/>
  </entity>
  <entity name="PedLinea" table="PED_LINEA">
    <field column="IDLINEA" id="true" name="idlinea" nullable="false"/>
    <field column="IDPEDIDO" foreignType="PedPedido" manyToOne="true" name="idpedido"/>
  </entity>
  <entity name="Cliente" table="CLIENTE">
    <field column="IDCLIENTE" id="true" name="idcliente"/>
  </entity>
</entities>
"""


def col(name: str, nullable: bool) -> dict[str, object]:
    return {"name": name, "nullable": nullable, "type": "int(11)"}


OBJECTS = [
    {
        "id": "table:VENTAS.PED_PEDIDO",
        "kind": "table",
        "name": "PED_PEDIDO",
        "path": "tables/ped-pedido.md",
        "hash": "sha256:a1",
        "comment": "Pedido",
        "columns": [
            col("IDPEDIDO", False),
            col("FECHA", True),
            col("IDCLIENTE", True),
            col("OBSERVACIONES", True),
        ],
        "fk_out": [{"columns": ["IDCLIENTE"], "ref": "table:VENTAS.CLIENTE"}],
        "fk_in": [],
    },
    {
        "id": "table:VENTAS.PED_LINEA",
        "kind": "table",
        "name": "PED_LINEA",
        "path": "tables/ped-linea.md",
        "hash": "sha256:a2",
        "comment": "Línea de pedido",
        "columns": [col("IDLINEA", False), col("IDPEDIDO", False)],
        "fk_out": [],
        "fk_in": [],
    },
    {
        "id": "table:VENTAS.CLIENTE",
        "kind": "table",
        "name": "CLIENTE",
        "path": "tables/cliente.md",
        "hash": "sha256:a3",
        "columns": [col("IDCLIENTE", False)],
        "fk_out": [],
        "fk_in": ["table:VENTAS.PED_PEDIDO"],
    },
]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


with tempfile.TemporaryDirectory() as tmp:
    export = Path(tmp) / "export_calidad"  # simula la exportación Markdown de util_bbdd
    manifest = {
        "format": "util_bbdd.doc.markdown",
        "format_version": 2,
        "database": "VENTAS",
        "schema": "VENTAS",
        "engine": "mariadb",
        "generated_at": "2026-11-07T08:00:00+00:00",
        "util_bbdd_version": "5.4.0",
    }
    write(export / "manifest.json", json.dumps(manifest))
    catalog = {"format": "util_bbdd.doc.catalog", "format_version": 1, "objects": OBJECTS}
    write(export / "docs/catalog.json", json.dumps(catalog))
    write(
        export / "docs/tables/ped-pedido.md",
        "# Tabla: PED_PEDIDO\n\nFK: [CLIENTE](cliente.md) · [PED_LINEA](ped-linea.md)\n",
    )
    write(export / "docs/tables/ped-linea.md", "# Tabla: PED_LINEA\n")
    write(export / "docs/tables/cliente.md", "# Tabla: CLIENTE\n")
    dest = Path(tmp) / "ventas_docs"  # raíz del destino

    print("1. Importación del alcance PED_*:")
    for kind, rel in import_pages(export, dest, "bd_calidad", ("PED_*",), env="Calidad").changes:
        print(f"  {kind:<12} {rel}")
    page = (dest / "docs/bd/tables/ped-pedido.md").read_text(encoding="utf-8")
    print("  ", page.splitlines()[-1])
    index = (dest / "docs/bd/index.md").read_text(encoding="utf-8").splitlines()
    print("   Frontera:", index[-1])
    again = import_pages(export, dest, "bd_calidad", ("PED_*",), env="Calidad").changes
    print("2. Segunda importación:", again or "sin cambios")

    subset = load_catalog(dest / "_fuentes/bd_calidad/catalog.json")
    write(Path(tmp) / "entities.xml", ENTITIES)
    model = load_entities(Path(tmp) / "entities.xml")
    print("3. Contraste código ↔ BD:")
    for f in compare(subset, model, ("PED_*",)):
        print(f"  {f.kind:<12} {f.obj:<26} {f.detail}")

    newer = {  # exportación completa siguiente: PED_PEDIDO con otra huella
        **catalog,
        "objects": [
            {**o, "hash": "sha256:b1"} if o["name"] == "PED_PEDIDO" else o
            for o in catalog["objects"]
        ],
    }
    write(dest / "docs/functional/pedidos.md", "Cada pedido se guarda en `PED_PEDIDO`.\n")
    write(dest / "docs/api/lineas.md", "La ventana `PedLineaWnd` edita las líneas.\n")
    print("4. Cambios sin alcance:", catalog_changes(newer, subset))
    print("   Cambios del alcance PED_*:", catalog_changes(newer, subset, ("PED_*",)))

    print("5. trace_map.toml:")
    print(build_tracemap(subset, dest / "docs", None, model, ("PED_*",)))
