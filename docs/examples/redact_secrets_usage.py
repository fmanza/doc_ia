"""Ejemplo: redactar credenciales de un documento convertido antes de copiarlo a _fuentes/.

Sin red y determinista: los valores son sintéticos y evidentes.
"""

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from redact_secrets import find_secrets, redact_tree  # noqa: E402

DOCUMENTO = """# Diseño técnico — Integraciones (ficticio)

| NOMBRE | VALOR | DESCRIPCIÓN |
|---|---|---|
| p1 | usuario_demo | Usuario de la llamada |
| p2 | -- | Password de la llamada |

**Ej.** https://idp.example/v1/token?grant_type=authorization_code&client_secret=Demo123Secret456Value

**Dirección de correo:** buzon@example.org
**Contraseña:** xxxxxx
"""

with tempfile.TemporaryDirectory() as tmp:
    md = Path(tmp) / "md" / "Diseno_Integraciones.md"  # salida de convert_to_md.py
    md.parent.mkdir()
    md.write_text(DOCUMENTO, encoding="utf-8")

    print("Antes:", find_secrets(md.read_text(encoding="utf-8")))
    for finding in redact_tree(md.parent):  # redacta en el sitio
        print(f"Redactado: {Path(finding.path).name}:{finding.line} · {finding.rule}")
    print("Después:", find_secrets(md.read_text(encoding="utf-8")))
    lines = md.read_text(encoding="utf-8").splitlines()
    print(next(line for line in lines if "client_secret" in line))
