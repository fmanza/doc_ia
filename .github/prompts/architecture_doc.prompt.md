# Prompt: architecture_doc — Decisión Arquitectónica / MADR (Arquetipo 5)

Documenta una decisión arquitectónica (ADR) para **doc_ia** usando solo
información verificable del código, issues, PRs y documentación existente.

**Estándar**: MADR 4.0 (Markdown Any Decision Records, septiembre 2024).
Referencia: [adr.github.io/madr](https://adr.github.io/madr/)

## Instrucción al modelo

```
Actúa como arquitecto de software senior especializado en documentación de decisiones
arquitectónicas siguiendo el estándar MADR 4.0.

Analiza el contexto proporcionado (código, issue, PR, discusión) para documentar
la decisión de forma objetiva. No asumas motivaciones ni consecuencias no verificables.

Elige el formato según la complejidad:
- FULL: decisiones críticas con múltiples opciones y consecuencias complejas
- MINIMAL: decisiones pequeñas o cuando el tiempo es limitado

--- FORMATO FULL ---

Genera un ADR en Markdown con este encabezado y secciones en este orden exacto:

---
status: "PROPUESTO | ACEPTADO | OBSOLETO | REEMPLAZADO POR ADR-NNN"
date: YYYY-MM-DD
deciders: [nombres o roles de quienes tomaron la decisión]
consulted: [nombres o roles consultados antes de la decisión]
informed: [nombres o roles informados tras la decisión]
---

# Use [Solución] for [Contexto/Problema]
(Título en forma "Use X for Y" — solución primero, problema después)

## Contexto y Problema
Qué situación motivó la decisión:
- Estado del sistema antes de la decisión
- Problema o limitación identificada
- Fuerzas en conflicto (requisitos, restricciones, trade-offs)

## Decisión
Enunciado claro de la decisión tomada.
Justificación: por qué esta opción sobre las alternativas.

## Consecuencias
Tabla: | Tipo | Descripción |
Tipos: Ventaja | Compromiso (trade-off) | Deuda técnica | Riesgo aceptado
Ser honesto sobre los trade-offs; no omitir consecuencias negativas verificables.

## Alternativas Consideradas
Tabla: | Alternativa | Pros | Contras | Motivo de rechazo |
Si no hubo alternativas documentadas: "*No aplica para este módulo.*"

## Estado y Revisión
Estado: [igual que el frontmatter status]
Fecha: YYYY-MM-DD
Si reemplaza a otro ADR: "Reemplaza a [ADR-NNN — título]"
Si es reemplazado: "Reemplazado por [ADR-NNN — título]"

--- FORMATO MINIMAL ---

---
status: "PROPUESTO | ACEPTADO | OBSOLETO"
date: YYYY-MM-DD
---

# Use [Solución] for [Contexto/Problema]

## Contexto y Problema

## Decisión

## Consecuencias

---

Restricciones (aplican a ambos formatos):
- El título SIEMPRE en forma "Use X for Y" (solución → problema), no solo el tema
- Si una sección queda vacía, escribe "*No aplica para este módulo.*" — nunca omitas la sección
- NO inventes motivaciones, fechas, decisores ni consecuencias
- NO documentes decisiones de implementación (cómo funciona algo); solo decisiones de diseño (por qué)
- Los campos `deciders`, `consulted`, `informed` pueden ser `[]` si no se conocen
- Si falta información verificable, añade subsección "### Pendiente de verificación"
- Responde SOLO con el Markdown (incluyendo frontmatter YAML), sin texto introductorio ni cierre
```

## Cómo usar este prompt

### Modo ADR único — Claude Code

```
Documenta la decisión arquitectónica sobre [TEMA] usando el
prompt en .github/prompts/architecture_doc.prompt.md.
Usa formato FULL si hay ≥2 alternativas; MINIMAL si es una decisión simple.
Guarda en docs/adr/ADR-[NNN]-[nombre-kebab-case].md.
Actualiza mkdocs.yml bajo la sección "Arquitectura".
Basa el contenido en: [PR/issue/commit/discusión de referencia]
```

### Cuándo crear un ADR

Crear un ADR cuando se toma una decisión que:
- Afecta la arquitectura pública (contratos de API, estructura de módulos)
- Elige entre múltiples enfoques con trade-offs no triviales
- Introduce o elimina una dependencia significativa
- Establece un patrón que otros módulos deben seguir

**No crear ADR** para: decisiones de implementación interna, cambios de estilo, bugfixes.

### Cuándo usar FULL vs MINIMAL

| Situación | Formato |
|---|---|
| ≥2 alternativas con trade-offs documentados | Full |
| Decisores y consultados conocidos | Full |
| Tiempo limitado / decisión simple | Minimal |
| Como placeholder hasta completar la investigación | Minimal |

## Numeración

Los ADRs se numeran secuencialmente: ADR-001, ADR-002, ...
Consultar `docs/adr/` para el número siguiente disponible.

## Compatibilidad con ADRs existentes

Los ADRs creados antes de MADR 4.0 (sin frontmatter YAML) siguen siendo válidos.
Al actualizar un ADR antiguo: añadir el frontmatter YAML sin modificar el contenido de las secciones.

## Output esperado

Markdown con frontmatter YAML + título H1 en forma `# Use X for Y` y las secciones del
Arquetipo 5. Formato FULL: 5 secciones. Formato MINIMAL: 3 secciones.
`status` siempre con valor explícito.
