"""Ejemplo: publicar capturas revisadas del origen WEB y comprobar el manual que las cita.

Sin red ni navegador y determinista: las capturas son ficheros sintéticos en una carpeta temporal.
"""

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from web_captures import check, publish  # noqa: E402

PNG = b"\x89PNG\r\n\x1a\n"  # cabecera PNG: basta para el ejemplo

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)  # raíz del destino (la carpeta con mkdocs.yml)
    staging = root / "_staging" / "kuniv"  # lo deja snapshot_sources.py sync
    (staging / "procesos").mkdir(parents=True)
    (staging / "procesos" / "listado.png").write_bytes(PNG + b"listado")
    (staging / "procesos" / "alta.png").write_bytes(PNG + b"alta con datos reales")

    # Solo se publica la captura que la persona ha revisado; la otra se queda en _staging/.
    published = publish(
        root, "kuniv", ["procesos/listado.png"], env="PRE", version="1.8.8", role="Coordinador"
    )
    print("Publicada:", published[0])

    page = root / "docs" / "manual" / "procesos.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text("![](../assets/manual/kuniv/procesos/listado.png)\n", encoding="utf-8")
    print("Sin texto alternativo:", [(f.kind, f.detail) for f in check(root)])

    alt = "![Listado de procesos de evaluación](../assets/manual/kuniv/procesos/listado.png)\n"
    page.write_text(alt, encoding="utf-8")
    print("Corregido:", check(root))

    (root / "docs/assets/manual/kuniv/procesos/alta.png").write_bytes(PNG + b"copiada a mano")
    print("Copiada a mano:", [(f.kind, Path(f.path).name) for f in check(root)])
