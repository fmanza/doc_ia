"""Tests para scripts/start-server.py — servidor local del ZIP offline (solo loopback)."""

from __future__ import annotations

import importlib.util
import socket
import sys
import threading
import urllib.request
from pathlib import Path
from types import ModuleType
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "start-server.py"


def _load() -> ModuleType:
    """El nombre con guion no es importable: se carga por ruta."""
    spec = importlib.util.spec_from_file_location("start_server", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run(module: ModuleType, server: Any, *argv: str) -> MagicMock:
    with (
        patch.object(module, "DocsServer", server) as tcp,
        patch.object(module.webbrowser, "open") as browser,
        patch.object(sys, "argv", ["start-server.py", *argv]),
    ):
        module.main()
    tcp.browser = browser
    return tcp


def test_binds_loopback_and_serves_script_dir() -> None:
    """Solo 127.0.0.1 (nunca todas las interfaces) y sin cambiar el directorio de trabajo."""
    module = _load()
    server = MagicMock()
    server.return_value.serve_forever.side_effect = KeyboardInterrupt
    cwd = Path.cwd()
    tcp = _run(module, server, "--port", "9001")
    (host, port), handler = tcp.call_args.args
    assert (host, port) == ("127.0.0.1", 9001)
    assert handler.keywords["directory"] == str(SCRIPT.parent)
    assert Path.cwd() == cwd
    tcp.browser.assert_called_once_with("http://127.0.0.1:9001")


def test_no_browser_flag() -> None:
    module = _load()
    server = MagicMock()
    server.return_value.serve_forever.side_effect = KeyboardInterrupt
    tcp = _run(module, server, "--no-browser")
    tcp.browser.assert_not_called()


def test_server_is_threaded_and_never_shares_port_on_windows() -> None:
    """Una conexión ociosa (preconexión del navegador) no bloquea; en Windows, sin SO_REUSEADDR."""
    module = _load()
    assert issubclass(module.DocsServer, module.http.server.ThreadingHTTPServer)
    assert module.DocsServer.allow_reuse_address is (sys.platform != "win32")


def test_idle_connection_does_not_block_real_server() -> None:
    """Loopback real, sin red externa: con un socket ocioso abierto, otra petición responde."""
    module = _load()
    handler = module.functools.partial(
        module.http.server.SimpleHTTPRequestHandler, directory=str(SCRIPT.parent)
    )
    with module.DocsServer(("127.0.0.1", 0), handler) as httpd:
        port = httpd.server_address[1]
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        with socket.create_connection(("127.0.0.1", port)):
            with urllib.request.urlopen(
                f"http://127.0.0.1:{port}/start-server.py", timeout=5
            ) as resp:
                assert resp.status == 200
        httpd.shutdown()


def test_second_server_on_same_port_fails() -> None:
    """Loopback real: el puerto ocupado se detecta también en Windows (sin SO_REUSEADDR)."""
    module = _load()
    handler = module.http.server.SimpleHTTPRequestHandler
    with module.DocsServer(("127.0.0.1", 0), handler) as first:
        with pytest.raises(OSError):
            module.DocsServer(("127.0.0.1", first.server_address[1]), handler)


def test_busy_port_exits_1_with_hint(capsys: pytest.CaptureFixture[str]) -> None:
    module = _load()
    server = MagicMock(side_effect=OSError(98, "Address already in use"))
    with pytest.raises(SystemExit) as exc:
        _run(module, server)
    assert exc.value.code == 1
    err = capsys.readouterr().err
    assert "8000" in err
    assert "--port 8001" in err
