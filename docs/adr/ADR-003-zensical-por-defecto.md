---
status: "ACEPTADO"
date: 2026-11-12
deciders: [Paco Manzano]
consulted: [Plan Architect]
informed: [mantenedores de doc_ia]
---

# Use Zensical as the only documentation generator

## Contexto y Problema

[ADR-001](ADR-001-mkdocs-material-por-defecto.md) eligió MkDocs + Material for MkDocs como
generador por defecto y dejó Zensical como alternativa compatible sobre el mismo
`mkdocs.yml`. Desde entonces el ecosistema ha cambiado:

- **Material for MkDocs** está en mantenimiento desde 2025-11-05 y llega a **fin de vida el
  2027-05-05**: hasta entonces solo recibe correcciones críticas y de seguridad.
- **MkDocs 1.x** no evoluciona y el **MkDocs 2.0** anunciado rompe temas, plugins y el formato
  de configuración; Material limita su dependencia a `mkdocs<2`.
- **Zensical**, del mismo equipo que Material, lee `mkdocs.yml` de forma nativa. La 0.1.0
  (2026-11-05) cierra la etapa alfa y abre una beta de tres meses; la 0.1.1 es la fijada. **No
  ejecuta la clave `hooks:`** ni la API de plugins de MkDocs, sin emitir ningún aviso.

doc_ia depende de dos pasos propios (`hooks/sync_root_docs.py` y `mkdocs_hooks.py`) para
sincronizar `CHANGELOG.md`/`CONTRIBUTING.md` y generar el ZIP `latest`.

La propuesta inicial (2026-10-28) fue un cambio escalonado: paridad no bloqueante en CI durante
≥ 2 semanas (C2) y MkDocs como respaldo hasta el 2027-05-05 (C5). El 2026-11-12 la paridad
llevaba 8 días en rojo sin verse (el paso no era bloqueante) por un fallo que afectaba también
a MkDocs: el logo enlazaba a una carpeta en el ZIP sin servidor. Mantener dos generadores costaba
más de lo que protegía.

Fuerzas en conflicto: fecha límite de soporte del stack actual frente a la juventud del
sucesor; seguridad del respaldo frente al coste (y la ceguera) de mantener dos builds.

## Decisión

**Zensical es el único generador de documentación de doc_ia, para su propio sitio y para los
proyectos destino. MkDocs queda fuera** (decisión del usuario, 2026-11-12):

1. **Build**: `python scripts/build_docs_zip.py` es el pipeline: sincroniza los ficheros raíz,
   `zensical build --strict`, ZIP `latest` (`mkdocs_hooks.py`) solo si el build termina con 0,
   y rechaza un `site/` que no se abra con doble clic en `index.html`. `--builder mkdocs` se
   rechaza con código 2; `--builder zensical` se acepta sin efecto durante una versión.
2. **Dependencias**: `zensical` y `zensical-ui` con versión exacta; fuera `mkdocs`,
   `mkdocs-material` y sus dependencias propias. `check_env.py` exige `zensical`.
3. **CI**: el build de Zensical es **bloqueante**; desaparecen el build MkDocs y la paridad.
4. **Configuración**: se mantiene `mkdocs.yml` como **fuente única**, sin la clave `hooks:`.
   Zensical lo lee de forma nativa y `scripts/doc_trace.py`, `kit.py`, los tests y los destinos
   dependen del nombre. `mkdocs_hooks.py` también conserva su nombre. Pasar a `zensical.toml`
   queda para cuando Zensical lo pida.
5. **Destinos**: `/document-project` ya no pregunta el generador. Un destino en MkDocs se migra
   en su Fase 0b, de forma explícita y registrada en el RESUMEN; si usa un plugin que Zensical
   no soporta, la migración se detiene y lo informa.

Condiciones cumplidas al aceptar: C1 (0.1.1 fijada), C3 (revisión visual, Mermaid incluido; la
búsqueda por `file://` y el móvil real quedan para la revisión humana antes de publicar), C4
(ZIP `latest` cubierto por tests), C10 (0 enlaces a carpeta en `site/`). C2 y C5 se retiran con
la decisión.

## Consecuencias

| Tipo | Descripción |
|---|---|
| Ventaja | Continuidad de soporte más allá del 2027-05-05 sin reescribir la configuración |
| Ventaja | Un solo build: lo que valida la CI es lo que se publica; el fallo deja de ser invisible |
| Ventaja | Build ≈4× más rápido y validación estricta más amplia (anclas, referencias) |
| Compromiso | `zensical serve` no sincroniza los ficheros raíz: construir con `build_docs_zip.py` |
| Compromiso | Los destinos MkDocs se migran al volver a ejecutar `/document-project` |
| Deuda técnica | Lista de plugins soportados mantenida a mano en `tests/test_zensical_compat.py` |
| Deuda técnica | Nombres heredados `mkdocs.yml` y `mkdocs_hooks.py` |
| Riesgo aceptado | Sin respaldo: Zensical en beta. Se mitiga con versión exacta, actualización deliberada (compatibilidad de plugins, rutas, Mermaid) y rollback por revert |

## Alternativas Consideradas

| Alternativa | Pros | Contras | Motivo de rechazo |
|---|---|---|---|
| Seguir con MkDocs + Material | Estable, sin trabajo | Sin soporte desde el 2027-05-05; MkDocs 2.0 incompatible | Solo aplaza el problema |
| Escalonado con respaldo MkDocs hasta 2027-05-05 (propuesta inicial) | Respaldo disponible | Dos builds; la paridad no bloqueante ocultó un fallo 8 días | Su coste superó la protección; sustituida por esta decisión |
| Fork comunitario de MkDocs (p. ej. ProperDocs) | Mantiene la API de hooks y plugins | Mantenimiento incierto; Material seguiría sin soporte | No resuelve el fin de vida del tema |
| Migrar a `zensical.toml` | Formato nativo de Zensical | `doc_trace.py`, `kit.py`, tests y destinos leen `mkdocs.yml` | Sin beneficio hoy; Zensical sigue leyendo `mkdocs.yml` |

## Estado y Revisión

Estado: **ACEPTADO** · Fecha: 2026-11-12 (propuesto el 2026-10-28)
Reemplaza a [ADR-001 — Use MkDocs Material as the default documentation generator](ADR-001-mkdocs-material-por-defecto.md).
Sesiones: `2026-10-28d_zensical_migration` (propuesta y preparación) y
`2026-11-12_zensical_paridad_f7` (decisión y migración).
Revisar al actualizar Zensical (plugins soportados, `hooks:`, `zensical.toml`).
