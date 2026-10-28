# Casos Límite Conocidos — doc_ia

> Plantilla inicial creada en el bootstrap (2026-06-10). Se puebla con el tiempo:
> cada caso límite descubierto en sesiones de trabajo se registra aquí con su contexto.

## Formato de registro

```markdown
## [área] — Título breve

- **Síntoma**: qué se observa
- **Causa**: por qué ocurre (verificado, no especulado)
- **Tratamiento**: cómo lo maneja el código o la instrucción IA
- **Sesión**: .ai/sessions/<fecha>/ donde se descubrió
```

## Casos registrados

## [mkdocs.yml] — `navigation.sections` impide colapsar el menú lateral

- **Síntoma**: En la documentación generada, los submenús del panel izquierdo no se pueden
  colapsar con clic. Los grupos del nav aparecen como etiquetas estáticas en gris tenue,
  no como elementos plegables. El botón ◀/▶ de sidebar tampoco aparece aunque
  `sidebar-toggle.js` esté cargado.
- **Causa**: `navigation.sections: true` en `theme.features` de `mkdocs.yml` activa el modo
  de grupos estáticos de Material, que deshabilita `.md-nav__item--nested`. Esto hace que
  `nav.css` (que aplica estilos a `--nested`) no tenga efecto sobre la colapsabilidad.
  Simultáneamente, si faltan `extra_css` y `extra_javascript`, los assets de toggle y Mermaid
  no se cargan en absoluto.
- **Tratamiento**:
  1. Eliminar `navigation.sections` de `theme.features` en `mkdocs.yml`.
  2. Crear `docs/assets/css/nav.css`, `docs/assets/css/mermaid.css`,
     `docs/assets/js/sidebar-toggle.js`
     (copiar desde `doc_ia/docs/assets/`; desde 2026-10-28 ya no se copia `mermaid.js`, ver § Mermaid; cambiar `STORAGE_KEY` en `sidebar-toggle.js`
     al nombre del proyecto, ej. `dpss_sidebar_collapsed`).
  3. Añadir `extra_css` y `extra_javascript` en `mkdocs.yml` referenciando esos assets.
  4. Añadir features universales ausentes: `navigation.tabs.sticky`, `navigation.footer`,
     `toc.follow`, `content.code.annotate`, `content.tabs.link`.
  5. Añadir markdown extensions universales ausentes: `pymdownx.highlight`,
     `pymdownx.inlinehilite`, `pymdownx.snippets`, `pymdownx.emoji`, `attr_list`, `md_in_html`.
- **Prevención**: La sección "Sincronización de Configuración Visual (Fase 0b)" de
  `/document-project` es ahora **OBLIGATORIA** al inicio de toda sesión (creación Y actualización).
  Ver checklist en `.claude/commands/document-project.md`.
- **Sesión**: `.ai/sessions/2026-06-12/` (dpss)

## [plugin MkDocs] — Plugin ZIP no encontrado al ejecutar `mkdocs build`

- **Síntoma**: `ERROR - Config value 'plugins': The "{nombre}_documentation_zip" plugin is not installed.`
  El build falla aunque el plugin fue creado e instalado correctamente.
- **Causa**: el entry point del plugin está registrado en un venv específico
  (`doc_ia\.venv\Lib\site-packages\{nombre}_docs-{versión}.dist-info`). Cuando el terminal
  no tiene ese venv activo, `mkdocs` resuelve a otro Python (p. ej.
  `C:\Users\{user}\AppData\Roaming\Python\Python314\Scripts\mkdocs.exe`) que no conoce el plugin.
  Hay múltiples `mkdocs` en el PATH del sistema; el que "gana" depende del orden del PATH
  y del venv activo en el terminal concreto.
