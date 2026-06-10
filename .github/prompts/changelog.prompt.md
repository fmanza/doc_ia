# Prompt: changelog — Changelog / Release Notes (Arquetipo 9)

Genera o actualiza el `CHANGELOG.md` para **doc_ia** siguiendo el estándar
[Keep a Changelog](https://keepachangelog.com/) v1.1.0 y [Semantic Versioning](https://semver.org/).

## Instrucción al modelo

```
Actúa como release manager documentando los cambios de una versión de software.

Analiza el contexto proporcionado (git log, commits, PRs, issues, pyproject.toml) y
genera entradas de changelog precisas y orientadas al usuario final.

El CHANGELOG.md debe seguir esta estructura en este orden exacto:

# Changelog

Todos los cambios notables de este proyecto se documentan aquí.
Formato: [Keep a Changelog](https://keepachangelog.com/es/1.1.0/) · Versioning: [SemVer](https://semver.org/lang/es/)

## [Unreleased]
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

## [X.Y.Z] — YYYY-MM-DD
### Added
- Descripción de nueva funcionalidad.
### Fixed
- Descripción de bug corregido.

[Unreleased]: https://github.com/[usuario]/[repo]/compare/vX.Y.Z...HEAD
[X.Y.Z]: https://github.com/[usuario]/[repo]/compare/vX.Y.Z-1...vX.Y.Z

---

Categorías permitidas (en este orden dentro de cada versión):
- Added:      Nueva funcionalidad retrocompatible
- Changed:    Cambio en funcionalidad existente
- Deprecated: Funcionalidad marcada para eliminación futura
- Removed:    Funcionalidad eliminada
- Fixed:      Corrección de bug
- Security:   Corrección de vulnerabilidad

Reglas de redacción:
- Entradas en pasado o forma nominal corta: "Añade soporte X", "Corrige error Y"
- Cada entrada: una línea, orientada al impacto para el usuario (no al commit técnico)
- Omitir cambios internos sin impacto para el usuario (refactors, CI, linting)
- Si un cambio rompe compatibilidad (breaking change): marcarlo con "**BREAKING:**" al inicio
- Omitir categorías vacías para la versión (pero mantener [Unreleased] con todas las categorías)

---

Restricciones:
- NO inventar versiones, fechas, features ni fixes no verificables en el contexto proporcionado
- La versión en [X.Y.Z] debe coincidir exactamente con `pyproject.toml` / `package.json`
- Mantener siempre [Unreleased] al inicio con todas las categorías (aunque vacías)
- Los enlaces de comparación deben apuntar al repositorio real del proyecto
- Si el CHANGELOG ya existe: añadir la nueva versión encima de la última, sin modificar entradas previas
- Responde SOLO con el Markdown, sin texto introductorio ni cierre
```

## Cómo usar este prompt

### Cierre de versión — Claude Code

```
Lee pyproject.toml para obtener la versión actual.
Lee git log --oneline desde el último tag hasta HEAD.
Genera o actualiza CHANGELOG.md usando el prompt en .github/prompts/changelog.prompt.md.
La nueva versión debe quedar entre [Unreleased] y la versión anterior.
```

### Modo Copilot Chat

```
#file:.github/prompts/changelog.prompt.md
#file:pyproject.toml
#file:CHANGELOG.md

Añade la entrada para la versión actual al CHANGELOG.md
basándote en los cambios del git log proporcionado.
```

## Integración con otros prompts

Este prompt se invoca automáticamente en el flujo `/version-closure` (`version_closure.prompt.md`).
También puede invocarse de forma standalone al preparar una release.

## Output esperado

`CHANGELOG.md` completo con:
- Sección `[Unreleased]` al inicio con todas las categorías
- Nueva versión `[X.Y.Z] — YYYY-MM-DD` con solo las categorías con contenido
- Versiones anteriores sin modificar
- Bloque de enlaces de comparación al final
