# Agentes Disponibles

Registro de agentes especializados en `.github/agents/` para orquestación del flujo de trabajo PLAN → AUDIT_PLAN → IMPLEMENT → AUDIT_CODE → VERSION.

## Invocación

**En Claude Code**:
```
/new-feature
/hotfix
/refactor
/security-review
/audit-code
/tech-debt
/maturity-assessment
/version-closure
```

**En Copilot Chat**: Usa `runSubagent` o invoca directamente con nombre del agente.

---

## Agentes por flujo

### 1. **Workflow Director** (`workflow-director.agent.md`)
- **Propósito**: Clasificar solicitudes, validar contexto mínimo, elegir fase siguiente
- **Salida**: Clasificación (new_feature | hotfix | refactor | security_review | tech_debt | maturity_assessment | version_closure)
- **Invocable**: No (interno)

### 2. **Plan Architect** (`plan-architect.agent.md`)
- **Propósito**: Preparar PLAN y AUDIT_PLAN, contrastar con código real, detectar riesgos
- **Salida**: PLAN (rutas, componentes, riesgos) + AUDIT_PLAN (veredicto)
- **Invocable**: Sí (fases new_feature, refactor)

### 3. **Feature Implementer** (`feature-implementer.agent.md`)
- **Propósito**: Ejecutar IMPLEMENT con alcance aprobado, aplicar cambios, validar tests
- **Invocable**: Sí (después de AUDIT_PLAN aprobado)

### 4. **Hotfix Responder** (`hotfix-responder.agent.md`)
- **Propósito**: RCA, fix mínimo, verificación; incidencias P1/P2 sin refactorizar
- **Política**: Solo fix acotado, prohibido refactorizar u optimizar

### 5. **Code Auditor** (`code-auditor.agent.md`)
- **Propósito**: AUDIT_CODE de implementaciones, revisar bugs, edge cases, contratos
- **Salida**: Scope, Findings, Compatibility, Coverage, Verdict
- **Invocable**: Sí (fase AUDIT_CODE)

### 6. **Documentation Reviewer** (`documentation-reviewer.agent.md`)
- **Propósito**: Revisar y auditar documentación completa, ejemplos, gaps, coherencia (sin editar)
- **Criterios**: Nivel 1 (crítico), Nivel 2 (alto), Nivel 3 (recomendado)
- **Prompt**: `.github/prompts/documentation_review.prompt.md`
- **Slash command**: No disponible — invocar mediante lenguaje natural en Claude Code

### 6b. **Documentation Generator** (`documentation-generator.agent.md`)
- **Propósito**: GENERAR documentación funcional y técnica con diagramas Mermaid
- **Entrada**: Módulo objetivo (`scripts/*.py` o prompt de arquetipo), tipo (`functional` | `technical` | `both`)
- **Salida**: Archivos `.md` en `docs/` + entrada sugerida para `mkdocs.yml`
- **Diferencia con Reviewer**: Reviewer audita, Generator crea contenido nuevo
- **Prompts base**: `.github/prompts/functional_doc.prompt.md` + `.github/prompts/technical_doc.prompt.md`
- ⚠️ **Sin workflow CI/CD de generación**: doc_ia prohíbe invocar APIs de IA desde código o CI;
  la generación ocurre siempre en el chat de la plataforma

### 7. **Config Reviewer** (`config-reviewer.agent.md`)
- **Propósito**: Revisar y consolidar ficheros de configuración IA, eliminando duplicación entre plataformas
- **Criterios**: DRY, autosuficiencia por entry point, coherencia de flujos, cero referencias huérfanas
- **Prompt**: `.github/prompts/config_review.prompt.md`
- **Uso clave**: auditoría posterior del bootstrap (`bootstrap_ai_config.prompt.md`)

### 8. **Security Reviewer** (`security-reviewer.agent.md`)
- **Propósito**: Auditoría de seguridad independiente: secretos, validación, workflows CI, principio "sin API keys"
- **Salida**: Executive summary, Findings, Evidence, Remediation, Verdict

### 9. **Maturity Assessment** (`maturity-assessment.agent.md`)
- **Propósito**: Evaluar madurez del repositorio completo (estructura, contratos, tests, readiness)

### 10. **Version Closer** (`version-closer.agent.md`)
- **Propósito**: Cierre de versión, resumir cambios, validar sincronización y handoff
- **Validación requerida**: `.github/instructions/sync.instructions.md` + `python -m mkdocs build --strict` sin errores

