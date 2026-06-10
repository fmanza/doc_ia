# TRACEABILITY

## Session metadata
- id: 2026-06-10c
- fecha: 2026-06-10
- rama: main
- skill: new_feature (Fase 5 — comando de producto document_project)
- fase: PLAN + IMPLEMENT + AUDIT_CODE + VERSION

## Prompt issued
"Fase 5 — Pieza nueva específica de doc_ia: document_project.prompt.md + /document-project
con validación obligatoria de inputs (origen, destino, generador, idioma; si faltan, DETENERSE)
orquestando el flujo de 7 fases del Documentation Generator; política explícita en
SHARED_INSTRUCTIONS (sin API keys, ejecución en chat, Python nunca invoca IA)."

## Nota previa
Antes de implementar se ejecutó el barrido de integridad Capa A vs origen que destapó el
hallazgo F5 (10 ficheros corruptos), remediado y commiteado por separado (44fae8d) bajo la
sesión `2026-06-10b_config_review`.

## AI output summary
- **Nuevo** `.github/prompts/document_project.prompt.md`: punto de entrada único del producto;
  4 inputs obligatorios (origen(es), destino, generador, idioma) con VALIDACIÓN bloqueante
  (patrón new_feature), política innegociable embebida, flujo orquestado Fases 0-7 del
  Documentation Generator, orden de salida (VALIDACIÓN → INVENTARIO → PLAN_DOC → GENERACIÓN →
  SYNC NAV → REVISIÓN → BUILD opt-in → RESUMEN), invocación por plataforma.
- **Nuevo** `.claude/commands/document-project.md`: conforme a COMMAND_TEMPLATE (10 secciones:
  cuándo usar + antipatrones, inputs con checkboxes, ⚠️ VALIDACIÓN, política de cambios,
  orden de salida, ejemplos deterministas, qué hacer si falla, referencias).
- **SHARED_INSTRUCTIONS.md**: principios innegociables endurecidos ("prohibido incrustar",
  cláusula de aplicación a document_project y arquetipos); nueva capacidad "Punto de entrada
  único para documentar" al frente de Capacidades principales.
- **Sincronización**: CLAUDE.md (fila /document-project en tabla + sección Documentación
  reapuntada al comando), AGENTS.md (20 prompts, 9 commands, asimetría actualizada:
  documentation-generator ahora tiene slash command), INTEGRATION_MAP.md (recuentos 20/9,
  grupo "Producto (1)", + fila docs.instructions.md que faltaba en la tabla de instructions).

## Artefactos generados

| Artefacto | Ruta | Estado |
|---|---|---|
| Prompt de producto | .github/prompts/document_project.prompt.md | nuevo |
| Slash command | .claude/commands/document-project.md | nuevo |
| Canónico | .github/SHARED_INSTRUCTIONS.md | política + capacidad |
| Gobernanza | CLAUDE.md, .github/AGENTS.md, .github/INTEGRATION_MAP.md | sincronizados |

## Directrices para Futuras IAs
- **[entrada-única]**: para documentar un proyecto usa siempre `/document-project` /
  `document_project.prompt.md`; los prompts de arquetipo sueltos son para páginas individuales.
- **[validación]**: los 4 inputs (origen, destino, generador, idioma) son bloqueantes — no
  inventar rutas ni elegir generador/idioma por el usuario.
- **[recuentos]**: tras esta sesión hay 20 prompts y 9 slash commands; AGENTS.md e
  INTEGRATION_MAP.md llevan los recuentos — actualizarlos al añadir piezas.

## Veredicto final
Veredicto: CLOSED
Pendientes al cierre:
- Dogfooding: primera ejecución real de /document-project sobre doc_ia (genera docs/ completo).
- F4 (sesión 2026-06-10b) sigue abierto para el dogfooding.
