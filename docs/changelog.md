# Changelog

Todos los cambios notables de este proyecto se documentan aquí.
Formato: [Keep a Changelog](https://keepachangelog.com/) · Versioning: [SemVer](https://semver.org/)

## [Unreleased]

### Added

- **Arquetipo 12 — Referencia del Sistema** (`docs/reference/`, condicional): configuración,
  CLI, errores y códigos de salida, eventos e interfaces publicadas; prompt
  `reference_doc.prompt.md`. Primera aplicación: `docs/reference/index.md` de doc_ia.
- **Regla transversal de evidencia y confianza** (`DOCUMENTATION_STANDARD.md` §3.16): bloque
  plegable "Evidencia" en los Arquetipos 1, 2 y 12, citas `ruta::símbolo` en código inline y
  leyenda ✅ ⚠️ 🔍 ❌.
- **Variante 6C**: subapartado §3 › Despliegue (arc42 §7, condicional) y escenarios de calidad
  en §4 (arc42 §10). Aplicado en `docs/architecture.md`.
- **ADR-002** — Use evidence-backed archetypes for repository documentation.
- **Trazabilidad funcional y de pruebas** (P2): columna `Test` en los criterios de aceptación del
  Arquetipo 1 §7, nueva §6 "Verificación y Tests" del Arquetipo 2 y subsección condicional
  "Actores y permisos" en el Arquetipo 1 §2.
- **Mapa Funcional** (Variante 1-I del Arquetipo 1, `docs/functional/index.md`): capacidades,
  recorridos transversales, actores y glosario global del sistema.
- **Arquetipo 12 §6 "Datos"** (condicional): `erDiagram` global y diccionario con sensibilidad
  por campo; aplicado a los ficheros con formato propio de doc_ia.

### Fixed

- `convert_to_md.py --device auto` detecta la GPU: el `CUDA_VISIBLE_DEVICES=""` que el módulo
  fija al importarse ya no se confunde con una elección del usuario.

### Changed

- Norma del Arquetipo 1 alineada con su prompt (8 secciones); las páginas con la estructura v1
  siguen siendo válidas en transición.
- Prompt del Arquetipo 2 alineado con la norma (§2 "Modelo de Datos / Contratos"); la directiva
  autodoc solo se usa si el generador tiene mkdocstrings.
- Material `CONTRATO` alimenta también el Arquetipo 12 §5; `INFRAESTRUCTURA` va a 6C §3 › Despliegue.

## [0.1.0] — 2026-06-10

### Added

- **Tooling determinista**: `scripts/check_env.py` (verificación de herramientas del entorno) y
  `scripts/build_docs_zip.py` (ZIP offline con SHA256 y checksums).
- **Bootstrap multiplataforma** (`.github/agents/`, `.github/prompts/`, `.claude/commands/`):
  replica el sistema de instrucciones IA en proyectos destino mediante modelo PULL.
- **Flujo `/document-project`** como comando de entrada único para documentar proyectos:
  validación obligatoria de inputs, inventario por fases, orquestación de arquetipos.
- **Soporte de orígenes heterogéneos** en `/document-project`: Fase 0a de clasificación
  (`CÓDIGO`, `NORMATIVA`, `ESPECIFICACIÓN`, `UI/PANTALLAS`, `REFERENCIA`); estrategias
  `federado`, `hub+satélite` y `monorepo` para múltiples orígenes de código.
- **11 arquetipos formales** de documentación con estructura fija y audiencia definida:
  - 1 — Funcional, 2 — Técnica/API, 3a — How-to (Diátaxis), 3b — Tutorial (Diátaxis),
    4 — Ejemplos de Código, 5 — ADR/MADR 4.0, 6 — Navegación Principal (Variantes A–D),
    7 — Onboarding Dev, 8 — Trazabilidad Normativa (condicional),
    9 — Changelog, 10 — Config Agente IA, 11 — Guía de Contribución.
- **Documentación completa de doc_ia** (dogfooding): 24 páginas en `docs/` cubriendo
  funcional, técnica, ejemplos, guías, arquitectura y ADRs para todos los módulos.
- **Descarga de documentación offline**: `dist/doc_ia-docs-{version}.zip` + SHA256; workflow
  GitHub Actions `docs-zip-release.yml` publica automáticamente en cada release.
- **UX del sitio**: márgenes, sidebar toggle, soporte Mermaid 11, tabs sticky.
- **Estados A/B/C** en el inventario de `/document-project` para distinguir páginas
  a crear, actualizar u omitir.

### Fixed

- Restauración de 10 ficheros de la Capa A corruptos durante el bootstrap inicial.
- Restauración de `config-reviewer.agent.md` y creación de `docs.instructions.md`
  tras corrupción del bootstrap.

[Unreleased]: https://github.com/fmanza/doc_ia/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/fmanza/doc_ia/releases/tag/v0.1.0
