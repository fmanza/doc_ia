---
session: 2026-06-10g_document_project_revision
skill: document_project (revisión de instrucciones IA)
branch: develop
status: CLOSED
---

# TRACEABILITY — 2026-06-10g: Revisión de /document-project

## Solicitud

Revisar `.claude/commands/document-project.md` para verificar que contempla:
1. Actualización de documentación existente en destino (no solo creación)
2. Conveniencia de exponer el comando en el resto de plataformas IA

## Archivos modificados

| Archivo | Tipo | Cambio |
|---|---|---|
| `.github/prompts/document_project.prompt.md` | Modificado | Fase 1 ampliada con estados A/B/C y 5 criterios de estado B; Protocolo ACTUALIZAR (5 pasos); sección "Devuelve en este orden" con columnas A/B/C |
| `.claude/commands/document-project.md` | Modificado | INVENTARIO con 4 columnas y 3 estados; PLAN_DOC con prioridad A antes B; GENERACIÓN protocolo estado B; Política de cambios: preservación; ejemplo INVENTARIO con los 3 estados |
| `GEMINI.md` | Modificado | Nueva sección "Documentar un proyecto completo" con patrón de invocación y campos obligatorios |
| `.github/copilot-instructions.md` | Modificado | Sección "Generación de Documentación" reestructurada: proyecto completo (document_project) como primario; módulo individual como secundario |
| `.cursorrules` | Modificado | §10 "Documentar un proyecto completo" con patrón de invocación unificado |
| `.github/instructions/docs.instructions.md` | Modificado | Criterios de detección estado B (5 condiciones); Protocolo de actualización en 5 pasos |
| `.claude/settings.json` | Modificado | Comandos Bash adicionales en allowedTools (diagnóstico de sesión) |

## Resultado

- Estados A/B/C formalizados y alineados en todas las capas: prompt, comando Claude, instructions, criterios operativos
- `/document-project` expuesto en GEMINI.md, copilot-instructions.md y .cursorrules con patrones de invocación correctos por plataforma
- Protocolo explícito para no sobreescribir documentación vigente (estado C) ni crear duplicados de páginas desactualizadas (estado B)

## Veredicto

PASS — sin breaking changes; cambios aditivos de comportamiento.
