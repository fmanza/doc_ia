"""Tests de scripts/web_captures.py: capturas sintéticas en tmp_path, sin red ni navegador."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from scripts.web_captures import MANIFEST, CaptureError, check, main, publish

PNG = b"\x89PNG\r\n\x1a\n" + b"captura-sintetica"


def _staging(root: Path, origin: str = "kuniv", *names: str) -> None:
    for name in names or ("procesos/listado.png",):
        path = root / "_staging" / origin / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(PNG + name.encode())


def _page(root: Path, rel: str, body: str) -> None:
    path = root / "docs" / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def _kinds(root: Path) -> list[tuple[str, str]]:
    return [(f.kind, f.path) for f in check(root)]


def test_publish_copies_only_listed_captures_and_registers_them(tmp_path: Path) -> None:
    _staging(tmp_path, "kuniv", "procesos/listado.png", "procesos/con_datos_reales.png")
    out = publish(
        tmp_path,
        "kuniv",
        ["procesos\\listado.png"],
        env="PRE",
        version="1.8.8",
        role="Coordinador",
        today="2026-11-10",
    )
    assert out == ["docs/assets/manual/kuniv/procesos/listado.png"]
    assert not (tmp_path / "docs/assets/manual/kuniv/procesos/con_datos_reales.png").exists()
    data = json.loads((tmp_path / MANIFEST).read_text(encoding="utf-8"))
    entry = data["origenes"]["kuniv"]
    assert (entry["entorno"], entry["version"]) == ("PRE", "1.8.8")
    record = entry["capturas"]["procesos/listado.png"]
    assert record["rol"] == "Coordinador"
    assert record["publicada"] == "2026-11-10"
    assert len(record["sha256"]) == 64


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"env": "http://10.0.0.1:8080/app"}, "URL"),
        ({"env": "PRE", "version": "https://pre.example/version"}, "URL"),
        ({"env": " "}, "vacío"),
    ],
)
def test_publish_rejects_urls_and_empty_metadata(
    tmp_path: Path, kwargs: dict[str, str], message: str
) -> None:
    _staging(tmp_path)
    params = {"env": "PRE", "version": "1.8.8", **kwargs}
    with pytest.raises(CaptureError, match=message):
        publish(tmp_path, "kuniv", ["procesos/listado.png"], **params)
    assert not (tmp_path / MANIFEST).exists()


@pytest.mark.parametrize("rel", ["../fuera.png", "C:/fuera.png", "notas.txt", "procesos/no.png"])
def test_publish_validates_every_capture_before_copying(tmp_path: Path, rel: str) -> None:
    _staging(tmp_path)
    with pytest.raises(CaptureError):
        publish(tmp_path, "kuniv", ["procesos/listado.png", rel], env="PRE", version="1.8.8")
    assert not (tmp_path / "docs").exists()
    assert not (tmp_path / MANIFEST).exists()


def test_check_is_clean_when_published_and_cited_with_alt(tmp_path: Path) -> None:
    _staging(tmp_path)
    publish(tmp_path, "kuniv", ["procesos/listado.png"], env="PRE", version="1.8.8")
    _page(
        tmp_path,
        "manual/procesos.md",
        "![Listado de procesos](../assets/manual/kuniv/procesos/listado.png){ loading=lazy }\n",
    )
    assert check(tmp_path) == []


def test_check_reports_unregistered_modified_missing_and_orphan(tmp_path: Path) -> None:
    _staging(tmp_path, "kuniv", "a.png", "b.png", "c.png")
    publish(tmp_path, "kuniv", ["a.png", "b.png", "c.png"], env="PRE", version="1.8.8")
    assets = tmp_path / "docs/assets/manual/kuniv"
    (assets / "a.png").write_bytes(b"editada tras la revision")
    (assets / "b.png").unlink()
    (assets / "copiada_a_mano.png").write_bytes(PNG)
    _page(tmp_path, "manual/index.md", "![A](../assets/manual/kuniv/a.png)\n")
    assert _kinds(tmp_path) == [
        ("sin_registrar", "docs/assets/manual/kuniv/copiada_a_mano.png"),
        ("modificada", "docs/assets/manual/kuniv/a.png"),
        ("falta", "docs/assets/manual/kuniv/b.png"),
        ("huerfana", "docs/assets/manual/kuniv/c.png"),
    ]


def test_check_reports_missing_alt_and_broken_links_but_ignores_code(tmp_path: Path) -> None:
    _staging(tmp_path)
    publish(tmp_path, "kuniv", ["procesos/listado.png"], env="PRE", version="1.8.8")
    body = (
        "![](../assets/manual/kuniv/procesos/listado.png)\n"
        '<img src="../assets/manual/kuniv/procesos/borrada.png" alt="Borrada">\n'
        "```markdown\n![](../assets/manual/kuniv/ejemplo.png)\n```\n"
        "![Logo](../assets/img/logo.png)\n"
    )
    _page(tmp_path, "manual/procesos.md", body)
    assert _kinds(tmp_path) == [
        ("sin_alt", "docs/manual/procesos.md"),
        ("rota", "docs/manual/procesos.md"),
    ]


def test_check_flags_a_url_written_into_the_manifest(tmp_path: Path) -> None:
    _staging(tmp_path)
    publish(tmp_path, "kuniv", ["procesos/listado.png"], env="PRE", version="1.8.8")
    path = tmp_path / MANIFEST
    data = json.loads(path.read_text(encoding="utf-8"))
    data["origenes"]["kuniv"]["nota"] = "http://10.0.0.1:8080/app"
    path.write_text(json.dumps(data), encoding="utf-8")
    _page(tmp_path, "m.md", "![L](assets/manual/kuniv/procesos/listado.png)\n")
    assert _kinds(tmp_path) == [("url", ".ai/captures.json")]


@pytest.mark.parametrize("origin", [".", "..", "a/b", ""])
def test_publish_rejects_origin_names_that_leave_staging(tmp_path: Path, origin: str) -> None:
    _staging(tmp_path)
    with pytest.raises(CaptureError, match="origen inválido"):
        publish(tmp_path, origin, ["procesos/listado.png"], env="PRE", version="1.8.8")
    assert not (tmp_path / "docs").exists()


def test_check_ignores_indented_fences_and_inline_code_and_reads_single_quotes(
    tmp_path: Path,
) -> None:
    _staging(tmp_path)
    publish(tmp_path, "kuniv", ["procesos/listado.png"], env="PRE", version="1.8.8")
    body = (
        '??? note "Ejemplo"\n\n'
        "    ````markdown\n    ![](../assets/manual/kuniv/no_existe.png)\n    ````\n\n"
        "Se cita así: `![](../assets/manual/kuniv/otra.png)`.\n\n"
        "<img src='../assets/manual/kuniv/procesos/listado.png' alt='Listado de procesos'>\n"
    )
    _page(tmp_path, "manual/procesos.md", body)
    assert check(tmp_path) == []


def test_check_rejects_a_malformed_manifest_entry(tmp_path: Path) -> None:
    path = tmp_path / MANIFEST
    path.parent.mkdir(parents=True)
    data = {"format": "doc_ia.web_captures", "format_version": 1, "origenes": {"kuniv": []}}
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(CaptureError, match="kuniv"):
        check(tmp_path)
    assert main(["--root", str(tmp_path), "check"]) == 2


def test_cli_exit_codes(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _staging(tmp_path)
    root = str(tmp_path)
    assert main(["--root", root, "check"]) == 0
    args = ["--root", root, "publish", "kuniv", "procesos/listado.png", "--version", "1.8.8"]
    assert main([*args, "--env", "PRE"]) == 0
    assert main(["--root", root, "check"]) == 1  # publicada y sin citar → huérfana
    assert main([*args, "--env", "https://pre.example"]) == 2
    out = capsys.readouterr()
    assert "huerfana" in out.out
    assert "pre.example" not in out.err  # el error no repite la URL
