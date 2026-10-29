#!/usr/bin/env python3
"""Servidor HTTP local para navegar la documentación doc_ia offline.

Incluido dentro del ZIP de documentación generado por mkdocs build. Solo usa la biblioteca
estándar: basta Python 3.7 o superior, sin instalar paquetes. Escucha únicamente en 127.0.0.1,
así que la documentación no queda expuesta a la red local.

Uso:
    python start-server.py
    python start-server.py --port 9000
"""

import argparse
import functools
import http.server
import sys
import webbrowser
from pathlib import Path

HOST = "127.0.0.1"


class DocsServer(http.server.ThreadingHTTPServer):
    """Un hilo por conexión: una conexión ociosa del navegador no bloquea las demás.

    En Windows, SO_REUSEADDR deja que dos servidores compartan puerto: se desactiva para que un
    puerto ocupado falle al arrancar en lugar de servir páginas de otro proceso.
    """

    allow_reuse_address = sys.platform != "win32"


def main() -> None:
    parser = argparse.ArgumentParser(description="Servidor offline para docs doc_ia.")
    parser.add_argument("--port", type=int, default=8000, help="Puerto (default: 8000)")
    parser.add_argument(
        "--no-browser", action="store_true", help="No abrir el navegador automáticamente"
    )
    args = parser.parse_args()

    # Servir desde el directorio donde está este script
    serve_dir = Path(__file__).resolve().parent
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(serve_dir))

    try:
        httpd = DocsServer((HOST, args.port), handler)
    except OSError as exc:
        print(f"[doc_ia-docs] No se puede usar el puerto {args.port}: {exc}", file=sys.stderr)
        print(
            f"[doc_ia-docs] Prueba otro puerto: python start-server.py --port {args.port + 1}",
            file=sys.stderr,
        )
        sys.exit(1)

    with httpd:
        url = f"http://{HOST}:{args.port}"
        print(f"[doc_ia-docs] Sirviendo documentación en {url}")
        print("[doc_ia-docs] Pulsa Ctrl+C para detener el servidor.")
        if not args.no_browser:
            webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[doc_ia-docs] Servidor detenido.")


if __name__ == "__main__":
    main()
