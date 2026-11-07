<!--
PLANTILLA — Kit de documentación de doc_ia (kit.py install la copia si falta, con {proyecto}).

Destino: <raíz del destino>/DOCUMENTAR.md (idioma `en`: DOCUMENT.md, traducido entero).
Es para quien MANTIENE la documentación (no va en el ZIP ni en docs/). Secciones fijas 0-6: no
omitir ni renumerar. El agente completa §3 con ejemplos reales de este proyecto en el CIERRE
(orígenes, nombre del manual, módulos), sin inventar rutas.
Borrar este comentario en el fichero generado.
-->
# Cómo documentar {proyecto}

Instrucciones para **generar o actualizar** la documentación de este repositorio con la IA (la
lectura de la documentación está en `VER_DOCUMENTACION.md`). Todo lo necesario vive aquí:

| Pieza | Ruta |
|---|---|
| Parámetros y decisiones de este proyecto | `.ai/prompts/documentar.prompt.md` |
| Metodología y scripts de doc_ia (copia fijada) | `.doc_ia/` (versión en `.doc_ia/kit.lock.json`) |
| Lanzadores | `.claude/commands/documentar.md`, `.github/prompts/documentar.prompt.md`, `AGENTS.md`, `GEMINI.md` |

## 0. Qué hace una sesión

Adquiere los orígenes (código, manuales, especificaciones, normativa), detecta qué ha cambiado
desde la última sesión, actualiza las páginas afectadas, verifica (`drift`, `decisions`, build
estricto), genera el ZIP y cierra con un registro en `.ai/sessions/` y un commit local.

## 1. Requisitos

- Python 3.11 o superior y `pip install -r requirements-docs.txt` (build de la documentación).
- Conversión de documentos: `pip install docling` (o `markitdown`; `pandoc` para `.doc`/`.odt`).
  Comprobar con `python .doc_ia/scripts/check_env.py`.
- Acceso a los orígenes del prompt de instancia: git/glab autenticado, carpetas de red,
  biblioteca de SharePoint sincronizada con OneDrive.
- Una plataforma IA con chat de agente: Claude Code, GitHub Copilot, Gemini, Codex o Cursor.

## 2. Lanzar

Abre **esta carpeta** como espacio de trabajo y:

| Plataforma | Cómo |
|---|---|
| Claude Code | `/documentar` (con modo opcional: `/documentar verificar`) |
| GitHub Copilot | `/documentar` en el chat (prompt `.github/prompts/documentar.prompt.md`) |
| Gemini · Codex · Cursor | «Documenta el proyecto siguiendo `AGENTS.md`» |

## 3. Ejemplos

| Quiero… | Escribe |
|---|---|
| Actualizar la documentación con lo último (lo habitual) | `/documentar` |
| Incorporar una versión nueva del manual u otro documento | `/documentar` (la detecta la adquisición y la registra en `.ai/sources.json`) |
| Aplicar las decisiones de cobertura ya tomadas en `docs/decisiones/` | `/documentar aplicar-decisiones` |
| Solo comprobar que todo está al día, sin generar | `/documentar verificar` |
| Regenerar todo desde cero | `/documentar completo` |
| Documentar solo una parte | `/documentar alcance: <módulo o rutas>` |
| Generar el ZIP para entregarlo | `/documentar zip` |
| Empezar en otro equipo | Clona o copia esta carpeta, cumple §1 y lanza `/documentar` (recrea `_staging/`) |

## 4. Qué deja cada sesión

- Páginas en `docs/`, texto de las fuentes en `_fuentes/`, estado en `.ai/doc_state.json` y
  `.ai/sources.json`.
- Registro en `.ai/sessions/AAAA-MM-DD/` (petición, contexto, trazabilidad y veredicto).
- Un commit local `docs(<proyecto>): …` (nunca `push`).
- Las fichas `COB-…` nuevas quedan **pendientes**: las decide una persona en `docs/decisiones/`.

## 5. Actualizar el kit

El kit se sincroniza solo al empezar cada sesión si doc_ia está disponible. A mano:

```bash
python <ruta de doc_ia>/scripts/kit.py sync --root .      # trae la versión actual de doc_ia
python .doc_ia/scripts/kit.py check --root .             # ¿alguien ha editado el kit?
```

No edites `.doc_ia/` ni los lanzadores: se sobrescriben. Lo propio del proyecto va en
`.ai/prompts/documentar.prompt.md`.

## 6. Problemas frecuentes

| Síntoma | Solución |
|---|---|
| `kit.py check` termina con 1 | Hay ficheros del kit editados o desfasados: `kit.py sync` desde doc_ia (o `--force` si los cambios locales sobran) |
| La sesión pasa a modo completo | Cambió la versión de doc_ia o el baseline no sirve; es normal tras actualizar el kit |
| Un origen no se encuentra | Revisa rutas y accesos del prompt de instancia (red, OneDrive, `glab auth status`) |
| `mkdocs build --strict` falla | Lo indica la sesión en REVISIÓN; `/documentar verificar` lo reproduce |
