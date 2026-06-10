# Prompt: howto_doc — Guía How-to (Arquetipo 3a)

Genera o actualiza guías orientadas a tarea (how-to) para **doc_ia** usando solo
información verificable del código, README, `docs/` y configuración del proyecto.

**Diferencia con Tutorial (Arquetipo 3b)**: Un how-to resuelve un problema concreto en el menor número de pasos. No explica el contexto ni guía el aprendizaje. Asume que el lector sabe qué quiere hacer.

## Instrucción al modelo

```
Actúa como technical writer especializado en documentación de usuario para proyectos Python.

Analiza el área de documentación proporcionada y el contexto real del repositorio.
No asumas pasos, comandos ni comportamientos que no aparezcan en el código real,
`pyproject.toml`, README o `docs/`.

Genera una guía how-to en Markdown siguiendo el Arquetipo 3a con estas secciones en este orden exacto:

# Cómo [verbo + objeto concreto]

## 1. Objetivo
Una frase: qué conseguirás. Verbos imperativos ("instala", "configura", "verifica").
NO incluir explicaciones sobre por qué o contexto de aprendizaje.

## 2. Requisitos Previos
Lista de herramientas, accesos o estado inicial requerido antes de comenzar.
Incluye: versiones mínimas, permisos necesarios, dependencias previas.

## 3. Pasos
Procedimiento secuencial numerado con bloques de código para cada paso.
Usa bloques ```bash para comandos de terminal.
Cada paso debe ser atómico, ejecutable y verificable de forma independiente.
Sin explicaciones de "por qué"; solo "qué hacer".

## 4. Verificación
Comando exacto para comprobar que la tarea fue completada con éxito.
Incluye el output esperado para que el usuario pueda comparar con su resultado real.
Si no hay verificación automatizable: describe el comportamiento visual esperado.

## 5. Variantes y Solución de Problemas
Tabla con columnas: | Escenario/Error | Causa probable | Solución |
Incluye: alternativas al flujo principal, configuraciones opcionales y errores conocidos.
Si no hay casos: "*No aplica para este módulo.*"

---

Restricciones:
- Si una sección queda vacía, escribe "*No aplica para este módulo.*" — nunca omitas la sección
- USA verbos imperativos: "instala", "ejecuta", "verifica" (no "puede instalarse", "se recomienda")
- NO inventes pasos, comandos, outputs ni errores
- Los comandos deben ser ejecutables con el código actual de la rama principal
- NO uses la directiva --8<-- para incluir código; embebe el código directamente en los bloques fenced
- Si falta información, añade subsección "### Pendiente de verificación" con preguntas concretas
- Responde SOLO con el Markdown, sin texto introductorio ni cierre
```

## Cómo usar este prompt

### Modo guía única — Claude Code

```
Lee [ruta_del_área_o_módulo] y genera la guía how-to usando el
prompt en .github/prompts/howto_doc.prompt.md.
Actualiza docs/guides/[nombre]_howto.md si existe, o crea la página si no hay equivalente.
Actualiza mkdocs.yml si se crea o mueve una página.
No inventes pasos ni comandos; si falta información, márcala como pendiente.
```

### Modo guía única — Copilot Chat

```
#file:.github/prompts/howto_doc.prompt.md
#file:[ruta_del_módulo_o_área]

Genera la guía how-to del área indicada siguiendo las instrucciones del prompt.
```

## Arquetipos de how-to en este proyecto

| Archivo | Tipo |
|---|---|
| `docs/guides/troubleshooting.md` | Solución de problemas frecuentes |
| `docs/guides/codex_guide.md` | Uso de Codex (OpenAI) en este proyecto |
| `docs/guides/claude_code_guide.md` | Uso de Claude Code en este proyecto |
| `docs/downloads.md` | Descarga de documentación offline (ZIP) |

> **Nota**: `docs/guides/onboarding_dev.md` se rige por el Arquetipo 7, no por este prompt.
> `docs/installation.md` se rige por el Arquetipo 6 Variante B (`landing_doc.prompt.md`).

## Output esperado

Markdown con título H1 `# Cómo [verbo + objeto]` y las 5 secciones del Arquetipo 3a numeradas
(`## 1.`–`## 5.`). `## 4. Verificación` debe incluir siempre al menos un comando ejecutable.
