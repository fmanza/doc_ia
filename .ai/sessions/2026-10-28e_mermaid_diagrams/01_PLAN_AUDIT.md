# PLAN + AUDIT_PLAN — Diagramas Mermaid

## Hallazgos de partida (análisis verificado)

- `&#40;` / `&#64;` en etiquetas se pintan con un `&` sobrante (`on_post_build&(config&)`),
  verificado renderizando con mermaid@11 y mermaid@12 en Edge headless. Mermaid usa `#64;`
  (sin `&`); la alternativa limpia es la etiqueta entre comillas `["Cl@ve"]`.
- `@` en `[...]` sin comillas sí es parse error en v11 y v12 (diagnóstico de 2026-06-12b correcto,
  remedio incorrecto).
- `\n` y `<br/>` funcionan los dos en v11 y v12; solo `<br/>` está documentado.
- Material 9.8.0 carga `unpkg.com/mermaid@11`; Zensical 0.0.73 carga `unpkg.com/mermaid@12`
  (v12: layout ELK, look `neo` por defecto en flowchart). Versión flotante y con red.
- Material solo aplica colores del tema a flowchart, sequence, class, state y ER.
- 8 de 23 diagramas superan 12 nodos; el flujo de document_project está dibujado 3 veces y
  el de convert_to_md 2 veces; ningún diagrama usa `accTitle`/`accDescr`.

## D1 — Fuente única

`docs.instructions.md` es Capa C en el bootstrap (se regenera, no se copia). Las reglas de
diagramas pasan a `DOCUMENTATION_STANDARD.md` §3.17 (Capa B); el resto de ficheros remiten.
El agente generador (Capa A) conserva un recordatorio de las reglas de sintaxis que rompen el render.

## Fases

| Fase | Contenido |
|---|---|
| M0 | Regla de comillas (prohibido `&#NN;`) en agente y prompt; `build_docs_zip.md:47`; tests `no_html_entities` y `special_chars_quoted`; EDGE_CASES |
| M1 | §3.17 en el estándar; el resto de ficheros remiten (docs.instructions, prompts de arquetipo, revisión) |
| M2 | `accTitle`/`accDescr` en los 23 diagramas, `\n` → `<br/>`, flechas etiquetadas en contexto; test de accesibilidad |
| M3 | Rediseño de 9 diagramas (grandes o duplicados) + test de ≤12 nodos + criterios AC |
| M4 | Job `mermaid` en CI con mermaid-cli (spike previo de código de salida) |
| M5 | Anexo a F10: Mermaid fijado y servido en local; EDGE_CASES divergencia 11/12 |
| Cierre | CHANGELOG `[Unreleased]`, TRACEABILITY, INDEX |

Simplificación aplicada: sin test para `<br/>` (ambas formas funcionan); solo se normaliza.

DoD por fase: ruff, format, mypy, pytest, `doc_trace drift` = 0, `matrix`, build `--strict`
con MkDocs y con Zensical; M0, M2 y M3 además verificación visual (render real v11/v12).

## AUDIT_PLAN — Veredicto GO_CONDICIONAL

| Fase | Veredicto | Condición |
|---|---|---|
| M0, M1, M5 | GO | — |
| M2 | GO_CONDICIONAL | C1: `accTitle`/`accDescr` renderizan en v11 y v12 para los tipos usados |
| M3 | GO_CONDICIONAL | C2: cada diagrama contrastado con su fuente; C3: render sin errores |
| M4 | GO_CONDICIONAL | C4: `mmdc` devuelve código ≠ 0 ante error de sintaxis |

Riesgos principales: contador de nodos heurístico (fixtures), mermaid-cli no detecta el `&`
(lo cubren los tests estáticos), drift de páginas selladas (re-sellado tras revisión),
cadena de suministro npm en CI (versión exacta, `contents: read`).
