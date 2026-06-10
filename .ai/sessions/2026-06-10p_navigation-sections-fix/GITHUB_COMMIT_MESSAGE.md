# GITHUB COMMIT MESSAGE

```
fix(util): eliminar navigation.sections incompatible con nav.css

nav.css requiere que navigation.sections esté ausente para que los grupos
del menú lateral sean colapsables (.md-nav__item--nested). Con la feature
activa, Material renderiza cabeceras estáticas y desactiva el colapso.

Cambios:
- util/mkdocs.yml: eliminar `- navigation.sections` de theme.features
- .github/templates/TEMPLATE_mkdocs.yml: comentar línea con aviso ⚠️
- .claude/commands/document-project.md: añadir tabla de compatibilidad
  de theme.features en Fase 0b (copiables vs decisión)

Validación: mkdocs build --strict (util) → 0 warnings

Fixes: defecto introducido en sesión o al sincronizar features sin
distinguir las incompatibles con nav.css
```
