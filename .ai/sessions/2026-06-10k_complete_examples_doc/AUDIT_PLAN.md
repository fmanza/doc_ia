# AUDIT_PLAN — 2026-06-10k: Completar documentación de Flujos IA

## Alcance

Validar el PLAN_DOC de la sesión `2026-06-10k` antes de iniciar la implementación.

---

## F1 — Corrección del inventario

| Verificación | Resultado |
|---|---|
| `docs/examples/` no tiene `archetypes_usage.md` | ✅ Confirmado (glob + revisión directa) |
| `docs/examples/` no tiene `bootstrap_usage.md` | ✅ Confirmado |
| `docs/api/` no tiene `document_project.md`, `archetypes.md`, `bootstrap.md` | ✅ Confirmado (solo `check_env.md` y `build_docs_zip.md`) |
| Las páginas de Tooling Determinista tienen los 3 arquetipos | ✅ Completas — fuera de alcance |
| `docs/functional/archetypes.md` y `bootstrap.md` tienen §5 Glosario (no §5 Ejemplos) | ✅ Son Arquetipo 1 — §5 = Glosario; correcto |

**Veredicto F1**: Inventario correcto. No hay falsos positivos ni falsos negativos.

---

## F2 — Corrección de arquetipos asignados

| Artefacto | Arquetipo asignado | Justificación | Riesgo |
|---|---|---|---|
| `archetypes_usage.md` | 4 — Ejemplos | Muestra cómo aplicar/seleccionar un arquetipo; audiencia: desarrolladores | Bajo |
| `bootstrap_usage.md` | 4 — Ejemplos | Muestra la invocación y el output del prompt de bootstrap; audiencia: desarrolladores | Bajo |
| `api/document_project.md` | 2 — Técnica | Describe contratos del slash command y del prompt file; no es script Python | Medio — ver F3 |
| `api/archetypes.md` | 2 — Técnica | Describe la arquitectura de los 8 arquetipos: estructura, reglas, prompts | Medio — ver F3 |
| `api/bootstrap.md` | 2 — Técnica | Describe el prompt de bootstrap y el agente Config Reviewer | Medio — ver F3 |

**Veredicto F2**: Arquetipos correctos. Los Flujos IA no tienen módulo Python pero sí
tienen "API" en forma de campos de entrada, fases y contratos de salida documentables en Arquetipo 2.

---

## F3 — Riesgo de inventar contenido

| Riesgo | Mitigación en el plan |
|---|---|
| Arquetipo 2 inventa firma o comportamiento del prompt | **Leer antes**: `.claude/commands/document-project.md`, `document_project.prompt.md`, `bootstrap_ai_config.prompt.md`, `documentation-generator.agent.md` — todo disponible en el repo |
| Arquetipo 4 inventa output de fases | Basarse en el output documentado en `functional/document_project.md` §3 y en la sesión `2026-06-10i` (ya verificado) |
| `archetypes_usage.md` inventa un arquetipo ficticio | Usar los 8 arquetipos reales de `DOCUMENTATION_STANDARD.md` §3; el ejemplo debe elegir un módulo real del repo |

**Veredicto F3**: Riesgos controlables. Las fuentes existen y son legibles. No hay dependency externa.

---

## F4 — Dependencias entre artefactos

```
E1 (archetypes_usage) ← A2 (api/archetypes) §5 depende de E1
E2 (bootstrap_usage)  ← A3 (api/bootstrap)  §5 depende de E2
E1, A1 existentes     ← A1 (api/document_project) §5 enlaza a examples/document_project_usage.md ✅ ya existe
```

**Riesgo de orden**: si A2 se crea antes que E1, §5 de A2 quedaría "Pendiente".
**Mitigación**: el plan fija el orden E1→E2→A1→A2→A3; no invertir.

---

## F5 — Impacto en build

| Escenario | Consecuencia | Mitigación |
|---|---|---|
| Se actualiza `mkdocs.yml` antes de crear los archivos | `mkdocs build --strict` falla con "página no encontrada" | Crear todos los archivos **antes** de N1+N2; hacer mkdocs update en un único paso al final |
| Un enlace relativo en §5 apunta a ruta incorrecta | Warning de link roto en build estricto | Usar rutas `../examples/` y `../functional/` consistentes con los ejemplos existentes |

**Veredicto F5**: Sin riesgos de build si se respeta el orden E→A→N.

---

## F6 — Cobertura post-plan

| Módulo | Arg. 1 | Arg. 2 | Arg. 4 | Estado post-plan |
|---|---|---|---|---|
| check_env | ✅ | ✅ | ✅ | Completo (sin cambios) |
| build_docs_zip | ✅ | ✅ | ✅ | Completo (sin cambios) |
| /document-project | ✅ | ✅ CREAR | ✅ | Completo |
| Arquetipos Formales | ✅ | ✅ CREAR | ✅ CREAR | Completo |
| Bootstrap IA | ✅ | ✅ CREAR | ✅ CREAR | Completo |

**Veredicto F6**: El plan cubre exactamente los gaps identificados. Nada fuera de alcance,
nada omitido.

---

## Veredicto final del AUDIT_PLAN

**GO** — El plan es correcto, completo y libre de riesgos no mitigados.

Condiciones de ejecución:
1. Leer los archivos de prompts y agentes antes de escribir cada Arquetipo 2.
2. Respetar el orden E1 → E2 → A1 → A2 → A3 → N1+N2.
3. Verificar build estricto al final antes de cerrar la sesión.
