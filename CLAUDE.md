# Instrucciones para Claude Code — doc_ia

Este fichero proporciona especialización a Claude Code cuando trabaja con doc_ia,
incluyendo slash commands, hooks de desarrollo y configuración integrada.

---

## ⚠️ Contexto previo obligatorio

Lee **primero**:
- **`.github/SHARED_INSTRUCTIONS.md`** — Fuente canónica: principios del proyecto (sin API keys,
  tooling determinista, ejecución en chat), arquitectura, calidad, comandos, documentación,
  flujo de trabajo, Conventional Commits. **Esta es la base.**
- **Este fichero** — Especialización para Claude Code únicamente.

---

## Slash commands de Claude Code

Usa estos comandos para activar flujos estructurados con automatización integrada:

| Comando | Propósito | Entrada | Salida |
|---|---|---|---|
| `/new-feature` | Nueva funcionalidad | Descripción + módulos | PLAN → AUDIT_PLAN → IMPLEMENT → AUDIT_CODE → VERSION |
| `/hotfix` | Bug P1/P2 mínimo | Descripción + impacto | RCA → FIX → AUDIT_CODE → VERSION |
| `/refactor` | Refactor sin cambios funcionales | Área + objetivo | PLAN → AUDIT_PLAN → IMPLEMENT → AUDIT_CODE |
| `/audit-code` | Auditoría técnica independiente | Rutas o cambios | Scope → Findings → Verdict |
| `/security-review` | Auditoría de seguridad | Áreas críticas | Findings by severity → Remediation |
| `/tech-debt` | Deuda técnica priorizada | Área o módulo | Findings por severidad → Plan de remediación |
| `/maturity-assessment` | Evaluación de madurez del repo | Área o evaluación completa | Executive summary → Findings → Maturity verdict |
| `/version-closure` | Cierre de versión | Sesión completada | Release notes → Changelog → Rollback → Handoff |

**Ejemplo de uso**:

```
/new-feature

Objetivo: Añadir validación de enlaces rotos al tooling de docs

Alcance: scripts/check_links.py (nuevo), tests/test_check_links.py (nuevo)

Restricciones:
  - Tooling determinista: sin red en tests, sin servicios IA
  - mypy strict + ruff sin errores
  - Documentación en docstrings + entrada en README
```

---

## Trasladar esta configuración IA a otro proyecto (bootstrap)

Para replicar este sistema de instrucciones IA (Claude / Gemini / Copilot / Cursor / Codex) en **otro
proyecto**, incluso de **otro lenguaje y arquitectura**, usa el prompt
[`.github/prompts/bootstrap_ai_config.prompt.md`](./.github/prompts/bootstrap_ai_config.prompt.md).
La auditoría posterior la hace el agente **Config Reviewer**.

**Modelo PULL — se invoca desde el proyecto DESTINO**, apuntando a este repo como plantilla de
solo lectura. El lenguaje y la arquitectura del destino son **parámetros de entrada**, no constantes.

| Capa | Acción | Ejemplos |
|---|---|---|
| **A — Metodología** | Copiar verbatim (revisar comandos embebidos) | `.github/agents/`, `.github/prompts/`, `.claude/commands/`, `.ai/sessions/TEMPLATE/` |
| **B — Especialización** | Copiar + reescribir dominio | `SHARED_INSTRUCTIONS.md`, `CLAUDE.md`, `GEMINI.md`, `copilot-instructions.md`, `.cursorrules` |
| **C — Contexto** | Regenerar analizando el destino | `.ai/{product,architecture,runtime,glossary,standards}.md` |
| **D — No copiar** | Excluir | `.ai/sessions/<fechas>/`, `CHANGELOG.md`, caches, `settings.local.json` |

---

## Configuración: Hooks y PostToolUse

```
.claude/
  settings.json           ← Configuración: ruff, mypy, pytest hooks (sobre scripts/ y tests/)
  settings.json.example   ← Plantilla de ejemplo
  settings.local.json     ← Personalización local (no versionado, git-ignored)
  commands/               ← Slash commands personalizados
  EDGE_CASES.md           ← Casos límite conocidos en el proyecto (se puebla con el tiempo)
  TESTING_GUIDE.md        ← Guía de testing con PostToolUse
```

**Orden de ejecución automático típico** (hooks PostToolUse sobre Edit|Write):

1. `python -m ruff check scripts tests` (linting)
2. `python -m mypy scripts` (type-checking strict)
3. `python -m pytest --collect-only -q tests` (validación de sintaxis de tests)

---

## 📐 Arquetipos Formales de Documentación

Toda documentación sigue los **7 arquetipos formales** definidos en
[`.github/DOCUMENTATION_STANDARD.md`](./.github/DOCUMENTATION_STANDARD.md):

