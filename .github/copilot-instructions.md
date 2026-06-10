# Instrucciones para GitHub Copilot Chat — doc_ia

## ⚠️ Contexto previo obligatorio

Lee **primero** estos ficheros en este orden:

1. **`.github/SHARED_INSTRUCTIONS.md`** — Fuente canónica: principios de doc_ia (sin API keys,
   tooling determinista, ejecución en chat), arquitectura, calidad, comandos, documentación,
   flujo de trabajo, Conventional Commits.
2. **Este fichero** — Especialización para Copilot Chat en VS Code/GitHub únicamente.

---

## Agentes disponibles en Copilot Chat

Usa estos agentes cuando solicites trabajo estructurado. Cada agente implementa una fase
del flujo canónico `PLAN → AUDIT_PLAN → IMPLEMENT → AUDIT_CODE → VERSION`.

| Agente | Fase | Propósito |
|---|---|---|
| **Workflow Director** | Clasificación | Clasificar solicitud (feature, hotfix, refactor, security_review, tech_debt, maturity_assessment, version_closure) |
| **Plan Architect** | PLAN + AUDIT_PLAN | Preparar plan, contrastar con código real, detectar riesgos y expansión de alcance |
| **Feature Implementer** | IMPLEMENT | Ejecutar cambios con alcance aprobado, aplicar patches acotados |
| **Hotfix Responder** | RCA + FIX + AUDIT_CODE + VERSION | RCA mínimo, fix acotado (P1/P2 sin refactorizar) |
| **Code Auditor** | AUDIT_CODE | Revisar bugs, edge cases, contratos, cobertura, arquitectura |
| **Security Reviewer** | security_review | Auditoría de seguridad independiente (secretos, validación, workflows) |
| **Documentation Reviewer** | audit (modo lectura) | Revisar docs, ejemplos, coherencia, gaps (sin editar) |
| **Documentation Generator** | IMPLEMENT (modo escritura) | Generar docs funcional/técnica con Mermaid en `docs/` |
| **Config Reviewer** | AUDIT_CODE (configuración IA) | Revisar y consolidar instrucciones IA, eliminar duplicación |
| **Explore** | lectura | Exploración rápida del repo, responder preguntas (sin editar) |
| **Maturity Assessment** | evaluación | Evaluar madurez del repositorio (estructura, tests, contratos, readiness) |
| **Version Closer** | VERSION | Resumir cambios, evidencias, pendientes, rollback, directrices para futuras IAs |

Ver [`.github/AGENTS.md`](./AGENTS.md) para el registro completo.

---

## Flujo recomendado en Copilot Chat

```text
→ Workflow Director (clasificar)
→ Plan Architect (preparar PLAN + AUDIT_PLAN)
→ Feature Implementer (ejecutar IMPLEMENT)
→ Code Auditor (verificar AUDIT_CODE)
→ Version Closer (cerrar VERSION)
```

**Solicitud de ejemplo para nueva feature**:

```markdown
Trabaja sobre doc_ia. Usa agentes si es necesario.

Objetivo: [describe el cambio]
Alcance: [rutas: scripts/, docs/, .github/prompts/, etc.]
Restricciones: [sin servicios IA, mypy strict, docs, etc.]

Primero revisa .github/SHARED_INSTRUCTIONS.md.
Luego planifica, implementa, audita y cierra versión.
```

---

## Reglas específicas para Copilot Chat

### Uso de `#file:` y selección

- Si usas `#file:` o selecciones de código, contrástalo con el árbol real del repositorio
- No asumir rutas basadas en títulos de ficheros; verifica con `file_search` si es necesario

### Contradicciones y prioridades

- Si una instrucción IA contradice `pyproject.toml` o el código real,
  **prioriza el código real** y explicita el supuesto en tu respuesta

### Validación de referencias heredadas

No propongas módulos, archivos o estructuras que no existan:
- ❌ `src/`, `managers/`, `bulk/`, `SyncDatabaseManager` — herencia de util_bbdd, no existen aquí
- ✅ El código vive en `scripts/` y `tests/`; usa `grep_search` para validar antes de referenciar

### Sincronización de instrucciones IA

Si cambias reglas comunes, actualiza **en este orden**:

1. **`.github/SHARED_INSTRUCTIONS.md`** (fuente canónica) — cambios globales
2. **`.github/copilot-instructions.md`** (este fichero) — especialización Copilot, si aplica
3. **`CLAUDE.md`** — especialización Claude Code, si aplica
4. **`.github/AGENTS.md`** — actualizar si cambian agentes

---

## Generación de Documentación

### Proyecto completo — punto de entrada único

Usa **`document_project.prompt.md`** para documentar cualquier proyecto (externo o el propio doc_ia).
Orquesta inventario (crear/actualizar/omitir), arquetipos, nav sync y revisión:

