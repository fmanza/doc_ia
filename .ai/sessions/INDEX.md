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
