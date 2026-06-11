# TRACEABILITY — 2026-06-12c

## Objetivo

Hacer `downloads.md` **siempre obligatorio** en todos los proyectos documentados con doc_ia,
eliminando la condición "solo si hay ZIP script" que causó su ausencia en socyalpro.

## Estado final: CLOSED ✅

---

## Cambios ejecutados

### 1. `document_project.prompt.md` (`.github/prompts/`)

- **Fase 1**: `TIENE_DOWNLOADS_PAGE` (condicional) → `TIENE_ZIP_SCRIPT` (señal técnica),
  con nota explícita "downloads.md SIEMPRE OBLIGATORIO independientemente del valor"
- **Fase 7b**: reescrita completamente — ya no es condicional; siempre ejecuta Variante A o B:
  - Variante A: `TIENE_ZIP_SCRIPT=true` → página completa con `build_docs_zip.py` + tabla real
  - Variante B: `TIENE_ZIP_SCRIPT=false` → build local manual + placeholder tabla pendiente
- **Item 8b** (checklist cierre): `ZIP OFFLINE (condicional)` → `DOWNLOADS (siempre)`

### 2. `documentation-generator.agent.md` (`.github/agents/`)

- **Fase 4** ("Páginas a generar"): añadida entrada explícita `downloads.md — SIEMPRE obligatorio`
  con descripción de Variante A/B

### 3. `DOCUMENTATION_STANDARD.md` (`.github/`)

- **§4.1 nav template** (línea ~876): comentario cambiado de
  `# si el proyecto genera artefactos descargables` →
  `# SIEMPRE obligatorio — Variante A (con build_docs_zip.py) o Variante B (sin script, build local + placeholder)`
- **§3.9 tabla "Guías adicionales"** (línea ~471): eliminada la implicación de que `downloads.md`
  es específico de "Tooling de documentación (doc_ia)"; nota añadida para clarificar que es
  página estándar top-level

### 4. `docs/downloads.md` (socyalpro — Variante B creada)

Página creada en `C:\Desarrollo\Proyectos\socyalpro\docs\downloads.md` con:
- Build local: requisitos, venv, mkdocs serve, mkdocs build --strict, Compress-Archive PowerShell
- Tabla placeholder `| — | — | — | — |` con nota "pendiente publicación automática"
- Nota sobre búsqueda offline (http.server)
- Enlaces relacionados (quickstart, installation, onboarding_dev)

Entrada añadida en `C:\Desarrollo\Proyectos\socyalpro\mkdocs.yml`:
```yaml
- Descargas: downloads.md
```

---

## Verificación

- `mkdocs build --strict` en socyalpro: OK (no errores de página faltante)
- `downloads.md` aparece en nav lateral de socyalpro

---

## Commit pendiente

Ver `GITHUB_COMMIT_MESSAGE.md`
