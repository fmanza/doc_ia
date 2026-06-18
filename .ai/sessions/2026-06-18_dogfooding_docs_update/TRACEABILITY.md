# TRACEABILITY — Sesión 2026-06-18

## Resumen cronológico

1. **VALIDACIÓN** — 4 parámetros obligatorios verificados (origen, destino, generador, idioma)
2. **Fase 0b** — Sincronización visual OK: 4 assets en disco, mkdocs.yml sin `navigation.sections`, .gitignore completo
3. **INVENTARIO** — 3 agentes en paralelo: (1) ficheros fuente, (2) documentación existente, (3) instrucciones IA
4. **PLAN_DOC** — 11 páginas B (ACTUALIZAR), 0 A (CREAR), 20+ C (OMITIR)
5. **GENERACIÓN** — Actualización de 5 ficheros `.ai/*.md` + 6 páginas `docs/`
6. **SYNC NAV** — Sin cambios (todas las actualizaciones in-place)
7. **BUILD** — `python -m mkdocs build --strict` OK (0 warnings, 3.13s)
8. **DOWNLOADS** — Tabla actualizada con fecha 2026-06-18
9. **CIERRE** — Artefactos de sesión creados

## Artefactos generados

| Artefacto | Ruta | Estado |
|---|---|---|
| `.ai/product.md` | `.ai/product.md` | ACTUALIZADO — capacidades 7→11 arquetipos, conteos, sitio 31pp, convert_to_md, mkdocs_hooks |
| `.ai/architecture.md` | `.ai/architecture.md` | ACTUALIZADO — árbol completo, hooks/, mkdocs_hooks.py, CHANGELOG/CONTRIBUTING, flujo completo |
| `.ai/glossary.md` | `.ai/glossary.md` | ACTUALIZADO — 30+ términos (antes 15), tipos de origen, Fase 0a/0b, md/, MADR 4.0 |
| `.ai/runtime.md` | `.ai/runtime.md` | ACTUALIZADO — convert_to_md, start-server, hooks MkDocs + PostToolUse detallados |
| `.ai/standards.md` | `.ai/standards.md` | ACTUALIZADO — ruff incluye hooks/, convención md/, 11 arquetipos, cierre de sesión |
| `docs/architecture.md` | `docs/architecture.md` | ACTUALIZADO §2 §3 — mapa módulos completo, flujo con Fases 0a/0b/cierre |
| `docs/ai-config/claude.md` | `docs/ai-config/claude.md` | ACTUALIZADO §1 §5 — fecha, 4 hooks PostToolUse + 2 hooks MkDocs |
| `docs/functional/document_project.md` | `docs/functional/document_project.md` | ACTUALIZADO §2 §3 §5 — 3 reglas nuevas (Fase 0b, md/, .ai/*.md), flujo con Fase 0b, 4 términos en glosario |
| `docs/api/document_project.md` | `docs/api/document_project.md` | ACTUALIZADO §1 §4 §5 — flujo con Fase 0b/cierre, 8→11 arquetipos, 3→6 escenarios |
| `docs/guides/onboarding_dev.md` | `docs/guides/onboarding_dev.md` | ACTUALIZADO §6 §7 §8 §10 — code map completo, ruff con hooks/, convert_to_md |
| `docs/downloads.md` | `docs/downloads.md` | ACTUALIZADO — fecha 2026-06-12→2026-06-18 |

## Directrices para Futuras IAs

- **[conteos]**: A 2026-06-18, doc_ia tiene 25 prompts, 12 agentes, 9 slash commands, 31 páginas docs/, 4 scripts, 1 hook, 1 mkdocs_hooks.py. Verificar con `ls .github/prompts/*.prompt.md | wc -l` antes de actualizar `.ai/product.md`.
- **[.ai/*.md]**: Los 5 ficheros de contexto deben actualizarse en cada sesión de dogfooding si los conteos o la estructura han cambiado. Fecha de referencia: header del fichero.
- **[ruff scope]**: El scope de ruff es `scripts tests hooks` (3 directorios). Si se lee en documentación solo `scripts tests`, es un defecto de sincronización.
- **[Fase 0b]**: Toda sesión `/document-project` debe verificar Fase 0b aunque el objetivo sea solo actualizar contenido. Assets CSS/JS y `navigation.sections` pueden desincronizarse entre sesiones.
- **[downloads.md]**: La fecha de la tabla debe coincidir con la fecha del último `mkdocs build` ejecutado en la sesión. El ZIP latest se regenera en cada build vía `mkdocs_hooks.py`.
- **[pyproject.toml]**: Contiene entry point residual `doc_ia_docs.docs_build_plugin:DocumentationZipPlugin` de la migración a hooks (sesión 2026-06-15). Es deuda técnica pendiente de limpiar con `/tech-debt`.

## Veredicto

**GO** — Documentación actualizada y build verificado. 11 artefactos actualizados, 0 errores de build.
