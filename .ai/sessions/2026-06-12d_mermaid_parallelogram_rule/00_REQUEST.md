# 00_REQUEST — 2026-06-12d

## Solicitud

Dos errores en `C:\Desarrollo\Proyectos\socyalpro\docs\`:

1. **Mermaid "Lexical error on line 10. Unrecognized text."** en Despliegue con Docker
   (`docs/guides/docker_howto.md`)
2. **`downloads.md` falta** en el site servido

## RCA

### Error Mermaid — `[/path]` como paralelogramo

Mermaid 11 interpreta `[/texto/]` como nodo paralelogramo. Cuando hay `/` al inicio
del label pero sin `/` de cierre, el lexer lanza "Lexical error on line N+1".

En `docker_howto.md`, los nodos de volúmenes usaban rutas UNIX:
```
VOL_FS[/opt/vdesk/data/core/filesystem/]  ← [/.../.../] → paralelogramo (accidentalmente válido)
VOL_JS[/opt/vdesk/data/jasper]            ← [/...] sin cierre → ERROR línea siguiente
VOL_CFG[/opt/vdesk/config]               ← ídem
VOL_STY[/opt/vdesk/styles]               ← ídem
```

También: `subgraph Servidor / VM` y `subgraph docker-compose` (sin ID alfanumérico).

### downloads.md falta en site

`site/` era un directorio generado antes de que se añadiera `downloads.md` a `docs/`.
El fichero existía en `docs/` pero `site/downloads/index.html` no existía.
Solución: `mkdocs build --strict`.

## Regla nueva para agentes

- `[/texto]` al inicio de un label en flowchart → parallelogram sin cierre → lexical error
- Rutas UNIX/Windows en labels → usar nombres descriptivos o `·`
- `subgraph` → siempre `subgraph id[título]` con ID alfanumérico sin hifens
