"""Tests para scripts/doc_trace.py — trazabilidad determinista docs ↔ código."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest
from scripts import doc_trace
from scripts.doc_trace import (
    OriginBaseline,
    build_llms_txt,
    build_matrix,
    changed_files,
    check_drift,
    collect_criteria,
    collect_test_ids,
    fingerprint,
    main,
    read_page_meta,
    stamp_page,
    write_baseline,
)


def _repo(tmp_path: Path) -> Path:
    (tmp_path / "docs").mkdir(parents=True)
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "mod.py").write_text("x = 1\n", encoding="utf-8")
    return tmp_path


def _page(repo: Path, frontmatter: str, name: str = "page.md") -> Path:
    page = repo / "docs" / name
    page.write_text(f"---\n{frontmatter}\n---\n# Título\n\nCuerpo.\n", encoding="utf-8")
    return page


# --- fingerprint ---


def test_fingerprint_ignores_line_endings(tmp_path: Path) -> None:
    lf = tmp_path / "lf.py"
    crlf = tmp_path / "crlf.py"
    lf.write_bytes(b"a = 1\nb = 2\n")
    crlf.write_bytes(b"a = 1\r\nb = 2\r\n")
    assert fingerprint(lf) == fingerprint(crlf)
    assert len(fingerprint(lf)) == 12


def test_fingerprint_markdown_ignores_frontmatter(tmp_path: Path) -> None:
    plain = tmp_path / "a.md"
    stamped = tmp_path / "b.md"
    plain.write_text("# Página\n", encoding="utf-8")
    stamped.write_text('---\narquetipo: "1"\n---\n# Página\n', encoding="utf-8")
    assert fingerprint(plain) == fingerprint(stamped)


# --- read_page_meta ---


def test_read_page_meta_without_frontmatter(tmp_path: Path) -> None:
    page = tmp_path / "p.md"
    page.write_text("# Sin frontmatter\n", encoding="utf-8")
    assert read_page_meta(page) is None


def test_read_page_meta_without_sources(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    assert read_page_meta(_page(repo, 'title: "x"')) is None


def test_read_page_meta_parses_fields(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    page = _page(repo, 'arquetipo: "2"\nfuentes:\n  src/mod.py: abc123\nrevisado: 2026-10-28')
    meta = read_page_meta(page)
    assert meta is not None
    assert meta.archetype == "2"
    assert meta.sources == {"src/mod.py": "abc123"}
    assert meta.reviewed == "2026-10-28"


# --- stamp_page + check_drift ---


def test_stamp_then_no_drift(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    page = repo / "docs" / "page.md"
    page.write_text("# Título\n\nCuerpo.\n", encoding="utf-8")
    stamp_page(page, repo, sources=["src/mod.py"], archetype="2", reviewed="2026-10-28")
    text = page.read_text(encoding="utf-8")
    assert text.startswith('---\narquetipo: "2"\nfuentes:\n  src/mod.py: ')
    assert text.endswith("# Título\n\nCuerpo.\n")
    assert check_drift(repo / "docs", repo) == []


def test_stamp_preserves_existing_sources_and_archetype(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    page = _page(repo, 'arquetipo: "1"\nfuentes:\n  src/mod.py: old\nrevisado: 2020-01-01')
    meta = stamp_page(page, repo, reviewed="2026-10-28")
    assert meta.archetype == "1"
    assert meta.sources == {"src/mod.py": fingerprint(repo / "src" / "mod.py")}


def test_drift_detects_stale_source(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    page = repo / "docs" / "page.md"
    page.write_text("# T\n", encoding="utf-8")
    stamp_page(page, repo, sources=["src/mod.py"], reviewed="2026-10-28")
    (repo / "src" / "mod.py").write_text("x = 2\n", encoding="utf-8")
    findings = check_drift(repo / "docs", repo)
    assert [(f.source, f.status) for f in findings] == [("src/mod.py", "stale")]


def test_drift_detects_missing_source(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _page(repo, 'arquetipo: "2"\nfuentes:\n  src/gone.py: abc\nrevisado: 2026-10-28')
    findings = check_drift(repo / "docs", repo)
    assert [f.status for f in findings] == ["missing"]


def test_drift_never_reads_outside_repo(tmp_path: Path) -> None:
    repo = _repo(tmp_path / "repo")
    (tmp_path / "secret.txt").write_text("token\n", encoding="utf-8")
    _page(repo, 'arquetipo: "2"\nfuentes:\n  ../secret.txt: abc\nrevisado: 2026-10-28')
    findings = check_drift(repo / "docs", repo)
    assert [f.status for f in findings] == ["outside_repo"]


def test_stamp_rejects_source_outside_repo(tmp_path: Path) -> None:
    repo = _repo(tmp_path / "repo")
    (tmp_path / "secret.txt").write_text("token\n", encoding="utf-8")
    page = repo / "docs" / "page.md"
    page.write_text("# T\n", encoding="utf-8")
    with pytest.raises(ValueError, match="fuera del repositorio"):
        stamp_page(page, repo, sources=["../secret.txt"])


def test_stamp_requires_sources(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    page = repo / "docs" / "page.md"
    page.write_text("# T\n", encoding="utf-8")
    with pytest.raises(ValueError, match="sin fuentes"):
        stamp_page(page, repo)


# --- matrix ---


def _functional(repo: Path) -> None:
    fdir = repo / "docs" / "functional"
    fdir.mkdir(parents=True)
    (fdir / "a.md").write_text(
        "## 7. Criterios de Aceptación\n\n"
        "| ID | Dado | Cuando | Entonces | Test |\n|---|---|---|---|---|\n"
        "| AC-01 | x | y | z | `tests/test_a.py::test_ok` |\n"
        "| AC-02 | x | y | z | Sin test |\n"
        "| AC-03 | x | y | z | `tests/test_a.py::test_ghost` |\n",
        encoding="utf-8",
    )
    tdir = repo / "tests"
    tdir.mkdir()
    (tdir / "test_a.py").write_text(
        "def test_ok():\n    pass\n\n\ndef test_uncited():\n    pass\n\n\n"
        "class TestGroup:\n    def test_method(self):\n        pass\n",
        encoding="utf-8",
    )


def test_collect_test_ids_includes_class_methods(tmp_path: Path) -> None:
    _functional(tmp_path)
    ids = collect_test_ids(tmp_path / "tests", tmp_path)
    assert ids == {
        "tests/test_a.py::test_ok",
        "tests/test_a.py::test_uncited",
        "tests/test_a.py::TestGroup::test_method",
    }


def test_matrix_reports_unknown_and_uncited(tmp_path: Path) -> None:
    _functional(tmp_path)
    criteria = collect_criteria(tmp_path / "docs" / "functional")
    assert [c.criterion for c in criteria] == ["AC-01", "AC-02", "AC-03"]
    report, unknown = build_matrix(
        criteria, collect_test_ids(tmp_path / "tests", tmp_path), tmp_path
    )
    assert unknown == ["tests/test_a.py::test_ghost"]
    assert "**Total**: 2/3 criterios con test." in report
    assert "`tests/test_a.py::test_uncited`" in report


def test_main_matrix_exit_code_on_unknown_test(tmp_path: Path) -> None:
    _functional(tmp_path)
    code = main(
        [
            "--root",
            str(tmp_path),
            "matrix",
            "--docs",
            str(tmp_path / "docs"),
            "--tests",
            str(tmp_path / "tests"),
        ]
    )
    assert code == 1


# --- llms ---


MKDOCS_YML = """site_name: Demo
site_description: Sitio de prueba
site_url: https://example.org/demo/
markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
nav:
  - Inicio: index.md
  - Funcional:
      - Mapa: functional/index.md
      - Área:
          - Módulo: functional/mod.md
  - Externo: https://example.org/
