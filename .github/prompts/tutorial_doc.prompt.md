# Prompt: tutorial_doc — Tutorial Guiado (Arquetipo 3b)

Genera o actualiza tutoriales de aprendizaje progresivo para **doc_ia** usando solo
información verificable del código, README, `docs/` y configuración del proyecto.

**Diferencia con How-to (Arquetipo 3a)**: Un tutorial lleva al lector por una experiencia
de aprendizaje guiada. Incluye "por qué funciona esto", anticipa y explica errores,
y termina con reflexión sobre lo aprendido. No asume conocimiento previo del área.

## Instrucción al modelo

```
Actúa como technical writer especializado en aprendizaje guiado (Diátaxis — cuadrante Tutorial).

El objetivo no es solo que el lector complete los pasos, sino que comprenda lo que está
aprendiendo. El tutorial construye confianza y comprensión progresiva.

Analiza el área proporcionada y el contexto real del repositorio.
No asumas capacidades, comandos ni comportamientos no verificables en el código real.

Genera un tutorial en Markdown siguiendo el Arquetipo 3b con estas secciones en este orden exacto:

# Tutorial: [Qué aprenderás a hacer]
(Título en forma de resultado: "Tutorial: Documentar tu primer proyecto con doc_ia")

## 1. Qué aprenderás
Resultado concreto al final del tutorial (1 párrafo).
Lista de 3-5 habilidades o conceptos que el lector dominará.
Tiempo estimado de realización.

## 2. Antes de empezar
Herramientas y versiones necesarias (lista verificable).
Nivel de conocimiento esperado: indica explícitamente qué se asume que el lector ya sabe.
Si el lector no cumple el nivel: enlazar a recurso previo (otro tutorial o how-to).

## 3. [Fase 1 — nombre descriptivo que indica qué se construye]
Introducción breve: qué harás en esta fase y por qué (1-2 frases).
Acción con código ejecutable.
"¿Qué ha pasado?": párrafo explicando por qué funciona lo que acaba de hacer (no cómo, sino por qué).
Errores frecuentes en esta fase: descripción + solución dentro de la misma fase.

## 4. [Fase 2 — nombre descriptivo]
(Repetir patrón: contexto → acción → por qué → errores frecuentes)

## [N fases según complejidad del tutorial]

## N+1. Resumen y Siguientes Pasos
Listado de lo aprendido (confirma las habilidades del §1).
Enlace a guías how-to relacionadas para usar en producción (Arquetipo 3a).
Recursos adicionales si el lector quiere profundizar.

---

Restricciones:
- Cada fase termina en un estado verificable: el lector sabe que ha tenido éxito
- Incluir el razonamiento detrás de cada paso, no solo el paso en sí
- Mantener hilo narrativo: el lector construye algo a lo largo de todo el tutorial
- Anticipar errores dentro de la fase donde ocurren (no aparcar todos al final)
- NO mezclar How-to y Tutorial: si el objetivo es "hacer X rápido", usa howto_doc.prompt.md
- NO inventes capacidades, módulos, APIs ni outputs no verificables
- Si falta información para una fase, añadir "### Pendiente de verificación" con preguntas
- Responde SOLO con el Markdown, sin texto introductorio ni cierre
```

## Cómo usar este prompt

### Modo tutorial único — Claude Code

```
Lee [ruta_del_área_o_módulo] y genera el tutorial de aprendizaje usando el
prompt en .github/prompts/tutorial_doc.prompt.md.
Crea docs/guides/[nombre]_tutorial.md.
Actualiza mkdocs.yml bajo la subsección temática correspondiente en "Guías".
No inventes capacidades ni outputs; si falta información, márcala como pendiente.
```

### Modo tutorial único — Copilot Chat

```
#file:.github/prompts/tutorial_doc.prompt.md
#file:[ruta_del_módulo_o_área]

Genera el tutorial de aprendizaje del área indicada siguiendo las instrucciones del prompt.
```

## Cuándo usar este arquetipo vs How-to

| Pregunta clave | Arquetipo |
|---|---|
| ¿El lector quiere resolver un problema concreto rápido? | 3a How-to |
| ¿El lector se acerca al área por primera vez? | 3b Tutorial |
| ¿El objetivo es que entienda el modelo mental, no solo que ejecute? | 3b Tutorial |
| ¿Los pasos asumen conocimiento previo? | 3a How-to |

## Output esperado

Markdown con título H1 `# Tutorial: [nombre]` y N+2 secciones (§1 Qué aprenderás,
§2 Antes de empezar, §3–§N Fases, §N+1 Resumen).
Cada fase con subsección "¿Qué ha pasado?" y gestión de errores frecuentes inline.
