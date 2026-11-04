# normative_traceability

Genera o actualiza un documento de trazabilidad normativa para el proyecto.

## Cuándo usar

- Al recibir un gap análisis normativo formal
- Cuando se incorpora nueva normativa de referencia al proyecto
- Al implementar un módulo que cubre un gap normativo documentado
- En revisiones de versión mayor que afecten a lógica de negocio regulada
- Cuando las personas han tomado decisiones en `docs/decisiones/<norma>_decisiones.md` (Arq. 13)

## Condición de activación

**Este prompt solo aplica si el proyecto tiene normativa de referencia.** Verificar primero en
`.ai/product.md` o `README.md`. Si no hay referencias a leyes, decretos, directivas o normas de
obligado cumplimiento → no generar este documento.

> **Este proyecto (doc_ia)**: actualmente sin normativa de referencia explícita. Si en el
> futuro se incorpora (ej. RGPD/LOPD-GDD para datos gestionados, accesibilidad, SOC2), aplicar
> este prompt en ese momento.

## Inputs requeridos

- **Normas de referencia**: identificadores exactos (ej. "RGPD 2016/679", "LOPD-GDD 3/2018")
- **Módulos del sistema**: leer `.ai/architecture.md` para obtener la lista real
- **Documentación existente**: leer `docs/functional/`, `docs/api/`, `.ai/product.md`

## Proceso de generación

### Paso 1 — Leer contexto
1. `.ai/product.md` — dominio, audiencia, normativa ya identificada
2. `.ai/architecture.md` — módulos, niveles, capas
3. `docs/functional/*.md` — funcionalidades documentadas con referencias normativas
4. `docs/normativa/` — si ya existe, actualizar en lugar de sobrescribir
5. `docs/decisiones/<norma>_decisiones.md` — si ya existe, **aplicar primero sus decisiones**
   (`coverage_decisions.prompt.md` § Modo aplicación) y no tocar sus campos de persona

### Paso 2 — Estructurar la cobertura

Por cada norma de referencia:
- Identificar los artículos y anexos relevantes para el sistema (no todos los artículos de la ley)
- Para cada artículo: buscar en el código y la documentación el módulo que lo implementa
- Asignar un ID estable `COB-<NORMA>-<NNN>` (conservar los existentes; nunca renumerar)
- Asignar símbolo de cobertura (leyenda canónica, DOCUMENTATION_STANDARD.md §3.8):
  - ✅ Cubierto: módulo identificado y comportamiento verificado en el código
  - ⚠️ Parcial: módulo identificado, pero con un hueco funcional o un defecto conocido
  - ❌ Gap: no hay módulo que lo implemente
  - 🔍 A verificar: la evidencia no basta (configuración en base de datos, sistemas externos o
    documentación organizativa no aportada)
- Si la fila ya tiene una decisión humana en el registro, su símbolo es el «Estado resultante»
  de la ficha, no el que se deduciría del código (si el código lo contradice, informarlo en
  «Pendiente de revisión humana» sin cambiarlo)

### Paso 3 — Clasificar gaps

- **Nivel 1 — Crítico**: riesgo de incumplimiento normativo real o auditoría bloqueada
- **Nivel 2 — Importante**: gap documental que dificulta mantenimiento o auditoría
- **Nivel 3 — Mejora**: detalle adicional sin impacto inmediato en cumplimiento

### Paso 4 — Escribir el documento

Guardar en `docs/normativa/<abbrev_norma>_traceability.md`.

Estructura del Arquetipo 8 del DOCUMENTATION_STANDARD:
- Propósito (versión del sistema + fecha de revisión)
- Una sección por norma con tablas de cobertura agrupadas por capítulos/temas
  (`| ID | Artículo | Obligación | Módulo/servicio | Doc de referencia | Cobertura |`)
- Resumen de gaps por severidad (tablas)
- Normativa complementaria referenciada
- Próximas acciones priorizadas (ordenadas por severidad)

### Paso 4b — Registro de Decisiones de Cobertura (Arquetipo 13, obligatorio)

Generar o actualizar `docs/decisiones/<norma>_decisiones.md` con
`.github/prompts/coverage_decisions.prompt.md` § Modo generación: una ficha por ID, campos de
persona intactos, página de trazabilidad sellada con `stamp` (el registro queda en `decisiones:`).

### Paso 5 — Actualizar mkdocs.yml

Verificar que existe la sección `Normativa` en `mkdocs.yml`:
- Posición: entre la sección `Funcional` (o equivalente) y `Arquitectura`/`ADR`

```yaml
- Normativa:
    - Trazabilidad <Norma>: normativa/<codigo>_traceability.md
- Decisiones:
    - Decisiones <Norma>: decisiones/<codigo>_decisiones.md
```

## Restricciones

- No inventar contenido normativo; describir obligaciones en términos del sistema, no copiar texto legal
- Marcar como 🔍 cualquier artículo sin evidencia suficiente
- No documentar como ✅ ningún artículo sin módulo identificado explícitamente
- No incluir artículos que no sean relevantes para la implementación del sistema
- Verificar que los módulos referenciados existen realmente en la arquitectura
- No rellenar ni modificar los campos de persona del registro de decisiones

## Formato de salida al usuario

```
## Documento generado
- docs/normativa/<archivo>.md — trazabilidad <Norma A> y <Norma B>

## Cobertura generada
- Artículos analizados: N
- ✅ Cubiertos: N | ⚠️ Parciales: N | ❌ Gaps: N | 🔍 A verificar: N

## Registro de decisiones
- docs/decisiones/<norma>_decisiones.md — [creado/actualizado] · Pendientes: N · Aplicadas: N
- doc_trace decisions: [0 | 1 con N hallazgos]

## mkdocs.yml
- [Añadido/ya existía] secciones Normativa y Decisiones

## Gaps Nivel 1 detectados
- [lista de gaps críticos con ID y acción recomendada]

## Pendiente de revisión humana
- [fichas `Pendiente` del registro, con la pregunta concreta para quien decide]
- [fichas inválidas o incompletas, con el motivo]
```
