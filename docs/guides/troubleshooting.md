# Troubleshooting

## 1. Objetivo

Diagnosticar y resolver los errores conocidos del tooling de doc_ia (verificación de
entorno, build de documentación y empaquetado offline). Es una guía how-to de
diagnóstico, no una explicación de arquitectura.

## 2. Requisitos Previos

- Entorno configurado según la [guía de incorporación](onboarding_dev.md).
- Terminal en la raíz del repositorio con el venv activado.

## 3. Pasos

1. Verifica el entorno de tooling:

   ```bash
   python scripts/check_env.py
   ```

2. Si falta alguna herramienta, reinstala dependencias:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Reproduce el build en modo estricto para localizar errores de documentación:

   ```bash
   python -m mkdocs build --strict
   ```

4. Si el fallo es del empaquetado, ejecuta el script con build incluido (descarta un
   `site/` obsoleto):

   ```bash
   python scripts/build_docs_zip.py
   ```

## 4. Verificación

```bash
python scripts/check_env.py
# Entorno de tooling documental completo.

python -m mkdocs build --strict
# INFO    -  Documentation built in X.XX seconds   (sin warnings)
```

## 5. Variantes y Solución de Problemas

| Escenario/Error | Causa probable | Solución |
|---|---|---|
| `Faltan herramientas: …` (exit 1) | Dependencias no instaladas o venv sin activar | Activar venv + `pip install -r requirements.txt` |
| Warning de MkDocs con `--strict` | Página en `nav:` inexistente, huérfana o enlace relativo roto | Corregir `mkdocs.yml` o el enlace; re-ejecutar el build |
| `ERROR: …\site does not exist` (exit 1) | `--no-build` sin un `site/` generado previamente | Ejecutar sin `--no-build` al menos una vez |
| `ERROR: …\site cannot be opened without a server` (exit 1) | `mkdocs.yml` sin `use_directory_urls: false`, sin el plugin `offline` o sin el shim local en `extra.polyfills` (el tema pide `https://unpkg.com/iframe-worker/shim`) | Restaurar las tres claves (ver [Referencia](../reference/index.md)); cada línea `- <página>: <problema>` dice qué falta |
| `index.html` del ZIP abre la página sin estilos ni menú | Se abrió dentro del ZIP, sin extraerlo | Extraer el ZIP completo y abrir `index.html` de la carpeta extraída |
| Con doble clic, la búsqueda no responde | El navegador o una política de empresa bloquea scripts de ficheros locales | Usar `python start-server.py` dentro de la carpeta extraída; no cambiar opciones de seguridad del navegador |
| El build con `--builder zensical` falla al arrancar | Zensical no está instalado (no es dependencia del proyecto) | Instalarlo aparte o usar el builder por defecto (`mkdocs`) |
| La cadena `--8<--` aparece literal en el sitio | Ruta del snippet incorrecta para `pymdownx.snippets` | Usar ruta relativa desde `docs/` (p. ej. `examples/foo.py`, NO `docs/examples/foo.py`) porque `base_path: [docs]` está activo en `mkdocs.yml` |
| El hook PostToolUse falla tras editar un script | ruff/mypy/pytest detectan un problema real | Ejecutar el comando del hook manualmente y corregir el hallazgo |
| `Motor 'docling' no disponible` | docling no instalado | `pip install docling` o usar `--engine markitdown` |
| `import torch` tarda 27+ minutos | GPU NVIDIA sin CUDA Toolkit | El script fija `CUDA_VISIBLE_DEVICES=""` por defecto; usar `--device cpu` (default) |
| `--device cuda` falla: `nvidia-smi no encontrado` | NVIDIA driver no instalado o nvidia-smi no en PATH | Instalar NVIDIA driver; verificar con `nvidia-smi` en terminal |
| `INVÁLID: cabecera PDF inválida` | Fichero PDF corrupto o no es PDF real | Verificar integridad del fichero; re-descargar si es necesario |
| `INVÁLID: archivo ZIP inválido` en DOCX/PPTX | Fichero Office corrupto | Abrir en Office para verificar; re-guardar si se puede abrir |
| RapidOCR PP-OCRv6 incompatible | Versión de PP-OCR no soportada | Usar `--no-ocr` o `--ocr-engine easyocr` |
| Ficheros `.msg` fallan con docling | Formato MSG con estructura compleja | Usar `--engine markitdown` para ficheros MSG |
| `--chunk` con motor markitdown/pandoc | Chunking solo disponible con docling | Usar `--engine docling --chunk` |
