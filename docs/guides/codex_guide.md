# Guía de uso de Codex (OpenAI)

## 1. Objetivo

Configurar y usar la extensión Codex de OpenAI para trabajar en `doc_ia` con prompts explícitos.
Codex **no usa un fichero de instrucciones propio**: lee `CLAUDE.md`,
`.github/SHARED_INSTRUCTIONS.md` y `.github/AGENTS.md`.

> **Principio del proyecto**: la cuenta y la sesión de Codex viven en la extensión del editor.
> Este repositorio **no versiona API keys** de ningún servicio IA.

## 2. Requisitos Previos

- VS Code instalado (versión 1.85+)
- Cuenta de OpenAI con acceso a Codex
- Extensión "Codex" de OpenAI instalada en VS Code
- Repositorio `doc_ia` clonado localmente

## 3. Pasos

### Paso 1 — Instalar la extensión

```bash
code --install-extension openai.codex
```

Configura la sesión en los ajustes de VS Code (`Ctrl+,` → buscar "Codex"). La credencial queda
en la configuración de usuario del editor, nunca en este repositorio.

### Paso 2 — Entender qué archivos lee Codex

| Archivo | Propósito |
|---|---|
| `CLAUDE.md` | Instrucciones transversales para asistentes de código |
| `.github/SHARED_INSTRUCTIONS.md` | Principios, arquitectura y políticas comunes (canónico) |
| `.github/AGENTS.md` | Registro de agentes y flujos especializados |
| `pyproject.toml` | Versión, Python soportado, herramientas reales |
| `.github/instructions/` | Reglas por ruta o tipo de archivo |

### Paso 3 — Flujo de trabajo recomendado

```
PLAN → IMPLEMENTAR → VERIFICAR
```

Nunca pedir código o documentación sin haber dado el contexto del módulo real.

### Paso 4 — Generar documentación funcional

```text
Lee scripts/check_env.py y genera documentación funcional
siguiendo las instrucciones del archivo .github/prompts/functional_doc.prompt.md.
Guarda el resultado en docs/functional/check_env.md.
```

### Paso 5 — Generar documentación técnica con Mermaid

```text
Usando el prompt en .github/prompts/technical_doc.prompt.md, genera documentación
técnica para scripts/build_docs_zip.py. Tipo de diagrama: flowchart TD.
Guarda en docs/api/build_docs_zip.md y añade la entrada en mkdocs.yml.
```

### Paso 6 — Diferencias con Claude Code y Copilot Chat

| Aspecto | Codex | Claude Code | Copilot Chat |
|---|---|---|---|
| Contexto inicial | Manual (prompt explícito) | `CLAUDE.md` automático | `copilot-instructions.md` automático |
| Slash commands | No | Sí (`/new-feature`, etc.) | Agentes (`@nombre`) |
| Ejecución de tests | Manual | Automática (hooks) | Manual |
| Mejor para | Módulo concreto con prompt explícito | Flujos completos | Auditorías y revisiones |

## 4. Verificación

```bash
# Validación estricta de enlaces y Markdown
python -m mkdocs build --strict
```

Si el build pasa sin errores, la documentación generada es válida. Revisar visualmente con:

```bash
python -m mkdocs serve
```

Navegar a `http://127.0.0.1:8000` y comprobar la nueva página.

## 5. Variantes y Solución de Problemas

| Error / Síntoma | Causa probable | Solución |
|---|---|---|
| Error de autenticación | Sesión expirada en la extensión | Renovar sesión en la configuración de VS Code (nunca versionar la credencial) |
| Codex inventa módulos o APIs | Prompt sin contexto del código real | Incluir el contenido del archivo fuente en el prompt |
| `mkdocs build` falla | Rutas incorrectas o links rotos | Revisar rutas relativas del `.md` generado |
| Diagrama Mermaid no válido | Sintaxis incorrecta generada | Validar en [mermaid.live](https://mermaid.live); regenerar con restricciones explícitas |
