# Prompt: functional_doc — Documentación funcional (Product Owner)

<!--
  NÚCLEO BASE compartido con dpss/.github/prompts/functional_doc.prompt.md
  ÚNICA SECCIÓN EDITABLE POR PROYECTO: ## Especialización de dominio (abajo)
  Última revisión: 2026-06-07
-->

Genera o actualiza documentación funcional para módulos de **doc_ia** usando solo
información verificable del código, README, `docs/` y configuración del proyecto.

---

## Especialización de dominio

<!-- ÚNICO BLOQUE EDITABLE PARA ESTE PROYECTO — no modificar el resto del fichero -->

- **Proyecto**: doc_ia — sistema de instrucciones IA y tooling determinista para documentar proyectos de desarrollo
- **Rol del modelo**: Senior Product Owner especializado en herramientas de documentación y developer experience
- **Actores por defecto en §3**: `Usuario` (desarrollador), `Plataforma IA (chat)`, `doc_ia` (instrucciones/tooling), `Proyecto origen`
- **Audiencia**: Desarrolladores y technical writers que documentan proyectos con asistentes IA
- **Fuente del glosario §8**: `.ai/glossary.md` (mantener coherencia con el glosario del proyecto)
- **Tabla §5 — columnas**: 3 columnas — `Regla | Descripción | Impacto si se viola` (sin columna normativa)
- **Referencia §7 QA**: equipo QA / tests de integración del proyecto

---

## Instrucción al modelo

```
Actúa como el rol definido en la "Especialización de dominio" de este prompt.

Lee el módulo Python proporcionado, la documentación existente y el contexto real del repositorio.
No asumas capacidades por el nombre del proyecto ni por historial previo.
Consulta la sección "Especialización de dominio" de este prompt antes de generar cualquier sección.

Genera un documento Markdown con estas 8 secciones en este orden exacto:

# [Título del Módulo/Funcionalidad]

## 1. Objetivo y Descripción
2-3 párrafos sin jerga técnica. Contexto de negocio: qué problema resuelve este módulo,
qué valor aporta al desarrollador o al flujo de documentación, por qué existe.
Evita nombres de clases, rutas y detalles de implementación.

## 2. Precondiciones
Lista de lo que debe existir o estar configurado antes de usar esta funcionalidad:
herramientas instaladas, parámetros requeridos (proyecto origen / destino), ficheros de configuración, etc.
Un ítem por precondición.
Si no hay precondiciones verificables en el código: "*No aplica para este módulo.*"

## 3. Flujo Principal
Diagrama Mermaid: usa `sequenceDiagram` para flujo I/O con actores secuenciales, o
`stateDiagram-v2` cuando el módulo tiene un ciclo de vida con estados discretos y
transiciones (ej: fases de un pipeline, estados de un documento). Ajustar actores/estados
al módulo real (eliminar los que no participen). Máximo 12 nodos.
Marca los puntos de decisión (alt/opt/loop) con el criterio de bifurcación en la nota.
Tras el diagrama: párrafo en lenguaje natural describiendo el flujo paso a paso.

## 4. Postcondiciones y Efectos
Estado observable del sistema TRAS la operación. Incluir:
- Qué ficheros se crean, modifican o eliminan (docs, ZIP, checksums, configuración)
- Qué artefacto produce el módulo (página Markdown, sitio HTML, ZIP, código de salida)
- Qué estado queda persistido (dist/, site/, mkdocs.yml actualizado)
Si el módulo es stateless y no produce efectos secundarios observables: "*No aplica para este módulo.*"

## 5. Reglas de Negocio
Tabla: | Regla | Descripción | Impacto si se viola |
Solo reglas con impacto real en la corrección del resultado.
No inventar; solo las verificadas en el código.

## 6. Límites, Flujos Alternativos y Casos Especiales

### Qué NO hace esta funcionalidad
Lista explícita de lo que está fuera del alcance de este módulo.

### Flujos alternativos
Casos de error, variantes de configuración o condiciones excepcionales con su tratamiento.
Si no hay flujos alternativos verificables: "*No aplica para este módulo.*"

### Casos especiales
Situaciones límite que el módulo maneja de forma diferente al flujo principal.
Si no hay: "*No aplica para este módulo.*"

## 7. Criterios de Aceptación
Derivar del código cuando sea posible. Formato Given/When/Then.

Tabla: | ID | Dado | Cuando | Entonces |
Ejemplo de fila: | AC-01 | El entorno tiene mkdocs instalado y site/ generado | Se ejecuta build_docs_zip.py | Se crea dist/doc_ia-docs-{versión}.zip con su .sha256 |

### Pendiente de validación QA
Si algún criterio no puede derivarse del código, listar aquí con la pregunta concreta al equipo QA.
Si todos los criterios están cubiertos en la tabla: omitir esta subsección.

## 8. Glosario de Dominio
Tabla: | Término | Definición |
Solo términos de dominio específicos de este módulo (no términos Python genéricos).
Si no hay términos específicos: "*No aplica para este módulo.*"
```

