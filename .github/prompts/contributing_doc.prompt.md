# Prompt: contributing_doc — Guía de Contribución (Arquetipo 11)

Genera o actualiza `CONTRIBUTING.md` para **doc_ia** usando solo información verificable
del proyecto (SHARED_INSTRUCTIONS.md, workflows, pyproject.toml, README).

**Diferencia con Onboarding Dev (Arquetipo 7)**: El onboarding es para quien se incorpora
al equipo y trabaja en el día a día. Esta guía es para colaboradores externos o primeras
contribuciones puntuales.

## Instrucción al modelo

```
Actúa como maintainer de proyecto open source escribiendo la guía de contribución.

Analiza los ficheros reales del proyecto (SHARED_INSTRUCTIONS.md, .github/workflows/,
pyproject.toml, CLAUDE.md) para describir el proceso y las convenciones con precisión.

NO inventes procesos, comandos, herramientas ni convenciones no verificables en el proyecto.

Genera CONTRIBUTING.md siguiendo el Arquetipo 11 con estas secciones en este orden exacto:

# Cómo Contribuir a [Nombre Proyecto]

## 1. Tipos de Contribución Aceptados
Lista de formas en que se puede contribuir (reportar bugs, proponer features,
mejorar docs, enviar PRs de código).
Si el proyecto NO acepta contribuciones externas: indicarlo explícitamente
y cerrar el archivo aquí con instrucciones de contacto.

## 2. Antes de Contribuir
Código de conducta: si existe, enlazar; si no, indicar "Este proyecto no tiene CoC formal."
Acuerdo de contribución (CLA): si aplica, indicar el proceso.
Forma de comunicar antes de empezar trabajo grande: issues, discussions, etc.

## 3. Proceso de Contribución
Pasos numerados:
1. Fork / clonar el repositorio
2. Crear rama desde [rama-principal] (nombre: feat/, fix/, docs/, chore/)
3. Implementar cambio con tests
4. Verificar calidad (ver §5)
5. Abrir PR con descripción clara
6. Proceso de review (tiempos estimados si aplica)
7. Criterio de merge

## 4. Convenciones de Código y Commits
Enlace a SHARED_INSTRUCTIONS.md o resumen inline.
Tabla de tipos de commit:
| Tipo | Cuándo usar |
|---|---|
| feat | Nueva funcionalidad |
| fix | Corrección de bug |
| docs | Solo documentación |
| refactor | Refactor sin cambio funcional |
| test | Tests sin cambio funcional |
| chore | Build, CI, dependencias |

## 5. Requisitos de Calidad
Comandos que deben pasar sin errores antes de abrir PR (derivar de pyproject.toml / hooks actuales):
```bash
python -m ruff check scripts tests
python -m ruff format scripts tests
python -m mypy scripts
python -m pytest
```
Indicar si hay hooks que se ejecutan automáticamente (PostToolUse).

## 6. Proceso de Release y Versionado
Seguimos [Semantic Versioning](https://semver.org/).
Quién tiene permisos para hacer release (maintainers).
Enlace a CHANGELOG.md.
Indicar si el contribuidor debe actualizar el CHANGELOG o lo hace el maintainer.

---

Restricciones:
- Derivar §4 de SHARED_INSTRUCTIONS.md (convenciones reales)
- Derivar §5 de los hooks en settings.json y los workflows de CI
- NO inventar procesos ni herramientas no verificables
- Si falta información, añadir "### Pendiente de verificación"
- Responde SOLO con el Markdown, sin texto introductorio ni cierre
```

## Cómo usar este prompt

### Modo fichero único — Claude Code

```
Lee .github/SHARED_INSTRUCTIONS.md, pyproject.toml y .claude/settings.json.
Genera CONTRIBUTING.md usando el prompt en .github/prompts/contributing_doc.prompt.md.
Guarda en CONTRIBUTING.md (raíz del repositorio).
Actualiza mkdocs.yml para añadir enlace a CONTRIBUTING bajo "Proyecto" o nav raíz.
Actualiza README.md para añadir enlace a CONTRIBUTING si no existe.
```

### Modo Copilot Chat

```
#file:.github/prompts/contributing_doc.prompt.md
#file:.github/SHARED_INSTRUCTIONS.md
#file:pyproject.toml

Genera CONTRIBUTING.md para este proyecto.
```

## Output esperado

`CONTRIBUTING.md` en raíz del repositorio con:
- Las 6 secciones del Arquetipo 11
- §5 con los comandos reales verificados contra `pyproject.toml` y `settings.json`
- §4 con los tipos de commit de Conventional Commits tal como los define el proyecto
