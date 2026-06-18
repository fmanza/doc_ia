# Arquitectura del Sistema

Vista panorámica de doc_ia (modelo arc42-lite + C4). Las decisiones puntuales con
trade-offs se registran como ADR en la sección Arquitectura.

## 1. Visión General y Objetivos de Calidad

doc_ia es un proyecto de **tooling plano** (sin librería de negocio, sin `src/`, sin
servidor): scripts deterministas + documentación + sistema de instrucciones IA
multiplataforma. La generación documental ocurre **en el chat** de la plataforma IA;
el código Python solo construye, valida y empaqueta.

```mermaid
flowchart TD
    subgraph Externo
        DEV[Desarrollador]
        ORIG[Proyecto origen a documentar]
        GH[GitHub Actions y Releases]
    end
    subgraph doc_ia
        CHAT[Chat de plataforma IA<br/>Claude, Gemini, Copilot, Cursor, Codex]
        INSTR[Instrucciones IA<br/>.github + .claude + .ai]
        TOOL[Tooling determinista<br/>scripts/]
        DOCS[docs/ + mkdocs.yml]
    end
    DEV --> CHAT
    CHAT --> INSTR
    INSTR --> ORIG
    CHAT --> DOCS
    TOOL --> DOCS
    DOCS --> GH
```

Objetivos de calidad: determinismo del tooling, cero credenciales, validación estricta
del sitio (`--strict`), trazabilidad de sesiones (`.ai/sessions/`).

## 2. Mapa de Módulos (Building Blocks)

| Carpeta | Responsabilidad |
|---|---|
| `scripts/` | Tooling determinista standalone: `check_env.py`, `build_docs_zip.py`, `convert_to_md.py`, `start-server.py` |
| `hooks/` | `sync_root_docs.py`: copia CHANGELOG.md / CONTRIBUTING.md a docs/ (hook MkDocs + PostToolUse) |
| `mkdocs_hooks.py` | Hook MkDocs nativo: genera `doc_ia-docs-latest.zip` + SHA256 en `site/` en cada build |
| `tests/` | Tests pytest del tooling (importan `scripts/` vía `sys.path`) |
| `docs/` + `mkdocs.yml` | Sitio MkDocs Material (este sitio, 31 páginas); `mkdocs.yml` es fuente única de navegación |
| `.github/` | Canónico (`SHARED_INSTRUCTIONS.md`), 12 agentes, 25 prompts, 3 instructions, 2 workflows CI |
| `.claude/` | 9 slash commands, hooks PostToolUse (sync_root_docs, ruff, mypy, pytest), plantillas |
| `.ai/` | Contexto persistente (product, architecture, glossary, runtime, standards) + sesiones trazadas |

Regla de capas: `scripts/` no importa de `docs/` ni `.github/`; `hooks/` no importa de
`scripts/`; los entry points de plataforma dependen del canónico, nunca entre sí.

## 3. Flujo en Ejecución (Runtime)

Operación típica — documentar un proyecto con `/document-project`:

```mermaid
flowchart TD
    A[Usuario en chat IA] --> B[/document-project<br/>VALIDACIÓN de 4 inputs]
    B -- inputs incompletos --> A
    B --> B0{¿≥2 orígenes o<br/>no es CÓDIGO?}
    B0 -- Sí --> F0a[Fase 0a — Clasificar orígenes<br/>8 tipos posibles]
    F0a --> B1
    B0 -- No --> B1[Fase 0b — Sincronización visual<br/>assets + mkdocs.yml + .gitignore]
    B1 --> C[Fase 1 — Inventario<br/>Estado A / B / C<br/>Señales ZIP offline]
    C --> D[Fases 2-4 — Generación por arquetipos<br/>funcional · técnica · ejemplos · guías]
    D --> E[Fase 5 — Sincronización de mkdocs.yml]
    E --> F[Fase 6 — Revisión Markdown · enlaces · Mermaid]
    F --> G[Fase 7 — Build opt-in + downloads.md]
    G --> H[Cierre — .ai/sessions/ + commit]
```

## 4. Conceptos Transversales y Estándares No Funcionales

| Dimensión | Mecanismo real en el repositorio |
|---|---|
| Seguridad | Sin API keys ni credenciales (`.gitignore` bloquea `.env`, `*.key`); el código nunca invoca servicios IA |
| Observabilidad | Salida por stdout con prefijos + códigos de retorno (`0`/`≠0`) aptos para CI y hooks |
| Rendimiento | Build incremental de MkDocs; ZIP por `shutil.make_archive`; sin servicios pesados |
| Compatibilidad | MkDocs Material por defecto; Zensical recíproco sobre el mismo `mkdocs.yml` (ver ADR-001) |
| Robustez/Errores | Fail-fast con `sys.exit` y mensajes explícitos; build estricto bloquea docs rotas |
| Tipado/Calidad | `mypy --strict` sobre `scripts/`, `ruff` lint+format, pytest determinista, hooks PostToolUse |

## 5. Decisiones, Extensión y Límites

- **Registro de decisiones**: [ADR-001 — MkDocs Material por defecto](adr/ADR-001-mkdocs-material-por-defecto.md).
- **Extensión soportada**: añadir un arquetipo (prompt nuevo en `.github/prompts/` +
  registro en `DOCUMENTATION_STANDARD.md`), un agente (`.github/agents/` + `AGENTS.md`),
  un slash command (`.claude/commands/` + tabla en `CLAUDE.md`) o un script determinista
  en `scripts/` con sus tests.
- **Anti-patrones (límites)**: incrustar API keys; añadir componentes programáticos que
  invoquen IA; generar documentación fuera del chat; duplicar reglas del canónico en los
  entry points.
