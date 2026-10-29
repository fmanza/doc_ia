# PLAN + AUDIT_PLAN + AUDIT_CODE — Modo incremental de `/document-project`

## PLAN (aprobado: D1-D4 recomendadas)
CIERRE → `doc_trace.py baseline` guarda el commit de cada origen CÓDIGO en
`<destino>/.ai/doc_state.json`. Fase 1 siguiente → `doc_trace.py changes`: `git diff` desde ese
commit (más pendientes y sin seguimiento) → páginas que citan cada fichero → solo eso se
inventaría; el resto queda en C sin leerse. Código 3 → modo completo.

| Fase | Ficheros | Estado |
|---|---|---|
| F1 Herramienta | `scripts/doc_trace.py` (`baseline`, `changes`, `OriginChange`, `OriginBaseline`, `ChangeReport`), `tests/test_doc_trace.py` (+9 funciones, 12 casos con git real) | ✅ |
| F2 Producto | prompt (parámetro `Modo`, Fase 1 incremental, INVENTARIO, CIERRE con baseline), comando, agente, `SHARED_INSTRUCTIONS.md`, plantilla `00_CONTEXT_SNAPSHOT.md` | ✅ |
| F3 Guardas y docs | `test_incremental_mode_rule_everywhere` (4); `docs/{functional,api,examples}/doc_trace.md` (AC-15..AC-21, 2.º diagrama), `docs/reference/index.md`, `docs/{functional,api}/document_project.md` (AC-12), mapa funcional; `.ai/{product,glossary}.md`, EDGE_CASES ×2, CHANGELOG; 9 páginas re-selladas | ✅ |

## AUDIT_PLAN — condiciones
| ID | Riesgo | Resolución |
|---|---|---|
| A1 | Cambios en ficheros sin cita | «Ficheros sin página» siempre listados; Fase 1 los clasifica (A o B de un módulo; Arq. 3/6/7 si cambia entrada o dependencias) |
| A2 | Baseline con árbol sucio | `changes` compara con el árbol de trabajo (`git diff <base>` sin `..HEAD`): lo pendiente se re-revisa; `baseline` avisa |
| A3 | Cambios de metodología | Versión de doc_ia en el estado; versión menor distinta → código 3 |
| A4 | Renombrados/borrados | `R` con ruta anterior; cuentan citas de ambas rutas; `D` cita colgante → B |
| A5 | Historial reescrito / clon superficial | `git cat-file -e <base>^{commit}` → código 3 |
| A6 | Orígenes con el mismo nombre | `--name` con la regla de `_fuentes/`; estado por clave |
| A7 | Rutas Windows/POSIX y subcarpetas | `git diff --relative -z`; citas en POSIX; test de subcarpeta y de «ñ» |
| A8 | `subprocess` | Lista sin shell, `-C`, timeout 60 s; git ausente → `None` |
| A9 | Drift CI | 9 páginas revisadas y re-selladas |

## AUDIT_CODE — GO
| ID | Hallazgo | Resolución |
|---|---|---|
| C1 | Probado sobre el historial real de doc_ia: 27 páginas «a revisar» por menciones en prosa (ADR, changelog, guías) | Citas (frontmatter + «Evidencia») separadas de menciones: 10 páginas, exactamente las revisadas en la feature anterior |
| C2 | Código 2 previsto en el PLAN choca con los errores de uso de argparse | `changes` usa **3** para «modo completo» (desviación del PLAN, documentada en referencia y API) |
| C3 | Destino dentro del origen: el commit del CIERRE sería «cambio» y `sucio` siempre true | `documentation_paths` + `DOC_ARTIFACTS` en `changes` y en `sucio`; test dedicado |
| C4 | Restos de sesiones previas: mapa funcional «52 de 75» (real 56/81 antes, 63/89 ahora), evidencias 8/9, 10/10, 0/10; referencia de `start-server.py` aún «excepción no capturada 🔍» | Corregidos con los valores de `doc_trace matrix`; fila y evidencia de `start-server.py` ✅ |
| C5 | Diagrama Mermaid nuevo sin validar en local (`mmdc` no instalado) | 12 nodos (límite §3.17), etiquetas especiales entre comillas, tests de conformidad verdes; lo valida el job `mermaid` de CI al hacer push |
| C6 | `ls-files --others` incluye cualquier fichero no ignorado del origen | Aparece en «Ficheros sin página»; el agente lo clasifica. Depende del `.gitignore` del origen |
| C7 | AC-12 (flujo en el chat) sin test automatizado | ⚠️ en la Evidencia; la coherencia de instrucciones sí tiene test |
| C8 | Sin cubrir por tests: timeout de git y `changes --output` | Riesgo bajo; anotado |

Verificado: ruff ✅ · mypy ✅ · pytest 241 ✅ · `mkdocs build --strict` ✅ · `doc_trace drift/llms/matrix` ✅ ·
ejemplo real (`mi_api` → `mi_api_docs`) con salida capturada en `docs/examples/doc_trace_usage.md`.

## Pendiente
- Sin commit hasta indicación del usuario.
- Primera ejecución real de `/document-project` en modo incremental sobre un destino externo.
