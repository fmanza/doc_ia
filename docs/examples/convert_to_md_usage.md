# Ejemplo: Convertir Documentos a Markdown

Uso de `scripts/convert_to_md.py` para preparar documentación en formatos binarios (PDF, DOCX, PPTX…) como fuente legible para el flujo `/document-project`.

## Precondición

```bash
# Verificar pandoc instalado
pandoc --version

# Si no está instalado:
winget install JohnMacFarlane.Pandoc   # Windows
brew install pandoc                    # macOS
sudo apt install pandoc                # Linux (Debian/Ubuntu)
```

## 1. Convertir un directorio completo

Convierte todos los ficheros convertibles en un directorio y sus subdirectorios.

```bash
python scripts/convert_to_md.py C:\proyectos\mi_api
```

**Resultado esperado**:

```
Convirtiendo 3 fichero(s) → C:\proyectos\mi_api\md
  OK      docs/manual_usuario.pdf → md/docs/manual_usuario.md
  OK      specs/requisitos.docx → md/specs/requisitos.md
  OK      presentacion.pptx → md/presentacion.md

Completado: 3 convertido(s) en md/
```

**Estructura generada** (refleja subdirectorios para evitar colisiones de nombres):

```
mi_api/
  docs/manual_usuario.pdf   →  md/docs/manual_usuario.md
  specs/requisitos.docx     →  md/specs/requisitos.md
  presentacion.pptx         →  md/presentacion.md
```

## 2. Convertir un fichero individual

```bash
python scripts/convert_to_md.py C:\proyectos\mi_api\docs\manual_usuario.pdf
```

**Resultado**:

```
Convirtiendo 1 fichero(s) → C:\proyectos\mi_api\docs\md
  OK      manual_usuario.pdf → md/manual_usuario.md
```

## 3. Vista previa sin ejecutar (--dry-run)

Lista qué se convertiría sin llamar a pandoc. Útil para verificar antes de procesar.

```bash
python scripts/convert_to_md.py C:\proyectos\mi_api --dry-run
```

**Resultado**:

```
Convirtiendo 3 fichero(s) → C:\proyectos\mi_api\md
  DRY-RUN docs/manual_usuario.pdf → md/docs/manual_usuario.md
  DRY-RUN specs/requisitos.docx → md/specs/requisitos.md
  DRY-RUN presentacion.pptx → md/presentacion.md

Completado: 3 convertido(s) en md/
```

## 4. Idempotencia: ficheros ya convertidos

Si un fichero ya existe en `md/`, se omite sin error. Permite re-ejecutar sin duplicar trabajo.

```bash
# Primera ejecución
python scripts/convert_to_md.py C:\proyectos\mi_api
# → OK manual_usuario.pdf → md/docs/manual_usuario.md

# Segunda ejecución (mismo directorio)
python scripts/convert_to_md.py C:\proyectos\mi_api
# → OMITIR manual_usuario.pdf → md/docs/manual_usuario.md (ya existe)
```

## 5. Gestión de errores

Si pandoc falla en un fichero (PDF protegido, formato no compatible), el script continúa con los demás y devuelve `exit 1` al terminar.

```bash
python scripts/convert_to_md.py C:\proyectos\mi_api
```

**Resultado con un fichero corrupto**:

```
Convirtiendo 2 fichero(s) → C:\proyectos\mi_api\md
  ERROR   docs/corrupto.pdf: pandoc: docs/corrupto.pdf: openBinaryFile: does not exist
  OK      specs/requisitos.docx → md/specs/requisitos.md

1 error(s). Revisa la salida de pandoc.
```

```bash
echo $?   # → 1 (error)
```

## Uso integrado en /document-project

Cuando el flujo detecta ficheros binarios en el origen (Fase 0b), propone ejecutar este script antes de inventariar. Los ficheros Markdown generados en `md/` se usan como fuente adicional en las Fases 2–4.

```
# Sugerencia automática de Fase 0b:
"Se detectaron 2 ficheros no legibles en el origen:
   docs/manual.pdf · specs/req.docx
Propuesta: python scripts/convert_to_md.py C:\proyectos\mi_api"
```

## Referencias

- [Referencia técnica: convert_to_md](../api/convert_to_md.md) — funciones, CLI, constantes, errores.
- [Verificación de Entorno](check_env_usage.md) — confirmar que pandoc está disponible.
- [Documentar un Proyecto](document_project_usage.md) — contexto de Fase 0b.