| Arquetipo | Propósito | Ubicación | Prompt |
|---|---|---|---|
| **1. Funcional** | ¿Qué hace y por qué? | `docs/functional/` | `functional_doc.prompt.md` |
| **2. Técnica/API** | ¿Cómo funciona internamente? | `docs/api/` | `technical_doc.prompt.md` |
| **3. Guía de Usuario** | ¿Cómo se usa/instala? | `docs/guides/` | `guide_doc.prompt.md` |
| **4. Ejemplos de Código** | ¿Cómo se implementa? | `docs/examples/` | `example_doc.prompt.md` |
| **5. Decisión Arquitectónica** | ¿Por qué se decidió así? | `docs/adr/` | `architecture_doc.prompt.md` |
| **6. Navegación Principal** *(variante)* | Intro + instalación + visión | `docs/index.md`, `installation.md`, `architecture.md` | `landing_doc.prompt.md` |
| **7. Onboarding Desarrolladores** | ¿Cómo me incorporo? | `docs/guides/onboarding_dev.md` | `onboarding_dev.prompt.md` |

**Características clave**:
- ✅ Secciones fijas: estructura inmutable (nunca omitir; escribir "No aplica" si vacío)
- ✅ Enlaces bidireccionales: Arquetipo 2 (§5) ↔ Arquetipo 4 (§5) obligatorios
- ✅ Parametrizables: en doc_ia los arquetipos son además **producto** — se aplican a proyectos
  origen externos pasando origen y destino como parámetros

## Documentación con Claude Code

Usa el **Documentation Generator** (agente) como **único punto de entrada** para crear o actualizar
documentación. No uses un único prompt masivo: trabaja siempre por fases separadas.

### Flujo por fases

```
Fase 1 — Inventariar: leer scripts/, README, docs/, mkdocs.yml
Fase 2 — Mapeo funcional (Senior Product Owner): objetivo, precondiciones, flujo, reglas
Fase 3 — Documentación técnica: responsabilidad, Mermaid, API pública, contratos, errores
Fase 4 — Ejemplos verificables: código real, resultado determinista, sin credenciales
Fase 5 — Sincronizar mkdocs.yml: añadir/mover/retirar entradas de navegación
Fase 6 — Revisión final: validar Markdown, enlaces relativos y sintaxis Mermaid
Fase 7 — Verificación de build (opt-in --verify-build): python -m mkdocs build --strict + leer site/
```

### Contrato documental obligatorio

1. Revisar documentación existente antes de crear páginas nuevas.
2. Separar siempre **funcional**, **técnico** y **ejemplos** en secciones diferenciadas.
3. MkDocs Material como generador por defecto (Zensical recíprocamente compatible); Mermaid.js para diagramas.
4. Actualizar `mkdocs.yml` cuando se creen, muevan o eliminen páginas en `docs/`.
5. No inventar capacidades, módulos, APIs, salidas, errores ni dependencias.
6. **Prohibido** delegar la generación de contenido a APIs de IA externas (principio del proyecto:
   la generación ocurre en este chat, nunca en componentes programáticos).

---

## 📦 Descarga de Documentación Offline

doc_ia proporciona **documentación en ZIP offline** con SHA256 checksums y auto-publicación
en GitHub Releases.

```bash
python scripts/build_docs_zip.py        # Build (mkdocs) + ZIP en dist/doc_ia-docs-{version}.zip
cat dist/doc_ia-docs-*.zip.sha256       # Ver checksum
sha256sum -c dist/*.sha256              # Validar (Linux/Mac)
```

El workflow `.github/workflows/docs-zip-release.yml` publica automáticamente una release
`docs-vX.Y.Z` en cada push a `main` con cambios en `docs/`.

---

## Checklist de sincronización

Cuando actualices **`.github/SHARED_INSTRUCTIONS.md`**, verifica:

- [ ] Los entry points (CLAUDE.md, GEMINI.md, copilot-instructions.md, .cursorrules) referencian secciones vigentes
- [ ] No hay duplicación de reglas entre `SHARED_INSTRUCTIONS.md` y especializaciones
- [ ] Rutas de archivos relativas y portables (`./.github/`, no rutas absolutas)
- [ ] Tabla de gobernanza en SHARED_INSTRUCTIONS.md refleja responsabilidad de cada fichero
- [ ] Si cambias slash commands, actualiza la tabla de comandos en este fichero

---

## Comandos útiles referenciados

```bash
python -m ruff check scripts tests   # Linting
python -m ruff format scripts tests  # Formato
python -m mypy scripts               # Type-checking (strict)
python -m pytest                     # Tests
python -m mkdocs build --strict      # Build de documentación
python -m mkdocs serve               # Documentación local
python scripts/check_env.py          # Verificación del entorno
python scripts/build_docs_zip.py     # ZIP offline con SHA256
```

---

*Actualizado: 2026-06-10*
