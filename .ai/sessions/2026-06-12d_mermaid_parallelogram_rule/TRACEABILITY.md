# TRACEABILITY — 2026-06-12d

## Objetivo

Corregir lexical error de Mermaid en `docker_howto.md` (rutas Unix como labels que disparan
la sintaxis paralelogramo) y regenerar `site/` para incluir `downloads.html`.

## Estado final: CLOSED ✅

---

## Cambios ejecutados

### 1. `docs/guides/docker_howto.md` (socyalpro)

Bloque Mermaid corregido:
- `subgraph Servidor / VM` → `subgraph srv[Servidor · VM]`
- `subgraph docker-compose` → `subgraph compose[docker-compose]`
- `DB[(Oracle / MySQL<br/>:1521 / :3306)]` → `DB[(Oracle · MySQL<br/>:1521 · :3306)]`
- `VOL_FS[/opt/vdesk/data/core/filesystem/]` → `VOL_FS[filesystem]`
- `VOL_JS[/opt/vdesk/data/jasper]` → `VOL_JS[jasper]`
- `VOL_CFG[/opt/vdesk/config]` → `VOL_CFG[config]`
- `VOL_STY[/opt/vdesk/styles]` → `VOL_STY[styles]`

### 2. `mkdocs build --strict` (socyalpro)

Rebuild del site → `site/downloads/index.html` y `site/guides/docker_howto/index.html`
generados correctamente.

### 3. `documentation-generator.agent.md` (doc_ia)

Regla Mermaid ampliada: `/` al inicio de `[...]` → PROHIBIDO (parallelogram Mermaid 11).
Rutas → nombres descriptivos. `<br/>` es seguro. `subgraph id[título]` sin hifens en ID.

### 4. `document_project.prompt.md` (doc_ia)

Misma regla añadida en sección Mermaid.

---

## Verificación

- `site/downloads/index.html` → ✅ existe
- `site/guides/docker_howto/index.html` → ✅ existe
- `mkdocs build --strict` → sin errores
