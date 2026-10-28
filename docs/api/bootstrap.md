---
arquetipo: "2"
fuentes:
  .github/agents/config-reviewer.agent.md: 376360c404e4
  .github/prompts/bootstrap_ai_config.prompt.md: e7ef8b2fb106
revisado: 2026-10-28
---
# bootstrap

Traslada el sistema de instrucciones IA de doc_ia a un proyecto destino de cualquier lenguaje y arquitectura, clasificando cada fichero en cuatro capas y emitiendo un plan de transferencia auditado.

## 1. Arquitectura y Diseño

```mermaid
flowchart TD
    accTitle: Fases del bootstrap de configuración IA
    accDescr: Desde el proyecto destino, el prompt de bootstrap recorre análisis, plan, auditoría del plan, implementación por capas, auditoría de código y versión.
    U[Usuario en el proyecto DESTINO] --> INV[Lee bootstrap_ai_config.prompt.md<br/>+ 8 parámetros obligatorios]
    INV --> AN[ANÁLISIS<br/>Clasificación A/B/C/D<br/>matriz de equivalencias]
    AN --> PL[PLAN<br/>ficheros a copiar·adaptar·regenerar]
    PL --> AP[AUDIT_PLAN<br/>riesgos funcionales·técnicos·seguridad<br/>Veredicto GO/GO_CONDICIONAL/NO_GO]
    AP --> IM[IMPLEMENT<br/>Capa A verbatim → Capa B reescrita → Capa C regenerada]
    IM --> AC[AUDIT_CODE<br/>Config Reviewer<br/>DRY · rutas portables · cero referencias huérfanas]
    AC --> VE[VERSION<br/>commit Conventional Commits · rollback]
```

## 2. Modelo de Datos / Contratos

### API pública

| Componente | Tipo | Descripción | Retorna |
|---|---|---|---|
| `bootstrap_ai_config.prompt.md` | prompt multiplataforma | Instrucciones completas del bootstrap; se invoca desde el proyecto destino | Fases ANÁLISIS → VERSION |
| `config-reviewer.agent.md` | agente | Audita la coherencia de las instrucciones IA generadas tras el bootstrap | AUDIT_CODE con veredicto |

### Contrato de entrada

| Parámetro | Tipo | Descripción | Restricciones |
|---|---|---|---|
| `Origen` | ruta | Ruta del repositorio doc_ia (solo lectura) | Obligatorio; el destino lee los ficheros del origen pero no los modifica |
| `Destino` | ruta | Raíz del proyecto que recibirá el sistema IA | Obligatorio; el código real del destino debe ser accesible para regenerar Capa C |
| `Lenguaje y framework` + `Arquitectura destino` | string | Stack real del destino (ej. TypeScript + NestJS) y su patrón (capas, hexagonal, MVC…) | Obligatorios (dos campos); determinan la matriz de equivalencias de comandos |
| `Plataformas IA activas` | lista | Plataformas a configurar (Claude Code, Gemini, Copilot, Cursor, Codex) | Obligatorio; determina qué entry points se crean |
| `Herramientas de calidad` | lista | Linter, formateador, type-checker y test runner del destino | Obligatorio; sustituye `ruff`/`mypy`/`pytest` en la Capa A |
| `Generador de documentación` | string | `mkdocs-material`, `Docusaurus`, `Hugo`, `ninguno`… | Obligatorio (admite `ninguno`); determina si `mkdocs.yml` se copia o se adapta |
| `Gestor de paquetes / build` | string | Comando de instalación y build del destino | Obligatorio |
| `Fase` | string | `PLAN y AUDIT_PLAN únicamente` o `completa` | Opcional; por defecto flujo completo |

### Capas de transferencia

| Capa | Carácter | Acción |
|---|---|---|
| **A — Metodología** | Agnóstico de lenguaje: ciclo PLAN/IMPLEMENT/VERSION, agentes, prompts, plantilla de sesión | Copiar verbatim (revisar comandos embebidos) |
| **B — Especialización** | Entry points IA + instrucciones compartidas; mezcla método + dominio | Copiar y reescribir las secciones de dominio |
| **C — Contexto de dominio** | 100 % específico del origen: módulos, lenguaje, motores, capacidades | Regenerar desde cero analizando el destino |
| **D — No copiar** | Historial y estado del origen: sesiones pasadas, CHANGELOG, caches | Excluir |

### Contrato de salida

