# Ejemplo: Convertir Documentos a Markdown

Uso de `scripts/convert_to_md.py` para preparar documentación en formatos binarios (PDF, DOCX,
PPTX, imágenes, email…) como fuente legible para el flujo `/document-project`.

## Precondición

Al menos un motor de conversión instalado:

```bash
pip install docling                            # Motor principal (OCR, GPU, batch)
pip install markitdown                         # Alternativa ligera
winget install JohnMacFarlane.Pandoc           # Para DOC/ODT/RST (Windows)
```

## 1. Conversión con motor por defecto (docling)

```bash
python scripts/convert_to_md.py C:\proyectos\mi_api
```

**Resultado esperado**:

```
Convirtiendo 3 fichero(s) con motor 'docling' -> C:\proyectos\mi_api\md
  INFO    Cargando motor docling (puede tardar unos minutos)...
  INFO    Motor docling listo.
  CONV    docs/manual_usuario.pdf ... OK -> md/docs/manual_usuario.md
  CONV    specs/requisitos.docx ... OK -> md/specs/requisitos.md
  CONV    img/diagrama.png ... OK -> md/img/diagrama.md

Completado: 3 convertido(s) en md/ (motor: docling)
```

## 2. Conversión con markitdown (sin docling)

Si docling no está instalado o se prefiere un motor más ligero:

```bash
python scripts/convert_to_md.py C:\proyectos\mi_api --engine markitdown
```

**Resultado**:

```
Convirtiendo 2 fichero(s) con motor 'markitdown' -> C:\proyectos\mi_api\md
  OK      docs/manual_usuario.pdf -> md/docs/manual_usuario.md
  OK      specs/requisitos.docx -> md/specs/requisitos.md

Completado: 2 convertido(s) en md/ (motor: markitdown)
```

## 3. Conversión con pandoc (formatos legacy)

Para DOC, ODT, RST y LaTeX:

```bash
python scripts/convert_to_md.py C:\proyectos\legacy --engine pandoc
```

## 4. Solo validación previa (--validate-only)

Verifica integridad sin convertir. Detecta ficheros vacíos, corruptos o con cabeceras inválidas:

```bash
python scripts/convert_to_md.py C:\proyectos\mi_api --validate-only
```

**Resultado**:

```
=== Validación previa (3 fichero(s), motor: docling) ===

  Motor docling: OK

  OK      docs/manual_usuario.pdf
  OK      specs/requisitos.docx
  INVÁLID img/corrupto.png: cabecera imagen .png inválida (fichero corrupto)

Validación completada: 1 error(es) de 3 fichero(s).
```

Validar para un motor específico:

```bash
python scripts/convert_to_md.py C:\proyectos\mi_api --validate-only --engine markitdown
```

## 5. Vista previa sin ejecutar (--dry-run)

```bash
python scripts/convert_to_md.py C:\proyectos\mi_api --dry-run
```

**Resultado**:

```
Convirtiendo 3 fichero(s) con motor 'docling' -> C:\proyectos\mi_api\md
  DRY-RUN docs/manual_usuario.pdf -> md/docs/manual_usuario.md
  DRY-RUN specs/requisitos.docx -> md/specs/requisitos.md
  DRY-RUN img/diagrama.png -> md/img/diagrama.md

Completado: 3 convertido(s) en md/ (motor: docling)
```

## 6. Re-conversión forzada (--force)

Por defecto, ficheros ya convertidos se omiten. Para forzar re-conversión:

```bash
python scripts/convert_to_md.py C:\proyectos\mi_api --force
```

## 7. Metadata frontmatter (--metadata)

Añade cabecera YAML con origen, motor y fecha:

```bash
python scripts/convert_to_md.py C:\proyectos\mi_api --metadata
```

**Fichero generado**:

```markdown
---
source: "manual_usuario.pdf"
engine: "docling"
engine_version: "2.100.0"
title: "Manual de Usuario"
converted_at: "2026-06-24T10:30:00"
---

# Contenido del documento convertido...
```

## 8. Chunking RAG (--chunk, solo docling)

Genera fragmentos optimizados para pipelines RAG:

```bash
python scripts/convert_to_md.py C:\proyectos\mi_api --chunk --chunk-max-tokens 256
```

**Estructura generada**:

```
md/
  docs/manual_usuario.md
  docs/chunks/manual_usuario/
    001.md
    002.md
    003.md
    _manifest.json
```

## 9. Aceleración GPU (--device cuda)

```bash
python scripts/convert_to_md.py C:\proyectos\mi_api --device cuda
# o autodetección:
python scripts/convert_to_md.py C:\proyectos\mi_api --device auto
```

## 10. Conversión batch (--batch-size, --workers)

Para directorios grandes con docling:

```bash
python scripts/convert_to_md.py C:\proyectos\gran_repo --batch-size 4 --workers 2
```

## 11. Idempotencia

Si un fichero ya existe en `md/`, se omite sin error. Permite re-ejecutar sin duplicar trabajo:

```bash
# Primera ejecución
python scripts/convert_to_md.py C:\proyectos\mi_api --engine markitdown
# → OK manual_usuario.pdf -> md/docs/manual_usuario.md

# Segunda ejecución
python scripts/convert_to_md.py C:\proyectos\mi_api --engine markitdown
# → OMITIR manual_usuario.pdf -> md/docs/manual_usuario.md (ya existe)
```

## 12. Gestión de errores

Ficheros inválidos se detectan en la validación previa. El script continúa con los válidos:

```
Convirtiendo 2 fichero(s) con motor 'docling' -> C:\proyectos\mi_api\md
  INVÁLID docs/corrupto.pdf: cabecera PDF inválida (fichero corrupto)
  CONV    specs/requisitos.docx ... OK -> md/specs/requisitos.md

1 error(es). Revisa la salida anterior.
```

## Uso integrado en /document-project

Cuando el flujo detecta ficheros binarios en el origen (Fase 0b), propone ejecutar este script
antes de inventariar:

```
"Se detectaron 2 ficheros no legibles en el origen:
   docs/manual.pdf · specs/req.docx
Propuesta: python scripts/convert_to_md.py C:\proyectos\mi_api"
```

## Referencias

- [Documentación funcional: convert_to_md](../functional/convert_to_md.md) — objetivo, flujo, comportamiento.
- [Referencia técnica: convert_to_md](../api/convert_to_md.md) — ConvertOptions, funciones, constantes.
- [Verificación de Entorno](check_env_usage.md) — confirmar disponibilidad de motores.
- [Documentar un Proyecto](document_project_usage.md) — contexto de Fase 0b.