---

## Restricciones

- Si una sección queda vacía, escribe `*No aplica para este módulo.*` — nunca omitas la sección
- NO expliques implementación, nombres de clases internas ni rutas de código fuente
- USA terminología de negocio, no técnica
- NO inventes capacidades, flujos, integraciones, salidas, reglas ni dependencias
- En §5, usa exactamente 3 columnas (sin columna normativa en este proyecto)
- En §7, prioriza criterios derivables del código; el placeholder QA es fallback, no primera opción
- En §3, ajusta los actores del domain slot al módulo real; elimina los que no participen
- NO uses la directiva `--8<--`; embebe el código directamente en bloques fenced
- Responde SOLO con el Markdown del documento, sin texto introductorio ni cierre
- Si falta información verificable, añade `### Pendiente de verificación` con preguntas concretas

---

## Cómo usar este prompt

### Modo módulo único — Claude Code

```
Lee [ruta_del_módulo] y genera la documentación funcional usando
.github/prompts/functional_doc.prompt.md.
Actualiza docs/functional/[nombre_módulo].md si existe, o crea la página si no hay equivalente.
Actualiza mkdocs.yml si se crea o mueve una página.
No inventes capacidades; si falta información, márcala como pendiente.
```

### Modo módulo único — Copilot Chat

```
#file:.github/prompts/functional_doc.prompt.md
#file:[ruta_del_módulo]

Genera la documentación funcional del módulo indicado siguiendo las instrucciones del prompt.
```

### Modo proyecto completo (iterativo por módulo)

No uses un único prompt masivo. Recorre el proyecto en fases:

```
Fase 1 — Inventariar módulos públicos desde scripts/.
  Lista todos los módulos exportados en __init__.py o __all__; agrúpalos por área.

Fase 2 — Para cada módulo (o área), aplica functional_doc.prompt.md:
  "Lee [ruta] y genera docs/functional/[nombre].md.
   Marca como pendiente cualquier sección no verificable."

Fase 3 — Actualizar mkdocs.yml:
  Añade o actualiza entradas en la sección docs/functional/ del nav.

Fase 4 — Revisión cruzada:
  Contrasta cada página generada con docs/api/ y docs/examples/
  para detectar inconsistencias.
```

## Prompt para diagramas Mermaid

Para generar únicamente el diagrama de secuencia de un módulo:

```
Basándote en la lógica del módulo [Nombre], genera exclusivamente el código Mermaid.js
para un diagrama de secuencia que ilustre la interacción entre los actores y el sistema,
omitiendo detalles de implementación (clases internas, rutas, variables).
Usa etiquetas en español. Máximo 12 nodos. Incluye puntos de decisión relevantes.
```

## Output esperado

Un fichero Markdown con:
- Título H1
- 8 secciones numeradas (`## 1.` — `## 8.`)
- Al menos un diagrama Mermaid (`sequenceDiagram` o `stateDiagram-v2`) en `## 3.`
- Tabla en `## 5.` con 3 columnas
- `## 7.` con tabla Given/When/Then (`| ID | Dado | Cuando | Entonces |`) y/o placeholder QA estructurado
- `## 8.` con tabla de términos o `*No aplica para este módulo.*`
