# Prompt: coverage_decisions — Registro de Decisiones de Cobertura (Arquetipo 13)

Genera, actualiza o **aplica** el registro de decisiones humanas sobre los apartados ⚠️ / ❌ / 🔍
de la documentación. La regla completa (estructura, campos, vocabulario, hallazgos) vive en
`.github/DOCUMENTATION_STANDARD.md` §3.18; este prompt solo describe el proceso.

## Cuándo usar

- Tras generar o actualizar una página del Arquetipo 8 (siempre) o de los Arquetipos 1/2/12 en un
  destino que tiene `docs/decisiones/` o cuyo usuario lo pide → **modo generación**.
- En cada revisión de la documentación, antes de regenerar páginas → **modo aplicación**.

## Inputs requeridos

- **Ámbito**: abreviatura de la norma (Arq. 8) o del módulo (Arq. 1/2/12), `[A-Z0-9]+`.
- **Páginas del ámbito**: `docs/normativa/<norma>_traceability.md` o las páginas funcional,
  técnica y de referencia del módulo.
- **Registro existente**: `docs/decisiones/<ámbito>_decisiones.md`, si ya existe.

## Modo generación

```
Actúa como analista de cumplimiento que prepara un documento de decisión para personas.
No decides: preparas cada apartado para que alguien decida con la información suficiente.

1. Lee las páginas del ámbito y localiza cada apartado ⚠️ / ❌ / 🔍 (en el Arq. 8, también ✅).
2. Asigna IDs COB-<ÁMBITO>-<NNN>: conserva los existentes; los nuevos toman el siguiente número
   libre. Nunca renumeres ni reutilices.
3. Escribe el ID en la página: en el Arq. 8, columna `ID`; en Arq. 1/2/12, al inicio de la celda
   «Elemento» del bloque "Evidencia". Enlázalo a su ficha.
4. Crea o actualiza `docs/decisiones/<ámbito>_decisiones.md` desde
   `.github/templates/DECISIONES_COBERTURA.template.md`:
   - Fichas nuevas con Decisión `Pendiente` y los campos de persona en `—`.
   - En «Evidencia», di qué falta exactamente para verificar (qué tabla de BD, qué sistema
     externo, qué documento organizativo).
   - NO modifiques ningún campo de persona de las fichas existentes.
   - Si cambia el estado de una ficha `Pendiente`, actualiza «Estado detectado».
   - Recalcula §2 Resumen.
5. Sella cada página del ámbito: `stamp` detecta los registros que enlaza y los guarda en
   `decisiones:` del frontmatter (no los añadas a `fuentes:`):
   python scripts/doc_trace.py [--root <origen>] stamp <página> [--archetype <n> si no tiene frontmatter]
6. Añade el registro al nav (sección «Decisiones», §3.18).
```

## Modo aplicación

```
1. Ejecuta `python scripts/doc_trace.py decisions` (o lee el registro si el destino no tiene
   el tooling). Clasifica: pendientes, decididas, hallazgos.
2. `invalid` / `incomplete` / `duplicate`: NO apliques esa ficha; repórtala en «Pendiente de
   revisión humana».
3. Para cada ficha con decisión válida y completa, en todas las filas que citan el ID:
   - el ID es un enlace a la ficha;
   - el último símbolo de la fila es el «Estado resultante» (admite `🔍 → ✅`) o `No aplica`;
   - las marcas del cuerpo de la página que repiten esa fila (⚠️ / 🔍 / ❌ al final de una frase
     o celda, sin ID) cambian igual: `decisions` no las comprueba;
   - en el Arq. 8, si la decisión cierra un gap, retíralo de «Resumen de gaps» y de
     «Próximas acciones»; si lo abre o lo mantiene, actualiza la acción con el contexto aportado.
   - Si la decisión aporta contexto verificable en el código, añádelo al bloque "Evidencia".
4. Añade una fila a §4 «Historial de revisiones» del registro y recalcula §2.
5. Re-sella las páginas tocadas (`stamp`) y repite `decisions` hasta que termine con 0
   (las pendientes no cuentan).
```

## Restricciones

- El agente nunca decide ni rellena campos de persona (Decisión, Contexto aportado, Responsable,
  Fecha, Estado resultante).
- No inventes contexto: el contexto nuevo solo procede de las fichas o del código verificable.
- No borres fichas ni reutilices IDs; un apartado retirado conserva su ficha.
- Sin datos personales, secretos ni URLs internas en el registro.

## Formato de salida al usuario

```
## Registro de decisiones — <Ámbito>
- docs/decisiones/<ámbito>_decisiones.md — [creado | actualizado]
- Fichas: N (nuevas: N) · Pendientes: N · Decididas: N

## Decisiones aplicadas
| ID | Decisión | Estado | Páginas actualizadas |

## Pendiente de revisión humana
- [fichas Pendiente con la pregunta concreta para quien decide]
- [fichas invalid / incomplete con el motivo]

## Verificación
- doc_trace decisions: [0 | 1 con N hallazgos]
```
