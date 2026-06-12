#!/usr/bin/env python3
"""Servidor HTTP local para navegar la documentación doc_ia offline.

Incluido dentro del ZIP de documentación generado por mkdocs build.

Uso:
    python start-server.py
    python start-server.py --port 9000
"""

import argparse
import http.server
import os
import socketserver
import webbrowser
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Servidor offline para docs doc_ia.")
    parser.add_argument("--port", type=int, default=8000, help="Puerto (default: 8000)")
    parser.add_argument(
        "--no-browser", action="store_true", help="No abrir el navegador automáticamente"
    )
    args = parser.parse_args()

    # Servir desde el directorio donde está este script
    serve_dir = Path(__file__).parent
    os.chdir(serve_dir)

    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", args.port), handler) as httpd:
        url = f"http://localhost:{args.port}"
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
