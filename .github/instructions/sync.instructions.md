---
applyTo: "CHANGELOG.md,CONTRIBUTING.md,docs/**,COMPATIBILITY.md,.ai/**,hooks/**"
---
# Sincronización raíz → docs/ y cierre de versiones

> **TL;DR** — Los ficheros Markdown de la raíz (`CHANGELOG.md`, `CONTRIBUTING.md`, …) son la
> fuente de verdad. Sus copias en `docs/` son **artefactos generados** por
> `hooks/sync_root_docs.py`; **nunca se editan directamente en `docs/`**.
> Antes de cerrar una versión, verifica también COMPATIBILITY.md y ejecuta `mkdocs build --strict`.

---

## Patrón de sincronización raíz → docs/ (`hooks/sync_root_docs.py`)

### Regla general

**Cualquier fichero Markdown de la raíz que deba aparecer en el sitio de documentación
se registra en `hooks/sync_root_docs.py` → `PAIRS` y nunca se edita en `docs/` directamente.**

| Fuente (raíz) | Copia generada (`docs/`) | Editar siempre en… |
|---|---|---|
| `CHANGELOG.md` | `docs/changelog.md` | `CHANGELOG.md` (raíz) |
| `CONTRIBUTING.md` | `docs/contributing.md` | `CONTRIBUTING.md` (raíz) |

### Cuándo se ejecuta el sync

- **Automático tras Edit/Write**: el hook `PostToolUse` de Claude Code ejecuta
  `python hooks/sync_root_docs.py` tras cada `Edit` o `Write`, sin acción manual.
- **MkDocs build**: el hook `on_pre_build` del propio MkDocs ejecuta el mismo script
  antes de compilar el sitio.
- **Manual**: `python hooks/sync_root_docs.py` desde la raíz del proyecto.

### Añadir un nuevo fichero al sync

Para que un nuevo fichero raíz aparezca automáticamente en `docs/`:

1. Añadir la tupla a `PAIRS` en `hooks/sync_root_docs.py`:
   ```python
   ("SECURITY.md", "security.md"),
   ```
2. Añadir la entrada en `nav:` de `mkdocs.yml`.
3. Nunca crear el fichero en `docs/` manualmente — el sync lo escribe en el siguiente build.
4. Si el fichero raíz usa enlaces relativos incompatibles con MkDocs (p.ej. a rutas fuera
   de `docs/`), añadir la sustitución al diccionario `_LINK_FIXES` del mismo script.

### Restricciones críticas

- **Prohibido** editar `docs/changelog.md`, `docs/contributing.md` o cualquier copia gestionada
  por `PAIRS`: el sync sobrescribirá los cambios en el siguiente build.
- Los hipervínculos Markdown dentro de ficheros raíz **no pueden apuntar a rutas fuera de
  `docs/`**: usa solo `code span` para referenciar paths del repositorio
  (ej. `.github/templates/TEMPLATE_mkdocs.yml`). Si el enlace es necesario, añade la URL
  absoluta al repo o mueve el recurso dentro de `docs/`.

---

## Cuándo aplicar estas reglas

Aplica este checklist en la fase **VERSION** de cualquier flujo:

- `feat:` que añade API pública nueva
- `fix:` que cambia comportamiento observable
- `refactor:` con renombramiento de símbolos exportados
- Cierre de sprint o release (slash command `/version-closure`)

---

## Checklist de sincronización obligatorio

### 1. CHANGELOG.md (raíz del repositorio)

- [ ] La versión nueva tiene entrada bajo `## [X.Y.Z] — YYYY-MM-DD`
- [ ] Secciones presentes según cambios: `Added`, `Changed`, `Fixed`, `Removed`, `Deprecated`
- [ ] Cada ítem referencia el módulo afectado: `scripts/`, `docs/`, `.github/prompts/`, `.claude/commands/`
- [ ] No hay entradas bajo `Unreleased` que deban estar en la versión cerrada

### 2. docs/changelog.md y docs/contributing.md (copias generadas)

- [ ] **No editar directamente** — son artefactos de `hooks/sync_root_docs.py`
- [ ] Si hay divergencia con la raíz, ejecutar `python hooks/sync_root_docs.py` para regenerar
- [ ] Verificar que el build no produzca warnings de links rotos en estas páginas

### 3. COMPATIBILITY.md / .ai/COMPATIBILITY.md

- [ ] Versión nueva añadida con columnas: `Versión | Python | Dependencias clave | Estado`
- [ ] Marcada como `✅ Activa` si es la release más reciente
- [ ] Versiones anteriores marcadas como `⚠️ Legacy` o `❌ EOL` según corresponda
- [ ] Si existe `.ai/COMPATIBILITY.md`, sincronizado con `docs/COMPATIBILITY.md`

### 4. pyproject.toml

- [ ] `version = "X.Y.Z"` actualizado y coincide con el CHANGELOG.md
- [ ] `requires-python = ">=3.12"` sin modificar (no incrementar sin decisión explícita)

### 5. MkDocs

- [ ] `mkdocs build` pasa sin errores ni warnings de links rotos
- [ ] Si se crearon páginas nuevas, están en `mkdocs.yml` bajo `nav:`
- [ ] Si se eliminaron páginas, se retiraron de `mkdocs.yml`

---

## Formato de entrada CHANGELOG

```markdown
## [0.2.0] — 2026-06-10

### Added
- `scripts/check_links.py`: validación de enlaces rotos en docs/ antes del build

### Fixed
- `scripts/build_docs_zip.py`: corregido nombre del ZIP cuando la versión contiene sufijo

### Changed
- `.github/prompts/functional_doc.prompt.md`: actores por defecto actualizados en §3
```

---

## Reglas de versionado (SemVer)

| Tipo de cambio | Incremento |
|---|---|
| API pública nueva sin breaking changes | `MINOR` (0.X.0) |
| Breaking change en API pública | `MAJOR` (X.0.0) |
| Bugfix sin cambio de API | `PATCH` (0.0.X) |
| Cambio solo en docs o tests | `PATCH` (0.0.X) |

---

### 6. `.ai/sessions/*/TRACEABILITY.md` (cierre de sesión)

- [ ] Sección `## Directrices para Futuras IAs` presente y poblada (no vacía, no solo `-`)
- [ ] Cada directriz tiene el formato `**[área]**: <hecho verificable>`
- [ ] Veredicto final es `CLOSED` (o `GO` / `GO_CONDICIONAL` si la sesión queda abierta)

---

## Comando de validación final

```bash
mkdocs build --strict
```

El flag `--strict` convierte warnings en errores, garantizando que no queden links rotos
ni referencias a páginas inexistentes en `mkdocs.yml`.

---

*Actualizado: 2026-05-22*
