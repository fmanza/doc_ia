# Cómo Contribuir a doc_ia

## 1. Tipos de Contribución Aceptados

- **Reportar bugs**: abre un issue en [GitHub](https://github.com/fmanza/doc_ia/issues)
  describiendo el comportamiento incorrecto, los pasos para reproducirlo y el output esperado.
- **Proponer mejoras**: abre un issue con la etiqueta `enhancement` antes de implementar
  un cambio significativo; permite alinear con la visión del proyecto.
- **Nuevos arquetipos o instrucciones IA**: las adiciones a `.github/prompts/` y
  `.github/agents/` son bienvenidas si siguen los principios innegociables del proyecto
  (sin API keys, sin componentes programáticos IA, ejecución en el chat).
- **Mejoras al tooling determinista**: `scripts/check_env.py` y `scripts/build_docs_zip.py`
  aceptan PRs si mantienen compatibilidad con `python -m ruff check` + `mypy strict` + `pytest`.
- **Mejoras de documentación**: correcciones, aclaraciones o nuevos ejemplos en `docs/`.

## 2. Antes de Contribuir

Este proyecto no requiere CLA. Al enviar un PR aceptas que tu contribución se distribuye
bajo la misma licencia que el proyecto.

Si tu cambio toca `.github/SHARED_INSTRUCTIONS.md`, `.github/DOCUMENTATION_STANDARD.md`
o `CLAUDE.md`, abre un issue previo para discutir el alcance — estos ficheros son la fuente
canónica del sistema y los cambios tienen impacto transversal.

## 3. Proceso de Contribución

1. Haz fork del repositorio y clona tu fork:
   ```bash
   git clone https://github.com/<tu-usuario>/doc_ia.git
   cd doc_ia
   ```
2. Crea una rama desde `develop` (nunca desde `main`):
   ```bash
   git checkout develop
   git checkout -b feat/descripcion-corta
   ```
   Prefijos válidos: `feat/`, `fix/`, `docs/`, `chore/`, `refactor/`.
3. Configura el entorno:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   # source .venv/bin/activate   # Linux/Mac
   python -m pip install -r requirements.txt
   python scripts/check_env.py
   ```
4. Implementa el cambio y añade o actualiza tests en `tests/` si corresponde.
5. Verifica la calidad (ver §5) antes de hacer commit.
6. Haz commit con [Conventional Commits](https://www.conventionalcommits.org/):
   ```bash
   git commit -m "feat(check_env): añadir verificación de zensical"
   ```
7. Abre un PR contra la rama `develop` del repositorio original con:
   - Descripción del cambio y motivación.
   - Output de `python -m pytest` sin errores.
   - Si afecta a `docs/`: output de `python -m mkdocs build --strict` sin warnings.

## 4. Convenciones de Código y Commits

Referencia completa: `.github/SHARED_INSTRUCTIONS.md` § Convenciones.

| Tipo commit | Cuándo usar |
|---|---|
| `feat` | Nueva funcionalidad visible para el usuario |
| `fix` | Corrección de bug |
| `docs` | Solo cambios en documentación |
| `chore` | Tareas de mantenimiento sin impacto funcional |
| `refactor` | Refactorización sin cambio de comportamiento |
| `test` | Añadir o corregir tests |

Formato: `tipo(ámbito): descripción imperativa en minúsculas` — máximo 72 caracteres.

## 5. Requisitos de Calidad

Los siguientes comandos deben ejecutarse sin errores antes de abrir PR:

```bash
python -m ruff check scripts tests   # Linting
python -m ruff format scripts tests  # Formato (verificar diff limpio)
python -m mypy scripts               # Type-checking strict
python -m pytest                     # Tests
python -m mkdocs build --strict      # Build de docs (si hay cambios en docs/)
```

Un PR que falle en cualquiera de estos comandos no será mergeado.

## 6. Proceso de Release y Versionado

Este proyecto sigue [Semantic Versioning](https://semver.org/):
- `MAJOR`: cambio incompatible en la API de los arquetipos o en los contratos de los scripts.
- `MINOR`: nueva funcionalidad retrocompatible (nuevo arquetipo, nuevo script, nuevo agente).
- `PATCH`: correcciones de bugs y mejoras de documentación.

Solo los mantenedores del proyecto tienen permisos de release. El proceso:
1. Actualizar `version` en `pyproject.toml`.
2. Cerrar la sección `[Unreleased]` en `CHANGELOG.md` con la nueva versión y fecha.
3. Crear tag `vX.Y.Z` en `main`; el workflow `docs-zip-release.yml` publica automáticamente
   el ZIP de documentación offline.

Historial de cambios: [CHANGELOG.md](changelog.md).
