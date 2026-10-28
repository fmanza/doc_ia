---
status: "PROPUESTO"
date: 2026-10-28
deciders: [Paco Manzano]
consulted: [Plan Architect]
informed: [mantenedores de doc_ia]
---

# Use Zensical as the default documentation generator

## Contexto y Problema

[ADR-001](ADR-001-mkdocs-material-por-defecto.md) eligió MkDocs + Material for MkDocs como
generador por defecto y dejó Zensical como alternativa compatible sobre el mismo
`mkdocs.yml`. Desde entonces el ecosistema ha cambiado:

- **Material for MkDocs** está en mantenimiento desde 2025-11-05 y llega a **fin de vida el
  2027-05-05**: hasta entonces solo recibe correcciones críticas y de seguridad.
- **MkDocs 1.x** no evoluciona y el **MkDocs 2.0** anunciado rompe temas, plugins y el formato
  de configuración; Material limita su dependencia a `mkdocs<2`.
- **Zensical**, del mismo equipo que Material, lee `mkdocs.yml` de forma nativa, pero está en
  **alfa** (0.0.x; 0.1 anunciada para el 2026-11-05) y **no ejecuta la clave `hooks:`** ni la API
  de plugins de MkDocs, sin emitir ningún aviso.

doc_ia depende de dos hooks (`hooks/sync_root_docs.py` y `mkdocs_hooks.py`) para sincronizar
`CHANGELOG.md`/`CONTRIBUTING.md` y generar el ZIP `latest`. Un spike sobre una copia del repo
(sesión `2026-10-28d_zensical_migration`) mostró paridad de contenido con Zensical 0.0.73:
mismas 39 páginas, mismas rutas, mismo DOM para los assets propios y build ≈4× más rápido. Pero
también mostró que, sin esos hooks, `--strict` falla en un checkout limpio y el ZIP `latest`
desaparece sin aviso.

Fuerzas en conflicto: fecha límite de soporte del stack actual frente a la inmadurez del
sucesor; paridad funcional frente a pérdidas silenciosas.

## Decisión

**Zensical pasa a ser el generador por defecto de doc_ia**, de forma escalonada y con MkDocs como
respaldo hasta el fin de vida de Material:

1. **Preparación (hecha)**:
   - `scripts/build_docs_zip.py --builder zensical` ejecuta él mismo los hooks que Zensical
     ignora, y el post-build solo si el build termina con 0.
   - La CI incluye un build de paridad no bloqueante.
   - `check_env.py` informa de Zensical.
   - `tests/test_zensical_compat.py` falla ante plugins no soportados y ante enlaces rotos al ZIP.
2. **Cambio de default**, cuando se cumplan **todas** las condiciones:
   - **C1** — Zensical ≥ 0.1 publicado y fijado con versión exacta.
   - **C2** — build de paridad en verde en CI (Python 3.12 y 3.14) durante ≥ 2 semanas.
   - **C3** — revisión visual en claro y oscuro de páginas representativas (Mermaid, tablas,
     pestañas, descargas) y del botón de la barra lateral.
   - **C4** — ZIP `latest` cubierto por tests en el pipeline de Zensical.
   - **C5** — cambio hecho antes del 2027-05-05.
3. Se mantiene `mkdocs.yml` como **fuente única** de configuración: no se crea `zensical.toml`.
   Zensical lo lee de forma nativa y `scripts/doc_trace.py` lo parsea.

Se elige Zensical frente a seguir con MkDocs, o frente a un fork, porque es el sucesor mantenido
por el mismo equipo y lee la configuración actual sin migrarla.

## Consecuencias

| Tipo | Descripción |
|---|---|
| Ventaja | Continuidad de soporte más allá del 2027-05-05 sin reescribir la configuración |
| Ventaja | Build ≈4× más rápido y validación estricta más amplia (anclas, referencias) |
| Ventaja | Abre el ZIP navegable sin conexión con `offline` + `privacy`, que con MkDocs en Windows aborta en strict |
| Compromiso | La lógica de los hooks pasa a un paso pre/post de `build_docs_zip.py`: `zensical serve` no sincroniza los ficheros raíz |
| Deuda técnica | Lista de plugins soportados mantenida a mano en `tests/test_zensical_compat.py` hasta que Zensical la exponga |
| Deuda técnica | Fallback MkDocs (hooks, paridad en CI, dependencias) hasta su retirada tras el 2027-05-05 |
| Riesgo aceptado | Zensical en alfa: cambios entre parches; se mitiga con versión exacta y paridad continua en CI |

## Alternativas Consideradas

| Alternativa | Pros | Contras | Motivo de rechazo |
|---|---|---|---|
| Seguir con MkDocs + Material | Estable, sin trabajo | Sin soporte desde el 2027-05-05; MkDocs 2.0 incompatible | Solo aplaza el problema |
| Fork comunitario de MkDocs (p. ej. ProperDocs) | Mantiene la API de hooks y plugins | Mantenimiento incierto; Material seguiría sin soporte | No resuelve el fin de vida del tema |
| Migrar ya, sin escalonar | Menos tiempo con dos generadores | Alfa sin `hooks:`; pérdidas silenciosas | Riesgo funcional sin necesidad: hay margen hasta mayo de 2027 |
| Migrar a `zensical.toml` | Formato nativo de Zensical | Dos fuentes de verdad durante la transición; `doc_trace.py` lee YAML | Viola la regla de fuente única |

## Estado y Revisión

Estado: PROPUESTO
Fecha: 2026-10-28
Reemplazará a [ADR-001 — Use MkDocs Material as the default documentation generator](ADR-001-mkdocs-material-por-defecto.md)
cuando pase a ACEPTADO (fase F8 del plan de migración, sesión `2026-10-28d_zensical_migration`).
Revisar al publicarse Zensical 0.1: si soporta `hooks:`, el paso pre/post de `build_docs_zip.py`
se mantiene igualmente, porque no depende del generador.
