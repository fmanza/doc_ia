<!--
PLANTILLA — Prompt de instancia del kit de documentación (CIERRE de document_project.prompt.md).

Destino: <raíz del destino>/.ai/prompts/documentar.prompt.md. Solo PARÁMETROS y DECISIONES de
ESTE proyecto: las reglas viven en `.doc_ia/` y no se repiten aquí. Lo crea la primera sesión y
lo actualiza cada CIERRE con las decisiones nuevas (alcance, clasificación, prioridades).
Secciones fijas 1-7: no omitir ni renumerar; vacías → "No aplica". Nada copiado de otros
destinos documentados con doc_ia.
Borrar este comentario en el fichero generado.
-->
# Prompt de instancia — documentar {proyecto}

Lo aplican `/documentar` y los lanzadores del kit (`AGENTS.md`). Las reglas están en
`.doc_ia/.github/prompts/document_project.prompt.md`; si algo de aquí las contradice, mandan
ellas y se avisa al usuario.

## 1. Parámetros

| Parámetro | Valor |
|---|---|
| Raíz del destino | {ruta} |
| Generador | zensical (único; ADR-003) |
| Idioma | {es \| en} |
| Modo por defecto | incremental (completo si no hay baseline) |
| Arquetipos | {lista y opt-in} |

## 2. Orígenes

| Nombre | Tipo | Forma | Origen | Ref / Versión |
|---|---|---|---|---|
| {nombre} | {CÓDIGO \| MANUAL \| …} | {repositorio + worktree \| fichero con {ver} \| carpeta \| SharePoint sincronizado} | {URL o ruta} | {rama \| patrón} |

## 3. Adquisición

{Comandos exactos de la Fase 0-pre para cada origen (snapshot_sources add/sync, fetch + worktree).}

## 4. Alcance

{Proyecto completo, o rutas `--path` vigentes (las guardadas en `.ai/doc_state.json`).}

## 5. Decisiones de contenido

{Prioridad entre fuentes, clasificación confirmada (normativa vs referencia), dominio sensible,
decisiones del usuario con su fecha.}

## 6. Independencia

Plantillas y artefactos de `.doc_ia/`; decisiones con evidencia de los orígenes de este proyecto.

## 7. Salida esperada

{Fases y artefactos que debe dejar cada sesión (CIERRE, commit local, ZIP).}
