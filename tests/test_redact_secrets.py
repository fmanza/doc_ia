"""Tests de scripts/redact_secrets.py: valores sintéticos evidentes, sin red."""

from __future__ import annotations

import time
from pathlib import Path

import pytest
from scripts.redact_secrets import REDACTED, find_secrets, main, redact, redact_tree

FAKE = "Abc123FakeSecretValue9"  # valor sintético: nunca un secreto real


@pytest.mark.parametrize(
    ("text", "rule"),
    [
        (f"client_secret={FAKE}&scope=openid", "client_secret"),
        (f"&amp;client\\_secret= **{FAKE}** &amp;redirect", "client_secret"),  # Markdown de docling
        (f"password={FAKE}", "password"),
        (f"**Contraseña:** {FAKE}", "password"),
        (f"https://host/api?user=demo&pass={FAKE}", "password"),
        (f"usuario (demo) y token({FAKE}-0000-1111)", "token"),
        (f"api_key: {FAKE}XYZ", "token"),
        (f"https://demo:{FAKE}@host.example/path", "url_basic_auth"),
    ],
)
def test_detects_and_redacts_value_only(text: str, rule: str) -> None:
    new, hits = redact(text)
    assert [r for _, r in hits] == [rule]
    assert FAKE not in new
    prefix = text.split(FAKE)[0]
    assert new.startswith(prefix + REDACTED)  # la clave se conserva; solo cambia el valor


def test_jwt_is_redacted_whole() -> None:
    jwt = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkZW1vMTIzNDUifQ.c2lnbmF0dXJlMTIzNDU2"
    new, hits = redact(f"id_token={jwt} fin")
    assert [r for _, r in hits] in (["jwt"], ["token"])
    assert jwt not in new


def test_private_key_block_is_redacted_whole() -> None:
    key = "-----BEGIN RSA PRIVATE KEY-----\nMIIEfake\nlinea2\n-----END RSA PRIVATE KEY-----"
    text = f"antes\n{key}\ndespués"
    new, hits = redact(text)
    assert hits == [(2, "private_key")]
    assert new == f"antes\n{REDACTED}\ndespués"


@pytest.mark.parametrize(
    "text",
    [
        # descripción de un parámetro, no un valor
        "| p2 | String | -- | Password de la llamada a la integración |",
        "**Contraseña:** xxxxxx",
        "password=<oculto>",
        "client_secret: proporcionado por SSO",
        "Password: obligatorio",
        "Token url: [https://idp.example/oauth2/v1/token](https://idp.example/oauth2/v1/token)",
        "password=${DB_PASSWORD}",
        f"client_secret={REDACTED}",
        "El token de acceso caduca a la hora.",
    ],
)
def test_ignores_placeholders_and_prose(text: str) -> None:
    assert find_secrets(text) == []
    assert redact(text)[0] == text


def test_redact_is_idempotent() -> None:
    once, _ = redact(f"client_secret={FAKE}")
    twice, hits = redact(once)
    assert (twice, hits) == (once, [])


def test_line_numbers_refer_to_original_text() -> None:
    text = (
        "uno\n-----BEGIN PRIVATE KEY-----\na\nb\n-----END PRIVATE KEY-----\n" + f"password={FAKE}\n"
    )
    assert find_secrets(text) == [(2, "private_key"), (6, "password")]


def test_redact_tree_preserves_line_endings_and_other_files(tmp_path: Path) -> None:
    md = tmp_path / "md" / "doc.md"
    md.parent.mkdir()
    md.write_bytes(f"a\r\nclient_secret={FAKE}\r\nb\r\n".encode())
    other = tmp_path / "md" / "notas.txt"
    other.write_text(f"password={FAKE}", encoding="utf-8")
    findings = redact_tree(tmp_path)
    assert [(f.line, f.rule) for f in findings] == [(2, "client_secret")]
    assert md.read_bytes() == f"a\r\nclient_secret={REDACTED}\r\nb\r\n".encode()
    assert FAKE in other.read_text(encoding="utf-8")  # solo .md


def test_check_mode_does_not_modify(tmp_path: Path) -> None:
    md = tmp_path / "doc.md"
    md.write_text(f"token={FAKE}", encoding="utf-8")
    assert len(redact_tree(tmp_path, check=True)) == 1
    assert FAKE in md.read_text(encoding="utf-8")


def test_cli_exit_codes_and_report_never_shows_value(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    md = tmp_path / "doc.md"
    md.write_text(f"linea\npassword={FAKE}\n", encoding="utf-8")
    assert main([str(tmp_path), "--check"]) == 1
    out = capsys.readouterr().out
    assert "doc.md:2 · password" in out
    assert FAKE not in out
    assert main([str(tmp_path)]) == 1  # redacta
    assert FAKE not in capsys.readouterr().out
    assert main([str(tmp_path)]) == 0  # ya no queda nada
    assert main([str(tmp_path / "no_existe")]) == 2


def test_large_document_is_fast(tmp_path: Path) -> None:
    md = tmp_path / "grande.md"
    rows = "| campo | valor | descripción larga de prueba |\n" * 20000
    md.write_text(rows + f"password={FAKE}\n", encoding="utf-8")
    start = time.perf_counter()
    findings = redact_tree(md, check=True)
    assert [f.rule for f in findings] == ["password"]
    assert time.perf_counter() - start < 5
