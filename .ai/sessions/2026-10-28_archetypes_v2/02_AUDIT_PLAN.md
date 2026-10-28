# AUDIT_PLAN — Arquetipos v2

## Riesgos funcionales

| ID | Riesgo | Sev. | Mitigación |
|---|---|---|---|
| F1 | Citas `ruta:línea` caducan con cualquier edición | Alta | Por defecto `ruta::símbolo`; línea solo como fallback |
| F2 | Citas a código fuera de `docs/` rompen `mkdocs build --strict` si son enlaces | Alta | Citas en código inline, nunca enlaces Markdown (regla explícita en §3.16) |
| F3 | Runbook / Seguridad / Modelo de datos sin caso real en doc_ia → validación imposible | Alta | S1 + S3 |
| F4 | Exceso de "No aplica" en librerías pequeñas | Media | Activación por señales del INVENTARIO (como Arq. 8) |
| F5 | La columna `Test` invita a forzar mapeos | Media | `Sin test` es válido; el revisor marca ❌ un test referenciado inexistente |
| F6 | Solapamiento Arq. 12 ↔ Arq. 2 §2 | Media | Arq. 2 = API interna del módulo; Arq. 12 = superficie de usuario/operador |

## Riesgos técnicos

| ID | Riesgo | Mitigación |
|---|---|---|
| T1 | Desincronización entre ~25 ficheros (mismo problema que el origen de esta sesión) | Checklist cerrado por entrega + Documentation Reviewer + Config Reviewer al cierre |
| T2 | Insertar §4 en 6C renumera | Despliegue como subapartado de §3; Arq. 2 crece con §6 al final |
| T3 | Huellas hash se disparan con cambios triviales | Aceptado (determinista); documentar en `EDGE_CASES.md`; opción: normalizar espacios |
| T4 | `yaml.safe_load` falla con `!!python/name:` de `mkdocs.yml` | `SafeLoader` que ignore tags desconocidos; test dedicado |
| T5 | LSP/ISP: API síncrona y pequeña (3–4 funciones, dataclasses frozen) — riesgo bajo | Funciones separadas por subcomando; sin jerarquías de clases |
| T6 | Drift en el hook PostToolUse ralentiza cada edición | Fuera del hook; manual o CI |

## Riesgos de seguridad

| ID | Riesgo | Mitigación |
|---|---|---|
| S-1 | Rutas `fuentes` del frontmatter con `../` fuera del repo | `resolve()` + `is_relative_to(repo_root)`; si no, `outside_repo` sin leer |
| S-2 | Citas que copian valores sensibles (secretos, URLs internas) | Citar ubicación, no contenido; Arq. 12 §1 documenta nombre/tipo/default, nunca el valor de un secreto |
| S-3 | `llms.txt` expone páginas internas | Solo entradas del `nav` (ya publicadas) |

## Simplificaciones (aceptadas e incorporadas al PLAN)

- **S1** — Modelo de datos (13) → Arq. 12 §6 "Datos" (condicional).
- **S2** — Mapa funcional (14) → variante índice del Arq. 1.
- **S3** — Runbook (15) y Seguridad (16) aplazados hasta un destino real; entretanto
  Seguridad = subapartado de 6C §4 y Runbook = how-to 3a. Registrado en ADR-002.
- **S4** — Un único script `scripts/doc_trace.py` con subcomandos.

Resultado: de 5 arquetipos nuevos a **1** (Arq. 12); de 2 scripts a **1**.

## Veredicto: GO_CONDICIONAL

| Entrega | Veredicto | Condiciones |
|---|---|---|
| P1 | GO | (a) ADR-002 MADR 4.0; (b) citas por símbolo y en código inline (F1, F2); (c) delimitación Arq. 12 ↔ Arq. 2 en la norma (F6); (d) `mkdocs build --strict` en verde |
| P2 | GO tras cierre de P1 | S1 + S2; dogfooding sobre las 13 páginas funcionales/técnicas con `Sin test` donde aplique |
| P3 | GO_CONDICIONAL | S4; tests de T4 y S-1; fuera del hook; tests sin red ni git; mypy strict + ruff |
| Arq. 15 / 16 | NO_GO temporal | S3 |

Versionado: cada entrega es MINOR (`feat`), sin breaking (sin renumeración; secciones nuevas
condicionales o al final).
