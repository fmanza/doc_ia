# 📚 Especificación de Estandarización de Documentación

Objetivo: Unificar la estructura de documentación técnica, funcional y general en **doc_ia**
y definir un flujo de trabajo repetible para otros proyectos con IA.

---

## 1. Objetivo

Estandarizar instrucciones de documentación para asegurar:
- **Claridad de usuario**: Documentación funcional orientada a "qué puedo hacer"
- **Claridad de desarrollador**: Documentación técnica orientada a "cómo funciona internamente"
- **Mantenibilidad**: Estructura agnóstica al lenguaje, fácil de auditar y actualizar
- **Automatización**: Generación de docs con agentes, validación con CI/CD
- **Versionamiento**: Sincronización CHANGELOG.md y COMPATIBILITY.md con releases

---

## 2. Estado Actual

### 2.1 Estructura MkDocs
- **Site**: `mkdocs.yml` (v1.5+, Material theme) — fuente única; no se usa `zensical.toml`
- **Webs de referencia oficial** (consultar con `--verify-tools` para validar versiones y plugins):
  - MkDocs: `https://www.mkdocs.org/about/release-notes/`
  - Material for MkDocs: `https://squidfunk.github.io/mkdocs-material/plugins/`
  - Zensical: `https://zensical.org/`
- **Secciones existentes**:
  - ✅ Guías (DUPLICATE_PROJECT_GUIDE, NEXT_STEPS, README_DUPLICADOR, ARCHITECTURE_VISUAL)
  - ✅ Funcional (`docs/functional/`) — 8 módulos
  - ✅ Ejemplos (`docs/examples/`) — 10+ ejemplos de uso
  - ✅ API/Referencias (`docs/api/`) — 8 módulos técnicos
  - ✅ Compatibilidad y Changelog

### 2.2 Archivos Generados
- Funcional: 8 archivos en `docs/functional/`
- Técnico: 8 archivos en `docs/api/`
- Generador: mkdocstrings integrado (Python docstrings → HTML)

### 2.3 Herramientas y Agentes
| Componente | Ubicación | Estado |
|------------|-----------|--------|
| **Configuración IA** | `CLAUDE.md`, `copilot-instructions.md` | ✅ Existente |
| **Agent: config-reviewer** | `.github/agents/config-reviewer.agent.md` | ✅ Existente |
| **Agent: documentation-generator** | `.github/agents/documentation-generator.agent.md` | ✅ Existente — soporta `--verify-tools` |
| **Agent: documentation-reviewer** | `.github/agents/documentation-reviewer.agent.md` | ✅ Existente |
| **Prompt: config_review** | `.github/prompts/config_review.prompt.md` | ✅ Existente |
| **Prompt: functional_doc** | `.github/prompts/functional_doc.prompt.md` | ✅ Existente |
| **Prompt: technical_doc** | `.github/prompts/technical_doc.prompt.md` | ✅ Existente |
| **Prompt: landing_doc** | `.github/prompts/landing_doc.prompt.md` | ✅ Existente |
| **Prompt: documentation_review** | `.github/prompts/documentation_review.prompt.md` | ✅ Existente |

### 2.4 Gaps Actuales
- ✅ Referencia OneDrive → reemplazada por referencias internas al repositorio (§4)
- ✅ Estructura funcional y técnica → mapeada explícitamente en §4.2
- ✅ Roles de agentes → documentados en orden de ejecución en §5
- ⚠️ Seguridad y Rendimiento → cubiertos como opcionales en §3.2 y §4.3; excluidos del nav por defecto

---

## 3. Propuesta de Cambios

### 3.1 Arquetipo 1 — Documentación Funcional (`docs/functional/`)

**Propósito**: Responder "¿Qué hace y por qué?"

**Audiencia**: Product Owner, QA, responsables de negocio.

**Ubicación**: `docs/functional/[módulo].md`

**Estructura obligatoria** (secciones numeradas, en este orden):

```
# [Título del Módulo/Funcionalidad]

## 1. Descripción General
Contexto de negocio y objetivo (2-3 párrafos, sin jerga técnica).

## 2. Reglas de Negocio
Tabla: | Regla | Descripción | Impacto si se viola |

## 3. Casos de Uso
### Flujo principal
Diagrama Mermaid sequenceDiagram (actor → módulo → salida).
### Flujos alternativos y de error
Variantes y casos de error verificables. Si no hay, "No aplica para este módulo."

## 4. Criterios de Aceptación      ← EJECUTABLE — derivar del código real
Tabla: | ID | Dado | Cuando | Entonces |
Derivar los criterios del código cuando sea posible (mismo formato que
functional_doc.prompt.md §7). Cerrar con el comando de verificación real.
Subsección "Pendiente de validación QA" SOLO para criterios no derivables
del código (fallback, no primera opción); si no hay, omitirla.

## 5. Glosario y Términos
Tabla: | Término | Definición |
Si no hay términos específicos: "No aplica para este módulo."
```

**Regla de sección vacía**: Si un subapartado queda vacío, escribe `*No aplica para este módulo.*` — nunca omitas la sección.

**Diagramas recomendados**: `sequenceDiagram` (flujo principal), `flowchart TD` (decisiones),
`stateDiagram-v2` (cuando el módulo tiene un ciclo de vida con estados discretos y transiciones).
Ver criterios de selección y niveles de prescripción en `docs.instructions.md`.

---

### 3.2 Arquetipo 2 — Documentación Técnica (`docs/api/`)

**Propósito**: Responder "¿Cómo está construido?"

**Audiencia**: desarrolladores que mantienen el tooling o extienden las instrucciones IA.

**Ubicación**: `docs/api/[módulo].md`

**Nota**: Los archivos generados automáticamente por herramientas autodoc (si se incorporan) quedan excluidos de este arquetipo.

**Estructura obligatoria** (secciones numeradas, en este orden):

```
# [Nombre del Componente/Módulo]

[Párrafo introductorio de una frase: responsabilidad exacta del módulo.]

## 1. Arquitectura y Diseño
Diagrama Mermaid (flowchart TD, classDiagram, sequenceDiagram, architecture-beta,
stateDiagram-v2 o erDiagram). Máximo 12 nodos. Ver criterios de selección y niveles
de prescripción en docs.instructions.md.

## 2. Modelo de Datos / Contratos
### API pública
Tabla: | Función/Clase | Firma simplificada | Descripción | Retorna |
### Contrato de entrada
Tabla: | Parámetro | Tipo | Descripción | Restricciones |
### Contrato de salida
Tipos, estructura y casos especiales.
### Errores y casos especiales
Excepciones propias del módulo y entradas inválidas.

## 3. Componentes y Clases
Responsabilidad de cada clase exportada.
Para módulos con una sola clase: "No aplica para este módulo."

## 4. Dependencias y Requisitos
Tabla: | Dependencia | Propósito | Requerida | Comportamiento sin ella |

## 5. Ejemplos Relacionados      ← OBLIGATORIO (enlace bidireccional con Arquetipo 4 §5)
Lista de enlaces a docs/examples/ con descripción de lo que ilustra cada uno.
Si no existe ningún ejemplo del módulo: "Pendiente — crear ejemplo en docs/examples/[nombre].md"
```

**Regla de sección vacía**: Si un subapartado queda vacío, escribe `*No aplica para este módulo.*`.

