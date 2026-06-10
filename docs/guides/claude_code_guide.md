# Guía de uso de Claude Code

## 1. Objetivo

Configurar y usar Claude Code para trabajar en `doc_ia` aprovechando los slash commands,
los hooks de calidad automáticos y el flujo de trabajo asistido por IA. Claude Code es la
plataforma primaria de doc_ia: carga `CLAUDE.md` automáticamente al abrir el proyecto,
ejecuta los hooks de PostToolUse tras cada edición y expone los slash commands sin
configuración adicional.

A diferencia de Codex (que requiere prompts explícitos) o Copilot Chat (que usa agentes
`@nombre`), Claude Code integra el ciclo completo `PLAN → IMPLEMENT → AUDIT → VERSION`
a través de slash commands en el chat.

## 2. Requisitos Previos

- Claude Code CLI instalado (`npm install -g @anthropic-ai/claude-code`) o extensión
  VS Code de Claude Code activada
- Cuenta de Anthropic con acceso a Claude Code
- Repositorio `doc_ia` clonado localmente y abierto como directorio de trabajo
- Python 3.11+ con `mkdocs-material`, `ruff`, `mypy` y `pytest` instalados
  (verificar con `python scripts/check_env.py`)

## 3. Pasos

### Paso 1 — Verificar que Claude Code carga el contexto del proyecto

Al abrir el directorio de `doc_ia`, Claude Code lee automáticamente `CLAUDE.md`. Para
confirmar que el contexto está activo, escribe en el chat:

```
¿Qué slash commands están disponibles en este proyecto?
```

La respuesta debe listar `/document-project`, `/new-feature`, `/hotfix`, `/refactor`,
`/audit-code`, `/security-review`, `/tech-debt`, `/maturity-assessment` y `/version-closure`.

### Paso 2 — Documentar un proyecto con /document-project

```
/document-project

Origen:    <ruta raíz del proyecto a documentar>
Destino:   <ruta donde escribir la documentación>
Generador: mkdocs-material
Idioma:    es
```

El flujo valida los cuatro parámetros, inventa el inventario, genera los documentos por
arquetipos y sincroniza `mkdocs.yml`. Ver el ejemplo completo en
[Ejemplo: Documentar un Proyecto](../examples/document_project_usage.md).

### Paso 3 — Crear una nueva funcionalidad con /new-feature

```
/new-feature

Objetivo: <descripción breve>
Alcance:  <módulos o rutas afectadas>
```

El flujo emite PLAN → AUDIT_PLAN y espera confirmación antes de pasar a IMPLEMENT.

### Paso 4 — Verificar que los hooks de calidad están activos

Los hooks de PostToolUse se configuran en `.claude/settings.json`. Tras cada edición
de un archivo en `scripts/` o `tests/`, deben ejecutarse automáticamente:

1. `python -m ruff check scripts tests` (linting)
2. `python -m mypy scripts` (type-checking)
3. `python -m pytest --collect-only -q tests` (validación de sintaxis de tests)

Para confirmar que están activos, edita un archivo en `scripts/` y comprueba que
Claude Code muestra la salida de los tres comandos en el chat.

### Paso 5 — Diferencias con otras plataformas IA

| Aspecto | Claude Code | Copilot Chat | Gemini | Codex |
|---|---|---|---|---|
| Contexto inicial | `CLAUDE.md` automático | `copilot-instructions.md` automático | `GEMINI.md` automático | Manual (prompt explícito) |
| Slash commands | Sí (`/document-project`, etc.) | Agentes (`@nombre`) | No (prompts directos) | No |
| Hooks automáticos | Sí (PostToolUse en `.claude/settings.json`) | No | No | No |
| Mejor para | Flujos completos + hooks de calidad | Auditorías y revisiones inline | Análisis y preguntas rápidas | Módulo concreto con prompt explícito |

## 4. Verificación

```bash
# Confirmar que Claude Code está instalado
claude --version

# Confirmar que el entorno de tooling está completo
python scripts/check_env.py
# Entorno de tooling documental completo.

# Confirmar que el sitio compila sin errores
python -m mkdocs build --strict
# INFO - Documentation built in X.Xs
```

El proyecto está listo cuando los tres comandos terminan sin errores.

## 5. Variantes y Solución de Problemas

| Error / Síntoma | Causa probable | Solución |
|---|---|---|
| Slash commands no disponibles | `CLAUDE.md` no se cargó | Asegurarse de abrir el directorio raíz del repo, no una subcarpeta |
| Hooks de PostToolUse no se ejecutan | `.claude/settings.json` no existe o está mal configurado | Copiar `.claude/settings.json.example` a `.claude/settings.json` y revisar la sección `hooks` |
| `CLAUDE.md` no carga instrucciones del proyecto | Claude Code usa configuración global en lugar del proyecto | Verificar que `--project` apunta al directorio correcto; revisar `.claude/settings.json` |
| El flujo `/document-project` se detiene en VALIDACIÓN | Alguno de los 4 parámetros obligatorios falta o es ambiguo | Completar Origen, Destino, Generador e Idioma antes de continuar |
| `mkdocs build --strict` falla tras generar docs | Enlace roto o página huérfana en `nav:` | Revisar que todas las entradas de `mkdocs.yml` apuntan a archivos existentes |
