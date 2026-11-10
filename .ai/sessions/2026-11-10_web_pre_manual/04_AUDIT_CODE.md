# AUDIT_CODE — scripts/web_captures.py y metodología del origen WEB

## Hallazgos y correcciones

| # | Severidad | Hallazgo | Corrección | Test |
|---|---|---|---|---|
| C1 | Alta | `NAME_RE` admitía `.` y `..` como nombre de origen: `publish` resolvía `_staging/..` y escribía fuera de `docs/assets/manual/` | `NAME_RE = ^(?!\.+$)[\w.-]+$` | `test_publish_rejects_origin_names_that_leave_staging` (4 casos) |
| C2 | Media | Un origen que no era objeto en un manifiesto editado a mano rompía `check` con un traceback (exit 1, no 2) | `read_manifest` valida cada origen y sus `capturas` | `test_check_rejects_a_malformed_manifest_entry` |
| C3 | Media | No se ignoraban bloques de código indentados (admoniciones `???`), los de 4+ delimitadores ni el código inline: falsos `rota` o `sin_alt` | `FENCE_RE` con indentación y `{3,}`; `INLINE_CODE_RE` | `test_check_ignores_indented_fences_and_inline_code_and_reads_single_quotes` |
| C4 | Baja | `<img src='…'>` con comillas simples no se reconocía: captura citada marcada como `huerfana` | `HTML_ATTR_RE` acepta comillas simples | mismo test |

## Revisado sin hallazgos

- **Seguridad**: los mensajes de error no repiten la URL rechazada; las rutas de captura se
  normalizan y se rechazan las absolutas, las que llevan unidad y las que salen con `..`; se
  valida todo antes de escribir. La metodología prohíbe en el modo navegador cualquier acción con
  efecto y trata el texto web como dato.
- **Rendimiento**: lineal en imágenes y páginas; huellas por bloques de 1 MiB.
- **Tipado**: mypy strict sin errores.
- **Edge cases**: rutas con `\` (Windows), atributos `{ … }` tras la imagen, `#`/`?` en la ruta,
  URL absolutas e imágenes fuera de `assets/manual/` ignoradas.

## Límites aceptados (documentados)

- Las imágenes con referencia (`![alt][ref]`) no se reconocen: la captura aparece como
  `huerfana`. Se citan con la forma directa.
- Un enlace simbólico dentro de `_staging/` se copia como fichero normal (`_staging/` lo crea
  `snapshot_sources.py`, que copia ficheros).
- `NAME_RE` de `snapshot_sources.py` también admite `.`/`..`. Es anterior a esta feature y queda
  fuera de su alcance (sin refactor). **Propuesta**: un hotfix aparte.

## Verificación

19 casos en `tests/test_web_captures.py`; suite completa, ruff, mypy y `mkdocs build --strict`
en verde; `doc_trace` sin drift. Documentación actualizada: funcional AC-09 – AC-11 (11/11),
técnica y referencia.

## Veredicto

**APROBADO**: las cuatro correcciones están aplicadas y probadas. Queda una propuesta fuera de
alcance (C1 en `snapshot_sources.py`).
