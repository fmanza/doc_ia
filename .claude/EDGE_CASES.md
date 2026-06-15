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
     `docs/assets/js/sidebar-toggle.js`, `docs/assets/js/mermaid.js`
     (copiar desde `doc_ia/docs/assets/`; cambiar `STORAGE_KEY` en `sidebar-toggle.js`
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
