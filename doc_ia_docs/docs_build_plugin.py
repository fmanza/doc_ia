"""Plugin mkdocs para generar descarga ZIP de la documentación doc_ia.

Genera automáticamente doc_ia-docs-latest.zip + .sha256 al final de cada
mkdocs build. Para activarlo: pip install -e . (una sola vez en el entorno).
"""

import hashlib
import os
import zipfile
from pathlib import Path

from mkdocs.config import Config
from mkdocs.plugins import BasePlugin


class DocumentationZipPlugin(BasePlugin):  # type: ignore[type-arg]
    """Plugin que genera ZIP de la documentación después del build."""

    config_options: dict = {}

    def on_post_build(self, config: Config) -> None:
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

            server_script = Path(__file__).parent.parent / "scripts" / "start-server.py"
            if server_script.exists():
                print(f"[ZIP] Incluyendo servidor local: {server_script.name}")
                zipf.write(server_script, arcname="start-server.py")

        sha256_hash = self._sha256(zip_path)
        sha256_file = zip_path.with_suffix(".zip.sha256")
        sha256_file.write_text(f"{sha256_hash}  {zip_path.name}\n", encoding="utf-8")

        file_size_mb = zip_path.stat().st_size / (1024 * 1024)
        print(f"[OK] ZIP creado: {zip_path.name} ({file_size_mb:.2f} MB)")
        print(f"[OK] SHA256: {sha256_hash}")
        print(f"[OK] Checksum guardado: {sha256_file.name}")

    def _sha256(self, file_path: Path) -> str:
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