- **Solución definitiva (2026-06-15)**: **no usar el sistema de plugins** para la generación del ZIP.
  Migrar a un hook MkDocs nativo (`mkdocs_hooks.py`) cargado mediante la clave `hooks:` de `mkdocs.yml`.
  El hook no requiere instalación, no usa entry points y funciona con cualquier Python que tenga `mkdocs`.
  Patrón canónico: `doc_ia/mkdocs_hooks.py` (solo cambiar `zip_path` para otro proyecto).
  ```yaml
  # mkdocs.yml — añadir:
  hooks:
    - mkdocs_hooks.py
  # y eliminar el plugin de la sección plugins:
  ```
- **Workaround temporal** (si no es posible migrar aún):
  - Activar el venv antes del build: `doc_ia\.venv\Scripts\Activate.ps1`
  - O invocar explícitamente: `python -m mkdocs build --strict`
    (donde `python` = `doc_ia\.venv\Scripts\python.exe`)
- **Sesión**: `.ai/sessions/2026-06-12/` (descubierto); `.ai/sessions/2026-06-15_hooks_migration/` (resuelto)

## [doc_trace] — `drift` marca páginas tras cambios triviales o tras editar `mkdocs.yml`/`CLAUDE.md`

- **Síntoma**: `python scripts/doc_trace.py drift` lista una página como `stale` aunque su
  contenido sigue siendo correcto.
- **Causa**: la huella es el SHA256 del fichero fuente completo (saltos normalizados a LF). Un
  comentario, un espacio o cualquier edición de una fuente compartida (p. ej. `mkdocs.yml` o
  `CLAUDE.md`, citadas por `docs/reference/index.md`) cambia la huella. Es intencionado: el
  script no interpreta el contenido.
- **Solución**: revisar la página contra el diff de la fuente (`git diff <fuente>`); si sigue
  siendo correcta, re-sellar con `python scripts/doc_trace.py stamp <página>`. No re-sellar a
  ciegas en bloque.
- **No es causa**: sellar una página que es fuente de otra (p. ej. el Mapa Funcional): el
  frontmatter de las fuentes `.md` se excluye de la huella.
- **Sesión**: `.ai/sessions/2026-10-28_archetypes_v2/` (P3)

## [mkdocs_hooks.py] — El ZIP `latest` se regenera aunque `mkdocs build --strict` falle

- **Síntoma**: tras un build estricto que termina con `Aborted with N warnings in strict mode`,
  `site/doc_ia-docs-latest.zip` y su `.sha256` tienen fecha nueva.
- **Causa**: MkDocs 1.6 ejecuta `on_post_build` antes de comprobar los avisos del modo estricto.
- **Decisión (2026-10-28)**: aceptado. El ZIP local de un build fallido no se distribuye: los
  workflows solo publican si el build termina con 0. No usar `site/` tras un build fallido.
  Con `build_docs_zip.py --builder zensical` no ocurre: el ZIP se genera solo tras un build OK.
- **Sesión**: `.ai/sessions/2026-10-28c_quality_pending/`

## [Zensical] — `hooks:` de `mkdocs.yml` se ignora en silencio

- **Síntoma**: `zensical build --strict` falla con `changelog.md: page does not exist` en un
  checkout limpio, o termina bien pero `site/` no contiene `doc_ia-docs-latest.zip` y los enlaces
  de `docs/downloads.md` al ZIP quedan rotos (ningún `--strict` valida `<a href>` en HTML crudo).
- **Causa**: Zensical (0.0.73) no soporta la clave `hooks:` ni la API de plugins de MkDocs y no
  emite ningún aviso (zensical.org/compatibility/configuration). Los plugins no soportados
  también se ignoran en silencio.
- **Tratamiento**: construir siempre con `python scripts/build_docs_zip.py --builder zensical`,
  que ejecuta `hooks/sync_root_docs.py` antes y `mkdocs_hooks.py` después de un build OK.
  `python -m zensical serve` no sincroniza: tras editar `CHANGELOG.md`/`CONTRIBUTING.md`, ejecutar
  `python hooks/sync_root_docs.py` (en Claude Code lo hace el PostToolUse).
