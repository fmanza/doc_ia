# 📥 Descargas

Descarga la documentación completa de **doc_ia** en formato offline (ZIP) para acceder a toda la información sin conexión a Internet.

---

## 📦 Documentación Offline

La documentación completa está disponible como un archivo ZIP comprimido que puedes descargar y abrir en cualquier navegador, incluso sin acceso a Internet y sin instalar nada: basta con extraerlo y hacer doble clic en `index.html`.

### Características del ZIP

- ✅ **Sin Python ni servidor** — Doble clic en `index.html` tras extraer el ZIP
- ✅ **Búsqueda offline** — Índice de búsqueda completo en local, también abriendo los ficheros directamente
- ✅ **Navegación interactiva** — Menú, referencias cruzadas, breadcrumbs
- ✅ **Diagramas Mermaid** — Flujos y arquitectura, dibujados sin conexión (Mermaid va incluido en el ZIP)
- ✅ **Responsive** — Compatible con móvil, tablet y desktop

---

## 🔗 Descarga Actual

| Versión | Tamaño | Checksum | Fecha |
|---|---|---|---|
| <a href="doc_ia-docs-latest.zip">doc_ia-docs-latest.zip</a> | ~2.9 MB | <a href="doc_ia-docs-latest.zip.sha256">.sha256</a> | 2026-11-13 |

**doc_ia 0.13.1** — Instrucciones IA y tooling para documentar proyectos de desarrollo

---

## 🚀 Cómo usar el ZIP

### Paso 1: Descargar

Descarga el ZIP desde el link superior.

### Paso 2: Extraer

Extrae **todo** el ZIP a una carpeta. En el Explorador de Windows: clic derecho → «Extraer todo…».

```bash
# Windows (PowerShell)
Expand-Archive doc_ia-docs-latest.zip -DestinationPath ./doc_ia-docs

# Linux / macOS
unzip doc_ia-docs-latest.zip -d ./doc_ia-docs
```

### Paso 3: Visualizar

Haz doble clic en `index.html` dentro de la carpeta extraída. Se abre en tu navegador con
navegación, búsqueda y diagramas, sin Python, sin servidor y sin conexión.

!!! warning "Extrae antes de abrir"
    Si haces doble clic en `index.html` **dentro** del ZIP sin extraerlo, el sistema abre solo ese
    fichero y la página sale sin estilos ni menú. Extrae siempre la carpeta completa.

!!! note "Alternativa: servidor local"
    El ZIP incluye también `start-server.py` (Python 3.7 o superior, sin instalar paquetes):
    `python start-server.py` (Windows: `py start-server.py`) abre `http://127.0.0.1:8000`,
    accesible solo desde tu equipo; para terminar, `Ctrl + C`. Es la única opción con los ZIP
    de doc_ia 0.3.0 o anteriores, que no se pueden abrir con doble clic.

!!! tip "¿Empezando desde cero?"
    El ZIP incluye `VER_DOCUMENTACION.md` (también en la raíz del repositorio): requisitos y pasos
    para Windows, macOS y Linux, y problemas frecuentes.

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

### Pipeline de build y ZIP automático

Zensical es el único generador (ADR-003) y no ejecuta `hooks:`, así que
`scripts/build_docs_zip.py` es el pipeline de build: copia `CHANGELOG.md` y `CONTRIBUTING.md` a
`docs/`, ejecuta `zensical build --strict` y, si termina sin errores, el paso post-build
`mkdocs_hooks.py` genera `doc_ia-docs-latest.zip` en `site/`. No requiere instalación ni activar
ningún venv específico: el pipeline carga los dos pasos por ruta. El ZIP lleva el índice de
búsqueda en JS porque se genera cuando el build ya ha terminado.

`mkdocs_hooks.py` es también el patrón canónico para otros proyectos: copiarlo al proyecto
destino y cambiar únicamente la línea `zip_path`.

### Generar ZIP versionado

```bash
# Build (Zensical, --strict) + ZIP latest + ZIP versionado + SHA256
python scripts/build_docs_zip.py

# ZIP de un site/ ya construido (sin build)
python scripts/build_docs_zip.py --no-build

# Vista previa local (no genera ZIP ni sincroniza CHANGELOG/CONTRIBUTING)
python -m zensical serve
```

Antes de empaquetar, el script comprueba que `site/` se puede abrir sin servidor (índice de
búsqueda en JS, ningún script remoto, ningún enlace a carpeta); si no, termina con código 1.

**Output**: `dist/doc_ia-docs-{versión}.zip` + `dist/doc_ia-docs-{versión}.zip.sha256` +
`dist/CHECKSUMS.txt` (histórico de hashes).

### Publicación automática (GitHub Releases)

El workflow `.github/workflows/docs-zip-release.yml` publica una release `docs-vX.Y.Z`
en cada push a `main` con cambios en `docs/`, adjuntando el ZIP y los checksums. Al crear el tag
`vX.Y.Z`, `.github/workflows/docs-release.yml` adjunta a esa release el mismo ZIP y su `.sha256`:
el ZIP es reproducible, así que las dos releases publican el mismo fichero con la misma huella.

Releases publicadas: [github.com/fmanza/doc_ia/releases](https://github.com/fmanza/doc_ia/releases)

---

## 📝 Información de versión

- **Versión de doc_ia**: 0.13.1
- **Generador**: Zensical 0.1.1 (Mermaid 12.2.0 incluido en el sitio, con la integración nativa del tema; plugin `offline` con iframe-worker 1.0.4 local)
- **Actualización**: 2026-10-29
