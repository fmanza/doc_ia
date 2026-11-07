<!--
PLANTILLA — CIERRE de document_project.prompt.md (contexto persistente del destino).

Destino: <raíz del destino>/.ai/glossary.md (raíz = carpeta con mkdocs.yml / zensical.toml).
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
# Glosario — {proyecto}

| Término | Significado | Fuente |
|---|---|---|
| {término del dominio, capa o abreviatura} | {definición} | {`ruta::símbolo` o `_fuentes/...`} |
