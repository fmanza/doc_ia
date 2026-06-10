# TRACEABILITY

## Session metadata
- id: 2026-06-10e
- fecha: 2026-06-10
- rama: main
- skill: refactor documental (Arquetipo 1 §4: placeholder QA → sección ejecutable)
- fase: IMPLEMENT + AUDIT_CODE + VERSION

## Prompt issued
"Cambiar el placeholder de las secciones '4. Criterios de Aceptación' de las páginas
funcionales como parte a ejecutar"

## Análisis
Existía una contradicción interna detectada al aplicar el cambio:
- `functional_doc.prompt.md` §7 (núcleo compartido, no editable) ya trataba los criterios
  como **derivables del código** (Given/When/Then) con el placeholder QA solo como fallback.
- `DOCUMENTATION_STANDARD.md` Arq 1 §4 imponía "PENDIENTE QA — placeholder hasta validación".
Las páginas del dogfooding siguieron al estándar. Resolución: alinear el estándar con el
prompt (el prompt manda; no se modifica su núcleo).

## AI output summary
- DOCUMENTATION_STANDARD.md Arq 1 §4: "← EJECUTABLE — derivar del código real"; tabla
  | ID | Dado | Cuando | Entonces | + comando de verificación; subsección "Pendiente de
  validación QA" solo como fallback para criterios no derivables.
- docs/functional/check_env.md §4: 3 criterios derivados del código (entorno completo →
  código 0; herramienta ausente → lista + código 1; conjunto alternativo → orden preservado)
  con comandos de verificación reales.
- docs/functional/build_docs_zip.md §4: 4 criterios (empaquetado estándar; --no-build sin
  site/ → exit 1; build estricto con error → sin ZIP; validación sha256sum -c).
- mkdocs build --strict: OK sin warnings.

## Directrices para Futuras IAs
- **[criterios-aceptacion]**: §4 del Arquetipo 1 es ejecutable — derivar los criterios del
  código en formato | ID | Dado | Cuando | Entonces | y cerrar con el comando de verificación;
  el placeholder QA es solo fallback para criterios no derivables.

## Veredicto final
Veredicto: CLOSED
Pendientes al cierre: ninguno nuevo (heredados: Flujos IA funcional, CHANGELOG.md).
