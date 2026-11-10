"""Tests de scripts/db_trace.py: exportación de util_bbdd inventada, sin red ni base de datos."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from scripts.db_trace import (
    DbTraceError,
    build_tracemap,
    catalog_changes,
    compare,
    import_pages,
    load_catalog,
    load_entities,
    main,
    rewrite_links,
)

ENTITIES = """<entities>
  <entity name="ModExp" table="MOD_EXP">
    <field column="IDEXP" id="true" name="idexp" nullable="false"><type>Integer</type></field>
    <field column="CODIGO" name="codigo" nullable="false"><type>String</type></field>
    <field column="IDBASE" foreignType="Base" manyToOne="true" name="idbase" nullable="false"/>
    <field column="IDCAT" foreignPackage="core" foreignType="CoreCatalogo" manyToOne="true"
      name="idcat"/>
    <field column="SOLO_CODIGO" name="solo" nullable="true"><type>String</type></field>
    <field foreignType="ModHijo" mappedBy="idexp" name="hijos" oneToMany="true"/>
  </entity>
  <entity name="ModSoloCodigo" table="MOD_SOLO_CODIGO">
    <field column="ID" id="true" name="id" nullable="false"><type>Integer</type></field>
  </entity>
  <entity name="Base" table="BASE"><field column="IDBASE" id="true" name="idbase"/></entity>
