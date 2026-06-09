# doc_ia

Proyecto IA para **documentar cualquier proyecto de desarrollo** mediante instrucciones IA
ejecutadas en los chats de los servicios contratados (Claude Code, Gemini, Copilot Chat,
Cursor, Codex). Los **orígenes a documentar** y el **destino de la documentación** son
parámetros obligatorios de cada ejecución.

## Principios

- **Sin API keys**: ninguna credencial de servicios IA se configura ni se versiona en este proyecto.
- **Sin componentes programáticos IA**: el código Python es exclusivamente tooling determinista
  (build de documentación, ZIP offline, validaciones). Nunca invoca servicios IA.
- **Ejecución en chat**: la generación documental ocurre siempre en el chat de la plataforma IA,
  guiada por las instrucciones de `.github/` y `.claude/`.

## Estado

Esqueleto inicial (Fase 0). Pendiente de ejecutar el bootstrap de configuración IA
(modelo PULL) desde este proyecto:

```text
# Abre ESTE proyecto en Claude Code y escribe:

Lee y aplica .github/prompts/bootstrap_ai_config.prompt.md
Origen (solo lectura): c:\Desarrollo\python\libs\util_bbdd
Destino: C:\Desarrollo\Proyectos\doc_ia
Lenguaje/arquitectura destino: Python tooling (scripts + docs, sin librería de negocio)
Plataformas IA activas: Claude Code, Gemini, Copilot, Cursor, Codex
Generador de documentación destino: Zensical/MkDocs Material
Fase: completa
```

## Entorno

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

## Comandos

```bash
python -m ruff check scripts tests   # Linting
python -m ruff format scripts tests  # Formato
python -m mypy scripts               # Type-checking
python -m pytest                     # Tests del tooling
python -m mkdocs build --strict      # Build de documentación
python -m mkdocs serve               # Documentación local
```
