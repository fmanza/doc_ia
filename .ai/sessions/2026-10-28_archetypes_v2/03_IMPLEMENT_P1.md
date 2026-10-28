# IMPLEMENT — Entrega P1

## Level 1 — Norma y prompts

| Fichero | Cambio |
|---|---|
| `.github/DOCUMENTATION_STANDARD.md` | §3.1 Arq. 1 → 8 secciones (espejo del prompt) + nota de transición v1→v2; §3.2 Arq. 2 §2 "Modelo de Datos / Contratos" con autodoc condicional + delimitación con Arq. 12; §3.6 6C con Despliegue y escenarios de calidad; §3.10 mapeos CONTRATO→Arq. 12 §5 e INFRAESTRUCTURA→6C §3 › Despliegue; **nuevo §3.15** (Arq. 12); **nuevo §3.16** (evidencia y confianza); §4.1 nav con "Referencia del Sistema"; criterio de completitud ampliado |
| `.github/prompts/functional_doc.prompt.md` | Bloque plegable "Evidencia" final + reglas de marcas de confianza |
| `.github/prompts/technical_doc.prompt.md` | §2 renombrado a "Modelo de Datos / Contratos" (como norma y páginas reales); autodoc solo con mkdocstrings; delimitación con Arq. 12; bloque "Evidencia" |
| `.github/prompts/landing_doc.prompt.md` | 6C §3 → "Runtime" + "Despliegue" (arc42 §7); §4 + escenarios de calidad (arc42 §10) |
| `.github/prompts/reference_doc.prompt.md` | **Nuevo** — Arquetipo 12 |

## Level 2 — Orquestación, agentes y entry points

`document_project.prompt.md`, `.claude/commands/document-project.md`,
`documentation-generator.agent.md`, `documentation-reviewer.agent.md` (alcance 11 y 12),
`documentation_review.prompt.md`, `docs.instructions.md`, `SHARED_INSTRUCTIONS.md`,
`CLAUDE.md`, `copilot-instructions.md`, `AGENTS.md` (26 prompts), `INTEGRATION_MAP.md`,
`.ai/{glossary,standards,product,architecture}.md`.

## Level 3 — Dogfooding sobre doc_ia

| Fichero | Cambio |
|---|---|
| `docs/reference/index.md` | **Nuevo** — 5 CLIs, 5 claves de configuración, 12 códigos de salida, 4 eventos, 5 interfaces; bloque "Evidencia" de 18 filas |
| `docs/architecture.md` | §3 › Despliegue (diagrama + tabla de 4 entornos) y 5 escenarios de calidad |
| `docs/adr/ADR-002-arquetipos-con-evidencia.md` | **Nuevo** — MADR 4.0 Full |
| `docs/{functional,api}/archetypes.md`, `docs/examples/archetypes_usage.md`, `docs/functional/origin_types.md`, `docs/index.md`, `docs/ai-config/claude.md`, `docs/api/document_project.md`, `docs/guides/onboarding_dev.md` | Catálogo 11→12, mapeos, recuentos (33 páginas) |
| `mkdocs.yml` | Entradas "Referencia del Sistema" y ADR-002 |
| `CHANGELOG.md` | `[Unreleased]` Added + Changed |

## Desviaciones respecto al PLAN

- **Arq. 2 §2**: el PLAN decía "norma = prompt" (renombrar a "API Reference"). Las 6 páginas
  `docs/api/` y la norma usaban "Modelo de Datos / Contratos" y el prompt pedía autodoc `:::`
  sin mkdocstrings en `mkdocs.yml` (se renderizaría como texto). Se alineó **el prompt con la
  norma** y el autodoc pasó a condicional.
- **Arq. 1**: las 7 páginas `docs/functional/` siguen la estructura v1 (5 secciones), no las 8
  del prompt. La norma se alinea con el prompt (más información) y la migración de las páginas
  pasa a P2, que ya las reescribe.
