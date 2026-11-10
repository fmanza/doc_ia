# TRACEABILITY

## Session metadata
- id: 2026-11-10
- fecha: 2026-11-10
- rama: develop
- skill: new_feature
- fase: PLAN + AUDIT_PLAN + IMPLEMENT + AUDIT_CODE + VERSION

## Prompt issued
1. «Analizar la posibilidad de incluir la versión desplegada en WEB en el entorno de PRE como
   opcional, para realizar un documento tipo manual de su funcionamiento, requisitos que se
   tienen que tener en cuenta. Solo análisis y PLAN. No se implementa nada.»
2. «AUDIT_PLAN y pregunta lo que necesites».
3. Destino UFV (`C:\Desarrollo\documentacion\UFV`) y URL de PRE (no versionada), navegador
   Claude in Chrome, guardar PLAN y AUDIT_PLAN como sesión.

## Context supplied
- Ver `00_CONTEXT_SNAPSHOT.md`.

## AI output summary
- PLAN emitido con el origen BD como patrón (`01_PLAN.md`).
- AUDIT_PLAN contra el repositorio: 9 hallazgos (H1-H9); precedente del ADR-002; tests de
  conformidad que afectan al plan; UFV con 9 pestañas confirma H3.
- 4 decisiones cerradas con el usuario; plan corregido y veredicto GO (`02_AUDIT_PLAN.md`).
- Sin cambios en código, prompts, estándar ni tests durante PLAN y AUDIT_PLAN; no se ha accedido
  a la web de PRE en ningún momento.
- IMPLEMENT (prompt «IMPLEMENT»), en tres capas, detalle en `03_IMPLEMENT.md`: `scripts/web_captures.py`
  (`publish` + `check`) y 13 casos de test; estándar §3.20 y origen WEB; prompt
  `user_manual_doc`; § Origen WEB y Fase 3c en el orquestador; comando, agente, instrucciones,
  kit, `CLAUDE.md`, `SHARED_INSTRUCTIONS`, `EDGE_CASES`, ADR-005; 4 tests de conformidad;
  documentación propia y sellado.
- Verificación: 485 tests en verde, ruff, mypy y `mkdocs build --strict` limpios; drift,
  matrix, decisions y llms sin hallazgos.
- AUDIT_CODE (prompt «Hazlo»): 4 hallazgos corregidos con tests (C1 nombre `..` sale de
  `_staging/`, C2 manifiesto mal formado, C3 bloques indentados y código inline, C4 `<img>` con
  comillas simples); veredicto APROBADO (`04_AUDIT_CODE.md`). 491 tests en verde.
- VERSION: commit `feat` y commit `release` 0.11.0 en `develop`; merge a `main`, push y tag
  quedan para confirmar con el usuario (pasos separados).

## Artefactos generados
| Artefacto | Ruta | Estado |
|---|---|---|
| REQUEST | `.ai/sessions/2026-11-10_web_pre_manual/00_REQUEST.md` | emitido |
| CONTEXT | `.ai/sessions/2026-11-10_web_pre_manual/00_CONTEXT_SNAPSHOT.md` | emitido |
| PLAN | `.ai/sessions/2026-11-10_web_pre_manual/01_PLAN.md` | emitido (superado por el plan corregido) |
| AUDIT_PLAN | `.ai/sessions/2026-11-10_web_pre_manual/02_AUDIT_PLAN.md` | GO |
| IMPLEMENT | `.ai/sessions/2026-11-10_web_pre_manual/03_IMPLEMENT.md` | completado |
| Script | `scripts/web_captures.py`, `tests/test_web_captures.py` | completado |
| Arquetipo 15 | `.github/DOCUMENTATION_STANDARD.md` §3.20, `.github/prompts/user_manual_doc.prompt.md` | completado |
| ADR | `docs/adr/ADR-005-origen-web-desplegada.md` | ACEPTADO |
| AUDIT_CODE | `.ai/sessions/2026-11-10_web_pre_manual/04_AUDIT_CODE.md` | APROBADO |

## Directrices para Futuras IAs
- **[origen WEB]**: `WEB` es una forma de adquisición de la Fase 0-pre que produce `UI/PANTALLAS`, no un tipo de origen nuevo.
- **[origen WEB]**: los scripts nunca navegan; la navegación (Claude in Chrome) ocurre en el chat y es opcional; la base son las capturas del usuario.
- **[PRE]**: solo lectura siempre; la URL de PRE nunca se escribe en ficheros versionados.
- **[nav]**: UFV y doc_ia tienen 9 pestañas: el manual va dentro de una pestaña que ya exista.
- **[arquetipos]**: el Arq. 15 se justifica por un destino real (UFV), según el criterio del ADR-002.
- **[web_captures]**: `publish` es la única vía de entrada a `docs/assets/manual/`; `check` compara la huella con `.ai/captures.json`, así que cualquier copia a mano aparece como `sin_registrar`.
- **[mapa funcional]**: las páginas funcionales de doc_ia no llevan «Actores y permisos» (el Mapa Funcional lo afirma en su Evidencia).

## Veredicto final
Veredicto: CLOSED
Pendientes al cierre:
- Merge `develop` → `main`, push y tag `v0.11.0` (confirmar con el usuario).
- Hotfix propuesto: `snapshot_sources.py` admite `.`/`..` como nombre de origen.
- Validar con UFV en una sesión `/document-project` con la opción `WEB`.
