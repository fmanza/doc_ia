# SESSION INDEX

Inventario de sesiones de trabajo controlado en `.ai/sessions/`.
Cada sesión sigue la estructura de artefactos definida en `TEMPLATE/`.

## Convención de nomenclatura

```
.ai/sessions/YYYY-MM-DD_<slug>/
  00_REQUEST.md           ← solicitud saneada y restricciones
  00_CONTEXT_SNAPSHOT.md  ← estado del repo y Gate G0
  NN_<FASE>.md            ← artefactos por fase (PLAN, IMPLEMENT, etc.)
  TRACEABILITY.md         ← resumen de lo ejecutado y veredicto final
  GITHUB_COMMIT_MESSAGE.md / COMMIT_MSG.txt ← mensaje de commit (si aplica)
```

## Sesiones

| Fecha      | Objetivo breve                                                                 | Rama | Skill                          | Estado | Trazabilidad                                       |
|------------|--------------------------------------------------------------------------------|------|--------------------------------|--------|----------------------------------------------------|
| 2026-06-10 | Bootstrap configuración IA multiplataforma desde util_bbdd (modelo PULL, capas A/B/C/D) | main | new_feature (bootstrap_ai_config) | CLOSED | `2026-06-10_bootstrap_ai_config/TRACEABILITY.md` |
| 2026-06-10b | Auditoría post-bootstrap (Config Reviewer): agente corrupto d→o restaurado + docs.instructions.md creado; ampliada con F5 (10 ficheros Capa A corruptos restaurados) | main | config_review | CLOSED | `2026-06-10b_config_review/TRACEABILITY.md` |
| 2026-06-10c | Fase 5: comando de producto /document-project + document_project.prompt.md (validación obligatoria origen/destino/generador/idioma) + política explícita en canónico | main | new_feature | CLOSED | `2026-06-10c_document_project/TRACEABILITY.md` |
| 2026-06-10d | Dogfooding: primera ejecución real de /document-project sobre doc_ia — 12 páginas (arquetipos 1-7) + nav completo + verify-build OK; cierra F4 | main | document_project | CLOSED | `2026-06-10d_dogfooding_docs/TRACEABILITY.md` |
| 2026-06-10e | Arquetipo 1 §4 ejecutable: criterios de aceptación derivados del código (estándar alineado con functional_doc §7) + 7 ACs reales en las páginas funcionales | main | refactor documental | CLOSED | `2026-06-10e_acceptance_criteria/TRACEABILITY.md` |
| 2026-06-10f | Enriquecimiento mkdocs.yml desde util_bbdd + UX: márgenes grid, sidebar toggle ◀/▶, fix Mermaid rendering; docs IA actualizadas (template canónico mkdocs.yml) | main | refactor + UX | CLOSED | `2026-06-10f_mkdocs_enrichment/TRACEABILITY.md` |
| 2026-06-10g | Revisión /document-project: estados A/B/C formalizados + protocolo ACTUALIZAR; expuesto en GEMINI.md, copilot-instructions.md y .cursorrules | develop | document_project (revisión) | CLOSED | `2026-06-10g_document_project_revision/TRACEABILITY.md` |
| 2026-06-10h | Dogfooding /document-project (2ª ejec.): 3 páginas funcionales nuevas (document_project, archetypes, bootstrap) + 2 correcciones en guías | develop | document_project | CLOSED | `2026-06-10h_dogfooding_docs2/TRACEABILITY.md` |
| 2026-06-10i | Ejemplo de uso del producto: `document_project_usage.md` (Arquetipo 4, 3 escenarios) + subsección "Flujos IA" en nav Ejemplos | develop | new_feature (Arquetipo 4) | CLOSED | `2026-06-10i_example_document_project/TRACEABILITY.md` |
