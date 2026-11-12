# Ejemplo: Generar ZIP Offline

## 1. Contexto del Ejemplo

Para distribuir la documentación a entornos sin conexión (o adjuntarla a una release)
existen dos ZIP complementarios, y los dos salen del mismo comando:

- **ZIP "latest"** (`mkdocs_hooks.py`, paso posterior al build): `site/doc_ia-docs-latest.zip`.
  Es el ZIP que sirve la página de descargas.
- **ZIP versionado** (`scripts/build_docs_zip.py`): `dist/doc_ia-docs-<versión>.zip` con SHA256
  acumulativo. Es el artefacto para releases.

Zensical es el único generador (ADR-003) y no ejecuta `hooks:`, así que
`scripts/build_docs_zip.py` es el pipeline de build: sincroniza los ficheros raíz, construye,
genera el ZIP "latest" y después el versionado. Este ejemplo muestra el pipeline y cómo validar
la integridad del resultado.

## 2. Implementación de Referencia

```bash
# Build estricto con Zensical + ZIP latest + ZIP versionado + SHA256 (caso normal)
python scripts/build_docs_zip.py

# Empaquetar el site/ existente sin reconstruir
python scripts/build_docs_zip.py --no-build

# Carpeta de salida alternativa
python scripts/build_docs_zip.py --output-dir /tmp/releases

# Vista previa local mientras se escribe (no genera ZIP ni sincroniza CHANGELOG/CONTRIBUTING)
python -m zensical serve
```

Salida: `site/doc_ia-docs-latest.zip` + `.sha256`, y `dist/doc_ia-docs-<versión>.zip` + `.sha256`
+ `dist/CHECKSUMS.txt`.

## 3. Explicación del Código

**Paso posterior (`mkdocs_hooks.py`)**:
- `on_post_build(config)` recibe `config["site_dir"]` del pipeline; nunca asume `site/` por nombre.
- Se ejecuta solo si `zensical build` termina con `0`, con el sitio ya completo: el ZIP lleva el
  índice de búsqueda `search.js`.
- Excluye `.zip` y `.sha256` del propio ZIP para evitar recursividad.
- Incluye `scripts/start-server.py` en la raíz del ZIP (alternativa: `python start-server.py` tras descomprimir).
- Sobreescribe el ZIP "latest" en cada build; no acumula histórico (sin versión en el nombre).

**Script (`build_docs_zip.py`)**:
- Antes del build copia `CHANGELOG.md` y `CONTRIBUTING.md` a `docs/` (`hooks/sync_root_docs.py`).
- El nombre del ZIP toma la versión de `pyproject.toml`: con `version = "0.1.0"` el resultado es `dist/doc_ia-docs-0.1.0.zip`.
- El build es **estricto por defecto** (`--strict`): cualquier warning detiene el proceso antes de empaquetar. `--no-strict` lo desactiva.
- `--no-build` falla con código `1` si no existe `site/` previo — evita empaquetar nada silenciosamente.
- Antes de empaquetar comprueba que `site/` se abre con doble clic en `index.html`; si no, código `1` (ver §4).
- `dist/CHECKSUMS.txt` es acumulativo: conserva el histórico de hashes con timestamp.
- `--builder mkdocs` (llamadas antiguas) termina con código `2`; `--builder zensical` se acepta sin efecto.

## 4. Ejecución y Pruebas

**Output del pipeline:**

```bash
python scripts/build_docs_zip.py
# [build_docs_zip] Pre-build: hooks/sync_root_docs.py
# [sync_root_docs] CHANGELOG.md -> ...\docs\changelog.md
# [build_docs_zip] Building with: <python> -m zensical build --strict
# [build_docs_zip] Post-build: mkdocs_hooks.py
# [ZIP] Generando descarga de documentacion: ...\site\doc_ia-docs-latest.zip
# [OK] ZIP creado: doc_ia-docs-latest.zip (X.XX MB)
# [OK] SHA256: <hash de 64 caracteres>
# [build_docs_zip] Created: ...\dist\doc_ia-docs-0.1.0.zip
# [build_docs_zip] ZIP created: doc_ia-docs-0.1.0.zip (X.XX MB)
# [build_docs_zip] SHA256: <hash de 64 caracteres>
# [build_docs_zip] Checksum saved to: doc_ia-docs-0.1.0.zip.sha256
# [build_docs_zip] All checksums in: CHECKSUMS.txt
```

Validar la integridad de una descarga:

```bash
sha256sum -c dist/doc_ia-docs-0.1.0.zip.sha256        # Linux/Mac (versionado)
sha256sum -c site/doc_ia-docs-latest.zip.sha256        # Linux/Mac (latest)
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

**Generador MkDocs pedido por una llamada antigua:**

```bash
python scripts/build_docs_zip.py --builder mkdocs
# build_docs_zip.py: error: builder 'mkdocs' is no longer supported: Zensical is the only documentation generator (ADR-003). Drop --builder.
echo $?   # 2 — no se construye nada
```

## 5. Referencias Relacionadas

- Documentación funcional: [ZIP de Documentación Offline](../functional/build_docs_zip.md)
- Referencia técnica: [build_docs_zip](../api/build_docs_zip.md)
- Ejemplos relacionados: [Verificar Entorno](check_env_usage.md)
- Página de descargas: [Descargas](../downloads.md)