"""


def test_build_llms_txt_tolerates_python_tags(tmp_path: Path) -> None:
    cfg = tmp_path / "mkdocs.yml"
    cfg.write_text(MKDOCS_YML, encoding="utf-8")
    content = build_llms_txt(cfg)
    assert content.startswith("# Demo\n\n> Sitio de prueba\n")
    assert "- [Inicio](https://example.org/demo/)" in content
    assert "- [Mapa](https://example.org/demo/functional/)" in content
    assert "- [Área › Módulo](https://example.org/demo/functional/mod/)" in content
    assert "Externo" not in content


def test_main_llms_check_detects_outdated(tmp_path: Path) -> None:
    cfg = tmp_path / "mkdocs.yml"
    cfg.write_text(MKDOCS_YML, encoding="utf-8")
    out = tmp_path / "llms.txt"
    assert main(["llms", "--config", str(cfg), "--output", str(out), "--check"]) == 1
    assert main(["llms", "--config", str(cfg), "--output", str(out)]) == 0
    assert main(["llms", "--config", str(cfg), "--output", str(out), "--check"]) == 0


def test_main_llms_without_nav_returns_error(tmp_path: Path) -> None:
    cfg = tmp_path / "mkdocs.yml"
    cfg.write_text("site_name: Demo\n", encoding="utf-8")
    assert main(["llms", "--config", str(cfg), "--output", str(tmp_path / "llms.txt")]) == 1


def test_main_stamp_missing_page_returns_error(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    missing = repo / "docs" / "no_existe.md"
    assert main(["--root", str(repo), "stamp", str(missing), "--source", "src/mod.py"]) == 1


def test_main_requires_subcommand() -> None:
    with pytest.raises(SystemExit) as exc:
        main([])
    assert exc.value.code == 2


# --- modo incremental: baseline + changes (repositorios git reales en tmp_path, sin red) ---


def _git(repo: Path, *args: str) -> str:
    cmd = ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", *args]
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout.strip()


def _origin(tmp_path: Path, name: str = "mi_api") -> Path:
    origin = tmp_path / name
    (origin / "src").mkdir(parents=True)
    (origin / "src" / "mod.py").write_text("def f():\n    return 1\n", encoding="utf-8")
    (origin / "src" / "old.py").write_text("x = 1\n", encoding="utf-8")
    _git(origin, "init", "-q", "-b", "main")
    _git(origin, "config", "core.autocrlf", "false")
    _git(origin, "add", "-A")
    _git(origin, "commit", "-q", "-m", "init")
    return origin


def _evidence(*cites: str) -> str:
    rows = "".join(f"    | `{c}` | ✅ |\n" for c in cites)
    return f'\n??? note "Evidencia"\n\n    | Elemento | Confianza |\n    |---|---|\n{rows}'


def _dest(tmp_path: Path) -> Path:
    dest = tmp_path / "dest"
    for folder in ("api", "examples", "functional", "guides"):
        (dest / "docs" / folder).mkdir(parents=True)
    docs = dest / "docs"
    (docs / "api" / "mod.md").write_text(
        "# mod\n\nVer [ejemplo](../examples/mod.md).\n" + _evidence("src/mod.py::f"),
        encoding="utf-8",
    )
    (docs / "examples" / "mod.md").write_text("# Ejemplo\n", encoding="utf-8")
    (docs / "functional" / "old.md").write_text(_evidence("src/old.py::x"), encoding="utf-8")
    (docs / "functional" / "otro.md").write_text(_evidence("lib/src/mod.py"), encoding="utf-8")
    (docs / "guides" / "nota.md").write_text("Se apoya en `src/mod.py`.\n", encoding="utf-8")
    return dest


def _origins_state(dest: Path) -> dict[str, dict[str, object]]:
    data = json.loads((dest / ".ai" / "doc_state.json").read_text(encoding="utf-8"))
    origins: dict[str, dict[str, object]] = data["origenes"]
    return origins


def _baseline(dest: Path, origin: Path, *extra: str) -> int:
    return main(["--root", str(dest), "baseline", "--origin", str(origin), *extra])


def _changes(dest: Path, origin: Path, *extra: str) -> int:
    return main(["--root", str(dest), "changes", "--origin", str(origin), *extra])


def test_baseline_records_clean_head(tmp_path: Path) -> None:
    origin, dest = _origin(tmp_path), _dest(tmp_path)
    assert _baseline(dest, origin) == 0
    data = json.loads((dest / ".ai" / "doc_state.json").read_text(encoding="utf-8"))
    assert data["doc_ia"] == doc_trace._doc_ia_version()
    entry = _origins_state(dest)["mi_api"]
    assert entry["commit"] == _git(origin, "rev-parse", "HEAD")
    assert (entry["rama"], entry["sucio"]) == ("main", False)


def test_changes_without_changes_exit_0(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    origin, dest = _origin(tmp_path), _dest(tmp_path)
    _baseline(dest, origin)
    assert _changes(dest, origin) == 0
    assert "Sin cambios" in capsys.readouterr().out


def test_changes_maps_files_to_citing_pages_and_examples(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Modificado (pendiente), alta sin seguimiento con ñ y renombrado confirmado."""
    origin, dest = _origin(tmp_path), _dest(tmp_path)
    _baseline(dest, origin)
    _git(origin, "mv", "src/old.py", "src/renamed.py")
    _git(origin, "commit", "-q", "-m", "rename")
    (origin / "src" / "mod.py").write_text("def f():\n    return 2\n", encoding="utf-8")
    (origin / "src" / "año.py").write_text("y = 1\n", encoding="utf-8")
    capsys.readouterr()
    assert _changes(dest, origin) == 1
    out = capsys.readouterr().out
    assert "| M | `src/mod.py` | `docs/api/mod.md` | `docs/guides/nota.md` |" in out
    assert "| R | `src/old.py → src/renamed.py` | `docs/functional/old.md` | — |" in out
    assert "| A | `src/año.py` | *Sin página* | — |" in out
    assert "## Páginas a revisar (2)" in out  # la mención en una guía no obliga a revisarla
    assert "- `docs/examples/mod.md`" in out
    assert "otro.md" not in out  # `lib/src/mod.py` no es una cita de `src/mod.py`


