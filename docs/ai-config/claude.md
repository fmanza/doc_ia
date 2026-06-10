# Configuración de Claude Code

Versión de modelo objetivo: claude-sonnet-4-6 · Fecha de revisión: 2026-06-11

## 1. Plataforma y Modelo

| Campo | Valor |
|---|---|
| Plataforma | Claude Code (CLI + extensión VS Code) |
| Modelo mínimo recomendado | claude-sonnet-4-6 |
| Fichero de configuración fuente | `CLAUDE.md` (instrucciones del proyecto) |
| Configuración de permisos y hooks | `.claude/settings.json` |
| Personalización local (no versionada) | `.claude/settings.local.json` |
| Slash commands | `.claude/commands/` (9 comandos) |
| Casos límite conocidos | `.claude/EDGE_CASES.md` |

`CLAUDE.md` delega la fuente canónica de principios, arquitectura y convenciones a
`.github/SHARED_INSTRUCTIONS.md`; solo contiene la especialización para Claude Code
(slash commands, hooks, arquetipos, bootstrap).

## 2. Contexto Obligatorio

Claude Code lee estos ficheros antes de actuar en el proyecto:

| Fichero | Propósito |
|---|---|
| `.github/SHARED_INSTRUCTIONS.md` | Fuente canónica: principios, arquitectura, calidad, Conventional Commits |
| `CLAUDE.md` | Especialización para Claude Code: slash commands, hooks, arquetipos |
| `.claude/settings.json` | Permisos explícitos y hooks PostToolUse activos |
| `.ai/product.md` | Identidad y propósito del producto (contexto de negocio) |
| `.ai/architecture.md` | Arquitectura técnica del proyecto |
| `.github/DOCUMENTATION_STANDARD.md` | Especificación de los 11 arquetipos formales |

## 3. Comandos y Slash Commands

| Comando | Propósito | Inputs obligatorios | Outputs |
|---|---|---|---|
| `/document-project` | Documentar un proyecto origen completo | Origen(es), Destino, Generador, Idioma | VALIDACIÓN → INVENTARIO → PLAN_DOC → GENERACIÓN → SYNC NAV → REVISIÓN → RESUMEN → CIERRE |
| `/new-feature` | Nueva funcionalidad | Descripción + módulos afectados | PLAN → AUDIT_PLAN → IMPLEMENT → AUDIT_CODE → VERSION |
| `/hotfix` | Bug P1/P2 urgente | Descripción del bug + impacto | RCA → FIX → AUDIT_CODE → VERSION |
| `/refactor` | Refactor sin cambios funcionales | Área + objetivo | PLAN → AUDIT_PLAN → IMPLEMENT → AUDIT_CODE |
| `/audit-code` | Auditoría técnica independiente | Rutas o cambios | Scope → Findings → Verdict |
| `/security-review` | Auditoría de seguridad | Áreas críticas | Findings by severity → Remediation |
| `/tech-debt` | Deuda técnica priorizada | Área o módulo | Findings por severidad → Plan |
| `/maturity-assessment` | Evaluación de madurez del repo | Área o evaluación completa | Executive summary → Verdict |
| `/version-closure` | Cierre de versión | Sesión completada | Release notes → Changelog → Handoff |

Los ficheros de definición de cada comando están en `.claude/commands/*.md`.

## 4. Permisos y Herramientas

Basado en `.claude/settings.json` (sección `permissions.allow`):

| Herramienta/Acción | Permitida | Condición |
|---|---|---|
| `Read` sobre `util_bbdd/**` | ✅ | Lectura del proyecto origen de bootstrap |
| `Bash(python -m ruff check scripts tests)` | ✅ | Linting automático (hook PostToolUse) |
| `Bash(python -m mypy scripts)` | ✅ | Type-checking automático (hook PostToolUse) |
| `Bash(python -m pytest --collect-only -q tests)` | ✅ | Validación de tests (hook PostToolUse) |
| `PowerShell(git push -u origin main)` | ✅ | Push a rama principal |
| `Read` sobre `/tmp/**` | ✅ | Acceso a ficheros temporales del sistema |
| Cualquier otra acción | Requiere aprobación del usuario | Fuera de la lista de permisos explícitos |

## 5. Hooks y Automatizaciones

| Evento | Comando ejecutado | Propósito |
|---|---|---|
| `PostToolUse` en `Edit\|Write` | `python -m ruff check scripts tests --quiet 2>&1 \| head -15` | Linting tras cualquier edición de código |
| `PostToolUse` en `Edit\|Write` | `python -m mypy scripts --no-error-summary 2>&1 \| head -10` | Type-checking tras cualquier edición de código |
| `PostToolUse` en `Edit\|Write` | `python -m pytest --collect-only -q tests 2>&1 \| head -10` | Validación de sintaxis de tests tras edición |

Los hooks se ejecutan automáticamente sobre `scripts/` y `tests/`. No se ejecutan sobre
`docs/`, `mkdocs.yml` ni otros ficheros no-Python.

## 6. Restricciones Explícitas

Derivadas de `CLAUDE.md` y `.github/SHARED_INSTRUCTIONS.md`:

- **Prohibido** incrustar API keys o invocar servicios IA desde el código — la generación
  documental ocurre siempre en el chat, nunca en componentes programáticos.
- **Prohibido** inventar módulos, APIs, salidas, errores o dependencias no presentes en el
  código fuente del origen.
- **Prohibido** modificar el código fuente del origen al documentarlo — `/document-project`
  solo escribe documentación y navegación (`mkdocs.yml`).
- **Prohibido** usar un único prompt masivo para documentar un proyecto completo — trabajar
  siempre por fases separadas (Fases 0-7).
- **Prohibido** omitir secciones de arquetipo aunque estén vacías — escribir
  `*No aplica para este módulo.*`.
- **Prohibido** saltar los inputs obligatorios de `/document-project` — si alguno falta,
  detenerse y preguntar al usuario.

## 7. Casos Límite Conocidos

*No aplica para esta configuración.* El fichero `.claude/EDGE_CASES.md` está vacío —
se poblará con el tiempo a medida que se descubran casos límite en sesiones de trabajo.