**Diagramas recomendados**: Ver tabla en `docs.instructions.md` y en `technical_doc.prompt.md`.

---

### 3.3 Arquetipo 3a — How-to (`docs/guides/`)

**Propósito**: Responder "¿Cómo resuelvo este problema concreto?"

**Diátaxis**: cuadrante *How-to* — orientado a **tarea**, asume conocimiento base, no enseña por qué.

**Diferencia con Tutorial (Arquetipo 3b, §3.11)**: Un how-to resuelve un problema concreto en el menor número de pasos; no explica el contexto ni guía el aprendizaje. Un tutorial lleva al lector por una experiencia de aprendizaje progresiva donde aprende haciendo.

**Audiencia**: usuarios finales, operadores y desarrolladores que quieren resolver una tarea específica.

**Ubicación**: `docs/guides/[nombre]_howto.md` o `docs/guides/[nombre]_guide.md`

**Prompt**: `.github/prompts/howto_doc.prompt.md`

**Estructura obligatoria** (secciones numeradas, en este orden):

```
# Cómo [verbo + objeto concreto]

## 1. Objetivo
Una frase: qué conseguirás. Verbos imperativos ("instala", "configura", "verifica").

## 2. Requisitos Previos
Lista: herramientas, versiones, accesos o estado inicial requerido.

## 3. Pasos
Procedimiento secuencial numerado con bloques de código.
Cada paso atómico, ejecutable y verificable de forma independiente.

## 4. Verificación
Comando exacto + output esperado para confirmar éxito.

## 5. Variantes y Solución de Problemas
Tabla: | Escenario/Error | Causa probable | Solución |
Si no hay casos conocidos: "No aplica para este módulo."
```

**Excepciones aceptadas**: `docs/index.md` y `docs/legacy-versions.md` están exentos de arquetipo (páginas especiales).

---

### 3.4 Arquetipo 4 — Guías de Ejemplos de Código (`docs/examples/`)

**Propósito**: Responder "¿Cómo se implementa?"

**Audiencia**: desarrolladores que quieren implementar un patrón concreto.

**Ubicación**: `docs/examples/[nombre].md`

**Estructura obligatoria** (secciones numeradas, en este orden):

```
# Ejemplo: [Nombre del Patrón/Funcionalidad]

## 1. Contexto del Ejemplo
Qué problema concreto resuelve este código (1-2 párrafos).

## 2. Implementación de Referencia
Exclusivamente: --8<-- "examples/[ruta].py"

## 3. Explicación del Código
Puntos críticos: concurrencia, rendimiento, contratos.
Para ejemplos triviales: "No aplica para este módulo."

## 4. Ejecución y Pruebas
Comando exacto + output esperado si determinista.

## 5. Referencias Relacionadas      ← OBLIGATORIO (enlace bidireccional con Arquetipo 2 §5)
- Documentación funcional: [enlace a docs/functional/...]
- Referencia técnica: [enlace a docs/api/...]
- Ejemplos relacionados: [otros ejemplos del mismo área si existen]
```

**Regla de snippet**: En `## 2.` usar siempre `--8<--`. Si el `.py` no existe, crearlo antes de referenciar.

---

### 3.5 Arquetipo 5 — Decisión Arquitectónica / ADR (`docs/adr/`)

**Propósito**: Responder "¿Por qué se decidió así?"

**Diátaxis**: cuadrante *Explanation* — razonamiento y contexto de una decisión concreta.

