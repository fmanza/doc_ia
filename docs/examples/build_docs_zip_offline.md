# Ejemplo: Generar ZIP Offline

## 1. Contexto del Ejemplo

Para distribuir la documentación a entornos sin conexión (o adjuntarla a una release)
hay que empaquetar el sitio generado en un ZIP versionado y verificable. Este ejemplo
muestra las invocaciones CLI típicas de `scripts/build_docs_zip.py` y cómo validar la
integridad del resultado.

## 2. Implementación de Referencia

Comandos CLI (código inline por ser fragmentos triviales, según las reglas de
`docs.instructions.md`):

```bash
# Build estricto con MkDocs + ZIP + SHA256 (caso normal)
python scripts/build_docs_zip.py

# Empaquetar el site/ existente sin reconstruir
python scripts/build_docs_zip.py --no-build

# Carpeta de salida alternativa
python scripts/build_docs_zip.py --output-dir /tmp/releases

# Builder alternativo (requiere zensical instalado)
python scripts/build_docs_zip.py --builder zensical
```

## 3. Explicación del Código

- El nombre del ZIP toma la versión de `pyproject.toml`: con `version = "0.1.0"` el
  resultado es `dist/doc_ia-docs-0.1.0.zip`.
- El build es **estricto por defecto** (`--strict`): cualquier warning de MkDocs detiene
  el proceso antes de empaquetar. `--no-strict` lo desactiva.
- `--no-build` falla con código `1` si no existe `site/` previo — evita empaquetar nada
  silenciosamente.
- `dist/CHECKSUMS.txt` es acumulativo: conserva el histórico de hashes con timestamp.

## 4. Ejecución y Pruebas

```bash
python scripts/build_docs_zip.py
# [build_docs_zip] Building with: <python> -m mkdocs build --strict
# [build_docs_zip] Created: ...\dist\doc_ia-docs-0.1.0.zip
# [build_docs_zip] ZIP created: doc_ia-docs-0.1.0.zip (X.XX MB)
# [build_docs_zip] SHA256: <hash de 64 caracteres>
# [build_docs_zip] Checksum saved to: doc_ia-docs-0.1.0.zip.sha256
# [build_docs_zip] All checksums in: CHECKSUMS.txt
```

Validar la integridad de una descarga:

```bash
sha256sum -c dist/doc_ia-docs-0.1.0.zip.sha256        # Linux/Mac
# doc_ia-docs-0.1.0.zip: OK
```

```powershell
# Windows (PowerShell): comparar con el contenido del .sha256
(Get-FileHash dist\doc_ia-docs-0.1.0.zip -Algorithm SHA256).Hash.ToLower()
Get-Content dist\doc_ia-docs-0.1.0.zip.sha256
```

El tamaño en MB y el hash varían con el contenido del sitio; el formato del output es
estable.

## 5. Referencias Relacionadas

- Documentación funcional: [ZIP de Documentación Offline](../functional/build_docs_zip.md)
- Referencia técnica: [build_docs_zip](../api/build_docs_zip.md)
- Ejemplos relacionados: [Verificar Entorno](check_env_usage.md)
- Página de descargas: [Descargas](../downloads.md)
