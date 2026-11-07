<!--
PLANTILLA — CIERRE de document_project.prompt.md (contexto persistente del destino).

Destino: <raíz del destino>/.ai/product.md (raíz = carpeta con mkdocs.yml / zensical.toml).
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
# Producto — {proyecto}

> Contexto persistente sobre el **proyecto fuente** documentado en este repositorio.
> Orígenes: {orígenes con ref/versión — ver `.ai/sources.json` y `.ai/doc_state.json`}.
> Revisado: {AAAA-MM-DD}.

## 1. Qué es

{Qué hace el producto o módulo y en qué sistema mayor se integra, si aplica.}

## 2. Audiencia

{Roles o perfiles que lo usan, tomados del código (roles, menús) o de los documentos.}

## 3. Capacidades

{Capacidades actuales verificadas en el código. Lo previsto en especificaciones va en §5.}

## 4. Marco legal y normativo

{Normas de obligado cumplimiento (Arquetipo 8) y referencias no vinculantes, por separado.}

## 5. Estado y evolución

{Versión documentada, decisiones abiertas (ADR propuestos), evolutivos previstos.}
