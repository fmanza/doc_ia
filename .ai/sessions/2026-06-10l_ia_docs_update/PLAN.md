# PLAN — 2026-06-10l: Actualizar documentación IA (multi-origen + guía Claude Code)

## Inventario de partida

### Páginas IA — clasificación completa

| Página | Estado | Motivo |
|---|---|---|
| `functional/document_project.md` | **B — desactualizado** | Sesión j añadió Fase 0a (clasificación de orígenes: CÓDIGO/NORMATIVA/ESPECIFICACIÓN/UI/REFERENCIA), nuevos parámetros opcionales (Tipo de cada origen, Estrategia) y flujo multi-origen. Ninguna sección refleja estos cambios. |
| `examples/document_project_usage.md` | **B — desactualizado** | Los 3 escenarios actuales solo cubren origen único. Falta Escenario 4: múltiples orígenes heterogéneos (el caso introducido en sesión j). |
| `guides/claude_code_guide.md` | **A — sin doc** | DOCUMENTATION_STANDARD §3.9 lista esta guía como recomendada para proyectos de tipo "Tooling de documentación". Solo existe codex_guide.md; Claude Code es la plataforma primaria del producto. |
| `functional/archetypes.md` | C — vigente | Sin cambios desde sesión h |
| `functional/bootstrap.md` | C — vigente | Sin cambios desde sesión h |
| `api/document_project.md` | C — vigente | Creado en sesión k incluyendo ya los parámetros multi-origen |
| `api/archetypes.md` | C — vigente | Sin cambios |
| `api/bootstrap.md` | C — vigente | Sin cambios |
| `examples/archetypes_usage.md` | C — vigente | Creado en sesión k |
| `examples/bootstrap_usage.md` | C — vigente | Creado en sesión k |
| `guides/codex_guide.md` | C — vigente | Sin cambios |

---

## PLAN_DOC

### P1 — ACTUALIZAR `functional/document_project.md`

Secciones afectadas (solo estas; el resto se conserva verbatim):

| Sección | Cambio necesario |
|---|---|
| §1 Descripción General | Ampliar para mencionar que el origen puede ser único o múltiple, y que los orígenes pueden ser de naturaleza heterogénea (CÓDIGO, NORMATIVA, etc.) |
| §2 Reglas de Negocio | Añadir fila: "Clasificación de orígenes" — cuando hay ≥2 orígenes o el único no es CÓDIGO, se ejecuta Fase 0a antes del inventario y se requiere confirmación del usuario |
| §3 Flujo principal (Mermaid) | Añadir nodo Fase 0a entre VALIDACIÓN e INVENTARIO (condicional: solo con ≥2 orígenes o no-CÓDIGO) |
| §3 Flujos alternativos | Añadir: "Orígenes heterogéneos" y "Estrategia multi-CÓDIGO" |
| §4 Criterios de Aceptación | Añadir AC-05 (multi-origen heterogéneo) y AC-06 (todos los orígenes son MATERIAL → detención) |
| §5 Glosario | Añadir: Tipo de origen, Estrategia, MATERIAL, Fase 0a, Clasificación de orígenes |

### P2 — ACTUALIZAR `examples/document_project_usage.md`

Secciones afectadas:

| Sección | Cambio necesario |
|---|---|
| §1 Contexto del Ejemplo | Ampliar: mencionar que también cubre el escenario de múltiples orígenes heterogéneos |
| §2 Implementación de Referencia | Añadir Escenario 4: múltiples orígenes (proyecto Python + PDF normativa + carpeta de pantallas) con Tipo de cada origen explícito |
| §3 Explicación del Código | Añadir: qué hace Fase 0a, cuándo se activa, por qué la Estrategia nunca se autodetecta |
| §4 Ejecución y Pruebas | Añadir: output esperado de la fase CLASIFICACIÓN DE ORÍGENES para el Escenario 4 |

### P3 — CREAR `guides/claude_code_guide.md`

Arquetipo 3 completo (5 secciones). Contenido:
- §1 Objetivo: usar doc_ia con Claude Code; en qué se diferencia de otras plataformas
- §2 Requisitos Previos: Claude Code CLI o extensión VS Code, repo clonado
- §3 Pasos: instalar Claude Code, abrir el repo, usar slash commands (/document-project, /new-feature, etc.), configurar hooks PostToolUse
- §4 Verificación: `claude --version`, invocar `/document-project` con los 4 parámetros, build OK
- §5 Variantes y Solución de Problemas: CLAUDE.md no cargado, hooks no ejecutados, workspace con rutas incorrectas

### N1 — ACTUALIZAR `mkdocs.yml`

Añadir `guides/claude_code_guide.md` bajo "Herramientas IA" junto a codex_guide.md.

---

## Orden de ejecución

```
P1 → P2 → P3 → N1 → verify-build
```

P1 antes que P2: el funcional es la fuente de verdad que el ejemplo refleja; actualizar primero
la descripción y los ACs garantiza que §3 y §4 del ejemplo sean coherentes.

P3 puede ejecutarse en paralelo con P1+P2 (no tiene dependencias entre sí).

---

## Resultado esperado al cierre

| Página | Estado antes | Estado después |
|---|---|---|
| `functional/document_project.md` | B | C (actualizado) |
| `examples/document_project_usage.md` | B | C (actualizado) |
| `guides/claude_code_guide.md` | A | C (creado) |
| `mkdocs.yml` | — | +1 entrada guides/claude_code_guide.md |
