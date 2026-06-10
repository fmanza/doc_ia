# AUDIT_PLAN — 2026-06-10l: Actualizar documentación IA

## Alcance

Validar el PLAN_DOC de la sesión `2026-06-10l` antes de iniciar la implementación.

---

## F1 — Corrección del inventario

| Verificación | Resultado |
|---|---|
| `functional/document_project.md` no menciona Fase 0a ni tipos de origen | ✅ Confirmado — §1 solo habla de 4 parámetros; §2 no tiene regla de clasificación; §3 flowchart va directo de VALIDACIÓN a INVENTARIO; §5 glosario sin términos multi-origen |
| `examples/document_project_usage.md` solo tiene escenarios de origen único | ✅ Confirmado — 3 escenarios, todos con un único `Origen:` |
| `guides/claude_code_guide.md` no existe | ✅ Confirmado (glob sobre docs/guides/) |
| `api/document_project.md` ya incluye los parámetros multi-origen | ✅ Confirmado — tabla Contrato de Entrada tiene Tipo de cada origen y Estrategia |
| Páginas C restantes no necesitan cambios | ✅ Confirmado |

**Veredicto F1**: Inventario correcto. 2 páginas B y 1 página A identificadas con precisión.

---

## F2 — Corrección de las secciones afectadas en P1

| Sección | ¿El cambio es necesario? | Fuente verificada |
|---|---|---|
| §1 ampliar para multi-origen | Sí — actualmente solo describe origen único | `.claude/commands/document-project.md` §Inputs tiene Tipo y Estrategia |
| §2 nueva fila Clasificación de orígenes | Sí — es una regla de negocio real con impacto verificable | `.github/prompts/document_project.prompt.md` Fase 0a |
| §3 Mermaid con Fase 0a condicional | Sí — el flowchart actual es incompleto para multi-origen | `.github/agents/documentation-generator.agent.md` Paso 0a |
| §3 flujo alternativo multi-origen | Sí — "Orígenes heterogéneos" y "Estrategia" son flujos reales | Misma fuente |
| §4 AC-05, AC-06 | Sí — son criterios verificables derivados del código real | Caso degenerado "sin CÓDIGO" en agent + prompt |
| §5 nuevos términos | Sí — Tipo de origen, Estrategia, MATERIAL son términos del dominio | `.github/DOCUMENTATION_STANDARD.md` §3.10 |

**Veredicto F2**: Cambios en P1 correctos y verificables. No hay riesgo de inventar: todas las fuentes están en el repo.

---

## F3 — Corrección de las secciones afectadas en P2

| Sección | ¿El cambio es necesario? | Riesgo |
|---|---|---|
| §1 ampliar contexto | Sí — actualmente el ejemplo dice "proyecto Python existente" sin mencionar multi-origen | Bajo |
| §2 Escenario 4 | Sí — la feature multi-origen no tiene ningún ejemplo ejecutable hasta ahora | Bajo — basarse en los ejemplos del command file |
| §3 explicación Fase 0a | Sí — el §3 actual solo explica los 4 parámetros obligatorios | Bajo |
| §4 output CLASIFICACIÓN | Sí — ninguna fase actual muestra la tabla de clasificación de orígenes | Bajo — basarse en el "Ejemplo de salida esperada" del command file |

**Veredicto F3**: Cambios en P2 correctos. El Escenario 4 debe usar los ejemplos reales del command file (`mi_api` + `ley_39.pdf` + `mockups/`) para no inventar.

---

## F4 — Arquetipo correcto para P3

| Verificación | Resultado |
|---|---|
| `guides/claude_code_guide.md` → Arquetipo 3 (Guía de Usuario) | ✅ Correcto — responde "¿Cómo se usa doc_ia con Claude Code?" |
| El Arquetipo 3 no requiere enlace bidireccional con Arquetipo 2 | ✅ Correcto — el enlace bidireccional es solo entre Arg. 2 §5 y Arg. 4 §5 |
| Patrón del Arquetipo 3: 5 secciones (Objetivo, Requisitos, Pasos, Verificación, Variantes) | ✅ Confirmado en `DOCUMENTATION_STANDARD.md` §3.3 |
| Contenido no inventado: basarse en CLAUDE.md, codex_guide.md como referencia de formato | ✅ Fuentes en el repo |

**Veredicto F4**: Arquetipo y contenido correctos para P3.

---

## F5 — Dependencias y orden de ejecución

```
P1 → P2: P2 §5 enlaza a functional/document_project.md; los nuevos ACs de P1
         deben estar antes para que §3 del ejemplo los pueda referenciar correctamente.

P3: independiente de P1 y P2; puede ejecutarse en paralelo.

N1: después de P3 (el archivo debe existir antes de entrar en mkdocs.yml).
```

Riesgo de orden: ninguno si se respeta P1→P2→P3→N1.

---

## F6 — Impacto en build

| Escenario | Consecuencia | Mitigación |
|---|---|---|
| mkdocs.yml actualizado (N1) antes de crear P3 | `mkdocs build --strict` falla: página no encontrada | Crear P3 antes de N1 |
| Mermaid de §3 P1 con sintaxis incorrecta | Warning en build, diagrama no renderizado | Validar sintaxis: `flowchart TD` con nodo condicional; seguir el patrón de functional/bootstrap.md |
| §5 de P2 no actualizado con nuevos ejemplos | No rompe build, pero §5 queda inconsistente con el contenido | Actualizar §5 si se añade Escenario 4 que no esté ya referenciado |

**Veredicto F6**: Sin riesgos de build si se respeta el orden.

---

## F7 — Coherencia con `api/document_project.md` (C — vigente)

`api/document_project.md` ya documenta los parámetros multi-origen (`Tipo de cada origen`,
`Estrategia`, `Fase 0a` en el flowchart). Al actualizar el funcional y el ejemplo, se
mantiene la coherencia:

| Documento | Estado multi-origen |
|---|---|
| `.claude/commands/document-project.md` | ✅ Actualizado en sesión j |
| `.github/prompts/document_project.prompt.md` | ✅ Actualizado en sesión j |
| `api/document_project.md` | ✅ Creado en sesión k con multi-origen |
| `functional/document_project.md` | ❌ → P1 lo resuelve |
| `examples/document_project_usage.md` | ❌ → P2 lo resuelve |

---

## Veredicto final del AUDIT_PLAN

**GO** — El plan es correcto, completo y libre de riesgos no mitigados.

Condiciones de ejecución:
1. Leer `functional/document_project.md` completo antes de escribir cualquier sección (protocolo ACTUALIZAR).
2. Basar el Escenario 4 de P2 en los ejemplos del command file para no inventar.
3. Respetar el orden P1 → P2 → P3 → N1.
4. Verificar build estricto al final.
