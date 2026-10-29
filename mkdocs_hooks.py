"""Hook MkDocs: genera ZIP offline de la documentación doc_ia tras cada build.

Cargado directamente por MkDocs mediante la clave `hooks:` de mkdocs.yml.
No requiere instalación ni registro de paquete.

Patrón de referencia para otros proyectos:
  Copiar este fichero y cambiar únicamente la línea zip_path (y VER_DOCUMENTACION.md por
  VIEW_DOCS.md en EXTRA_FILES si la documentación está en inglés).
"""

import hashlib
import os
import zipfile
from pathlib import Path

# Ficheros fuera de site/ que viajan en la raíz del ZIP: servidor local e instrucciones.
EXTRA_FILES = ("scripts/start-server.py", "VER_DOCUMENTACION.md")


def on_post_build(config, **kwargs):
    site_dir = Path(config.get("site_dir", "site"))
    zip_path = site_dir / "doc_ia-docs-latest.zip"

    if not site_dir.exists():
        print(f"[ZIP] WARN directorio {site_dir} no encontrado")
        return

    print(f"\n[ZIP] Generando descarga de documentacion: {zip_path}")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(site_dir):
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in (".zip", ".sha256"):
                    continue
                arcname = file_path.relative_to(site_dir)
                zipf.write(file_path, arcname=arcname)

        for extra in EXTRA_FILES:
            extra_path = Path(__file__).parent / extra
            if extra_path.exists():
                print(f"[ZIP] Incluyendo: {extra_path.name}")
                zipf.write(extra_path, arcname=extra_path.name)

    sha256_hash = _sha256(zip_path)
    sha256_file = zip_path.with_suffix(".zip.sha256")
    sha256_file.write_text(f"{sha256_hash}  {zip_path.name}\n", encoding="utf-8")

    file_size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"[OK] ZIP creado: {zip_path.name} ({file_size_mb:.2f} MB)")
    print(f"[OK] SHA256: {sha256_hash}")
    print(f"[OK] Checksum guardado: {sha256_file.name}")


def _sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()