**Estándar**: **MADR 4.0** (Markdown Any Decision Records, septiembre 2024 — [adr.github.io/madr](https://adr.github.io/madr/)).

**Audiencia**: arquitectos de software, tech leads, responsables de plataforma.

**Ubicación**: `docs/adr/ADR-[NNN]-[nombre-kebab-case].md`

**Prompt**: `.github/prompts/architecture_doc.prompt.md`

**Formatos disponibles**:
- **Full** (decisiones críticas con múltiples opciones y consecuencias complejas)
- **Minimal** (decisiones pequeñas: solo Contexto, Decisión, Consecuencias)

**Estructura obligatoria — formato Full**:

```markdown
---
status: "PROPUESTO | ACEPTADO | OBSOLETO | REEMPLAZADO POR ADR-NNN"
date: YYYY-MM-DD
deciders: [nombres o roles]
consulted: [nombres o roles]
informed: [nombres o roles]
---

# Use [Solución] for [Contexto/Problema]   ← Título en forma "Use X for Y"

## Contexto y Problema
Estado anterior, problema identificado, fuerzas en conflicto.

## Decisión
Enunciado claro + justificación breve vs alternativas.

## Consecuencias
Tabla: | Tipo | Descripción |
Tipos: Ventaja / Compromiso (trade-off) / Deuda técnica / Riesgo aceptado

## Alternativas Consideradas
Tabla: | Alternativa | Pros | Contras | Motivo rechazo |
Si no documentadas: "No aplica para este módulo."

## Estado y Revisión
Estado explícito + fecha YYYY-MM-DD.
Si reemplaza a otro ADR: enlazar con "Reemplaza a [ADR-NNN]".
```

**Estructura obligatoria — formato Minimal**:

```markdown
---
status: "PROPUESTO | ACEPTADO | OBSOLETO"
date: YYYY-MM-DD
---

# Use [Solución] for [Contexto/Problema]

## Contexto y Problema
## Decisión
## Consecuencias
```

**Cuándo usar cada formato**:
- Full: decisiones que afectan API pública, eligen entre ≥2 enfoques con trade-offs, introducen/eliminan dependencia significativa, o establecen patrón reutilizable.
- Minimal: decisiones de alcance acotado, tiempo limitado para documentar, o como placeholder hasta completar el Full.

Documenta **una decisión concreta con trade-offs**, no la visión global del sistema (esa es la Variante C del Arquetipo 6). Los documentos de planificación (roadmap, release plans) se marcan con `<!-- arquetipo: informativo-libre -->` y quedan exentos.

---

### 3.6 Arquetipo 6 — Páginas de Navegación Principal (`docs/` raíz)

**Propósito**: Responder "¿Qué es, cómo lo instalo y cómo está organizado?" en las páginas de entrada.

**Audiencia**: cualquier visitante que llega a la documentación por primera vez.

**Ubicación**: `docs/index.md` (Inicio), `docs/installation.md` (Instalación), `docs/architecture.md` (Arquitectura).

**Prompt**: `.github/prompts/landing_doc.prompt.md` (tres variantes A/B/C, 5 secciones cada una).

Estas páginas entran directamente en `nav:` (nivel raíz), no bajo `functional/`, `api/`, `examples/` ni `adr/`:

- **Variante A — Inicio**: Identidad y Propósito → Capacidades → Quick Start → Mapa de la Documentación → Compatibilidad y Soporte.
- **Variante B — Instalación**: Requisitos → Instalación del Paquete → Drivers por Motor → Verificación → Solución de Problemas.
- **Variante C — Arquitectura** (modelo **arc42-lite + C4**): Visión General y Objetivos de Calidad (C4 nivel 1) → Mapa de Módulos / Building Blocks (C4 nivel 3) → Flujo en Ejecución (Runtime) → Conceptos Transversales y Estándares No Funcionales (checklist NFR) → Decisiones, Extensión y Límites (enlace a `docs/adr/`).
- **Variante D — Quick Start**: Prerequisito mínimo → Primer comando → Primer resultado visible → Siguiente paso sugerido. Objetivo: tiempo hasta la primera experiencia exitosa < 5 min. Ubicación: `docs/quickstart.md`. Audiencia: visitante que llega por primera vez y quiere ver el producto funcionando antes de leer la documentación completa. No sustituye a la Variante B (instalación detallada); enlaza a ella al final.

**Distinción con otros arquetipos**:
- El Arquetipo 5 (`architecture_doc`) documenta **un ADR concreto** (decisión con trade-offs, formato MADR-lite); la Variante C es la **vista panorámica del sistema** (arc42-lite + C4) y enlaza al log de ADR. Ambas conviven bajo la sección "Arquitectura" del nav y forman un modelo único: panorámica + decisiones.
- El Arquetipo 3 (`guide_doc`) cubre guías genéricas (async, drivers, troubleshooting); la Variante B es específica de instalación del paquete y drivers.

**Excepción**: `docs/index.md` y `docs/legacy-versions.md` seguían exentos en v1; con este arquetipo `index.md` pasa a regirse por la Variante A. `legacy-versions.md` permanece exento.

---

### 3.7 Arquetipo 7 — Guía de Incorporación para Desarrolladores (`docs/ONBOARDING_DEV.md`)

**Propósito**: Responder "¿Cómo me incorporo al proyecto y pongo en marcha mi entorno?"

**Audiencia**: desarrolladores que se incorporan al proyecto por primera vez.

**Ubicación**: `docs/guides/onboarding_dev.md` (todos los proyectos — mismo convenio que el resto de guías)

**Prompt**: `.github/prompts/onboarding_dev.prompt.md`

**Secciones obligatorias** (11, en este orden):

```
## 1. Prerequisitos del Entorno      — tabla: Herramienta | Versión mínima | Verificar con | Notas
## 2. Obtener el Código              — clone, rama de trabajo, submódulos/dependencias privadas
## 3. Configurar el Entorno          — venv/IDE, credenciales, registros privados, ficheros de config
## 4. Primera Compilación/Instalación — comando principal + tabla de errores frecuentes
## 5. Infraestructura Local           — BD, contenedores, servicios; "*No aplica*" si librería stateless
## 6. Ejecutar la Aplicación          — puertos, URLs, credenciales; "*No aplica*" si librería
## 7. Mapa del Código                 — árbol simplificado, responsabilidad por módulo/paquete, regla de capas
## 8. Convenciones y Herramientas     — lint, format, tipos, tests — verificar contra SHARED_INSTRUCTIONS.md
## 9. Flujo de Trabajo Git            — ramas, Conventional Commits, PR/MR
                                        Diagrama recomendado: `gitgraph` cuando el proyecto
                                        tiene branching definido (main + feature + release)
## 10. Verificación del Entorno       — tabla: Verificación | Comando | Output esperado
## 11. Recursos y Referencias         — .ai/*.md, docs/ relevantes, normativa, contacto
```

**Regla de sección vacía**: §5 y §6 **siempre** están presentes. Si el proyecto no requiere infraestructura o no tiene servidor, escribir `*No aplica para este proyecto.*` con explicación breve. Nunca omitir la sección.

**Distinción con Arquetipo 3** (Guías de Usuario):
- Arquetipo 3 documenta **cómo usar o configurar una funcionalidad** (guía how-to para usuarios finales).
- Arquetipo 7 documenta **cómo unirse al equipo de desarrollo** (entorno, código, convenciones, workflow).

**Cuándo actualizar**: en cada release mayor, tras cambios de stack o infraestructura, o cuando un nuevo desarrollador detecte que la guía está desactualizada.

---

### 3.8 Arquetipo 8 — Trazabilidad Normativa (`docs/normativa/`) — **Condicional**

**Propósito**: Responder "¿Qué obligaciones legales o reglamentarias están cubiertas por este sistema?"

**Condición de activación**: SOLO si el proyecto hace referencia explícita a leyes, decretos,
directivas, normas UNE o cualquier normativa de obligado cumplimiento. Verificar en `.ai/product.md`
o `README.md`. Si no hay normativa de referencia → **este arquetipo no aplica** y la carpeta
`docs/normativa/` no se crea.

> **Este proyecto (doc_ia)**: sistema de instrucciones IA y tooling determinista de documentación,
> sin normativa de referencia explícita. El arquetipo no aplica actualmente. Si en el futuro se
> incorpora normativa (ej. RGPD para datos de proyectos documentados, accesibilidad), aplicar entonces.

**Audiencia**: auditores de cumplimiento, técnicos de normativa, responsables de proyecto.

**Ubicación**: `docs/normativa/<abbrev_norma>_traceability.md`  
**Naming**: nombre en minúsculas con guión bajo (ej. `ley39_rd174_traceability.md`, `rgpd_traceability.md`)

**Estructura obligatoria** (secciones en este orden):

```
# Trazabilidad Normativa — <Nombre de las normas>

(versión del sistema analizado + fecha de revisión)

## Propósito

## 1. <Norma A> — <Nombre corto>
  ### 1.1 <Grupo de artículos>
  Tabla: | Artículo | Obligación | Módulo/servicio | Doc de referencia | Cobertura |
  ### ...

## 2. <Norma B> — ...

## N. Resumen de gaps por severidad
  ### Nivel 1 — Crítico (riesgo de incumplimiento o auditoría bloqueada)
  Tabla: | ID | Gap | Norma | Módulo afectado | Acción recomendada |
  ### Nivel 2 — Importante (gap documental, dificulta mantenimiento)
  ### Nivel 3 — Mejora

## N+1. Normativa complementaria referenciada
Tabla: | Norma | Objeto | Cobertura en el sistema |

## N+2. Próximas acciones priorizadas
```

**Leyenda de cobertura**:

| Símbolo | Significado |
|---------|-------------|
| ✅ | Cubierto — implementado y documentado |
| ⚠️ | Parcial — implementado pero con gap documental o funcional conocido |
| ❌ | Gap — no implementado o sin documentación verificable |
| 🔍 | A verificar — evidencia insuficiente para determinar cobertura |

**Sección MkDocs** (solo si el arquetipo aplica):

```yaml
- Normativa:                                                     # Entre "Funcional" y "Arquitectura"
    - Trazabilidad <Nombre norma>: normativa/<codigo>_traceability.md
```

**Cuándo crear**: al comenzar el proyecto si la normativa es conocida desde el inicio, o en la
primera auditoría de cumplimiento formal.

**Cuándo actualizar**:
- Cuando cambia la normativa de referencia (modificación legal, nuevo artículo)
- Cuando se implementa un módulo que cubre un gap documentado
- En cada revisión de versión mayor que afecte lógica de negocio regulada

**Restricciones estrictas**:
- No inventar contenido normativo sin verificar contra el texto oficial
- Marcar como 🔍 cualquier artículo sin evidencia suficiente en código o documentación
- No documentar como ✅ ningún artículo sin módulo del sistema identificado
- No copiar texto legal verbatim; describir la obligación en términos del sistema

**Prompt de generación**: `.github/prompts/normative_traceability.prompt.md`

---

### 3.9 Estándar de la Sección Guías (`docs/guides/`)

Esta sección define el contrato mínimo y las reglas de nomenclatura para **todos los proyectos**.

#### Convenio de nombres

| Regla | Correcto | Incorrecto |
|---|---|---|
| Nombre en minúsculas | `connection_guide.md` | `CONNECTION_GUIDE.md` |
| Palabras con guión bajo | `async_guide.md` | `async-guide.md`, `asyncGuide.md` |
| Ubicación siempre en `guides/` | `docs/guides/troubleshooting.md` | `docs/TROUBLESHOOTING.md` |
| Sin subcarpetas dentro de `guides/` | `guides/deployment_guide.md` | `guides/ops/deployment.md` |

#### Conjunto mínimo obligatorio

| Fichero | Arquetipo | Contenido | Mandatorio |
|---|---|---|---|
| `guides/onboarding_dev.md` | 7 | Incorporación: entorno, código, convenciones, verificación | ✅ Siempre |
| `guides/troubleshooting.md` | 3a | Problemas frecuentes por categoría + solución verificable | ✅ Siempre |
| `CONTRIBUTING.md` (raíz) | 11 | Proceso de contribución, convenciones, calidad | ⚙️ Opt-in — no generado por defecto |
| `CHANGELOG.md` (raíz) | 9 | Historial de cambios por versión (Keep a Changelog) | ⚙️ Opt-in — no generado por defecto |

#### Guías adicionales según tipo de proyecto

| Tipo de proyecto | Guías recomendadas |
|---|---|
| Tooling de documentación (doc_ia) | guías de plataformas IA (`claude_code_guide.md`, `codex_guide.md`, …) — `downloads.md` es página estándar top-level, no una guía |
| Aplicación con servidor (dpss) | `despliegue_docker.md` o `deployment_guide.md` |
| Cualquier proyecto con herramientas IA | Subsección "Herramientas IA" en Guías: claude_code_guide.md, codex_guide.md, etc. |

#### Estructura de la sección en `mkdocs.yml`

```yaml
- Guías:
    - Incorporación para Desarrolladores: guides/onboarding_dev.md   # Siempre primero
    - [Grupos operativos según el proyecto]:                           # Conexión, Despliegue, etc.
        - [Guía específica]: guides/[nombre_guia].md
    - Errores y Diagnóstico:
        - Troubleshooting: guides/troubleshooting.md                  # Siempre en esta subsección
    - Herramientas IA:                                                 # Si el proyecto usa herramientas IA
        - [Nombre herramienta]: guides/[tool]_guide.md
```

#### Cuándo actualizar

- Al incorporar el primer desarrollador externo → generar `onboarding_dev.md` si no existe.
- Tras cambios de stack, build tool o infraestructura → actualizar `onboarding_dev.md`.
- Cuando se reporta un error no documentado → añadir a `troubleshooting.md`.
- Cuando se añade una herramienta IA nueva → añadir su guía en Herramientas IA.

---

### 3.10 Documentación con Múltiples Orígenes

Cuando `/document-project` recibe más de un `Origen`, o cuando el único origen no es un proyecto de código, es obligatorio ejecutar la **Fase 0a — Clasificación de orígenes** antes de inventariar.

#### Tipos de origen

| Tipo | Señales de detección | Tratamiento documental |
|------|---------------------|----------------------|
| `CÓDIGO` | Archivos fuente (`.py`, `.js`, `.ts`, `.cs`, `.java`, `.go`, `.rs`, …), `pyproject.toml`, `package.json`, `pom.xml`, `Cargo.toml`, `go.mod`, `src/`, `tests/` | Documentar como proyecto: inventario completo + arquetipos 1–7 |
| `NORMATIVA` | PDFs/docs con palabras clave en nombre: `ley`, `decreto`, `directiva`, `rgpd`, `gdpr`, `une`, `iso`, `reglamento`, `compliance` | Activar Arquetipo 8; enriquece §2 (Reglas de Negocio) del Arquetipo 1 del proyecto principal |
| `ESPECIFICACIÓN` | Word/PDF de requisitos, user stories, pliego, casos de uso; ficheros `.feature` (BDD/Gherkin); carpetas `specs/`, `requirements/`, `ux/`, `user-stories/` | Enriquece Arquetipo 1 §2+§3+§4 del proyecto principal |
| `UI/PANTALLAS` | Wireframes, mockups, capturas (`.png`, `.jpg`, `.pdf` de diseño); carpetas `mockups/`, `screens/`, `wireframes/`, `figma-exports/` | Enriquece Arquetipo 1 §3 (Casos de Uso) y Arquetipo 3 (Guías) |
| `REFERENCIA` | Manuales de terceros, RFCs, especificaciones de protocolo **ajenas al proyecto** | Enriquece Arquetipo 2 §4 (Dependencias) o Arquetipo 5 (ADR) |
| `CONTRATO` | Especificaciones machine-readable de las APIs/datos del **propio proyecto**: `.yaml`/`.json` con clave `openapi:` o `asyncapi:`; `.graphql`/`.gql`; `.proto`; `.avsc`; `.sql` DDL en `db/`/`migrations/`; `.dbml`; carpetas `api/`, `contracts/`, `schemas/`, `proto/` | Enriquece Arquetipo 2 §1 (Arquitectura) y §2 (Modelo de Datos / Contratos) |
| `INFRAESTRUCTURA` | IaC y despliegue: `.tf`; `Dockerfile`, `docker-compose.yml`; YAML en `k8s/`, `deploy/`, `manifests/`, `helm/`; playbooks Ansible; CloudFormation en `cloudformation/` | Enriquece Arquetipo 2 §4 (Dependencias) y Arquetipo 6D (Arquitectura — vista despliegue) |
| `MANUAL` | Documentación narrativa del **propio proyecto**: `.pdf`, `.docx`, `.md` con `manual`/`guide`/`runbook`/`ayuda`/`help` en nombre; carpetas `manuals/`, `help/`, `user-docs/`; `.chm` | Enriquece Arquetipos 3a §3, 3b §3, 6A/B §1 (Descripción) y 7 §3+§5 |

**Regla**: la autodetección propone el tipo; el usuario confirma antes de continuar al INVENTARIO. Nunca se asume el tipo sin confirmación.

**Caso degenerado**: si no hay ningún origen de tipo `CÓDIGO`, `/document-project` no aplica. Usar directamente el prompt de arquetipo correspondiente (`normative_traceability.prompt.md`, `functional_doc.prompt.md`, etc.).

#### Mapeo MATERIAL → arquetipos (referencia rápida)

| Tipo origen | Arquetipo | Sección(es) que enriquece |
|-------------|-----------|--------------------------|
| `NORMATIVA` | 8 + 1 (proyecto principal) | Arq. 8 completo; Arq. 1 §2 Reglas de Negocio |
| `ESPECIFICACIÓN` | 1 (proyecto principal) | §2 Reglas de Negocio, §3 Casos de Uso, §4 Criterios de Aceptación |
| `UI/PANTALLAS` | 1 + 3 | Arq. 1 §3 Casos de Uso; Arq. 3 §3 Pasos |
| `REFERENCIA` | 2 o 5 | Arq. 2 §4 Dependencias; o Arq. 5 (decisión ADR) |
| `CONTRATO` | 2 (proyecto principal) | §1 Arquitectura (interfaces publicadas); §2 Modelo de Datos / Contratos |
| `INFRAESTRUCTURA` | 2 + 6 | Arq. 2 §4 Dependencias y Requisitos; Arq. 6D §3 (vista despliegue) |
| `MANUAL` | 3a · 3b · 6 · 7 | Arq. 3a §3 Pasos; Arq. 3b §3; Arq. 6A/B §1; Arq. 7 §3 y §5 |

Los orígenes MATERIAL **no generan páginas propias** en `docs/`; su contenido enriquece las secciones indicadas de los arquetipos del proyecto principal.

#### Estrategia para múltiples orígenes CÓDIGO

Cuando hay ≥2 orígenes de tipo `CÓDIGO`, el agente pregunta al usuario la estrategia (nunca la autodetecta):

| Estrategia | Descripción | Cuándo elegir |
|------------|-------------|---------------|
| `federado` | Cada proyecto tiene su propio `docs/` y `mkdocs.yml` independientes | Repos separados, equipos distintos, sin destino compartido |
| `hub+satélite` | Un proyecto "hub" concentra el destino; los demás se documentan como secciones dentro de él | Un destino claro, uno de los proyectos es el consumidor de los demás |
| `monorepo` | Un `mkdocs.yml` raíz agrupa secciones por proyecto | Monorepo, mismo equipo, mismo destino para todos |

Con estrategia `hub+satélite`, el INVENTARIO genera un sub-inventario por proyecto; el PLAN_DOC indica qué secciones del `mkdocs.yml` del hub reciben las páginas de los satélites.

---

### 3.11 Arquetipo 3b — Tutorial Guiado (`docs/guides/`)

**Propósito**: Responder "¿Cómo aprendo a usar esto paso a paso?"

**Diátaxis**: cuadrante *Tutorial* — orientado a **aprendizaje**, el lector aprende haciendo bajo guía.

**Diferencia con How-to (Arquetipo 3a, §3.3)**: Un tutorial lleva al lector por una experiencia de aprendizaje progresiva; incluye el "por qué funciona esto", permite y anticipa errores, y finaliza con reflexión sobre lo aprendido. No asume conocimiento previo del área.

**Audiencia**: usuarios que se acercan a la funcionalidad por primera vez y necesitan ser guiados.

**Ubicación**: `docs/guides/[nombre]_tutorial.md`

**Prompt**: `.github/prompts/tutorial_doc.prompt.md`

**Estructura obligatoria** (secciones numeradas, en este orden):

```
# Tutorial: [Qué aprenderás a hacer]

## 1. Qué aprenderás
Resultado concreto al final del tutorial (1 párrafo). Listado de habilidades adquiridas.

## 2. Antes de empezar
Herramientas, versiones, estado inicial. Nivel de conocimiento esperado.

## 3. [Fase/Paso 1 — nombre descriptivo]
Acción + explicación de por qué funciona. Código ejecutable.
Subsección: "¿Qué ha pasado?" — reflexión sobre lo ocurrido.

## 4. [Fase/Paso 2 — nombre descriptivo]
(Repetir patrón: acción → por qué → reflexión)

## N. Resumen y Siguientes Pasos
Qué has aprendido. Enlace a guías how-to relacionadas (Arquetipo 3a) para uso en producción.
```

**Reglas**:
- Cada fase termina con un estado verificable (el lector sabe que ha tenido éxito).
- Anticipar y explicar errores frecuentes dentro de la fase donde ocurren, no en una sección al final.
- Mantener un hilo narrativo: el lector construye algo a lo largo del tutorial.
- Distinguir `guides/*_tutorial.md` (tutorial) de `guides/*_guide.md` / `guides/*_howto.md` (how-to) en el nombre de fichero.

---

### 3.12 Arquetipo 9 — Changelog / Release Notes (`CHANGELOG.md`)

**Propósito**: Registrar cronológicamente los cambios significativos por versión para usuarios y mantenedores.

**Estándar**: [Keep a Changelog](https://keepachangelog.com/) v1.1.0 + [Semantic Versioning](https://semver.org/).

**Audiencia**: usuarios finales, QA, ops, decisores que necesitan saber qué cambió y cuándo.

**Ubicación**: `CHANGELOG.md` (raíz del repositorio — fichero único). Enlazar desde `nav:` como entrada directa.

**Prompt**: `.github/prompts/changelog.prompt.md`

**Estructura obligatoria**:

```markdown
# Changelog

Todos los cambios notables de este proyecto se documentan aquí.
Formato: [Keep a Changelog](https://keepachangelog.com/) · Versioning: [SemVer](https://semver.org/)

## [Unreleased]
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

## [X.Y.Z] — YYYY-MM-DD
### Added
- Descripción de nueva funcionalidad.
### Fixed
- Descripción de bug corregido.

[Unreleased]: https://github.com/[usuario]/[repo]/compare/vX.Y.Z...HEAD
[X.Y.Z]: https://github.com/[usuario]/[repo]/compare/vX.Y.Z-1...vX.Y.Z
```

**Categorías permitidas** (en este orden dentro de cada versión):

| Categoría | Cuándo usarla |
|-----------|--------------|
| `Added` | Nueva funcionalidad (retrocompatible) |
| `Changed` | Cambio en funcionalidad existente |
| `Deprecated` | Funcionalidad marcada para eliminación futura |
| `Removed` | Funcionalidad eliminada |
| `Fixed` | Corrección de bug |
| `Security` | Corrección de vulnerabilidad |

**Reglas**:
- Mantener siempre una sección `[Unreleased]` al inicio.
- Al hacer release: renombrar `[Unreleased]` a `[X.Y.Z] — YYYY-MM-DD` y crear nueva `[Unreleased]` vacía.
- Entradas en pasado o forma nominal ("Añade X", "Corrige Y"); nunca "Vamos a añadir...".
- No documentar cada commit; solo cambios con impacto para el usuario o integrador.
- Actualizar en sincronía con `pyproject.toml` / `package.json` (ver `.github/instructions/sync.instructions.md`).

**Sección MkDocs** (siempre presente si el proyecto tiene CHANGELOG.md):

```yaml
- Changelog: changelog.md   # Entrada directa en nav raíz o bajo "Proyecto"
```

---

### 3.13 Arquetipo 10 — Configuración de Agente IA (`docs/ai-config/`)

**Propósito**: Documentar las instrucciones de sistema, permisos, comandos y automatizaciones configuradas para cada plataforma de IA en el proyecto.

**Origen**: Arquetipo propio de doc_ia — no existe estándar externo para este tipo de documento en 2024-2025. El proyecto lo define e implementa como referencia.

**Audiencia**: desarrolladores que integran, configuran o auditan agentes IA en el proyecto; equipos que replican la configuración en otros proyectos.

**Ubicación**: `docs/ai-config/[plataforma].md` (ej: `claude.md`, `gemini.md`, `copilot.md`)

**Prompt**: `.github/prompts/ai_config_doc.prompt.md`

**Estructura obligatoria** (secciones numeradas, en este orden):

```
# Configuración de [Nombre Plataforma IA]

[Versión del modelo objetivo] [Fecha de revisión]

## 1. Plataforma y Modelo
Nombre, versión mínima del modelo, fichero de configuración fuente (CLAUDE.md, copilot-instructions.md, etc.).

## 2. Contexto Obligatorio
Lista de ficheros que el agente debe leer antes de actuar:
- [fichero] — propósito

## 3. Comandos y Slash Commands
Tabla: | Comando | Propósito | Inputs obligatorios | Outputs |

## 4. Permisos y Herramientas
Tabla: | Herramienta/Acción | Permitida | Condición |
Basada en el fichero de configuración real (settings.json, etc.).

## 5. Hooks y Automatizaciones
Tabla: | Evento | Comando ejecutado | Propósito |
Si no hay hooks: "No aplica para esta configuración."

## 6. Restricciones Explícitas
Lista de lo que el agente nunca debe hacer en este proyecto (derivado de la sección prohibiciones del fichero fuente).

## 7. Casos Límite Conocidos
Lista de comportamientos inesperados documentados (de EDGE_CASES.md si existe).
Si no hay: "No aplica para esta configuración."
```

**Reglas**:
- Derivar el contenido del fichero fuente real (CLAUDE.md, copilot-instructions.md, etc.) — no inventar permisos ni comandos.
- Actualizar cuando cambie el fichero fuente o se añadan hooks.
- La sección §4 debe reflejar el estado real de `settings.json` o equivalente.

**Sección MkDocs** (solo si el proyecto tiene ≥1 plataforma IA configurada):

```yaml
- Configuración IA:
    - Claude Code: ai-config/claude.md
    - GitHub Copilot: ai-config/copilot.md
```

---

### 3.14 Arquetipo 11 — Guía de Contribución (`CONTRIBUTING.md`)

**Propósito**: Explicar cómo contribuir al proyecto (issues, PRs, convenciones, proceso de release).

**Diferencia con Arquetipo 7 (Onboarding Dev)**: El onboarding es para quien se incorpora al equipo y trabaja en el día a día; esta guía es para colaboradores externos o primeras contribuciones puntuales.

**Audiencia**: contribuidores externos, colaboradores ocasionales, usuarios que quieren reportar bugs o proponer mejoras.

**Ubicación**: `CONTRIBUTING.md` (raíz del repositorio — fichero único). Enlazar desde `README.md` y desde `nav:`.

**Prompt**: `.github/prompts/contributing_doc.prompt.md`

**Estructura obligatoria** (secciones numeradas, en este orden):

```markdown
# Cómo Contribuir a [Nombre Proyecto]

## 1. Tipos de Contribución Aceptados
Lista: reportar bugs, proponer mejoras, enviar PRs de código, mejorar documentación, etc.
Enlace a la política de issues si existe.

## 2. Antes de Contribuir
Código de conducta (referencia externa si aplica). Requerimientos de CLA si aplica.

## 3. Proceso de Contribución
1. Fork / Clonar el repositorio
2. Crear rama desde [rama-principal] (nombre: `feat/`, `fix/`, `docs/`, `chore/`)
3. Implementar cambio + tests
4. Verificar calidad (lint, tipos, tests)
5. Abrir PR con descripción según la plantilla
6. Proceso de review y merge
Diagrama opcional: `gitgraph` para visualizar el flujo de fork/branch/PR/merge.

## 4. Convenciones de Código y Commits
Referencia a SHARED_INSTRUCTIONS.md / Conventional Commits.
Tabla: | Tipo commit | Cuándo usar |

## 5. Requisitos de Calidad
Herramientas y comandos que deben pasar antes de abrir PR:
```bash
python -m ruff check scripts tests
python -m mypy scripts
python -m pytest
```
Sin errores: merge no procede.

## 6. Proceso de Release y Versionado
Referencia a SemVer. Quién tiene permisos de release. Enlace a CHANGELOG.md.
```

**Reglas**:
- Derivar §4 de `SHARED_INSTRUCTIONS.md` (convenciones) y `.github/workflows/` (CI actual).
- Mantener actualizado cuando cambien las herramientas de calidad.
- Si el proyecto no acepta contribuciones externas: indicarlo explícitamente en §1.

**Sección MkDocs**:

```yaml
- Contribuir: contributing.md   # Entrada directa en nav raíz o bajo "Proyecto"
```

---

## 4. Configuración Recomendada mkdocs.yml

La siguiente configuración es la **referencia estándar** para todos los proyectos.
Adapta los valores de `site_*`, `extra.version` y `nav` a cada proyecto; el resto es la base común.

### 4.1 Configuración Completa (Referencia)

> Basada en la experiencia de `util_bbdd` y `doc_ia` (actualizada 2026-06-10).
> Ver la guía operativa completa en `docs.instructions.md` → "mkdocs.yml — Base de referencia".

```yaml
site_name: [Nombre del Proyecto]
site_description: [Descripción breve del proyecto]
site_author: [Autor / Equipo]
site_url: https://[usuario].github.io/[repo]/
repo_url: https://github.com/[usuario]/[repo]
repo_name: [usuario]/[repo]
docs_dir: docs
site_dir: site

theme:
  name: material
  language: es  # o en
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: blue
      toggle:
        icon: material/brightness-7
        name: Cambiar a modo oscuro
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: blue
      toggle:
        icon: material/brightness-4
        name: Cambiar a modo claro
  features:
    - navigation.tabs           # Pestañas principales en la barra superior
    - navigation.tabs.sticky    # Pestañas visibles al hacer scroll
    - navigation.top            # Botón "volver arriba"
    - navigation.footer         # Anterior / Siguiente en el footer
    - content.code.copy         # Botón copiar en bloques de código
    - content.code.annotate     # Anotaciones en código
    - content.tabs.link         # Tabs de código sincronizadas
    - search.highlight
    - search.suggest
    - toc.follow
  icon:
    repo: fontawesome/brands/github

plugins:
  - search:
      lang: es  # o en
  # Solo si el proyecto tiene código Python con docstrings a autodocumentar:
  # - mkdocstrings:
  #     handlers:
  #       python:
  #         paths: [src]
  #         options:
  #           docstring_style: google
  #           show_source: true
  #           show_root_heading: true
  #           show_root_full_path: false
  #           show_symbol_type_heading: true
  #           show_symbol_type_toc: true
  #           merge_init_into_class: true
  #           members_order: source
  #           filters: ["!^_"]

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.snippets:
      base_path: [docs]   # ← rutas --8<-- relativas a docs/, ej: "examples/foo.py"
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
  - tables
  - toc:
      permalink: true
  - attr_list
  - md_in_html

nav:
  - Inicio: index.md
  - Instalación: installation.md
  - Descargas: downloads.md   # SIEMPRE obligatorio — Variante A (con build_docs_zip.py) o Variante B (sin script, build local + placeholder)

  # ── Audiencia: Product Owner, QA, responsables de negocio ──────────────────
  - Documentación Funcional:
      - [Área de dominio]:
          - [Nombre módulo]: functional/[modulo].md

  # ── Audiencia: Desarrolladores, ingenieros, DBAs ────────────────────────────
  - Referencia Técnica:
      - [Área de dominio]:
          - [Nombre módulo]: api/[modulo].md

  # ── Ejemplos de código ──────────────────────────────────────────────────────
  - Ejemplos:
      - [Área de dominio]:
          - [Caso de uso]: examples/[caso].md

  # ── Guías de uso y operación ────────────────────────────────────────────────
  - Guías:
      - Incorporación:
          - Onboarding de Desarrolladores: guides/onboarding_dev.md
      - Errores y Diagnóstico:
          - Troubleshooting: guides/troubleshooting.md
      - Herramientas IA:   # Si el proyecto usa herramientas IA
          - [Nombre herramienta]: guides/[tool]_guide.md

  # ── Contexto del proyecto ────────────────────────────────────────────────────
  - Arquitectura:
      - [Visión del Sistema]: architecture.md
      - [ADR-NNN — Título]: adr/ADR-NNN-titulo.md

extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/[usuario]/[repo]
    # Solo si está en PyPI:
    # - icon: fontawesome/brands/python
    #   link: https://pypi.org/project/[nombre]/

extra_javascript:
  - https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js
  - assets/js/mermaid.js        # ← copia desde doc_ia/docs/assets/
  - assets/js/sidebar-toggle.js # ← copia desde doc_ia/docs/assets/

extra_css:
  - assets/css/mermaid.css  # ← copia desde doc_ia/docs/assets/
  - assets/css/nav.css      # ← copia desde doc_ia/docs/assets/
```

**Notas críticas:**
- `!!python/name:` genera advertencias en linters YAML estándar — falso positivo; válido para MkDocs.
- Sin `extra_javascript` (CDN Mermaid + `assets/js/mermaid.js`), los diagramas no se renderizan en el browser aunque el build pase.
- `navigation.sections` y `navigation.tabs` son compatibles técnicamente, pero con tabs activados los grupos de área se muestran en la sidebar del tab activo; `navigation.sections` no aporta valor adicional. No incluir ambos.
- Los cuatro assets (`assets/js/mermaid.js`, `assets/js/sidebar-toggle.js`, `assets/css/mermaid.css`, `assets/css/nav.css`) deben copiarse desde `doc_ia/docs/assets/` sin modificación.
- La indentación de `nav:` usa **4 espacios extra por nivel**: secciones a 2 espacios, ítems de primer nivel a 6, segundo nivel a 10.

---

### 4.2 Navegación de doc_ia (Implementación Actual)

Mapeo concreto del proyecto sobre la estructura anterior.
La fuente canónica de la navegación es siempre `mkdocs.yml`; este bloque refleja
los grupos principales como referencia rápida:

```yaml
nav:
  - Inicio: index.md
  - Instalación: installation.md
  - 📥 Descargas: downloads.md

  # ── Audiencia: Product Owner, responsables de documentación ────────────────
  - Documentación Funcional:
      - Tooling Determinista:
          - Verificación de Entorno: functional/check_env.md
          - ZIP de Documentación Offline: functional/build_docs_zip.md
      # pendiente: Flujos IA (functional/archetypes.md, functional/bootstrap.md)

  # ── Audiencia: Desarrolladores, mantenedores del proyecto ──────────────────
  - Referencia Técnica:
      - Tooling Determinista:
          - check_env: api/check_env.md
          - build_docs_zip: api/build_docs_zip.md

  # ── Ejemplos de código ─────────────────────────────────────────────────────
  - Ejemplos:
      - Tooling Determinista:
          - Verificar Entorno: examples/check_env_usage.md
          - Generar ZIP Offline: examples/build_docs_zip_offline.md

  # ── Guías de uso y operación ───────────────────────────────────────────────
  - Guías:
      - Incorporación:
          - Onboarding de Desarrolladores: guides/onboarding_dev.md
      - Errores y Diagnóstico:
          - Troubleshooting: guides/troubleshooting.md
      - Herramientas IA:
          - Guía de Codex (OpenAI): guides/codex_guide.md

  # ── Contexto del proyecto ──────────────────────────────────────────────────
  - Arquitectura:
      - Visión del Sistema: architecture.md
      - ADR-001 — MkDocs Material por defecto: adr/ADR-001-mkdocs-material-por-defecto.md
```

> **Nota**: implementado en el dogfooding 2026-06-10 (nombres con guiones bajos según el
> canónico). Pendiente: páginas funcionales de Flujos IA (archetypes, bootstrap).

---

### 4.3 Secciones Opcionales (Agregar según necesidad)

| Sección | Ubicación | Arquetipo | Cuándo agregar |
|---------|-----------|-----------|----------------|
| **Quick Start** | `docs/quickstart.md` | 6 Variante D | Cuando la instalación completa supera 5 min y se quiere mostrar el producto de forma rápida |
| **Tutorial Guiado** | `docs/guides/*_tutorial.md` | 3b (§3.11) | Curvas de aprendizaje complejas; usuarios que llegan al proyecto sin conocimiento previo |
| **Changelog** | `CHANGELOG.md` + enlace nav | 9 (§3.12) | Opt-in explícito — proyectos con releases versionados |
| **Contribución** | `CONTRIBUTING.md` + enlace nav | 11 (§3.14) | Opt-in explícito — proyectos open source o con colaboradores externos |
| **Configuración IA** | `docs/ai-config/` | 10 (§3.13) | Proyectos con ≥1 plataforma IA configurada (CLAUDE.md, copilot, etc.) |
| **Seguridad** | `docs/security/` | — | Proyectos con auth, datos sensibles o auditoría |
| **FAQ** | `docs/faq.md` | — | Preguntas frecuentes por módulo |
| **Glosario** | `docs/glossary.md` | — | Dominio específico con muchos términos |
| **Web Interface** | `docs/web-interface.md` | — | Si el proyecto tiene UI web |
| **Arquitectura Web API** | `docs/architecture/web-api.md` | — | Si existe `src/**/web/` con FastAPI/Flask/etc. |
| **Microservicios** | `docs/architecture/microservices.md` | — | Si el proyecto expone o consume múltiples servicios |
| **Docker / Contenedores** | `docs/architecture/docker.md` | — | Si existe `Dockerfile` o `docker-compose.yml` en el repo |
| **Normativa** | `docs/normativa/` | 8 (§3.8) | **Solo** si el proyecto referencia leyes, decretos o normativas de obligado cumplimiento |

---

## 5. Roles de Agentes y Flujo de Trabajo

### Flujo Recomendado para Documentación

| Fase | Agente | Tarea | Entrada | Salida |
|------|--------|-------|---------|--------|
| **1. Planificación** | `Plan Architect` | Validar estructura actual vs propuesta | `mkdocs.yml` + código fuente | `PLAN` + `AUDIT_PLAN` |
| **2. Validación IA** | `config-reviewer` | Revisar coherencia en `CLAUDE.md`, `copilot-instructions.md` | Archivos IA | Findings + recomendaciones |
| **3. Exploración** | `Explore` | Mapear módulos existentes vs faltantes | `src/`, `docs/` | Matriz de cobertura |
| **4. Generación** | `documentation-generator` | Crear/actualizar docs funcional + técnica | Código fuente + prompts | Archivos en `docs/` + `mkdocs.yml` |
| **5. Auditoría** | `documentation-reviewer` | Validar completitud, ejemplos, coherencia | Docs generadas | Findings + mejoras |
| **6. Verificación de config** (opt-in `--verify-tools`) | `documentation-generator` | Fetch webs oficiales — validar plugins y versiones en `mkdocs.yml` | Config + webs MkDocs/Zensical/PyPI | Discrepancias por severidad |
| **6b. Verificación de build** (opt-in `--verify-build`) | `documentation-generator` | Build + inspección HTML generado — alias bug, snippets, Mermaid, nav | `site/` (Modo A) o `localhost:8000` (Modo B `--serve`) | Hallazgos por página + acciones recomendadas |
| **7. Cierre** | `Version Closer` | Sincronizar `CHANGELOG.md` + `COMPATIBILITY.md` | Cambios completados | Release notes |

### Cuándo Usar Cada Agente

| Agente | Cuándo | Comando | Scope |
|--------|--------|---------|-------|
| `documentation-generator` | Generar docs por primera vez o actualizar módulo completo | `/new-feature "generar doc [módulo]"` | `scripts/` → `docs/` |
| `documentation-reviewer` | Auditar docs existentes (calidad, ejemplos, claridad) | `/audit-code` | `docs/functional/`, `docs/api/` |
| `config-reviewer` | Sincronizar instrucciones IA entre archivos de configuración | `/config-review` | `CLAUDE.md`, `copilot-instructions.md` |
| `Plan Architect` | Cambio estructural en `mkdocs.yml` o nuevo módulo importante | `/new-feature` o `/refactor` | `mkdocs.yml` |

---

## 6. Restricciones y Decisiones

### Restricciones Generales

- ✅ **MkDocs v1.5+** — No usar versiones antiguas, usar Material theme
- ✅ **Diagramas Mermaid** — Agnóstico a Graphviz, integrado en mkdocs
- ✅ **Lenguaje agnóstico** — Ejemplos Python en carpetas separadas si hay múltiples lenguajes
- ✅ **NO inventar código** — Todos los ejemplos deben validarse contra `scripts/` y el árbol real
- ✅ **Encoding UTF-8** — Todos los archivos markdown
- ❌ **NO guardar en OneDrive o Google Drive** — Usar referencias internas al repositorio

### Decisiones Críticas

1. **Separación Funcional ↔ Técnica**: Cada módulo tiene 2 documentos separados, no mezcladas
   - Funcional: `docs/functional/[módulo].md` (usuario final)
   - Técnica: `docs/api/[módulo].md` (desarrollador)

2. **Ubicaciones Fijas** (No cambiar sin consenso):
   - Funcional: `docs/functional/[módulo].md`
   - Técnica: `docs/api/[módulo].md`
   - Ejemplos: `docs/examples/[caso].md` (ficheros **planos en disco**, sin subcarpetas por tipo).
     En `nav:` **se agrupan en subsecciones por área funcional**, igual que `Referencia Técnica`
     y `Documentación Funcional` (ver `docs.instructions.md` → "Agrupación en subsecciones por área").
   - Guías: `docs/guides/[nombre].md` (ficheros en carpeta `guides/`, **nombre siempre en minúsculas con guiones bajos**).
     En `nav:` **se agrupan en subsecciones temáticas** (Incorporación, Conexión y Drivers, Errores y Diagnóstico,
     Rendimiento, Migración de Versión, Herramientas IA…), no por módulo.

3. **Actualización de mkdocs.yml**: Automatizada con `mkdocstrings` + agente `documentation-generator`

4. **Build CI/CD**: `mkdocs build` validado en cada PR, detecta links rotos

5. **Versionamiento**: Sincronizar CHANGELOG.md según `.github/instructions/sync.instructions.md`

---

## 7. Cómo Proceder

Los pasos corresponden 1:1 con las fases de §5.

### Paso 1: Planificar (20 min)
```text
@Plan Architect
Validar estructura docs/ vs mkdocs.yml real. Entregar PLAN + AUDIT_PLAN.
```

### Paso 2: Validar Configuración IA (30 min)
```text
@config-reviewer
Revisar coherencia propuesta vs código real en scripts/.
Validar que estructura propuesta es implementable.
```

### Paso 3: Explorar Módulos (15 min)
```text
@Explore
Mapear módulos en scripts/ vs docs/. Identificar faltantes. Solo lectura.
```

### Paso 4: Generar/Actualizar Documentación (1-2 h)
```text
@documentation-generator
Generar docs para módulo específico O proyecto completo.
Actualiza mkdocs.yml automáticamente.
```

### Paso 5: Auditar Documentación (30 min)
```text
@documentation-reviewer
Validar ejemplos contra código real.
Verificar coherencia, completitud, claridad.
Reportar mejoras.
```

### Paso 6: Integración y Build (15 min)
```text
@Code Auditor
Ejecutar mkdocs build. Verificar links. Reportar errores de build.
```

### Paso 7: Sincronizar Versión (20 min)
```text
@Version Closer
Actualizar CHANGELOG.md.
Generar release notes.
```

### Criterio de Completitud

La estandarización se considera **completa** cuando:

- [ ] `mkdocs build --strict` finaliza sin errores ni warnings de links rotos
- [ ] Todos los módulos en `scripts/` tienen doc funcional (`docs/functional/`) y técnica (`docs/api/`)
- [ ] Todos los archivos referenciados en `docs/examples/` existen en disco
- [ ] `CHANGELOG.md` (cuando exista) refleja la versión actual de `pyproject.toml`
- [ ] Las instrucciones IA (`CLAUDE.md`, `copilot-instructions.md`) son coherentes con el código real
- [ ] Todos los documentos en `nav:` (excepto `legacy-versions.md`) tienen exactamente las secciones numeradas de su arquetipo asignado (`index.md`, `INSTALLATION.md` y `ARCHITECTURE.md` se rigen por el Arquetipo 6)
- [ ] Las secciones vacías contienen `*No aplica para este módulo.*` en lugar de estar omitidas
- [ ] Los prompts `.github/prompts/howto_doc.prompt.md`, `tutorial_doc.prompt.md` y `example_doc.prompt.md` existen y son coherentes con Arquetipos 3a, 3b y 4
- [ ] Si hay releases: `CHANGELOG.md` sigue el estándar Keep a Changelog (Arquetipo 9) y tiene entrada `[Unreleased]`
- [ ] Si hay ≥1 plataforma IA configurada: existe `docs/ai-config/[plataforma].md` derivado del fichero fuente real (Arquetipo 10)
- [ ] Si el proyecto acepta contribuciones: `CONTRIBUTING.md` existe en raíz y enlaza desde README (Arquetipo 11)

---

## 📎 Referencias Internas

- [`.github/SHARED_INSTRUCTIONS.md`](.github/SHARED_INSTRUCTIONS.md) — Fuente canónica de arquitectura
- [`CLAUDE.md`](CLAUDE.md) — Instrucciones para Claude Code
- [`.github/copilot-instructions.md`](.github/copilot-instructions.md) — Instrucciones para Copilot Chat
- [`.github/instructions/docs.instructions.md`](.github/instructions/docs.instructions.md) — Guía de estilo para documentación
- [`pyproject.toml`](pyproject.toml) — Versión actual del proyecto
- [`.ai/product.md`](.ai/product.md) — Contexto de producto
- [`mkdocs.yml`](mkdocs.yml) — Configuración actual de MkDocs
- [`.github/instructions/sync.instructions.md`](.github/instructions/sync.instructions.md) — Sincronización de versiones
