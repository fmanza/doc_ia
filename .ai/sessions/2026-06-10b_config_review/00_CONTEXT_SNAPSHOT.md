# CONTEXT SNAPSHOT

## Contexto del repositorio revisado
- Configuración IA completa instalada por el bootstrap (commit a8ebf2c, sesión
  `2026-06-10_bootstrap_ai_config`): canónico + 5 entry points, 12 agentes, 19 prompts,
  8 commands, `.ai/*`, workflows, tooling ZIP.
- Origen de contraste (solo lectura): `c:\Desarrollo\python\libs\util_bbdd`.

## Estado actual observado
- Puertas de calidad en verde al inicio: ruff=0, mypy=0, pytest 2/2, mkdocs build --strict OK.
- Remote `origin` configurado y main publicado en GitHub (fmanza/doc_ia).

## Estado Git relevante
- Rama activa: main (tracking origin/main, al día tras push de a8ebf2c)
- Working tree limpio al inicio de la auditoría

## Clasificación metodológica
- Tipo principal: config_review (auditoría independiente + remediación de críticos)
- Estado real de alcance: acotado (ficheros de configuración IA del bootstrap)
- Consecuencia: proceder con fase completa

## Gate G0 · Context Ready
Veredicto: GO
Condiciones pendientes (si aplica): ninguna.
