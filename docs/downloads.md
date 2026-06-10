# 📥 Descargas

Descarga la documentación completa de **doc_ia** en formato offline (ZIP).

---

## 📦 Documentación Offline

La documentación completa está disponible como un archivo ZIP comprimido que puedes descargar
y abrir en cualquier navegador sin conexión a Internet.

### Características del ZIP

- ✅ **Búsqueda offline** — Índice de búsqueda completo
- ✅ **Navegación interactiva** — Menú y referencias cruzadas
- ✅ **Diagramas Mermaid** — Flujos y arquitectura
- ✅ **Responsive** — Compatible con móvil, tablet y desktop

---

## 🔗 Descarga Actual

Las versiones publicadas están disponibles en **GitHub Releases** del repositorio
(tags `docs-vX.Y.Z`), cada una con el ZIP y su checksum adjuntos.

**Cómo usar**

1. Descarga el ZIP y su `.sha256` desde la release
2. Extrae los archivos: `unzip doc_ia-docs-X.Y.Z.zip`
3. Abre `index.html` en tu navegador

> **Nota sobre la búsqueda offline**: los navegadores no permiten ejecutar Web Workers desde
> `file:///`. Si necesitas búsqueda completa, sirve la carpeta extraída con
> `python -m http.server 8000` y navega a `http://localhost:8000`. Sin servidor, la navegación
> funciona pero la búsqueda queda deshabilitada.

---

## 🔐 Validar Integridad (SHA256)

El archivo `.sha256` adjunto contiene el hash de integridad del ZIP. Descarga ambos archivos
y valida según tu plataforma.

### Método 1: Terminal (Linux/macOS)

```bash
sha256sum -c doc_ia-docs-X.Y.Z.zip.sha256
# Salida esperada: doc_ia-docs-X.Y.Z.zip: OK ✅
```

### Método 2: PowerShell (Windows)

```powershell
$hash = (Get-FileHash doc_ia-docs-X.Y.Z.zip -Algorithm SHA256).Hash
$checksum = (Get-Content doc_ia-docs-X.Y.Z.zip.sha256).Split()[0]
if ($hash -eq $checksum) { Write-Host "✅ Integridad verificada" } else { Write-Host "❌ Checksum no coincide" }
```

### Método 3: macOS (con shasum)

```bash
shasum -a 256 -c doc_ia-docs-X.Y.Z.zip.sha256
```

---

## 🛠️ Para Desarrolladores

### Generar ZIP Localmente

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

### Publicación automática

El workflow `.github/workflows/docs-zip-release.yml` publica una release `docs-vX.Y.Z`
en cada push a `main` con cambios en `docs/`, adjuntando el ZIP y los checksums.

---

## ❓ FAQ

- **¿Cómo buscar en el ZIP offline?**
  Sirve la carpeta con `python -m http.server` y usa el campo de búsqueda (requiere JavaScript).

- **¿Puedo actualizar el ZIP?**
  Sí. Descarga la última versión desde GitHub Releases o constrúyelo localmente.

- **¿Incluye código fuente?**
  No. El ZIP contiene solo documentación HTML/CSS/JS.

- **¿Funcionan los links internos?**
  Sí. Todos los links relativos funcionan dentro del ZIP.

---

## 🔗 Enlaces Relacionados

- [Inicio](index.md) — Página principal de la documentación
- [Guía de Codex](guides/codex_guide.md) — Uso de Codex (OpenAI) en este proyecto

---

*Última actualización: 2026-06-10*