Seis bloques en el chat, en este orden: ANÁLISIS → PLAN → AUDIT_PLAN → IMPLEMENT → AUDIT_CODE → VERSION.

### Errores y casos especiales

| Caso | Comportamiento |
|---|---|
| Parámetro obligatorio faltante | El flujo se detiene antes del ANÁLISIS y pide completarlo |
| Generador de docs no indicado | Como cualquier campo obligatorio: el flujo se detiene y lo pide (se admite `ninguno`) |
| Bootstrap lanzado desde el origen en lugar del destino | Riesgo de arrastrar suposiciones del stack origen; el prompt exige invocarlo desde el destino y explica por qué |
| Fichero de Capa D presente en el origen | Se excluye siempre; no se copia ni con instrucciones explícitas del usuario 🔍 |

## 3. Componentes y Clases

| Componente | Ruta | Responsabilidad |
|---|---|---|
| Prompt de bootstrap | `.github/prompts/bootstrap_ai_config.prompt.md` | Clasificación por capas, matrix de equivalencias, instrucciones por plataforma, salida esperada |
| Config Reviewer | `.github/agents/config-reviewer.agent.md` | Auditoría post-bootstrap: DRY, rutas portables, cero referencias huérfanas, veredicto APROBADO/RECHAZADO |

## 4. Dependencias y Requisitos

| Dependencia | Propósito | Requerida | Comportamiento sin ella |
|---|---|---|---|
| Código real del proyecto destino | Fuente para regenerar Capa C (`.ai/*.md`, instrucciones por lenguaje) | Sí | La Capa C queda vacía o con contenido del origen, no del destino |
| Entry points IA del origen (Capa A+B) | Plantillas que se copian o reescriben | Sí | Sin ellas no hay nada que transferir |
| `.github/DOCUMENTATION_STANDARD.md` | Si el destino publica docs: plantilla de arquetipos (Capa B) | Solo si el destino publica docs | La documentación del destino no hereda los arquetipos formales |

## 5. Ejemplos Relacionados

- [Ejemplo: Bootstrap de Configuración IA](../examples/bootstrap_usage.md) — invocación
  a un servicio TypeScript + NestJS, salida esperada del ANÁLISIS y del PLAN, y resultado
  tras completar el IMPLEMENT.

## 6. Verificación y Tests

*Sin tests automatizados.* El bootstrap es un prompt ejecutado en el chat del proyecto destino.
Riesgo principal sin cubrir: que la clasificación por capas (A/B/C/D) quede desfasada respecto a
los ficheros reales de doc_ia; solo lo detecta la auditoría posterior del Config Reviewer.

??? note "Evidencia"

    | Elemento | Fuente | Confianza |
    |---|---|---|
    | `bootstrap_ai_config.prompt.md` | `.github/prompts/bootstrap_ai_config.prompt.md` | ✅ |
    | `config-reviewer.agent.md` y veredicto APROBADO / APROBADO CON CONDICIONES / RECHAZADO | `.github/agents/config-reviewer.agent.md` | ✅ |
    | 8 parámetros obligatorios | `.github/prompts/bootstrap_ai_config.prompt.md` (sección "Contexto a completar") | ✅ |
    | `Fase` opcional (`PLAN y AUDIT_PLAN únicamente` o `completa`) | `.github/prompts/bootstrap_ai_config.prompt.md` (ejemplo de invocación) | ✅ |
    | Capas A/B/C/D y sus acciones | `.github/prompts/bootstrap_ai_config.prompt.md` (sección "Clasificación por capas") | ✅ |
    | Seis bloques ANÁLISIS → VERSION | `.github/prompts/bootstrap_ai_config.prompt.md` (salida esperada) | ✅ |
    | Parada por parámetro faltante | `.github/prompts/bootstrap_ai_config.prompt.md` (VALIDACIÓN) | ✅ |
    | Invocación desde el destino (modelo PULL) | `.github/prompts/bootstrap_ai_config.prompt.md` (sección "Método y dirección de la llamada") | ✅ |
    | Capa D excluida aunque el usuario lo pida | `.github/prompts/bootstrap_ai_config.prompt.md` (Capa D: "Excluir explícitamente", sin mención a peticiones del usuario) | 🔍 |
    | Dependencias: código del destino, Capa A+B del origen, norma documental | `.github/prompts/bootstrap_ai_config.prompt.md` | ✅ |
