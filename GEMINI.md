# Instrucciones para Gemini Code Assist — doc_ia

Este fichero proporciona especialización para Gemini Code Assist al trabajar con el repositorio `doc_ia`.

---

## ⚠️ Contexto previo obligatorio

Lee **primero**:
- **`.github/SHARED_INSTRUCTIONS.md`** — Fuente canónica: principios del proyecto (sin API keys, tooling determinista, ejecución en chat), arquitectura, calidad, comandos, documentación, flujo de trabajo, Conventional Commits. **Esta es la base.**
- **Este fichero** — Especialización para Gemini Code Assist únicamente.

---

## Flujo de Trabajo Recomendado

Para cambios estructurados, sigue el ciclo de vida definido en el proyecto:

1. **PLAN**: Analizar el objetivo, alcance y riesgos. Contrastar con el código real antes de proponer cambios.
2. **AUDIT_PLAN**: Verificar la viabilidad del plan y detectar expansiones de alcance no deseadas.
3. **IMPLEMENT**: Ejecutar los cambios aplicando los estándares de calidad del proyecto.
4. **AUDIT_CODE**: Revisión técnica independiente (bugs, edge cases, contratos, cobertura).
5. **VERSION**: Cierre de versión, actualización de CHANGELOG y documentación de rollback.

---

## Estándares de Código y Calidad

Al generar código para este proyecto, asegúrate de cumplir con:

- **Python 3.12+**: Uso de características modernas de Python.
- **Tipado Estricto**: Todas las funciones y métodos con type hints completos. Pasar `mypy --strict`.
- **Calidad y Estilo**: Seguir las reglas de `ruff` (`pyproject.toml`).
- **F-Strings**: Usar exclusivamente f-strings para interpolación de cadenas.
- **Tooling determinista**: los scripts de `scripts/` nunca invocan servicios IA ni requieren
  credenciales; salida por código de retorno; ejecutables standalone.
- **SOLID**: Seguir los principios de diseño definidos en las instrucciones compartidas.

---

## Sincronización de Instrucciones IA

Si se modifican reglas comunes o flujos, actualiza los ficheros en este orden:

1. **`.github/SHARED_INSTRUCTIONS.md`** (Fuente canónica)
2. **`.github/copilot-instructions.md`** (Especialización Copilot)
3. **`CLAUDE.md`** (Especialización Claude Code)
4. **`GEMINI.md`** (Este fichero)

**Validación**: Verifica que no haya duplicación de contenido entre `SHARED_INSTRUCTIONS.md` y las especializaciones, y que todas las rutas sean relativas y portables.

---

## Bootstrap de configuración IA a otro proyecto

Para replicar este sistema de instrucciones IA (Claude / Gemini / Copilot / Cursor / Codex) en otro proyecto,
incluso de **otro lenguaje y arquitectura**, usa el prompt
[`bootstrap_ai_config.prompt.md`](.github/prompts/bootstrap_ai_config.prompt.md).

**Método y dirección — modelo PULL**: se invoca **desde el proyecto destino**, apuntando a este repo
como plantilla de solo lectura; el lenguaje/arquitectura del destino es un **parámetro**. Capas:
**A** copiar verbatim · **B** copiar + reescribir dominio · **C** regenerar analizando el destino ·
**D** excluir. Detalle completo en el propio prompt.

---

## Documentar un proyecto completo

Usa **`document_project.prompt.md`** como **punto de entrada único** para documentar cualquier proyecto
(externo o el propio doc_ia). Orquesta automáticamente inventario, clasificación crear/actualizar/omitir,
generación por arquetipos, sincronización de nav y revisión.

```
Lee y aplica `.github/prompts/document_project.prompt.md` con los siguientes parámetros:

Origen(es): <ruta raíz del proyecto a documentar>
Destino: <ruta donde se escribe la documentación>
Generador: mkdocs-material
Idioma: es
```

**Campos obligatorios**: Origen(es), Destino, Generador, Idioma — si falta alguno, el prompt se detiene
y pide los datos antes de continuar.

Para una página suelta usa directamente el prompt de arquetipo correspondiente
(`functional_doc.prompt.md`, `technical_doc.prompt.md`, etc.).

---

## Comandos de Desarrollo Rápidos

```bash
python -m ruff check scripts tests   # Linting
python -m ruff format scripts tests  # Formato
python -m mypy scripts               # Type-checking (strict)
python -m pytest                     # Ejecución de tests
python -m mkdocs serve               # Previsualizar documentación
python -m mkdocs build --strict      # Build con validación estricta
python scripts/build_docs_zip.py     # Generar ZIP offline con SHA256 checksums
```

### Validación de Markdown — Checklist obligatorio

Ver `.github/SHARED_INSTRUCTIONS.md` § "Validación de Markdown en documentación".

**Puntos críticos**:
- ✅ Listas: usar `- item` o `1. item`, NUNCA dos espacios al final de línea
- ✅ Enlaces a archivos estáticos: rutas relativas reales, NO placeholders `#`
- ✅ Validar: `python -m mkdocs build --strict` sin errores

---

## 📦 Descarga de Documentación Offline

doc_ia ofrece **documentación en ZIP offline** con SHA256 checksums y auto-publicación en GitHub Releases.

- **Local**: `python scripts/build_docs_zip.py` genera el ZIP en `dist/`
- **CI/CD**: `.github/workflows/docs-zip-release.yml` auto-publica releases
- **Validación**: `sha256sum -c dist/*.sha256` (Linux/Mac) o `Get-FileHash` (Windows)

Para reutilizar el sistema en otros proyectos: ver `.github/prompts/bootstrap_ai_config.prompt.md`
(sección "📦 Descarga de Documentación Offline").

---

*Actualizado: 2026-06-10*
