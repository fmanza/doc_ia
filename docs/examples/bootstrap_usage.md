# Ejemplo: Bootstrap de Configuración IA a Otro Proyecto

## 1. Contexto del Ejemplo

Cuando quieres trasladar el sistema de instrucciones IA de doc_ia a un proyecto existente
— por ejemplo un servicio TypeScript — el bootstrap clasifica automáticamente cada fichero
en cuatro capas (A verbatim, B adaptar, C regenerar, D excluir) y produce un plan de
transferencia listo para ejecutar.

Este ejemplo muestra la invocación desde el proyecto destino, el PLAN que genera y el
resultado esperado tras completar el IMPLEMENT.

## 2. Implementación de Referencia

Invocación desde el proyecto destino (código inline — el flujo ocurre en el chat):

**Escenario — Bootstrap completo a un servicio TypeScript + NestJS**

```
# Abrir el PROYECTO DESTINO en Claude Code y escribir:

Lee y aplica .github/prompts/bootstrap_ai_config.prompt.md

Origen (solo lectura):             c:\Desarrollo\python\libs\doc_ia
Destino:                           c:\repos\mi_servicio_nestjs
Lenguaje/arquitectura destino:     TypeScript + NestJS hexagonal
Plataformas IA activas:            Claude Code, GitHub Copilot Chat
Generador de documentación:        Docusaurus
Fase:                              PLAN y AUDIT_PLAN únicamente.
```

**Escenario — Solo PLAN (estimación de esfuerzo antes de comprometerse)**

```
Lee y aplica .github/prompts/bootstrap_ai_config.prompt.md

Origen (solo lectura):             c:\Desarrollo\python\libs\doc_ia
Destino:                           c:\repos\mi_api_go
Lenguaje/arquitectura destino:     Go + Clean Architecture
Plataformas IA activas:            Claude Code, Cursor
Generador de documentación:        Hugo
Fase:                              PLAN y AUDIT_PLAN únicamente.
```

## 3. Explicación del Código

- El bootstrap se invoca **siempre desde el proyecto destino** (modelo PULL): la IA
  necesita ver el código real del destino para reescribir capas B y C sin arrastrar
  suposiciones del stack de origen.
- Si el destino usa un generador diferente (Docusaurus, Hugo), la plantilla de
  `mkdocs.yml` no se copia; se adapta o se omite.
- `Fase: PLAN y AUDIT_PLAN únicamente` permite estimar el esfuerzo sin ejecutar la
  transferencia. Cambiar a `completa` para ejecutar IMPLEMENT + AUDIT_CODE + VERSION.
- Los ficheros de la **capa D** (sesiones pasadas, CHANGELOG, caches) nunca se copian;
  el bootstrap los excluye explícitamente.

## 4. Ejecución y Pruebas

**Salida esperada del ANÁLISIS** (primer bloque que devuelve el agente):

```
ANÁLISIS

| Fichero | Capa | Acción |
|---|---|---|
| .github/agents/*.agent.md | A | Copiar verbatim (revisar comandos embebidos Python → TS) |
| .github/prompts/*.prompt.md | A | Copiar verbatim (revisar comandos embebidos) |
| .claude/commands/*.md | A | Copiar verbatim |
| CLAUDE.md | B | Copiar + reescribir dominio (Python → TypeScript + NestJS) |
| .github/SHARED_INSTRUCTIONS.md | B | Copiar + reescribir comandos y arquitectura |
| .ai/product.md | C | Regenerar desde cero (árbol real del destino) |
| .ai/architecture.md | C | Regenerar desde cero |
| .ai/sessions/<fechas>/ | D | Excluir |
| CHANGELOG.md | D | Excluir |
```

**Salida esperada del PLAN** (segundo bloque):

```
PLAN

Ficheros a copiar verbatim (Capa A):   12 ficheros
Ficheros a reescribir dominio (Capa B): 6 ficheros
Ficheros a regenerar (Capa C):          5 ficheros
Ficheros excluidos (Capa D):           todo .ai/sessions/<fechas>/

Comandos equivalentes detectados:
  python -m pytest   → jest / vitest
  python -m ruff     → eslint
  python -m mypy     → tsc --noEmit
  mkdocs build       → docusaurus build
```

Tras IMPLEMENT + auditoría con Config Reviewer, el destino tiene los entry points IA
activos sin referencias al stack Python del origen.

## 5. Referencias Relacionadas

- Documentación funcional: [Bootstrap de Configuración IA](../functional/bootstrap.md)
- Referencia técnica: [bootstrap](../api/bootstrap.md)
- Ejemplos relacionados: [Documentar un Proyecto](document_project_usage.md)
