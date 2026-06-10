# REQUEST

## Session metadata
- id: 2026-06-11b
- fecha: 2026-06-11
- rama: develop
- skill: refactor documental
- fase solicitada: IMPLEMENT directo

## Solicitud original saneada

"Revisar la documentación de `util_bbdd` en el apartado Descargas — 'Descarga Actual' —
donde se genera el ZIP y la Checksum; incluir en las instrucciones IA de doc_ia todo lo
necesario para que se cree ese fichero y su Checksum."

Ejemplo proporcionado:
```
| Versión | Tamaño | Checksum | Fecha |
| util_bbdd-docs-latest.zip ~2.5 MB | .sha256 | 2026-06-06 |
```

## Objetivo operativo de esta sesión

1. Actualizar `docs/downloads.md` en doc_ia: sección "Descarga Actual" con tabla real
   (versión, tamaño, link .sha256, fecha) igual que util_bbdd.
2. Añadir en `CLAUDE.md` instrucciones precisas para mantener esa tabla tras cada build
   de ZIP (comandos para extraer versión, tamaño, hash, fecha).

## Restricciones explícitas

- No inventar capacidades ni URLs: usar datos reales del artefacto `dist/doc_ia-docs-0.1.0.zip`.
- Solo una fila en la tabla (versión más reciente); el histórico vive en `dist/CHECKSUMS.txt`.
- Build `mkdocs build --strict` debe quedar limpio tras los cambios.

## Resultado esperado

- `docs/downloads.md`: tabla "Descarga Actual" con datos reales de v0.1.0.
- `CLAUDE.md`: subsección "Actualizar tabla Descarga Actual" con plantilla y comandos.
- Build `mkdocs build --strict`: sin errores.
- Sesión `.ai/sessions/2026-06-11b_downloads_table_update/` creada.
- Commit preparado para GitHub.
