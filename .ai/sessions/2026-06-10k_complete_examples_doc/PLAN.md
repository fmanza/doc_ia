# PLAN — 2026-06-10k: Completar documentación de Flujos IA

## Inventario de partida

### Estado actual por sección del producto

| Módulo / Capacidad | Arquetipo 1 (Funcional) | Arquetipo 2 (Técnica) | Arquetipo 4 (Ejemplo) |
|---|---|---|---|
| `check_env` | ✅ `functional/check_env.md` | ✅ `api/check_env.md` | ✅ `examples/check_env_usage.md` |
| `build_docs_zip` | ✅ `functional/build_docs_zip.md` | ✅ `api/build_docs_zip.md` | ✅ `examples/build_docs_zip_offline.md` |
| `/document-project` | ✅ `functional/document_project.md` | ❌ FALTANTE | ✅ `examples/document_project_usage.md` |
| Arquetipos Formales | ✅ `functional/archetypes.md` | ❌ FALTANTE | ❌ FALTANTE |
| Bootstrap IA | ✅ `functional/bootstrap.md` | ❌ FALTANTE | ❌ FALTANTE |

**Conclusión**: Tooling Determinista completo. Flujos IA con 5 gaps (2 Arquetipo 4 + 3 Arquetipo 2).

---

## PLAN_DOC

### Acciones por prioridad

#### Prioridad 1 — Arquetipo 4 (Ejemplos)

| ID | Acción | Archivo | Basado en |
|---|---|---|---|
| E1 | CREAR | `docs/examples/archetypes_usage.md` | `functional/archetypes.md` + `DOCUMENTATION_STANDARD.md` §3 |
| E2 | CREAR | `docs/examples/bootstrap_usage.md` | `functional/bootstrap.md` + `.github/prompts/bootstrap_ai_config.prompt.md` |

**Por qué primero**: los Arquetipo 2 necesitan §5 con enlace a su ejemplo; si los ejemplos
no existen al escribir los técnicos, §5 quedaría con "Pendiente".

#### Prioridad 2 — Arquetipo 2 (Técnica/API)

| ID | Acción | Archivo | Fuentes a leer antes |
|---|---|---|---|
| A1 | CREAR | `docs/api/document_project.md` | `.claude/commands/document-project.md`, `.github/prompts/document_project.prompt.md` |
| A2 | CREAR | `docs/api/archetypes.md` | `.github/DOCUMENTATION_STANDARD.md` §3, prompts de arquetipos |
| A3 | CREAR | `docs/api/bootstrap.md` | `.github/prompts/bootstrap_ai_config.prompt.md`, `.github/agents/config-reviewer.agent.md` |

#### Prioridad 3 — Sincronización de navegación

| ID | Acción | Archivo | Detalle |
|---|---|---|---|
| N1 | ACTUALIZAR | `mkdocs.yml` | Añadir E1, E2 bajo "Flujos IA" en "Ejemplos" |
| N2 | ACTUALIZAR | `mkdocs.yml` | Nueva subsección "Flujos IA" bajo "Referencia Técnica" con A1, A2, A3 |

---

## Orden de ejecución

```
E1 → E2 → A1 → A2 → A3 → N1+N2 (en el mismo paso) → verify-build
```

Los ejemplos (E1, E2) van primero para que cuando se creen los técnicos (A1–A3) sus §5
puedan enlazar a los ejemplos ya existentes.

---

## Resultado esperado al cierre

| Sección mkdocs.yml | Entradas actuales | Entradas tras el plan |
|---|---|---|
| Ejemplos › Flujos IA | 1 (`document_project_usage`) | 3 (+`archetypes_usage`, +`bootstrap_usage`) |
| Referencia Técnica › Flujos IA | 0 | 3 (`document_project`, `archetypes`, `bootstrap`) |

Cobertura final: todos los módulos y capacidades del producto tendrán los 3 arquetipos
obligatorios (Funcional + Técnica + Ejemplo).
