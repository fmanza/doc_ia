"""Ejemplo: instantánea versionada de un manual con snapshot_sources (sin red, determinista)."""

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from snapshot_sources import (  # noqa: E402
    MANIFEST,
    declare,
    format_change,
    read_manifest,
    sync_source,
    write_manifest,
)

with tempfile.TemporaryDirectory() as tmp:
    share = Path(tmp) / "Modulos"  # simula la carpeta compartida de solo lectura
    dest = Path(tmp) / "mi_modulo_docs"  # raíz del destino
    share.mkdir()
    for version in ("1.2.9", "1.2.50"):
        (share / f"Manual_Modulo_v{version}.docx").write_bytes(version.encode())
    (share / "Manual_Modulo_v1.2.50.pdf").write_bytes(b"pdf")  # otro formato: no encaja

    manifest = dest / MANIFEST
    data = read_manifest(manifest)
    declare(data, "manual", str(share / "Manual_Modulo_v{ver}.docx"), ())

    def sync(day: str) -> None:
        changes = sync_source(dest, "manual", data["fuentes"]["manual"], day)
        if changes:
            write_manifest(manifest, data)
        print(f"{day}: {len(changes)} cambio(s)")
        for change in changes:
            print(format_change("manual", change))

    sync("2026-11-02")
    sync("2026-11-03")  # sin cambios: idempotente

    # Conversión previa y versión nueva: la ruta estable no cambia y el .md se invalida.
    converted = dest / "_staging" / "manual" / "md" / "Manual_Modulo.md"
    converted.parent.mkdir(parents=True)
    converted.write_text("conversión de la v1.2.50", encoding="utf-8")
    (share / "Manual_Modulo_v1.2.51.docx").write_bytes(b"1.2.51")
    sync("2026-11-05")

    staged = sorted(p.relative_to(dest).as_posix() for p in dest.rglob("*") if p.is_file())
    print("Ficheros en el destino:", ", ".join(staged))
    for event in read_manifest(manifest)["fuentes"]["manual"]["historial"]:
        previous = event.get("version_anterior", "—")
        print(f"  {event['fecha']} {event['cambio']}: v{event['version']} (antes {previous})")