</entities>
"""


def _col(name: str, nullable: bool) -> dict[str, object]:
    return {"name": name, "nullable": nullable, "type": "int(11)"}


def _objects() -> list[dict[str, object]]:
    return [
        {
            "id": "table:S.MOD_EXP",
            "kind": "table",
            "name": "MOD_EXP",
            "path": "tables/mod-exp.md",
            "hash": "sha256:1",
            "comment": "Expediente",
            "columns": [
                _col("IDEXP", False),
                _col("CODIGO", True),
                _col("IDBASE", False),
                _col("IDCAT", True),
                _col("SOLO_BD", True),
            ],
            "fk_out": [{"columns": ["IDBASE"], "ref": "table:S.OTRA"}],
            "fk_in": ["table:S.MOD_HIJO"],
        },
        {
            "id": "table:S.MOD_HIJO",
            "kind": "table",
            "name": "MOD_HIJO",
            "path": "tables/mod-hijo.md",
            "hash": "sha256:2",
            "columns": [_col("ID", False)],
            "fk_out": [{"columns": ["IDEXP"], "ref": "table:S.MOD_EXP"}],
            "fk_in": [],
        },
        {
            "id": "view:S.V_MOD",
            "kind": "view",
            "name": "V_MOD",
            "path": "views/v-mod.md",
            "hash": "sha256:3",
            "columns": [_col("ID", False)],
        },
        {
            "id": "table:S.BASE",
            "kind": "table",
            "name": "BASE",
            "path": "tables/base.md",
            "hash": "sha256:4",
            "columns": [_col("IDBASE", False)],
            "fk_out": [],
            "fk_in": [],
        },
    ]


def _export(tmp_path: Path) -> Path:
    exp = tmp_path / "export"
    docs = exp / "docs"
    (docs / "tables").mkdir(parents=True)
    (docs / "views").mkdir()
    manifest = {
        "format": "util_bbdd.doc.markdown",
        "format_version": 2,
        "database": "S",
        "schema": "S",
        "engine": "mariadb",
        "generated_at": "2026-11-07T01:00:00+00:00",
        "util_bbdd_version": "5.4.0",
    }
    (exp / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    catalog = {"format": "util_bbdd.doc.catalog", "format_version": 1, "objects": _objects()}
    (docs / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
    (docs / "tables/mod-exp.md").write_text(
        '---\n{"id": "table:S.MOD_EXP"}\n---\n# Tabla: MOD_EXP\n\n'
        "| FK | [BASE](base.md) | [MOD_HIJO](mod-hijo.md#col-idexp) |"
        " [web](https://x.org) | [x](#col-idexp) |\n",
        encoding="utf-8",
    )
    (docs / "tables/mod-hijo.md").write_text(
        "# Tabla: MOD_HIJO\n[MOD_EXP](mod-exp.md)\n", encoding="utf-8"
    )
    (docs / "tables/base.md").write_text("# Tabla: BASE\n", encoding="utf-8")
    (docs / "views/v-mod.md").write_text(
        "# Vista: V_MOD\n[MOD_EXP](../tables/mod-exp.md)\n", encoding="utf-8"
    )
    return exp


def _entities(tmp_path: Path) -> Path:
    path = tmp_path / "entities.xml"
    path.write_text(ENTITIES, encoding="utf-8")
    return path


# --- contrato ---


def test_rejects_foreign_or_newer_formats(tmp_path: Path) -> None:
    exp = _export(tmp_path)
    data = json.loads((exp / "docs/catalog.json").read_text(encoding="utf-8"))
    (exp / "docs/catalog.json").write_text(
        json.dumps({**data, "format_version": 2}), encoding="utf-8"
    )
    with pytest.raises(DbTraceError, match="no soportada"):
        load_catalog(exp / "docs/catalog.json")
    (exp / "manifest.json").write_text('{"format": "otro"}', encoding="utf-8")
    assert main(["info", "--export", str(exp)]) == 2


# --- select ---


def test_rewrite_links_keeps_imported_and_external() -> None:
    text = "[BASE](base.md) [HIJO](mod-hijo.md#col-a) [web](https://x.org) [a](#col-b)"
    out = rewrite_links(text, "tables/mod-exp.md", {"tables/mod-hijo.md"})
    assert out == "`BASE` [HIJO](mod-hijo.md#col-a) [web](https://x.org) [a](#col-b)"
    assert (
        rewrite_links("[E](../tables/x.md)", "views/v.md", {"tables/x.md"}) == "[E](../tables/x.md)"
    )


def test_import_pages_selects_scope_and_is_idempotent(tmp_path: Path) -> None:
    exp, root = _export(tmp_path), tmp_path / "VG"
    report = import_pages(exp, root, "bd_calidad", ("MOD_*", "V_MOD"), env="Calidad")
    created = {rel for _, rel in report.changes}
    assert "docs/bd/tables/mod-exp.md" in created and "docs/bd/views/v-mod.md" in created
    assert not (root / "docs/bd/tables/base.md").exists()
    page = (root / "docs/bd/tables/mod-exp.md").read_text(encoding="utf-8")
    assert "`BASE`" in page and "[MOD_HIJO](mod-hijo.md#col-idexp)" in page
    index = (root / "docs/bd/index.md").read_text(encoding="utf-8")
    assert "mariadb" in index and "`OTRA`" in index  # frontera por FK
    assert "| Entorno | **Calidad** |" in index
    subset = json.loads((root / "_fuentes/bd_calidad/catalog.json").read_text(encoding="utf-8"))
    assert [o["name"] for o in subset["objects"]] == ["MOD_EXP", "MOD_HIJO", "V_MOD"]
    assert import_pages(exp, root, "bd_calidad", ("MOD_*", "V_MOD"), env="Calidad").changes == []


def test_import_pages_retires_objects_out_of_scope(tmp_path: Path) -> None:
    exp, root = _export(tmp_path), tmp_path / "VG"
    import_pages(exp, root, "bd", ("MOD_*",), env="Calidad")
    report = import_pages(exp, root, "bd", ("MOD_EXP",), env="Calidad")
    assert ("retirado", "docs/bd/tables/mod-hijo.md") in report.changes
    page = (root / "docs/bd/tables/mod-exp.md").read_text(encoding="utf-8")
    assert "`MOD_HIJO`" in page  # el enlace al objeto retirado pasa a texto


def test_import_pages_without_matches_is_an_error(tmp_path: Path) -> None:
    with pytest.raises(DbTraceError, match="ningún objeto"):
        import_pages(_export(tmp_path), tmp_path / "VG", "bd", ("NADA_*",), env="Calidad")


# --- compare ---


def test_compare_reports_tables_columns_nullability_and_fk(tmp_path: Path) -> None:
    exp = _export(tmp_path)
    findings = compare(
        load_catalog(exp / "docs/catalog.json"), load_entities(_entities(tmp_path)), ("MOD_*",)
    )
    got = {(f.kind, f.obj) for f in findings}
    assert ("tabla", "MOD_SOLO_CODIGO") in got  # solo en el código
    assert ("tabla", "MOD_HIJO") in got  # solo en la BD
    assert ("columna", "MOD_EXP.SOLO_BD") in got
    assert ("columna", "MOD_EXP.SOLO_CODIGO") in got
    assert ("nulabilidad", "MOD_EXP.CODIGO") in got
    assert ("fk", "MOD_EXP.IDBASE") in got  # código → BASE, BD → OTRA
    assert ("fk", "MOD_EXP.IDCAT") in got  # relación sin FK en la BD
    assert len(got) == 7


def test_compare_cli_exit_codes(tmp_path: Path) -> None:
    exp, ent = _export(tmp_path), _entities(tmp_path)
    args = ["compare", "--catalog", str(exp / "docs/catalog.json"), "--entities", str(ent)]
    assert main([*args, "--include", "MOD_*"]) == 1
    assert main([*args, "--include", "BASE"]) == 0


# --- changes y tracemap ---


def test_catalog_changes_by_hash(tmp_path: Path) -> None:
    old = load_catalog(_export(tmp_path) / "docs/catalog.json")
    new = {
        **old,
        "objects": [
            {**o, "hash": "sha256:9"} if o["name"] == "MOD_EXP" else o
            for o in old["objects"]
            if o["name"] != "BASE"
        ]
        + [{"id": "table:S.NUEVA", "hash": "x", "name": "NUEVA"}],
    }
    assert catalog_changes(new, old) == [
        ("alta", "table:S.NUEVA"),
        ("baja", "table:S.BASE"),
        ("modificado", "table:S.MOD_EXP"),
    ]


def test_tracemap_from_documentation_evidence(tmp_path: Path) -> None:
    exp = _export(tmp_path)
    docs = tmp_path / "VG/docs"
    (docs / "functional").mkdir(parents=True)
    (docs / "api").mkdir()
    (docs / "functional/expediente.md").write_text("Guarda en `MOD_EXP`.\n", encoding="utf-8")
    (docs / "api/modelo.md").write_text("Tabla MOD_EXP y vista V_MOD.\n", encoding="utf-8")
    (docs / "bd").mkdir()
    (docs / "bd/x.md").write_text("MOD_EXP\n", encoding="utf-8")  # la sección importada no cuenta
    toml = build_tracemap(
        load_catalog(exp / "docs/catalog.json"), docs, None, None, ("MOD_*", "V_*")
    )
    assert '[tables."MOD_EXP"]' in toml
    assert 'functional = ["docs/functional/expediente.md"]' in toml
    assert 'technical = ["docs/api/modelo.md"]' in toml
    assert '[views."V_MOD"]' in toml
    assert "MOD_HIJO" not in toml  # sin evidencia → sin entrada
    assert "docs/bd/" not in toml


def test_entity_code_and_page_classification() -> None:
    from scripts.db_trace import is_entity_code, is_functional

    assert is_entity_code("gui/window/MvgAgresionWnd.java", "MvgAgresion")
    assert is_entity_code("api/IMvgAgresionService.java", "MvgAgresion")
    assert is_entity_code("web/pages/MvgAgresion/index.zul", "MvgAgresion")
    assert not is_entity_code("gui/window/MvgAgresioninfoWnd.java", "MvgAgresion")
    assert is_functional("functional/expediente.md")
    assert is_functional("guides/registrar_howto.md")
    assert not is_functional("guides/onboarding_dev.md")
    assert not is_functional("api/modelo.md")


def test_tracemap_finds_pages_by_entity_name(tmp_path: Path) -> None:
    exp, ent = _export(tmp_path), _entities(tmp_path)
    docs = tmp_path / "VG/docs"
    (docs / "functional").mkdir(parents=True)
    (docs / "functional/expediente.md").write_text(
        "Pantalla `ModExpWnd::onSave`.\n", encoding="utf-8"
    )
    (docs / "functional/otra.md").write_text("Pantalla `ModExpediente`.\n", encoding="utf-8")
    catalog = load_catalog(exp / "docs/catalog.json")
    toml = build_tracemap(catalog, docs, None, load_entities(ent), ("MOD_EXP",))
    assert 'functional = ["docs/functional/expediente.md"]' in toml  # «ModExpediente» no es ModExp


def test_select_requires_env_and_does_not_write_partially(tmp_path: Path) -> None:
    exp, root = _export(tmp_path), tmp_path / "VG"
    with pytest.raises(DbTraceError, match="entorno"):
        import_pages(exp, root, "bd", ("MOD_*",), env=" ")
    (exp / "docs/tables/mod-hijo.md").unlink()
    with pytest.raises(DbTraceError, match="páginas inexistentes"):
        import_pages(exp, root, "bd", ("MOD_*",), env="Calidad")
    assert not (root / "docs/bd").exists()


@pytest.mark.parametrize(
    ("name", "subdir"), [("..", "bd"), (".", "bd"), ("a/b", "bd"), ("bd", ".."), ("bd", ".")]
)
def test_select_rejects_name_or_subdir_outside_their_folder(
    tmp_path: Path, name: str, subdir: str
) -> None:
    """`--subdir ..` retiraba como «obsoletos» los .md de la raíz del destino."""
    exp, root = _export(tmp_path), tmp_path / "VG"
    keep = root / "README.md"
    keep.parent.mkdir(parents=True)
    keep.write_text("# no se borra\n", encoding="utf-8")
    with pytest.raises(DbTraceError, match="fuera de"):
        import_pages(exp, root, name, ("MOD_*",), subdir=subdir, env="Calidad")
    assert keep.is_file()
    assert sorted(p.name for p in root.iterdir()) == ["README.md"]


def test_select_accepts_nested_subdir(tmp_path: Path) -> None:
    """Uso real (varias bases en un destino): `--subdir bd/<base>`."""
    exp, root = _export(tmp_path), tmp_path / "VG"
    import_pages(exp, root, "bd_calidad", ("MOD_*",), subdir="bd/calidad", env="Calidad")
    assert (root / "docs/bd/calidad/tables/mod-exp.md").is_file()


def test_select_rejects_catalog_paths_outside_the_section(tmp_path: Path) -> None:
    exp, root = _export(tmp_path), tmp_path / "VG"
    data = json.loads((exp / "docs/catalog.json").read_text(encoding="utf-8"))
    data["objects"][0]["path"] = "../fuera.md"
    (exp / "docs/catalog.json").write_text(json.dumps(data), encoding="utf-8")
    (exp / "fuera.md").write_text("# fuera\n", encoding="utf-8")
    with pytest.raises(DbTraceError, match="fuera de"):
        import_pages(exp, root, "bd", ("MOD_*",), env="Calidad")
    assert not root.exists()


def test_select_cli_rejects_dot_dot_name(tmp_path: Path) -> None:
    exp, root = _export(tmp_path), tmp_path / "VG"
    args = ["select", "--export", str(exp), "--root", str(root), "--name", ".."]
    assert main([*args, "--env", "Calidad", "--include", "MOD_*"]) == 2
    assert not root.exists()


def test_rewrite_links_leaves_images_alone() -> None:
    text = "![diagrama](img/er.png) [BASE](base.md)"
    assert rewrite_links(text, "tables/a.md", set()) == "![diagrama](img/er.png) `BASE`"


def test_catalog_with_incomplete_object_is_an_error(tmp_path: Path) -> None:
    exp = _export(tmp_path)
    data = json.loads((exp / "docs/catalog.json").read_text(encoding="utf-8"))
    data["objects"].append({"id": "table:S.X", "kind": "table"})
    (exp / "docs/catalog.json").write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(DbTraceError, match="sin name, path"):
        load_catalog(exp / "docs/catalog.json")


def test_compare_ignores_routines(tmp_path: Path) -> None:
    exp = _export(tmp_path)
    data = json.loads((exp / "docs/catalog.json").read_text(encoding="utf-8"))
    data["objects"].append(
        {"id": "procedure:S.MOD_PROC", "kind": "procedure", "name": "MOD_PROC", "path": "r/p.md"}
    )
    findings = compare(data, load_entities(_entities(tmp_path)), ("MOD_*",))
    assert "MOD_PROC" not in {f.obj for f in findings}


def test_changes_limited_to_scope(tmp_path: Path) -> None:
    full = load_catalog(_export(tmp_path) / "docs/catalog.json")
    subset = {**full, "objects": [o for o in full["objects"] if o["name"].startswith("MOD_")]}
    assert catalog_changes(full, subset) == [("alta", "table:S.BASE"), ("alta", "view:S.V_MOD")]
    assert catalog_changes(full, subset, ("MOD_*",)) == []
