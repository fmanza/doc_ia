# IMPLEMENT — Entrega P2

## Level 1 — Norma y prompts

| Fichero | Cambio |
|---|---|
| `.github/DOCUMENTATION_STANDARD.md` | Arq. 1 §2 subsección condicional "Actores y permisos"; §7 columna `Test`; **Variante 1-I — Mapa funcional**; Arq. 2 **§6 Verificación y Tests**; Arq. 12 **§6 Datos** (S1); §3.10 con numeración v2 del Arq. 1 |
| `.github/prompts/functional_doc.prompt.md` | Roles condicionales, columna `Test`, sección "Variante índice — Mapa funcional (1-I)" |
| `.github/prompts/technical_doc.prompt.md` | §6 Verificación y Tests; output esperado 6 secciones |
| `.github/prompts/reference_doc.prompt.md` | §6 Datos (erDiagram + diccionario con sensibilidad); señal de activación nueva |

## Level 2 — Orquestación

`documentation-generator.agent.md` (Fase 2: columna Test + Mapa 1-I; tabla MATERIAL v2),
`documentation-reviewer.agent.md` (tests inexistentes = Nivel 1; Mapa obligatorio con ≥2 páginas),
`document_project.prompt.md` (Fase 2 + numeración v2), `.claude/commands/document-project.md`.

## Level 3 — Dogfooding (3 forks en paralelo + hilo principal)

| Ámbito | Resultado |
|---|---|
| 7 páginas `docs/functional/` | Migradas a v2 (8 secciones) + columna `Test` + bloque Evidencia. 52 criterios; 15 con test (check_env 4/4, convert_to_md 11/12) |
| 6 páginas `docs/api/` | §6 Verificación y Tests + bloque Evidencia; hechos falsos corregidos (ver TRACEABILITY) |
| `docs/reference/index.md` | §6 Datos: frontmatter, manifiesto de chunks, `.sha256`, `CHECKSUMS.txt` |
| `docs/functional/index.md` | **Nuevo** Mapa Funcional: 7 capacidades, 2 recorridos, glosario global |
| `mkdocs.yml` | "Mapa Funcional" como primera entrada de Documentación Funcional |

## Verificación

- 25 tests citados en `docs/` → los 25 existen (`def test_` en `tests/`).
- `mkdocs build --strict` OK; ruff OK; pytest 76 OK; bloques Mermaid sin líneas partidas.