- **Guardas**: `tests/test_zensical_compat.py` falla si `mkdocs.yml` declara un plugin fuera de
  `ZENSICAL_SUPPORTED_PLUGINS` o si los enlaces al ZIP de `docs/downloads.md` no resuelven al
  ZIP `latest` (p. ej. al cambiar `use_directory_urls`). Al actualizar Zensical, revisar la lista
  contra zensical.org/compatibility/plugins.
- **Sesión**: `.ai/sessions/2026-10-28d_zensical_migration/` (F1, F4)

## [Mermaid] — CDN propio + `mermaid.run()` duplican el render del tema

- **Síntoma**: los diagramas se ven, pero cada bloque `.mermaid` contiene además un SVG de error
  de Mermaid oculto. Con carreras de carga, en algún diagrama puede llegar a verse «Syntax error
  in text».
- **Causa** (verificada con Edge headless + CDP, `DOM.getDocument(pierce=True)`): con
  `custom_fences: mermaid`, Material (y Zensical) cargan Mermaid por sí mismos y pintan cada
  diagrama en un shadow root **cerrado**. El `mermaid.run()` de `assets/js/mermaid.js` (más el CDN
  `mermaid@11`) procesa después el mismo bloque, ya transformado, y falla: 23/23 SVG de error
  ocultos en doc_ia.
- **Contraprueba**: sin `custom_fences` no se genera ningún `.mermaid` y el diagrama sale como
  código. Ni el CDN ni `mermaid.js` lo arreglan, porque también buscan `.mermaid`. La pieza
  imprescindible es `custom_fences`. La RCA de 2026-06-12a (socyalpro) atribuyó el fallo a la
  falta del CDN.
- **Tratamiento**: `extra_javascript` sin CDN de Mermaid ni `assets/js/mermaid.js`; `custom_fences`
  obligatorio (Fase 0b / Fase 5). Verificado en doc_ia: 23/23 diagramas visibles con MkDocs y con
  Zensical, en claro y en oscuro; en oscuro el tema aplica sus colores. Mermaid se sigue cargando
  desde CDN (lo hace el tema): el ZIP offline necesita red para los diagramas hasta F10 (`privacy`).
- **Prevención**: `tests/test_docs_conformance.py::test_mermaid_nodes_do_not_start_with_slash`
  para errores de sintaxis que `--strict` no ve; verificación visual con CDP antes de cambiar la
  integración.
- **Sesión**: `.ai/sessions/2026-10-28d_zensical_migration/` (F6a, F6)

## [Mermaid] — Entidades HTML en labels se pintan con un `&` sobrante

- **Síntoma**: `H[on_post_build&#40;config&#41;]` se ve como `on_post_build&(config&)`; la regla
  `@` → `&#64;` (sesión 2026-06-12b) pinta `Cl&@ve`. El build `--strict` pasa y Mermaid no da error.
- **Causa** (verificada renderizando con mermaid@11 y @12 en Edge headless): Mermaid no decodifica
  entidades HTML; su sintaxis propia es `#64;` (sin `&`). El `&` queda como texto.
- **Diagnóstico previo correcto, remedio incorrecto**: sin comillas, `@`, `(`, `)`, `{` o `}`
  dentro de `[...]` o `{...}` sí son parse error en v11 y v12.
- **Tratamiento**: label entre comillas dobles (`A["Cl@ve (firma)"]`); una `"` interna → `#quot;`.
  `#`, `#64;`, `A@{ shape: … }` y `["/ruta"]` entre comillas renderizan bien.
- **Prevención**: `tests/test_docs_conformance.py::test_mermaid_no_html_entities` y
  `::test_mermaid_special_chars_quoted` (detector calibrado con fixtures renderizadas).
- **Pendiente fuera de doc_ia**: los destinos que aplicaron la regla `&#64;` (socyalpro) muestran
  el `&`; corregir con un hotfix en cada repositorio.
- **Sesión**: `.ai/sessions/2026-10-28e_mermaid_diagrams/` (M0)
