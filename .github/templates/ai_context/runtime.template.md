<!--
PLANTILLA — CIERRE de document_project.prompt.md (contexto persistente del destino).

Destino: <raíz del destino>/.ai/runtime.md (raíz = carpeta con mkdocs.yml / zensical.toml).
Describe el PROYECTO FUENTE documentado, no doc_ia. Lo lee una IA futura en su
00_CONTEXT_SNAPSHOT antes de empezar.

Reglas:
  · Rellenar SOLO con lo observado en los orígenes de ESTE proyecto durante el INVENTARIO
    (código, documentos de _fuentes/, .ai/sources.json, .ai/doc_state.json). Nunca inventar.
  · Otros destinos documentados con doc_ia (proyectos hermanos) NO son plantilla ni fuente:
    no copiar su texto, sus valores ni sus decisiones.
  · Secciones fijas: no omitir ni renumerar; vacías → "*No aplica para este proyecto.*".
  · Cada dato verificable con su fuente (`ruta::símbolo` o `_fuentes/...`) cuando no sea obvio.
  · Sesiones posteriores: actualizar solo lo que el INVENTARIO detecte como cambiado.
Borrar este comentario al rellenar.
-->
# Runtime — repositorio de documentación de {proyecto}

## 1. Estructura

{Tabla | Ruta | Contenido | del destino: docs/, mkdocs.yml, _fuentes/, _staging/, .ai/…}

## 2. Orígenes y cómo refrescarlos

{Por origen: forma (Fase 0-pre), ruta de trabajo y comando de refresco (snapshot_sources sync, git fetch + checkout del worktree…).}

## 3. Comandos

{changes, drift, decisions, build --strict, ZIP — con las rutas reales de este destino.}

## 4. Primera vez en otro equipo

{Cómo recrear _staging/ (worktrees, sincronización de SharePoint) sin datos de este equipo.}
