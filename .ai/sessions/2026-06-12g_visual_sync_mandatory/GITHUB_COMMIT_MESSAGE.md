# Mensaje de commit — 2026-06-12g

```
docs(tooling): elevar sincronización visual MkDocs a requisito obligatorio

Detectado en dpss: navigation.sections activo + ausencia de assets CSS/JS
causaban que el menú lateral no fuera colapsable y los márgenes fueran
excesivamente anchos.

Cambios en doc_ia:
- CLAUDE.md: añade Fase 0b al flujo de /document-project como OBLIGATORIO
- .claude/commands/document-project.md: sección Fase 0b marcada OBLIGATORIO
  + checklist de 5 puntos (assets, navigation.sections ausente, extensions)
- .claude/EDGE_CASES.md: caso límite navigation.sections registrado con
  síntoma, causa verificada y tratamiento paso a paso
- .claude/settings.json: comandos aprobados de sesiones anteriores
- .ai/sessions/2026-06-12g_visual_sync_mandatory/: artefactos de sesión

Regla canónica: si nav.css está en extra_css → navigation.sections debe
estar AUSENTE de theme.features. Los 4 assets (nav.css, mermaid.css,
sidebar-toggle.js, mermaid.js) son obligatorios en todo proyecto destino.

Sesión: .ai/sessions/2026-06-12g_visual_sync_mandatory/
Páginas: 0 creadas · 3 actualizadas (CLAUDE.md, document-project.md, EDGE_CASES.md)
```
