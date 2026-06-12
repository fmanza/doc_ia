# TRACEABILITY

## Session metadata

- id: 2026-06-12-pandoc
- fecha: 2026-06-12
- rama: develop
- skill: new_feature
- fase: IMPLEMENT + AUDIT_CODE (inline)

## Prompt issued

> Actualizar la documentación IA, para que cuando se encuentre documentos que no pueda leer
> use "pandoc" para convertirlos en formato md. Se creará una carpeta md donde se dejen estos
> ficheros. También se actualizará la documentación para este proyecto y disponer de
> instrucciones claras de como instalar "pandoc". Ejemplo en Windows:
> `winget install JohnMacFarlane.Pandoc`

## Context supplied

Exploración completa de estructura vía agente Explore: `SHARED_INSTRUCTIONS.md`,
`document_project.prompt.md`, `check_env.py`, `installation.md`, `mkdocs.yml`,
`test_check_env.py`, `CLAUDE.md`, plantilla de sesiones.

## AI output summary

1. Creado `scripts/convert_to_md.py`: detecta extensiones no legibles (.pdf, .docx, .pptx…),
   llama a pandoc, deposita en `<origen>/md/` con estructura reflejada; idempotente, `--dry-run`.
2. Actualizado `scripts/check_env.py`: añadida `missing_system_tools()` con `shutil.which`;
   pandoc ausente produce aviso + instrucciones de instalación pero exit 0 (opcional).
3. Corregida línea larga (ruff E501) en `convert_to_md.py` — variable auxiliar para f-string.
4. Actualizado `tests/test_check_env.py`: 2 tests nuevos para `missing_system_tools`.
5. Actualizado `docs/installation.md`: sección pandoc con tabla por plataforma y admonition.
6. Creada `docs/functional/convert_to_md.md`: arquetipo 1 con diagrama Mermaid y tabla de
   comportamientos; referencias solo a páginas existentes.
7. Actualizado `mkdocs.yml`: entrada `Conversión de Documentos a Markdown` bajo Tooling Determinista.
8. Actualizado `.github/SHARED_INSTRUCTIONS.md`: `convert_to_md.py` en arquitectura,
   responsabilidades y comandos de desarrollo.
9. Actualizado `.github/prompts/document_project.prompt.md`: nueva Fase 0b (conversión pandoc)
   entre Fase 0 y Fase 1; sección "Devuelve en este orden" actualizada a `Fase 0+0b+1`.
10. Actualizado `CLAUDE.md`: comando `convert_to_md.py` en tabla de referencia.
11. Verificación final: ruff ✅ · mypy strict ✅ · pytest 4/4 ✅ · mkdocs build --strict ✅

## Artefactos generados

| Artefacto | Ruta | Estado |
|---|---|---|
| Script conversión | `scripts/convert_to_md.py` | creado |
| Verificación entorno | `scripts/check_env.py` | actualizado |
| Tests entorno | `tests/test_check_env.py` | actualizado |
| Instalación pandoc | `docs/installation.md` | actualizado |
| Doc funcional | `docs/functional/convert_to_md.md` | creado |
| Navegación | `mkdocs.yml` | actualizado |
| Canónico IA | `.github/SHARED_INSTRUCTIONS.md` | actualizado |
| Flujo documental | `.github/prompts/document_project.prompt.md` | actualizado |
| Entrada Claude | `CLAUDE.md` | actualizado |
| REQUEST | `.ai/sessions/2026-06-12-pandoc/00_REQUEST.md` | creado |
| CONTEXT_SNAPSHOT | `.ai/sessions/2026-06-12-pandoc/00_CONTEXT_SNAPSHOT.md` | creado |
| TRACEABILITY | `.ai/sessions/2026-06-12-pandoc/TRACEABILITY.md` | creado |

## Directrices para Futuras IAs

**[pandoc / check_env]**: pandoc es herramienta de sistema, no paquete Python. Verificar con
`shutil.which`, no con `importlib.util.find_spec`. Está en `SYSTEM_TOOLS`, separado de
`REQUIRED_TOOLS`. Su ausencia es aviso (exit 0), no fallo crítico.

**[convert_to_md]**: la carpeta de salida es `<origen>/md/` reflejando la estructura de
subdirectorios (`output_path` usa `relative_to`). Los ficheros ya en `md/` se excluyen de
la detección con `"md" not in p.relative_to(source).parts[:-1]`.

**[document_project Fase 0b]**: fase condicional — solo si hay ficheros binarios en el origen.
Si no hay, omitir completamente. Los ficheros convertidos en `md/` reciben el mismo tratamiento
que `.md` nativos en Fases 2-4.

**[ruff E501]**: límite de línea 100 chars. f-strings con paths relativos pueden superarlo;
asignar a variable auxiliar antes de interpolar en el string.

**[sesiones mismo día]**: cuando ya existe una carpeta `YYYY-MM-DD/`, usar sufijo descriptivo
(`YYYY-MM-DD-<tema>/`) para no sobreescribir la sesión anterior.

## Veredicto final

Veredicto: CLOSED
Pendientes al cierre:
- Commit + push a develop (preparado en esta sesión).
