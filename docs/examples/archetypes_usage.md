# Ejemplo: Aplicar Arquetipos Individualmente

## 1. Contexto del Ejemplo

Cuando quieres documentar **un único módulo** o actualizar una sola página, no hace falta
invocar el flujo completo `/document-project`: aplica directamente el prompt del arquetipo
correspondiente. Este ejemplo muestra cómo seleccionar el arquetipo correcto para un módulo
dado y cómo invocar cada prompt de forma individual en cualquier plataforma IA.

El patrón es útil también cuando `/document-project` ya generó el inventario y quieres
ejecutar solo una fase concreta sin repetir el ciclo entero.

## 2. Implementación de Referencia

Invocaciones directas de arquetipo (código inline — el flujo ocurre en el chat):

**Paso 1 — Seleccionar el arquetipo adecuado**

```
# Pregunta que responde cada arquetipo:
#
#  ¿Qué hace y por qué?                     → Arq. 1: functional_doc.prompt.md
#  ¿Cómo funciona internamente?              → Arq. 2: technical_doc.prompt.md
#  ¿Cómo resuelvo esta tarea concreta?       → Arq. 3a: howto_doc.prompt.md
#  ¿Cómo aprendo esto paso a paso?           → Arq. 3b: tutorial_doc.prompt.md
#  ¿Cómo se implementa?                      → Arq. 4: example_doc.prompt.md
#  ¿Por qué se decidió así?                  → Arq. 5: architecture_doc.prompt.md (MADR 4.0)
#  ¿Qué es el proyecto / cómo empiezo?       → Arq. 6: landing_doc.prompt.md (Var. A/B/C/D)
#  ¿Cómo me incorporo?                       → Arq. 7: onboarding_dev.prompt.md
#  ¿Qué normativa aplica?                    → Arq. 8: normative_traceability.prompt.md (condicional)
#  ¿Qué cambió en cada versión?              → Arq. 9: changelog.prompt.md
#  ¿Cómo está configurado el agente IA?      → Arq. 10: ai_config_doc.prompt.md
#  ¿Cómo contribuyo al proyecto?             → Arq. 11: contributing_doc.prompt.md
```

**Paso 2 — Invocar el prompt elegido (Arquetipo 1 sobre un módulo Python)**

```
Lee y aplica .github/prompts/functional_doc.prompt.md

Módulo a documentar: scripts/check_env.py
Destino:             docs/functional/check_env.md
Idioma:              es
```

**Arquetipo 2 sobre el mismo módulo**

```
Lee y aplica .github/prompts/technical_doc.prompt.md

Módulo a documentar: scripts/check_env.py
Destino:             docs/api/check_env.md
Idioma:              es
```

**Arquetipo 4 sobre el mismo módulo**

```
Lee y aplica .github/prompts/example_doc.prompt.md

Módulo a documentar: scripts/check_env.py
Ejemplo a crear:     docs/examples/check_env_usage.md
Archivo de soporte:  docs/examples/check_env_usage.py
Idioma:              es
```

**Arquetipo 9 — Changelog** (crear o actualizar `CHANGELOG.md` tras un release)

```
Lee y aplica .github/prompts/changelog.prompt.md

Proyecto: doc_ia
Versión a cerrar: 0.1.0
Fecha: 2026-06-10
Destino: CHANGELOG.md
Idioma: es
```

**Arquetipo 10 — Configuración de Agente IA** (documentar Claude Code en el proyecto)

```
Lee y aplica .github/prompts/ai_config_doc.prompt.md

Plataforma: Claude Code
Fichero fuente: CLAUDE.md + .claude/settings.json
Destino: docs/ai-config/claude.md
Idioma: es
```

**Arquetipo 11 — Guía de Contribución**

```
Lee y aplica .github/prompts/contributing_doc.prompt.md

Proyecto: doc_ia
Convenciones: .github/SHARED_INSTRUCTIONS.md
Destino: CONTRIBUTING.md
Idioma: es
```

**Arquetipo 3b — Tutorial** (experiencia de aprendizaje progresiva sobre un flujo)

```
Lee y aplica .github/prompts/tutorial_doc.prompt.md

Módulo a documentar: flujo /document-project (primer uso)
Destino: docs/guides/document_project_tutorial.md
Idioma: es
```

## 3. Explicación del Código

- Cada prompt produce exactamente las secciones numeradas del arquetipo asignado;
  si una sección no aplica al módulo, se escribe `*No aplica para este módulo.*`
  — nunca se omite.
- Los arquetipos 2 y 4 requieren **enlace bidireccional** entre sí: §5 del Arquetipo 2
  enlaza al ejemplo, §5 del Arquetipo 4 enlaza al técnico. Al aplicarlos por separado,
  el autor debe añadir esos enlaces manualmente si los archivos se crean en sesiones distintas.
- El Arquetipo 8 es **condicional**: solo se invoca si el proyecto origen referencia
  normativa de obligado cumplimiento (leyes, decretos, directivas); si no, se omite.
- Los Arquetipos **9 (Changelog)** y **11 (Contribución)** son **opt-in**: `/document-project`
  no los genera por defecto aunque el proyecto tenga releases o acepte contribuciones.
  Para incluirlos se usan dos vías — parámetro en el flujo o invocación directa del prompt
  (ambas se muestran en esta página y en [Documentar un Proyecto](document_project_usage.md)).
- Antipatrón: no usar `/document-project` para un solo archivo — invoca el prompt
  de arquetipo directamente como se muestra aquí.

## 4. Ejecución y Pruebas

El agente lee el módulo indicado, genera el documento siguiendo la estructura fija del
arquetipo y lo escribe en la ruta destino. Output esperado tras Arquetipo 1:

```
docs/functional/check_env.md creado.

Secciones generadas:
  ## 1. Descripción General     ✔
  ## 2. Reglas de Negocio       ✔
  ## 3. Casos de Uso            ✔
  ## 4. Criterios de Aceptación ✔
  ## 5. Glosario y Términos     ✔
```

Verificar el resultado:

```bash
python -m mkdocs build --strict
# INFO - Documentation built in X.Xs
# ✔ Sin errores (después de actualizar mkdocs.yml con la nueva entrada)
```

## 5. Referencias Relacionadas

- Documentación funcional: [Arquetipos Formales](../functional/archetypes.md)
- Referencia técnica: [archetypes](../api/archetypes.md)
- Ejemplos relacionados: [Documentar un Proyecto](document_project_usage.md)
