"""Tests para scripts/doc_trace.py — trazabilidad determinista docs ↔ código."""

from __future__ import annotations

from pathlib import Path

import pytest
from scripts.doc_trace import (
    build_llms_txt,
    build_matrix,
    check_drift,
    collect_criteria,
    collect_test_ids,
    fingerprint,
    main,
    read_page_meta,
    stamp_page,
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