```text
# Invocar con /runSubagent Documentation Generator + document_project.prompt.md
Lee y aplica .github/prompts/document_project.prompt.md con los siguientes parámetros:

Origen(es): <ruta raíz del proyecto a documentar>
Destino: <ruta donde se escribe la documentación>
Generador: mkdocs-material
Idioma: es
```

Los 4 parámetros son obligatorios. Si falta alguno, el prompt pide los datos antes de continuar.

### Módulo individual

Para documentar un único módulo, aplica directamente el prompt de arquetipo:

```text
# Funcional
Lee scripts/[modulo].py y genera la documentación funcional
usando .github/prompts/functional_doc.prompt.md.
Guarda en docs/functional/[nombre].md y actualiza mkdocs.yml.

# Técnica
Lee scripts/[modulo].py y genera la documentación técnica
usando .github/prompts/technical_doc.prompt.md.
Guarda en docs/api/[nombre].md y actualiza mkdocs.yml.
```

Regla crítica: no inventar. Lee el código fuente antes de generar cualquier sección.
Criterio de completitud: `python -m mkdocs build --strict` sin errores + todos los
scripts de `scripts/` documentados.

**Para auditar documentación sin editar**, usa **Documentation Reviewer** con
`.github/prompts/documentation_review.prompt.md` como criterio (hallazgos Nivel 1/2/3).

## 📐 Arquetipos Formales de Documentación

Toda documentación sigue los **7 arquetipos formales** de
[`.github/DOCUMENTATION_STANDARD.md`](DOCUMENTATION_STANDARD.md):
Funcional (`docs/functional/`), Técnica (`docs/api/`), Guía (`docs/guides/`),
Ejemplos (`docs/examples/`), ADR (`docs/adr/`), Navegación Principal (`docs/index.md`,
`installation.md`, `architecture.md`) y Onboarding (`docs/guides/onboarding_dev.md`).

- ✅ Secciones fijas: estructura inmutable (nunca omitir; "No aplica" si vacío)
- ✅ Enlaces bidireccionales: Arquetipo 2 (§5) ↔ Arquetipo 4 (§5) obligatorios
- ✅ En doc_ia los arquetipos son además **producto**: se aplican a proyectos origen externos
  pasando origen y destino como parámetros

---

## Bootstrap de configuración IA a otro proyecto

Para **trasladar este sistema de instrucciones IA** a otro proyecto usa el prompt
[`bootstrap_ai_config.prompt.md`](prompts/bootstrap_ai_config.prompt.md) y audita el resultado con
**Config Reviewer**.

**Modelo PULL**: invoca **desde el proyecto destino**, apuntando a este repo como plantilla de
solo lectura. Capas: **A** copiar verbatim · **B** copiar + reescribir dominio · **C** regenerar ·
**D** excluir. Detalle completo en el propio prompt.

---

## Integración con Claude Code

- **Cambios aprobados en Claude Code** se pueden auditar con **Code Auditor** (Copilot)
- **Documentación generada en Claude Code** se revisa con **Documentation Reviewer** (Copilot)
- **Configuración IA** se sincroniza vía **Config Reviewer**

### Validación de Markdown — Checklist obligatorio

Ver `.github/SHARED_INSTRUCTIONS.md` § "Validación de Markdown en documentación".

- ✅ Listas: `- item` o `1. item`, NUNCA dos espacios al final de línea
- ✅ Enlaces a archivos estáticos: rutas relativas reales, NO placeholders `#`
- ✅ Validar: `python -m mkdocs build --strict` sin errores

---

## 📦 Descarga de Documentación Offline

doc_ia proporciona **documentación en ZIP offline** con SHA256 checksums y auto-publicación
en GitHub Releases.

```bash
python -m mkdocs build --strict
python scripts/build_docs_zip.py
sha256sum -c dist/*.sha256
```

El workflow `.github/workflows/docs-zip-release.yml` se ejecuta en cada `push` a `main`
con cambios en `docs/` (o manualmente desde Actions UI). Resultado: release `docs-vX.Y.Z`
con ZIP + checksums adjuntos.

---

## Checklist de sincronización

Cuando actualices **`.github/SHARED_INSTRUCTIONS.md`**, verifica:

- [ ] Los entry points contienen referencias a secciones shared actualizadas
- [ ] No hay duplicación de contenido entre SHARED_INSTRUCTIONS.md y especializaciones
- [ ] Rutas de archivos relativas y portables (`./.github/...`, no `file://...`)
- [ ] Tabla de gobernanza en SHARED_INSTRUCTIONS.md refleja responsabilidad de cada fichero

---

*Actualizado: 2026-06-10*
