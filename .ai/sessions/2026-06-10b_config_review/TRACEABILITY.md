# TRACEABILITY

## Session metadata
- id: 2026-06-10b
- fecha: 2026-06-10
- rama: main
- skill: config_review (auditoría post-bootstrap)
- fase: ANÁLISIS + AUDIT + REMEDIACIÓN + VERSION

## Prompt issued
"Auditoría post-bootstrap con Config Reviewer (config_review.prompt.md) sobre la
configuración IA instalada en a8ebf2c"

## Context supplied
- Configuración IA completa del destino (commit a8ebf2c)
- Origen util_bbdd (solo lectura) como referencia de contraste
- `.github/prompts/config_review.prompt.md` + `.github/agents/config-reviewer.agent.md`

## Hallazgos

| ID | Severidad | Hallazgo | Estado |
|---|---|---|---|
| F1 | CRÍTICO | `config-reviewer.agent.md` corrupto: todas las "d" minúsculas sustituidas por "o" (48 líneas afectadas). Origen sano → corrupción introducida al escribir la copia en el bootstrap. | CORREGIDO — restaurado desde origen + adaptaciones doc_ia |
| F2 | ALTO | `.github/instructions/docs.instructions.md` no copiado en el bootstrap pero referenciado 7 veces (DOCUMENTATION_STANDARD ×4, documentation-generator.agent, technical_doc.prompt, config_review.prompt). Referencias rotas. | CORREGIDO — creado adaptado a doc_ia (solo reglas operativas; arquetipos delegados a DOCUMENTATION_STANDARD.md por DRY) |
| F3 | BAJO | `/config-review` citado como slash command en el agente y en DOCUMENTATION_STANDARD:624, pero no existe en `.claude/commands/` (tampoco en origen; AGENTS.md ya documenta que no tiene slash command). | MITIGADO — sección Invocación del agente restaurado reapuntada al prompt; resto heredado del origen, sin cambio |
| F4 | BAJO | Menciones residuales de dominio util_bbdd en DOCUMENTATION_STANDARD.md §7 ("módulos en src/", COMPATIBILITY.md) — ambiguas porque el estándar también se aplica a proyectos origen externos con src/. | ABIERTO — revisar en el dogfooding de docs/ |

## AI output summary
- Verificación de integridad textual: grep de patrones de corrupción (d→o) sobre todo el
  repo → solo `config-reviewer.agent.md` afectado; tras remediación, 0 ocurrencias.
- Verificación referencial: `docs.instructions.md` era la única referencia rota del set
  `instructions/` (architecture/introspection/render/tests.instructions del origen no se
  referencian en doc_ia — exclusión correcta del bootstrap).
- F1: restauración desde origen con adaptaciones: ejemplo de commit `doc_ia-config-review-vX.Y.Z`,
  invocación Claude Code vía prompt (sin slash command), criterio "multibase/OOP" → "tooling
  determinista, sin APIs de IA".
- F2: `docs.instructions.md` nuevo (~330 líneas): principios, delegación de arquetipos al
  estándar, agrupación nav por áreas (adaptada a doc_ia + proyectos origen), autodoc genérico,
  Mermaid (criterios + architecture-beta), flujo proyecto completo (8 arquetipos),
  --verify-tools/--verify-build, reglas Markdown críticas, snippets --8<-- (ejemplos planos
  en disco según decisión de doc_ia, sin subcarpetas del origen).
- Puertas tras remediación: mkdocs build --strict OK (ficheros .github/ no afectan build),
  greps de corrupción y referencias = 0.

## Veredicto final
Veredicto: APROBADO CON CONDICIONES (F4 abierto, severidad baja)
Pendientes al cierre:
- F4: limpiar menciones src/ y COMPATIBILITY.md en DOCUMENTATION_STANDARD.md §7 durante el dogfooding.
- Dogfooding de docs/ (pendiente heredado de la sesión 2026-06-10).