def test_changes_matches_prefixed_citations_of_multi_origin(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    origin, dest = _origin(tmp_path), _dest(tmp_path)
    (dest / "docs" / "api" / "mod.md").write_text(
        _evidence("api_core/src/mod.py::f"), encoding="utf-8"
    )
    _baseline(dest, origin, "--name", "api_core")
    (origin / "src" / "mod.py").write_text("changed\n", encoding="utf-8")
    capsys.readouterr()
    assert _changes(dest, origin, "--name", "api_core") == 1
    assert "| M | `src/mod.py` | `docs/api/mod.md` |" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("entry", "version", "reason"),
    [
        (None, None, "sin baseline"),
        ({"commit": None}, None, "no estaba bajo git"),
        ({"commit": "f" * 40}, None, "no está en el historial"),
        ({"commit": "HEAD"}, "0.0.1", "doc_ia 0.0.1"),
    ],
)
def test_changes_falls_back_to_full_mode_exit_3(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    entry: dict[str, object] | None,
    version: str | None,
    reason: str,
) -> None:
    origin, dest = _origin(tmp_path), _dest(tmp_path)
    if entry is not None:
        state = {"doc_ia": version or doc_trace._doc_ia_version(), "origenes": {"mi_api": entry}}
        (dest / ".ai").mkdir()
        (dest / ".ai" / "doc_state.json").write_text(json.dumps(state), encoding="utf-8")
    assert _changes(dest, origin) == 3
    captured = capsys.readouterr()
    assert "Modo completo" in captured.out
    assert reason in captured.err


