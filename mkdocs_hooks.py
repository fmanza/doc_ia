"""Paso post-build: genera el ZIP offline `latest` de la documentación doc_ia en site/.

Lo ejecuta `scripts/build_docs_zip.py` tras un `zensical build` correcto (Zensical no tiene
`hooks:`). El nombre es heredado de la etapa MkDocs y se mantiene (ADR-003).
No requiere instalación ni registro de paquete.

Patrón de referencia para otros proyectos:
  Copiar este fichero y cambiar únicamente la línea zip_path (y VER_DOCUMENTACION.md por
  VIEW_DOCS.md en EXTRA_FILES si la documentación está en inglés).
"""

import hashlib
import os
import subprocess
import time
import zipfile
from pathlib import Path

# Ficheros fuera de site/ que viajan en la raíz del ZIP: servidor local e instrucciones.
EXTRA_FILES = ("scripts/start-server.py", "VER_DOCUMENTACION.md")

# ZIP reproducible: mismo contenido → mismos bytes. Entradas ordenadas, fecha y permisos fijos.
ZIP_MIN_DATE_TIME = (1980, 1, 1, 0, 0, 0)
ZIP_MIN_EPOCH = 315532800  # 1980-01-01T00:00:00Z
ZIP_FILE_MODE = 0o644


def on_post_build(config, **kwargs):
    site_dir = Path(config.get("site_dir", "site"))
    zip_path = site_dir / "doc_ia-docs-latest.zip"

    if not site_dir.exists():
        print(f"[ZIP] WARN directorio {site_dir} no encontrado")
        return

    print(f"\n[ZIP] Generando descarga de documentacion: {zip_path}")

    date_time = _zip_date_time(Path(__file__).parent)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in sorted(p for p in site_dir.rglob("*") if p.is_file()):
            if file_path.suffix in (".zip", ".sha256"):
                continue
            _add_entry(zipf, file_path, file_path.relative_to(site_dir).as_posix(), date_time)

        for extra in EXTRA_FILES:
            extra_path = Path(__file__).parent / extra
            if extra_path.exists():
                print(f"[ZIP] Incluyendo: {extra_path.name}")
                _add_entry(zipf, extra_path, extra_path.name, date_time)

    sha256_hash = _sha256(zip_path)
    sha256_file = zip_path.with_suffix(".zip.sha256")
    sha256_file.write_text(f"{sha256_hash}  {zip_path.name}\n", encoding="utf-8")

    file_size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"[OK] ZIP creado: {zip_path.name} ({file_size_mb:.2f} MB)")
    print(f"[OK] SHA256: {sha256_hash}")
    print(f"[OK] Checksum guardado: {sha256_file.name}")


def _zip_date_time(root: Path) -> tuple:
    """Fecha fija de las entradas: SOURCE_DATE_EPOCH, si no la del último commit, si no 1980."""
    epoch = os.environ.get("SOURCE_DATE_EPOCH", "").strip()
    if not epoch:
        try:
            epoch = subprocess.run(
                ["git", "log", "-1", "--format=%ct"],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            ).stdout
            epoch = (epoch or "").strip()
        except OSError:
            epoch = ""
    if epoch.isdigit() and int(epoch) >= ZIP_MIN_EPOCH:
        return tuple(time.gmtime(int(epoch))[:6])
    return ZIP_MIN_DATE_TIME


def _add_entry(zipf: zipfile.ZipFile, path: Path, arcname: str, date_time: tuple) -> None:
    info = zipfile.ZipInfo(arcname, date_time=date_time)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = ZIP_FILE_MODE << 16
    zipf.writestr(info, path.read_bytes())


def _sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()
