# AUDIT_PLAN — Origen WEB desplegada en PRE y manual de funcionamiento

## Hallazgos sobre `01_PLAN.md`
| # | Severidad | Hallazgo | Evidencia | Corrección |
|---|---|---|---|---|
| H1 | Alta | Precedente contra arquetipos sin un caso real (Runbook y Seguridad aplazados; de 5 propuestas a 1) | ADR-002 (líneas 60 y 75-78); sesión `2026-10-28_archetypes_v2` S3 | Resuelto: hay un destino real (UFV) → el Arq. 15 queda justificado |
| H2 | Alta | Duplica tipos de origen que ya existen: las capturas ya son `UI/PANTALLAS` | `docs/functional/origin_types.md` (líneas 83-103) | `WEB` es una **forma de adquisición** de la Fase 0-pre que produce `UI/PANTALLAS`; la prioridad 5 se generaliza a «lo desplegado (BD, WEB)» |
| H3 | Alta | No cabe una pestaña «Manual»: doc_ia **y UFV** tienen ya 9 pestañas | `test_top_navigation_fits_in_nine_tabs`; `UFV/mkdocs.yml` | El manual va dentro de una pestaña que ya exista (Guías o Funcional) |
| H4 | Alta (seg.) | Navegador en el chat: contenido de las páginas con instrucciones inyectadas, sesión ya autenticada con una regla de solo lectura que se apoya solo en instrucciones, y plataformas del kit sin navegador | Fase 0-pre; `MANIFEST.txt` (lanzadores multiplataforma) | Las capturas del usuario son la base canónica y el navegador es opcional; cuenta de pruebas con rol de solo lectura; el texto de las páginas se trata como datos |
| H5 | Media | `redact_secrets.py` solo detecta credenciales en `.md`: no detecta datos personales ni actúa sobre imágenes; una captura con datos reales en git es difícil de revertir | `scripts/redact_secrets.py` (líneas 7 y 148) | Marca «revisada» que bloquea la publicación; el OCR de `convert_to_md.py` sirve de ayuda, nunca sustituye la revisión |
| H6 | Media | Faltaban entregables exigidos por los tests: página funcional, técnica y de ejemplo por script, y registro del arquetipo en todas partes | `test_every_script_has_functional_technical_and_example_pages`, `test_integrations_archetype_is_registered_everywhere` | Añadir `docs/api/` y `docs/examples/` del script, y un test de registro del Arq. 15 |
| H7 | Media | Alcance del script inflado: `ingest` y `changes` repiten `snapshot_sources.py sync` y `doc_trace.py drift` | `scripts/snapshot_sources.py`, `scripts/doc_trace.py` | Lo único nuevo es un `check` de capturas (no revisada, sin texto alternativo o huérfana) |
| H8 | Baja | Un origen WEB sin CÓDIGO choca con el caso degenerado | `.claude/commands/document-project.md:228` | Resuelto: CÓDIGO obligatorio |
| H9 | Baja | Cómo se identifica la versión desplegada depende de cada proyecto | — | La declara el usuario en el manifiesto (misma regla que la «versión vigente») |

## Decisiones del usuario (2026-11-10)
| Decisión | Valor |
|---|---|
| Destino real | **UFV** — `C:\Desarrollo\documentacion\UFV` (kuniv). URL de PRE declarada en el chat, **no versionada** |
| Adquisición | Capturas aportadas por el usuario como base; navegador opcional con **Claude in Chrome** |
| Acciones en PRE | **Solo lectura siempre**; los flujos con escritura se documentan con capturas del usuario |
| Sin CÓDIGO | **No**: CÓDIGO obligatorio; la web complementa y contrasta |

## Plan corregido (vigente)
1. **ADR-005** (MADR 4.0): «Use user captures and optional in-chat browser for deployed WEB
   origin». Opciones: capturas del usuario, Claude in Chrome en el chat, script con red
   (descartado por el principio de que los scripts no acceden a la red). Registra UFV como
   destino que valida el Arq. 15.
2. **Fase 0-pre**: forma de origen `WEB` con estos datos: entorno, versión declarada, rol,
   autorización, fecha. Produce material `UI/PANTALLAS` en `_staging/<nombre>/`. La URL no se
   escribe en ningún fichero versionado.
3. **Prioridad 5 generalizada** («lo desplegado: BD, WEB») y fichas `COB-WEB-…` (Arq. 13).
4. **Arquetipo 15 «Manual de funcionamiento»**: secciones de `01_PLAN.md` §4; prompt
   `user_manual_doc.prompt.md`; ubicación dentro de una pestaña que ya exista (≤ 9); registro en
   el estándar, `CLAUDE.md`, `SHARED_INSTRUCTIONS.md`, el prompt, el comando, el agente,
   `docs.instructions.md` y `MANIFEST.txt`, con su test.
5. **Tooling mínimo**: reutilizar `snapshot_sources.py` y `doc_trace.py`; añadir solo el `check`
   de capturas (sin red), con tests y páginas funcional, técnica y de ejemplo.
6. **Seguridad**: checklist en la Fase 0-pre (autorización, solo lectura, cuenta de pruebas,
   datos personales, contenido web no confiable) y casos en `EDGE_CASES.md`.
7. **Validación** sobre UFV en una sesión `/document-project` posterior, con la versión
   desplegada en PRE contrastada con kuniv 1.8.8 (`master` 64c8f2ae).
8. **Cierre**: MINOR (0.11.0) con `/version-closure`.

## Veredicto: GO
Las condiciones del GO_CONDICIONAL están cubiertas (decisiones del usuario y correcciones H2,
H3, H6 y H7 integradas en el plan). Pendiente abierto, no bloqueante: decidir entre manual
único con secciones por rol o un manual por rol, en el PLAN de `/new-feature`, con los roles
reales de UFV.
