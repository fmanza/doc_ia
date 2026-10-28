# PLAN — Arquetipos v2 (máxima información funcional y técnica)

## Inputs (derivados del análisis previo)

| Campo | Valor |
|---|---|
| Objetivo | Ampliar los arquetipos para extraer la máxima información funcional y técnica de un repositorio: vistas globales, referencia consultable y trazabilidad con evidencia |
| Módulos | Norma, prompts, agentes, entry points, docs dogfooding, `mkdocs.yml`; en P3 `scripts/` + `tests/` |
| API pública | P1/P2: ninguna Python (contrato = secciones de arquetipos). P3: un script nuevo con CLI |
| Contrato de entrada | Origen(es) CÓDIGO + MATERIAL opcional (CONTRATO, INFRAESTRUCTURA, ESPECIFICACIÓN…) |
| Contrato de salida | Páginas con secciones fijas, evidencia citada, enlaces válidos con `mkdocs build --strict`, salida determinista |
| Reglas de negocio | No inventar; secciones nuevas condicionales con "No aplica"; numeración actual preservada |
| Restricciones técnicas | Sin APIs IA, sin dependencias nuevas (PyYAML ya viene con mkdocs), mypy strict + ruff, tests sin red |
| Formatos | Markdown, frontmatter YAML, Mermaid, `llms.txt` |

## Objetivo

Ejecutar la ampliación en **tres entregas independientes** (P1 → P2 → P3), cada una con su
sesión y commit, validando cada una con dogfooding sobre doc_ia antes de la siguiente.
Simplificaciones S1–S4 del AUDIT_PLAN **aplicadas** a este plan.

## Entregas

### P1 — Alineación y base (esta sesión)
1. **Norma = prompts**: Arq. 1 pasa a las 8 secciones del prompt; Arq. 2 §2 pasa a
   "API Reference" (Autodoc · API pública · Contratos de entrada/salida/errores).
2. **§3.16 Evidencia y confianza** (transversal): cita `ruta::símbolo` (fallback `ruta:línea`)
   en código inline, nunca como enlace; leyenda ✅ ⚠️ 🔍 ❌ (la del Arq. 8) generalizada.
3. **§3.15 Arquetipo 12 — Referencia del sistema** (`docs/reference/`, Diátaxis *Reference*):
   §1 Configuración · §2 CLI y comandos · §3 Errores y códigos de salida · §4 Eventos y
   mensajes · §5 Interfaces publicadas. Prompt nuevo `reference_doc.prompt.md`.
   Delimitación con Arq. 2: Arq. 2 = API interna de un módulo; Arq. 12 = superficie que ve el
   usuario u operador.
4. **6C**: §3 se divide en "Runtime" y "Despliegue" (condicional, arc42 §7); §4 añade 3–5
   escenarios de calidad (arc42 §10). `INFRAESTRUCTURA` → 6C §3 › Despliegue;
   `CONTRATO` → Arq. 2 §1–§2 y Arq. 12 §5.
5. **Dogfooding**: `docs/reference/` de doc_ia (CLI de los scripts, configuración, códigos de
   salida), vista de despliegue en `docs/architecture.md`, ADR-002, CHANGELOG `[Unreleased]`.

### P2 — Funcional global y trazabilidad
1. Arq. 1 §2: tabla `Rol | Puede | No puede` (condicional).
2. Arq. 1 §7: columna `Test` (`tests/x.py::test_y` o `Sin test`).
3. Arq. 2 §6 nuevo "Verificación y tests" (al final, preserva §5↔§5).
4. **S2** — Mapa funcional como variante índice del Arq. 1 (`docs/functional/index.md`):
   `Capacidad → Módulo → AC → Tests`, recorridos transversales, glosario global.
5. **S1** — Modelo de datos como Arq. 12 §6 "Datos" (condicional): `erDiagram` global +
   diccionario `Entidad · Campo · Tipo · Restricción · Sensibilidad · Evidencia` +
   `stateDiagram-v2` de ciclos de vida.

### P3 — Tooling determinista (S4: un único script)
1. Frontmatter de trazabilidad por página: `arquetipo`, `fuentes` (ruta → sha256[:12]), `revisado`.
2. `scripts/doc_trace.py` con subcomandos `drift`, `matrix` (AC-xx ↔ tests) y `llms`
   (`docs/llms.txt` desde `nav`). Fuera del hook PostToolUse; manual o CI.
3. `tests/test_doc_trace.py` + páginas `docs/{functional,api,examples}/doc_trace.md`.

## Rutas afectadas

**Transversales**: `.github/DOCUMENTATION_STANDARD.md`, `.github/agents/documentation-{generator,reviewer}.agent.md`,
`.github/prompts/documentation_review.prompt.md`, `.github/instructions/docs.instructions.md`,
`.github/SHARED_INSTRUCTIONS.md`, `.github/prompts/document_project.prompt.md`,
`.claude/commands/document-project.md`, entry points (`CLAUDE.md`, `GEMINI.md`,
`.github/copilot-instructions.md`, `.cursorrules`, `.github/AGENTS.md`, `.github/INTEGRATION_MAP.md`),
`.ai/{glossary,standards,product}.md`, `docs/{functional,api}/archetypes.md`,
`docs/examples/archetypes_usage.md`, `docs/functional/origin_types.md`, `mkdocs.yml`, `CHANGELOG.md`.

| Entrega | Rutas específicas |
|---|---|
| P1 | `functional_doc`, `technical_doc`, `landing_doc`, **nuevo** `reference_doc.prompt.md`, **nuevo** `docs/reference/`, `docs/architecture.md`, **nuevo** `docs/adr/ADR-002-*.md` |
| P2 | `functional_doc`, `technical_doc`, `reference_doc`, **nuevo** `docs/functional/index.md`, páginas funcionales (7) y técnicas (6) de doc_ia |
| P3 | **nuevos** `scripts/doc_trace.py`, `tests/test_doc_trace.py`, `docs/{functional,api,examples}/doc_trace.md`; paso opcional en `.github/workflows/` |

## Tipos necesarios (P3)

```python
@dataclass(frozen=True)
class PageMeta:
    page: Path
    archetype: str
    sources: dict[str, str]   # ruta relativa → sha256[:12]

@dataclass(frozen=True)
class DriftFinding:
    page: Path
    source: str
    status: Literal["stale", "missing", "outside_repo"]

def read_page_meta(page: Path) -> PageMeta | None: ...
def check_drift(docs_dir: Path, repo_root: Path) -> list[DriftFinding]: ...   # orden estable
def build_llms_txt(mkdocs_yml: Path, site_url: str | None) -> str: ...
def main(argv: list[str] | None = None) -> int: ...   # 0 OK · 1 drift · 2 error de uso
```

## Riesgos (detalle en 02_AUDIT_PLAN.md)
- Funcional: exceso de "No aplica"; citas por línea frágiles.
- Técnico: sincronización manual de ~25 ficheros.
- Seguridad: rutas del frontmatter fuera del repo; valores sensibles en citas.
