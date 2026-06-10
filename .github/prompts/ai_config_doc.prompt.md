# Prompt: ai_config_doc — Configuración de Agente IA (Arquetipo 10)

Genera o actualiza la documentación de configuración de una plataforma IA para **doc_ia** usando solo
información verificable de los ficheros de configuración reales del proyecto.

**Origen del arquetipo**: Tipo propio de doc_ia (2024-2025) — no existe estándar externo para
documentar configuraciones de agentes IA (CLAUDE.md, copilot-instructions.md, .cursorrules, etc.).

## Instrucción al modelo

```
Actúa como arquitecto de sistemas IA documentando la configuración de un agente en un proyecto.

Analiza los ficheros de configuración reales de la plataforma indicada (CLAUDE.md,
copilot-instructions.md, .cursorrules, settings.json, etc.) y genera documentación
precisa que permita a otro desarrollador entender y replicar la configuración.

NO inventes permisos, comandos, restricciones ni hooks que no aparezcan en los ficheros fuente.

Genera la documentación en Markdown siguiendo el Arquetipo 10 con estas secciones en este orden exacto:

# Configuración de [Nombre Plataforma IA]

> Versión del modelo objetivo: [modelo] · Fichero fuente: [ruta] · Revisado: YYYY-MM-DD

## 1. Plataforma y Modelo
- Plataforma: [nombre]
- Versión mínima del modelo: [modelo ID]
- Fichero de configuración principal: [ruta relativa al repo]
- Ficheros de soporte: [lista de rutas relevantes]

## 2. Contexto Obligatorio
Lista de ficheros que el agente debe leer antes de actuar, en orden de prioridad:
| Fichero | Propósito |
|---------|-----------|
| [ruta] | [qué información aporta] |

## 3. Comandos y Slash Commands
| Comando | Propósito | Inputs obligatorios | Outputs esperados |
|---------|-----------|--------------------|--------------------|
| /[cmd] | [descripción] | [inputs] | [outputs] |
Si no hay slash commands configurados: "*No aplica para esta configuración.*"

## 4. Permisos y Herramientas
| Herramienta / Acción | Permitida | Condición o restricción |
|---------------------|-----------|------------------------|
| [herramienta] | ✅ / ❌ / ⚠️ Condicional | [cuando aplica] |
Basada en el fichero settings.json o equivalente real.
Si no hay configuración de permisos explícita: "*No aplica para esta configuración.*"

## 5. Hooks y Automatizaciones
| Evento | Comando ejecutado | Propósito |
|--------|------------------|-----------|
| PostToolUse (Edit\|Write) | [comando] | [propósito] |
Si no hay hooks configurados: "*No aplica para esta configuración.*"

## 6. Restricciones Explícitas
Lista de lo que el agente nunca debe hacer en este proyecto:
Derivar literalmente de la sección de prohibiciones / restricciones del fichero fuente.
Si no hay restricciones explícitas: "*No aplica para esta configuración.*"

## 7. Casos Límite Conocidos
Lista de comportamientos inesperados documentados o advertencias relevantes.
Fuente: EDGE_CASES.md o sección equivalente en el fichero fuente.
Si no hay casos documentados: "*No aplica para esta configuración.*"

---

Restricciones:
- Todo el contenido debe ser verificable en los ficheros fuente indicados
- NO inferir permisos ni restricciones no explicitados
- Si un dato no está en el fichero fuente, añadir "### Pendiente de verificación"
- Usar ✅ (permitido), ❌ (denegado), ⚠️ (condicional) en columnas de permisos
- Responde SOLO con el Markdown, sin texto introductorio ni cierre
```

## Cómo usar este prompt

### Modo plataforma única — Claude Code

```
Lee [CLAUDE.md | copilot-instructions.md | .cursorrules | settings.json] y genera
la documentación de configuración usando el prompt en .github/prompts/ai_config_doc.prompt.md.
Crea docs/ai-config/[plataforma].md (ej: claude.md, copilot.md, gemini.md).
Actualiza mkdocs.yml bajo la sección "Configuración IA" si no existe aún.
```

### Modo Copilot Chat

```
#file:.github/prompts/ai_config_doc.prompt.md
#file:CLAUDE.md
#file:.claude/settings.json

Genera la documentación de configuración de Claude Code para este proyecto.
```

## Plataformas soportadas en doc_ia

| Plataforma | Fichero fuente | Doc destino |
|---|---|---|
| Claude Code | `CLAUDE.md` + `.claude/settings.json` | `docs/ai-config/claude.md` |
| GitHub Copilot | `.github/copilot-instructions.md` | `docs/ai-config/copilot.md` |
| Cursor | `.cursorrules` | `docs/ai-config/cursor.md` |
| Gemini | `GEMINI.md` | `docs/ai-config/gemini.md` |
| OpenAI Codex | `docs/guides/codex_guide.md` | Combinar con Arquetipo 3a |

## Output esperado

Markdown con título H1 `# Configuración de [Plataforma]` y las 7 secciones del Arquetipo 10.
Las secciones con tablas deben tener al menos una fila de contenido real o la nota "*No aplica*".
