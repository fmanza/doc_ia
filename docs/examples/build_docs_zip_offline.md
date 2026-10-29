# Ejemplo: Generar ZIP Offline

## 1. Contexto del Ejemplo

Para distribuir la documentación a entornos sin conexión (o adjuntarla a una release)
existen dos mecanismos complementarios:

- **Hook automático** (`mkdocs_hooks.py`): genera `site/doc_ia-docs-latest.zip` en cada
  `mkdocs build`, sin ningún comando adicional. Es el ZIP que sirve la página de descargas.
- **Script manual** (`scripts/build_docs_zip.py`): genera `dist/doc_ia-docs-<versión>.zip`
  versionado con SHA256 acumulativo. Es el artefacto para releases.

Este ejemplo muestra ambos mecanismos y cómo validar la integridad del resultado.

## 2. Implementación de Referencia

### Hook automático — ZIP "latest" (sin comandos adicionales)

El hook se activa con cualquier build. No requiere instalación:

```bash
# ZIP latest generado automáticamente junto al build
python -m mkdocs build

# También durante el servidor local (on_post_build se invoca al arrancar)
python -m mkdocs serve
```

Salida: `site/doc_ia-docs-latest.zip` + `site/doc_ia-docs-latest.zip.sha256`.

### Script manual — ZIP versionado

```bash
# Build estricto con MkDocs + ZIP + SHA256 (caso normal)
python scripts/build_docs_zip.py

# Empaquetar el site/ existente sin reconstruir
python scripts/build_docs_zip.py --no-build

# Carpeta de salida alternativa
python scripts/build_docs_zip.py --output-dir /tmp/releases

# Builder alternativo (requiere zensical instalado). El script ejecuta los hooks que
# Zensical ignora: sincroniza CHANGELOG/CONTRIBUTING antes y genera el ZIP latest después
python scripts/build_docs_zip.py --builder zensical
```

## 3. Explicación del Código

**Hook (`mkdocs_hooks.py`)**:
- `on_post_build(config)` recibe `config["site_dir"]` directamente de MkDocs; nunca asume `site/` por nombre.
- Excluye `.zip` y `.sha256` del propio ZIP para evitar recursividad.
- Incluye `scripts/start-server.py` en la raíz del ZIP (alternativa: `python start-server.py` tras descomprimir).
- Se ejecuta después del plugin `offline` (`on_post_build.mkdocs_priority = -200`), así que el ZIP lleva `search/search_index.js`.
- Sobreescribe el ZIP "latest" en cada build; no acumula histórico (sin versión en el nombre).

**Script (`build_docs_zip.py`)**:
- El nombre del ZIP toma la versión de `pyproject.toml`: con `version = "0.1.0"` el resultado es `dist/doc_ia-docs-0.1.0.zip`.
- El build es **estricto por defecto** (`--strict`): cualquier warning detiene el proceso antes de empaquetar. `--no-strict` lo desactiva.
- `--no-build` falla con código `1` si no existe `site/` previo — evita empaquetar nada silenciosamente.
- Antes de empaquetar comprueba que `site/` se abre con doble clic en `index.html`; si no, código `1` (ver §4).
- `dist/CHECKSUMS.txt` es acumulativo: conserva el histórico de hashes con timestamp.

## 4. Ejecución y Pruebas

**Hook — output del build:**

```bash
python -m mkdocs build
# INFO    -  Cleaning site directory
# INFO    -  Building documentation to directory: ...\site
# ...
# [ZIP] Generando descarga de documentacion: ...\site\doc_ia-docs-latest.zip
# [ZIP] Incluyendo servidor local: start-server.py
# [OK] ZIP creado: doc_ia-docs-latest.zip (X.XX MB)
# [OK] SHA256: <hash de 64 caracteres>
# [OK] Checksum guardado: doc_ia-docs-latest.zip.sha256
```

**Script — output del empaquetado versionado:**

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
sha256sum -c dist/doc_ia-docs-0.1.0.zip.sha256        # Linux/Mac (script)
sha256sum -c site/doc_ia-docs-latest.zip.sha256        # Linux/Mac (hook)
# doc_ia-docs-0.1.0.zip: OK
```

```powershell
# Windows (PowerShell): comparar con el contenido del .sha256
(Get-FileHash dist\doc_ia-docs-0.1.0.zip -Algorithm SHA256).Hash.ToLower()
Get-Content dist\doc_ia-docs-0.1.0.zip.sha256
```

El tamaño en MB y el hash varían con el contenido del sitio; el formato del output es
estable.

**Abrir el ZIP sin servidor** (lo que hará quien lo reciba):

```powershell
Expand-Archive dist\doc_ia-docs-0.1.0.zip -DestinationPath $env:TEMP\doc_ia-docs
Invoke-Item $env:TEMP\doc_ia-docs\index.html   # equivale al doble clic
```

```bash
unzip dist/doc_ia-docs-0.1.0.zip -d /tmp/doc_ia-docs
xdg-open /tmp/doc_ia-docs/index.html            # macOS: open
```

**Sitio que no se abre sin servidor** — por ejemplo, si se quita el shim local de
`extra.polyfills` y el tema vuelve a pedirlo a unpkg:

```bash
python scripts/build_docs_zip.py --no-build
# [build_docs_zip] ERROR: ...\site cannot be opened without a server (use_directory_urls: false, `offline` plugin, local iframe-worker in extra.polyfills):
#   - 404.html: remote script https://unpkg.com/iframe-worker/shim
#   - adr/ADR-001-mkdocs-material-por-defecto.html: remote script https://unpkg.com/iframe-worker/shim
#   ...
#   ... and N more
echo $?   # 1 — no se crea ningún ZIP
```

## 5. Referencias Relacionadas

- Documentación funcional: [ZIP de Documentación Offline](../functional/build_docs_zip.md)
- Referencia técnica: [build_docs_zip](../api/build_docs_zip.md)
- Ejemplos relacionados: [Verificar Entorno](check_env_usage.md)
- Página de descargas: [Descargas](../downloads.md)