### 11. **Explore** (`explore.agent.md`)
- **Propósito**: Exploración rápida del repositorio, Q&A sin modificaciones

---

## Matriz de relaciones

| Fase | Agente | Output | Next |
|------|--------|--------|------|
| CLASIFICACIÓN | Workflow Director | Tipo de tarea | PLAN |
| PLAN | Plan Architect | PLAN + AUDIT_PLAN | IMPLEMENT (si GO) o RETORNO |
| IMPLEMENT | Feature Implementer | Cambios por archivo | AUDIT_CODE |
| AUDIT_CODE | Code Auditor | Hallazgos, Severidad | CORRECCIÓN (si issues) o VERSION |
| VERSION | Version Closer | Release notes, Changelog | FIN |
| HOTFIX DIRECTO | Hotfix Responder | PLAN + FIX + AUDIT + VERSION | FIN |
| AUDITORÍA INDEPENDIENTE | Security/Documentation/Config/Maturity Reviewer | Executive summary + Findings | BACKLOG |

---

## Registro de herramientas y restricciones

| Agente | read | write | search | exec | web_fetch |
|--------|------|-------|--------|------|-----------|
| Plan Architect | ✅ | ❌ | ✅ | ❌ | ❌ |
| Feature Implementer | ✅ | ✅ | ❌ | ✅ | ❌ |
| Hotfix Responder | ✅ | ✅ | ❌ | ✅ | ❌ |
| Code Auditor | ✅ | ❌ | ✅ | ❌ | ❌ |
| Documentation Reviewer | ✅ | ❌ | ✅ | ❌ | ❌ |
| Documentation Generator | ✅ | ✅ | ✅ | ❌ | ❌ |
| Config Reviewer | ✅ | ❌ | ✅ | ❌ | ❌ |
| Security Reviewer | ✅ | ❌ | ✅ | ❌ | ❌ |
| Maturity Assessment | ✅ | ❌ | ✅ | ❌ | ❌ |
| Version Closer | ✅ | ❌ | ✅ | ❌ | ❌ |
| Explore | ✅ | ❌ | ✅ | ❌ | ❌ |
| Workflow Director | ✅ | ❌ | ✅ | ❌ | ❌ |

---

## Bootstrap a otro proyecto (cross-project)

Para **trasladar este sistema de instrucciones IA a otro proyecto** (incluso de otro lenguaje y
arquitectura) usa el prompt `bootstrap_ai_config` y, como auditor del resultado, el agente
**Config Reviewer**.

- **Prompt**: [`.github/prompts/bootstrap_ai_config.prompt.md`](prompts/bootstrap_ai_config.prompt.md)
- **Auditor**: `config-reviewer.agent.md` (DRY + referencias huérfanas)
- **Método**: modelo **PULL** — se invoca **desde el proyecto destino**, apuntando a este repo
  como plantilla de solo lectura.
- **Capas**: A (copiar verbatim) · B (copiar + reescribir dominio) · C (regenerar) · D (excluir).

---

## Configuración

- **Prompts**: `.github/prompts/*.prompt.md` — 19 prompts: 11 de método (`new_feature`, `hotfix`,
  `refactor`, `audit_code`, `security_review`, `tech_debt`, `maturity_assessment`, `version_closure`,
  `config_review`, `documentation_review`, `normative_traceability`) + 7 arquetipos documentales
  (`functional_doc`, `technical_doc`, `guide_doc`, `example_doc`, `architecture_doc`, `landing_doc`,
  `onboarding_dev`) + `bootstrap_ai_config`
- **Instrucciones**: `.github/instructions/*.instructions.md` — reglas por tipo de archivo
- **Hooks**: `.claude/settings.json` — comandos PostToolUse (lint, type-check, test collection)

Modificar un agente: editar su archivo `.agent.md` en `.github/agents/`.

---

## Nota: Asimetría slash commands ↔ agentes

Los **slash commands** de Claude Code (`.claude/commands/`) cubren 8 flujos. Los **agentes**
(`.github/agents/`) son 12: los 8 anteriores más `documentation-reviewer`,
`documentation-generator`, `config-reviewer`, `explore` y `workflow-director` (interno).
Los de documentación y `config-reviewer` no tienen slash command pero son invocables por
lenguaje natural (Claude Code) o mediante sus prompts (Copilot Chat).

Ver gobernanza completa en [`.github/INTEGRATION_MAP.md`](INTEGRATION_MAP.md).
