"""Ejemplo: auditar la trazabilidad docs ↔ código con doc_trace desde código propio."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from doc_trace import (  # noqa: E402
    build_matrix,
    check_drift,
    collect_criteria,
    collect_test_ids,
)

findings = check_drift(ROOT / "docs", ROOT)
print(f"Fuentes desactualizadas: {len(findings)}")
for f in findings:
    print(f"  {f.status}: {f.page.relative_to(ROOT).as_posix()} <- {f.source}")

criteria = collect_criteria(ROOT / "docs" / "functional")
_, unknown = build_matrix(criteria, collect_test_ids(ROOT / "tests", ROOT), ROOT)
with_test = sum(1 for c in criteria if c.tests)
print(f"Criterios con test: {with_test}/{len(criteria)}")
print(f"Tests citados inexistentes: {len(unknown)}")
