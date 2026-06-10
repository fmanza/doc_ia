# Ejemplo: Documentar un Proyecto con /document-project

## 1. Contexto del Ejemplo

Cuando tienes un proyecto Python existente sin documentación (o con documentación
desactualizada), el comando `/document-project` cubre el ciclo completo desde el
inventario hasta la publicación del sitio: detecta qué módulos necesitan documentación
nueva, qué páginas están desactualizadas y cuáles siguen vigentes, y genera los
documentos siguiendo los arquetipos formales sin sobrescribir lo que ya es correcto.

Este ejemplo muestra dos escenarios: documentar un proyecto **desde cero** (estado A)
y actualizar la documentación de un proyecto **parcialmente documentado** (estados A+B).

## 2. Implementación de Referencia

Invocación desde Claude Code (código inline — el flujo ocurre en el chat, no en Python):

**Escenario 1 — Proyecto sin documentación previa**

```
/document-project

Origen:    c:\Desarrollo\python\libs\mi_libreria
Destino:   c:\Desarrollo\python\libs\mi_libreria\docs
Generador: mkdocs-material
Idioma:    es
```

**Escenario 2 — Actualización parcial (restringir a un módulo)**

```
/document-project

Origen:    c:\Desarrollo\python\libs\mi_libreria
Destino:   c:\Desarrollo\python\libs\mi_libreria\docs
Generador: mkdocs-material
Idioma:    es
Alcance:   scripts/conversor.py  (solo este módulo)
```

**Escenario 3 — Incluir verificación de build al final**

```
/document-project

Origen:    c:\Desarrollo\python\libs\mi_libreria
Destino:   c:\Desarrollo\python\libs\mi_libreria\docs
Generador: mkdocs-material
Idioma:    es
Flags:     --verify-build
```

## 3. Explicación del Código

- Los cuatro parámetros (`Origen`, `Destino`, `Generador`, `Idioma`) son **obligatorios**.
  Si falta alguno, el flujo se detiene antes del inventario y pide que se complete.
- `Alcance` es opcional: restringe el inventario a un subconjunto de módulos o arquetipos.
  Sin él, se inventarían todos los módulos detectados en `Origen`.
- `--verify-build` ejecuta `python -m mkdocs build --strict` al final de la sesión y
  reporta errores de compilación (enlaces rotos, snippets faltantes, Mermaid inválido).
- La generación ocurre **en el chat**, no en componentes programáticos: ningun paso
  llama a APIs de IA externas ni ejecuta Python para generar el texto de los documentos.

## 4. Ejecución y Pruebas

**Fase VALIDACIÓN** — el agente confirma los cuatro parámetros antes de continuar:

```
✔ Origen:    c:\Desarrollo\python\libs\mi_libreria  (accesible)
✔ Destino:   c:\Desarrollo\python\libs\mi_libreria\docs
✔ Generador: mkdocs-material
✔ Idioma:    es
```

**Fase INVENTARIO** — clasifica cada módulo en A / B / C:

```
INVENTARIO
  scripts/parser.py       → A  (sin página en docs/)
  scripts/conversor.py    → A  (sin página en docs/)
  scripts/validador.py    → B  (docs/api/validador.md desactualizado: firma cambiada)
  scripts/utils.py        → C  (docs/api/utils.md vigente — omitir)
```

**Fase PLAN_DOC** — acción derivada por módulo:

```
PLAN_DOC
  CREAR    docs/functional/parser.md
  CREAR    docs/api/parser.md
  CREAR    docs/examples/parser_usage.md
  CREAR    docs/functional/conversor.md
  CREAR    docs/api/conversor.md
  CREAR    docs/examples/conversor_usage.md
  ACTUALIZAR  docs/api/validador.md  (§2 Modelo de Datos — firma parse_entry)
  OMITIR   docs/api/utils.md
```

**Fase GENERACIÓN** — el agente escribe cada archivo respetando el arquetipo asignado.

**Fase SYNC NAV** — actualiza `mkdocs.yml` con las entradas nuevas y modificadas.

**Fase REVISIÓN** — comprueba Markdown, enlaces relativos y sintaxis Mermaid.

**Fase RESUMEN**:

```
RESUMEN
  Creados:      6 archivos nuevos (2 funcional, 2 técnica, 2 ejemplos)
  Actualizados: 1 archivo (api/validador.md §2)
  Omitidos:     1 archivo vigente (api/utils.md)
  mkdocs.yml:   sincronizado (3 entradas añadidas)
  Build:        no ejecutado (omitir --verify-build para activar)
```

Con `--verify-build`, la fase final ejecuta el build estricto:

```bash
python -m mkdocs build --strict
# INFO - Documentation built in X.Xs
# ✔ Build completado sin errores
```

## 5. Referencias Relacionadas

- Documentación funcional: [Documentar un Proyecto](../functional/document_project.md)
- Arquetipos formales: [Arquetipos Formales](../functional/archetypes.md)
- Ejemplos relacionados: [Verificar Entorno](check_env_usage.md), [Generar ZIP Offline](build_docs_zip_offline.md)
