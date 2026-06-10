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
| El build con `--builder zensical` falla al arrancar | Zensical no está instalado (no es dependencia del proyecto) | Instalarlo aparte o usar el builder por defecto (`mkdocs`) |
| La cadena `--8<--` aparece literal en el sitio | Ruta del snippet incorrecta para `pymdownx.snippets` | Usar ruta desde la raíz del repo (p. ej. `docs/examples/...py`) |
| El hook PostToolUse falla tras editar un script | ruff/mypy/pytest detectan un problema real | Ejecutar el comando del hook manualmente y corregir el hallazgo |