def test_baseline_without_git_then_changes_is_full_mode(tmp_path: Path) -> None:
    origin, dest = tmp_path / "sin_git", _dest(tmp_path)
    origin.mkdir()
    with patch.object(doc_trace, "_git", return_value=None):
        assert _baseline(dest, origin) == 0
    assert _origins_state(dest)["sin_git"]["commit"] is None
    assert _changes(dest, origin) == 3


def test_destination_inside_origin_ignores_its_own_artifacts(tmp_path: Path) -> None:
    """Origen = destino: docs/, .ai/, mkdocs.yml y VER_DOCUMENTACION.md no son cambios."""
    origin = _origin(tmp_path)
    (origin / "docs").mkdir()
    (origin / "docs" / "mod.md").write_text("`src/mod.py::f`\n", encoding="utf-8")
    (origin / "mkdocs.yml").write_text("site_name: x\n", encoding="utf-8")
    _git(origin, "add", "-A")
    _git(origin, "commit", "-q", "-m", "docs")
    (origin / "docs" / "mod.md").write_text("`src/mod.py::f` editado\n", encoding="utf-8")
    (origin / "VER_DOCUMENTACION.md").write_text("# Ver\n", encoding="utf-8")
    assert _baseline(origin, origin) == 0
    assert _origins_state(origin)["mi_api"]["sucio"] is False
    _git(origin, "add", "-A")
    _git(origin, "commit", "-q", "-m", "cierre de documentación")
    assert _changes(origin, origin) == 0
    (origin / "src" / "mod.py").write_text("changed\n", encoding="utf-8")
    assert _changes(origin, origin) == 1


def test_origin_in_subfolder_of_repository_uses_origin_relative_paths(tmp_path: Path) -> None:
    repo = tmp_path / "mono"
    origin = repo / "backend"
    (origin / "src").mkdir(parents=True)
    (origin / "src" / "mod.py").write_text("a\n", encoding="utf-8")
    (repo / "frontend.js").write_text("b\n", encoding="utf-8")
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "init")
    (origin / "src" / "mod.py").write_text("changed\n", encoding="utf-8")
    (repo / "frontend.js").write_text("changed\n", encoding="utf-8")
    changes = changed_files(origin, "HEAD")
    assert [(c.kind, c.path) for c in changes or []] == [("M", "src/mod.py")]


def test_write_baseline_keeps_other_origins(tmp_path: Path) -> None:
    state = tmp_path / ".ai" / "doc_state.json"
    write_baseline(state, "a", OriginBaseline("1" * 40, "main", False, "2026-10-29"))
    write_baseline(state, "b", OriginBaseline("2" * 40, "dev", True, "2026-10-30"))
    data = json.loads(state.read_text(encoding="utf-8"))
    assert list(data["origenes"]) == ["a", "b"]
    assert data["origenes"]["b"] == {
        "commit": "2" * 40,
        "rama": "dev",
        "sucio": True,
        "fecha": "2026-10-30",
    }
