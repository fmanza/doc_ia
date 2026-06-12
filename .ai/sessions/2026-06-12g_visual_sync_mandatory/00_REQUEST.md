# Sesión 2026-06-12g — Visual Sync Mandatory

## Origen de la sesión

Problema detectado en producción (dpss): el menú lateral de la documentación generada
no era colapsable y los márgenes eran excesivamente anchos. La causa fue identificada
comparando el `mkdocs.yml` de dpss con el de doc_ia como referencia.

## Objetivo

1. **Corregir dpss**: aplicar la configuración visual correcta (assets + mkdocs.yml).
2. **Documentar el requisito en doc_ia**: elevar la Sincronización Visual (Fase 0b)
   de "Recomendado" a **OBLIGATORIO** en todo `/document-project`, tanto en creación
   como en actualización.

## Inputs

| Parámetro | Valor |
|---|---|
| Proyecto afectado (fix) | `C:\Desarrollo\Proyectos\dpss` |
| Repositorio de reglas (doc) | `c:\Desarrollo\python\libs\doc_ia` |
| Archivos modificados en doc_ia | `CLAUDE.md`, `.claude/commands/document-project.md`, `.claude/EDGE_CASES.md`, `.claude/settings.json` |

## Restricciones

- Sin commit en dpss (restricción de sesión anterior).
- Commit en doc_ia: autorizado por el usuario.
