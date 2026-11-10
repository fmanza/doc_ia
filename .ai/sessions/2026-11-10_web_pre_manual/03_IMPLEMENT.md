# IMPLEMENT — Origen WEB desplegada y Arquetipo 15

Ejecuta el plan corregido de `02_AUDIT_PLAN.md`, en tres capas.

## Capa 1 — Tooling determinista

| Fichero | Cambio |
|---|---|
| `scripts/web_captures.py` (nuevo) | `publish` (copia a `docs/assets/manual/<origen>/` solo las capturas indicadas y registra en `.ai/captures.json` huella, entorno, versión y rol; valida todo antes de copiar; rechaza URLs y rutas fuera del origen) y `check` (`sin_registrar`, `modificada`, `falta`, `rota`, `sin_alt`, `huerfana`, `url`). Sin red. Exit 0/1/2 |
| `tests/test_web_captures.py` (nuevo) | 10 funciones de test, 19 casos (tras AUDIT_CODE), sin red ni navegador |

**Desviación respecto al plan corregido (H7)**: el plan preveía solo `check`. Se añade
`publish` porque `check` necesita un registro de capturas revisadas contra el que comparar, y
publicar a través de la herramienta es lo que impide que una imagen sin revisar entre sin
avisar. El resto del plan (adquisición y versiones) se resuelve con `snapshot_sources.py`, y el
`drift` con `doc_trace.py`, sin código nuevo.

## Capa 2 — Metodología

| Fichero | Cambio |
|---|---|
| `.github/DOCUMENTATION_STANDARD.md` | §2.3 (prompt), §3.10 (origen WEB en `UI/PANTALLAS`, mapeo, excepción a «MATERIAL no genera páginas»), §3.16 (Evidencia obligatoria también en el Arq. 15), **§3.20 Arquetipo 15**, §4.3 |
| `.github/prompts/user_manual_doc.prompt.md` (nuevo) | Portada + página por área con secciones fijas, Evidencia, `COB-WEB` y sin URL |
| `.github/prompts/document_project.prompt.md` | Opción `WEB`, **§ Origen WEB** (requisitos previos, plan de capturas, modos `capturas`/`navegador`, solo lectura, revisión, `publish`, contraste, `check`, incremental), forma de origen en la Fase 0-pre, Fase 0a, **Fase 3c**, Fase 6, prioridad 5 «Lo desplegado (BD, WEB)», INVENTARIO y CIERRE «Capturas» |
| `.claude/commands/document-project.md` | Input `WEB`, política (solo lectura, revisión, `check`), tipo `UI/PANTALLAS`, generación, casos límite y referencias |
| `.github/agents/documentation-generator.agent.md` | Prompt, mapeo, inventario y **§7 Manual de funcionamiento** |
| `.github/instructions/docs.instructions.md` | `docs/manual/` → Arq. 15 y prompt `user_manual_doc` |
| `.github/kit/MANIFEST.txt` | `user_manual_doc.prompt.md` y `scripts/web_captures.py` |
| `CLAUDE.md`, `.github/SHARED_INSTRUCTIONS.md` | Tabla de arquetipos (15), Evidencia, comandos de `web_captures.py` |
| `.claude/EDGE_CASES.md` | Caso «Origen WEB: aplicación desplegada en PRE» |
| `docs/adr/ADR-005-origen-web-desplegada.md` (nuevo) | Decisión MADR 4.0 con alternativas |
| `tests/test_docs_conformance.py` | 4 tests: registro del Arq. 15, estructura del prompt, reglas del origen WEB y ausencia de `docs/manual/` en doc_ia |

## Capa 3 — Documentación propia (dogfooding)

- Nuevas: `docs/functional/web_captures.md` (AC-01 – AC-08, 8/8), `docs/api/web_captures.md`,
  `docs/examples/web_captures_usage.{md,py}`.
- Actualizadas: arquetipos (funcional AC-17, técnica), mapa funcional (151/176), tipos de
  origen, `document_project` (funcional y técnica), referencia del sistema (CLI, códigos,
  interfaces), `mkdocs.yml` (4 entradas, sin pestañas nuevas), `llms.txt`, `CHANGELOG.md`
  `[Unreleased]`.
- Sellado: `stamp` de las páginas nuevas y las afectadas; las marcadas por `drift` por cambios
  añadidos (nav, MANIFEST, prompt) se revisaron y se volvieron a sellar.

## Verificación

| Comprobación | Resultado |
|---|---|
| `python -m pytest` | 485 passed |
| `ruff check` + `ruff format --check` + `mypy scripts` | Sin errores |
| `python -m mkdocs build --strict` | Sin avisos |
| `doc_trace.py drift` / `matrix` / `decisions` / `llms` | Sin drift · 0 tests inexistentes · 0 hallazgos · 65 páginas |
| `python docs/examples/web_captures_usage.py` | Salida igual a la documentada |

## Decisión tomada sin preguntar

- **Manual único con el rol indicado en cada tarea**: un manual por rol solo si los roles no
  comparten pantallas (§3.20). Es la opción recomendada en el AUDIT_PLAN; se revisará con los
  roles reales de UFV.
