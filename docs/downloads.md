# 📥 Descargas

Descarga la documentación completa de **doc_ia** en formato offline (ZIP) para acceder a toda la información sin conexión a Internet.

---

## 📦 Documentación Offline

La documentación completa está disponible como un archivo ZIP comprimido que puedes descargar y abrir en cualquier navegador, incluso sin acceso a Internet.

### Características del ZIP

- ✅ **Búsqueda offline** — Índice de búsqueda completo en local
- ✅ **Navegación interactiva** — Menú, referencias cruzadas, breadcrumbs
- ✅ **Diagramas Mermaid** — Flujos y arquitectura, dibujados sin conexión (Mermaid va incluido en el ZIP)
- ✅ **Responsive** — Compatible con móvil, tablet y desktop

---

## 🔗 Descarga Actual

| Versión | Tamaño | Checksum | Fecha |
|---|---|---|---|
| <a href="../doc_ia-docs-latest.zip">doc_ia-docs-latest.zip</a> | ~1.1 MB | <a href="../doc_ia-docs-latest.zip.sha256">.sha256</a> | 2026-10-28 |

**doc_ia 0.2.0** — Instrucciones IA y tooling para documentar proyectos de desarrollo

---

## 🚀 Cómo usar el ZIP

### Paso 1: Descargar

Descarga el ZIP desde el link superior.

### Paso 2: Extraer

```bash
# Windows (PowerShell)
Expand-Archive doc_ia-docs-latest.zip -DestinationPath ./doc_ia-docs

# Linux / macOS
unzip doc_ia-docs-latest.zip -d ./doc_ia-docs
```

### Paso 3: Visualizar

#### **Opción A (Recomendada — Búsqueda completa) ⭐**

```bash
cd doc_ia-docs
python start-server.py
```

El ZIP incluye `start-server.py`. Al ejecutarlo, abre el navegador automáticamente en `http://localhost:8000`. Los navegadores no permiten Web Workers desde `file:///` por seguridad; el servidor HTTP local lo resuelve automáticamente.

#### **Opción B (Navegación sin búsqueda)**

Abre directamente `index.html` en tu navegador.

- ✅ Todos los menús y referencias funcionan
- ✅ Diagramas Mermaid visibles
- ❌ Búsqueda deshabilitada (limitación de seguridad del navegador)

---

## 🔐 Validar Integridad (SHA256)

### Windows (PowerShell)

```powershell
$hash = (Get-FileHash doc_ia-docs-latest.zip -Algorithm SHA256).Hash
Write-Host "SHA256 calculado: $hash"
Get-Content doc_ia-docs-latest.zip.sha256
# Deben coincidir exactamente ✅
```

### Linux / macOS

```bash
sha256sum -c doc_ia-docs-latest.zip.sha256
# Salida esperada: doc_ia-docs-latest.zip: OK ✅
```

---

## 🛠️ Para Desarrolladores

### ZIP automático (hook MkDocs)

El hook `mkdocs_hooks.py` genera `doc_ia-docs-latest.zip` automáticamente en `site/`
en cada `mkdocs build`. No requiere instalación ni activar ningún venv específico:
MkDocs lo carga directamente desde `mkdocs.yml` mediante la clave `hooks:`.

```yaml
# mkdocs.yml (extracto)
hooks:
  - hooks/sync_root_docs.py
  - mkdocs_hooks.py
```

Este hook es también el patrón canónico para otros proyectos: copiar `mkdocs_hooks.py`
al proyecto destino y cambiar únicamente la línea `zip_path`.

### Generar ZIP versionado

```bash
# Build (MkDocs Material) + ZIP + SHA256
python scripts/build_docs_zip.py

# ZIP de un site/ ya construido (sin build)
python scripts/build_docs_zip.py --no-build

# Con Zensical, si está instalado (recíprocamente compatible)
python scripts/build_docs_zip.py --builder zensical
```

**Output**: `dist/doc_ia-docs-{versión}.zip` + `dist/doc_ia-docs-{versión}.zip.sha256` +
`dist/CHECKSUMS.txt` (histórico de hashes).

### Publicación automática (GitHub Releases)

El workflow `.github/workflows/docs-zip-release.yml` publica una release `docs-vX.Y.Z`
en cada push a `main` con cambios en `docs/`, adjuntando el ZIP y los checksums.

Releases publicadas: [github.com/fmanza/doc_ia/releases](https://github.com/fmanza/doc_ia/releases)

---

## 📝 Información de versión

- **Versión de doc_ia**: 0.2.0
- **Generador**: MkDocs + Material for MkDocs (Mermaid 12.2.0 incluido en el sitio, con la integración nativa del tema)
- **Actualización**: 2026-10-28
