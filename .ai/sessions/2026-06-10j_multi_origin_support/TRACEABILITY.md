---
session: 2026-06-10j_multi_origin_support
skill: new_feature (extensión de /document-project — soporte de orígenes heterogéneos)
branch: develop
status: CLOSED
---

# TRACEABILITY — 2026-06-10j: Soporte de múltiples orígenes heterogéneos en /document-project

## Solicitud

Extender `/document-project` para detectar y gestionar orígenes de naturaleza diferente
(código vs. material de entrada: normativa, pantallas, especificaciones, referencias).

## Contexto de partida

El campo `Origen(es)` aceptaba múltiples rutas pero las trataba de forma homogénea como
proyectos de código. No existía mecanismo para distinguir orígenes MATERIAL ni para elegir
una estrategia cuando hay varios proyectos de código.

## Fases ejecutadas

PLAN → AUDIT_PLAN → IMPLEMENT

## Archivos modificados

| Archivo | Tipo | Cambio |
|---|---|---|
| `.claude/commands/document-project.md` | ACTUALIZADO | + campos `Tipo de cada origen` y `Estrategia`; + sección CLASIFICACIÓN DE ORÍGENES (paso 2 del flujo); numeración 2-8 → 3-9; 3 ejemplos de entrada |
| `.github/prompts/document_project.prompt.md` | ACTUALIZADO | + campos opcionales sincronizados; + Fase 0a en el flujo orquestado; + paso 2 CLASIFICACIÓN en Devuelve |
| `.github/agents/documentation-generator.agent.md` | ACTUALIZADO | + Paso 0a completo: tabla de señales, mapeo MATERIAL→arquetipos, estrategias multi-CÓDIGO, protocolo de ejecución; Fase 1 actualizada para sub-inventarios |
| `.github/DOCUMENTATION_STANDARD.md` | ACTUALIZADO | + §3.10 "Documentación con Múltiples Orígenes": tipos, mapeo, estrategias |

## Decisiones tomadas

- **Autodetección propone, usuario confirma**: la clasificación de tipo nunca se asume;
  se presenta tabla y se espera confirmación antes de pasar al INVENTARIO.
- **Estrategia multi-CÓDIGO nunca autodetectada**: depende del contexto organizacional,
  no de los archivos; siempre se pregunta al usuario.
- **Orígenes MATERIAL no generan páginas propias**: su contenido enriquece secciones
  concretas de los arquetipos del proyecto CÓDIGO principal.
- **Caso degenerado sin CÓDIGO**: detención explícita con mensaje orientativo hacia los
  prompts de arquetipo directos.
- **Compatibilidad hacia atrás**: con origen único de tipo CÓDIGO, la Fase 0a se omite
  (marcada como "origen único — fase omitida").

## Directrices para Futuras IAs

- **[/document-project multi-origen]**: cuando se reciben ≥2 orígenes, ejecutar siempre
  Fase 0a antes de INVENTARIO; la tabla de clasificación requiere confirmación explícita
  del usuario antes de continuar.
- **[tipos de origen]**: las señales de detección están en el Paso 0a del agente
  `documentation-generator.agent.md` y en §3.10 de `DOCUMENTATION_STANDARD.md`.
- **[estrategia multi-CÓDIGO]**: `federado` / `hub+satélite` / `monorepo` — siempre
  preguntar al usuario; no inferir de la estructura de directorios.
- **[origen sin CÓDIGO]**: si todos los orígenes son MATERIAL, `/document-project` no
  aplica; redirigir al prompt de arquetipo correspondiente.

## Veredicto

CLOSED — los 4 ficheros modificados son coherentes entre sí; el comportamiento para
origen único de tipo CÓDIGO no cambia; la nueva fase 0a cubre todos los escenarios
identificados en el PLAN.
