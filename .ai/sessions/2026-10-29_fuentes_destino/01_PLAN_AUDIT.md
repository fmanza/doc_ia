# PLAN + AUDIT_PLAN — Carpeta canónica de fuentes convertidas en el destino

## Regla propuesta (R)
1. **Nombre único**: `_fuentes/` (D1) en la **raíz del destino** = carpeta que contiene
   `mkdocs.yml`/`zensical.toml` (la misma raíz que ya usan `.gitignore` y `.ai/`; `{destino}/..`
   cuando el destino es `docs/`). Siempre fuera de `docs_dir`.
2. **Estructura**: `_fuentes/<nombre_origen>/<ruta relativa al origen, verbatim>` (D3).
   `<nombre_origen>` = nombre de la carpeta raíz del origen; si dos orígenes comparten nombre,
   se añade el padre (`<padre>_<nombre>`). Ej.: `Legales/md/CA/ley.md` →
   `_fuentes/doc_referencia/Legales/md/CA/ley.md`.
3. **Qué se copia**: los `.md` de toda carpeta `md/` válida del origen (Paso 0) y las imágenes
   que referencian (`--image-export referenced`). **No** se copian binarios ni chunks RAG.
4. **Cuándo**: Fase 0c, paso nuevo tras la conversión y antes de la Fase 1, en toda sesión con
   contenido en `md/` (D2: también si origen y destino son el mismo repositorio).
5. **Idempotencia**: copiar si falta o si el contenido difiere (hash); nunca editar a mano;
   huérfanos (en `_fuentes/` sin equivalente en el origen) → se listan en INVENTARIO y solo se
   borran con confirmación.
6. **Contexto**: Fases 2-4 leen de `_fuentes/` (copia en el repositorio destino). La evidencia
   (§3.16) y el frontmatter `fuentes:` de `doc_trace` pueden apuntar a `_fuentes/...`.
7. **Migración** de destinos con nombres no canónicos (`.fuentes/`, `fuentes/` en la raíz; `md/` retirado en AUDIT_CODE):
   detectar en INVENTARIO → confirmar → `git mv` a `_fuentes/` (si conviven, fusionar por hash;
   conflicto → DETENER) → reescribir referencias en `docs/**/*.md` y frontmatter `fuentes:` →
   `doc_trace stamp --root <raíz destino>` de las páginas tocadas.
8. **Git**: `_fuentes/` nunca en `.gitignore`; entra en el commit del CIERRE (`git add _fuentes/`).

## Decisiones (pendientes de confirmar)
| ID | Decisión | Recomendada | Motivo |
|---|---|---|---|
| D1 | Nombre | `_fuentes/` | `.fuentes/` es oculta: ripgrep/Grep y `ls` la saltan por defecto → el agente pierde ese contexto en Fases 2-4. `fuentes/` no indica «generado». `_` es visible, se ordena primero y marca artefacto. |
| D2 | Origen = destino (mismo repo) | Copiar igualmente | Regla sin excepciones («siempre»); coste: duplicado de texto. |
| D3 | Ruta interna | Verbatim (con `md/`) | Determinista y reversible al fichero original; sin colisiones. |

## Impacto
| Área | Impacto |
|---|---|
| `convert_to_md.py` y sus tests | Ninguno (sigue escribiendo en `<origen>/md/`). |
| Build MkDocs/Zensical, `--strict`, ZIP offline | Ninguno: `_fuentes/` está fuera de `docs_dir`, no se publica. |
| Trazabilidad (`doc_trace`) | **Positivo**: hoy una fuente fuera del repo destino da `outside_repo`; con `_fuentes/` dentro, el drift detecta cambios en normativa/especificación. |
| Destinos existentes con `.fuentes/`/`_fuentes/` | Migración única (regla 7); enlaces y evidencias a la ruta vieja se rompen si no se reescriben. |
| Tamaño del repo destino | Texto: bajo. Imágenes referenciadas: medio; chunks excluidos. |
| Confidencialidad | El **texto** de documentos de terceros (REFERENCIA/NORMATIVA) pasa a versionarse en el destino (los binarios siguen ignorados). Riesgo aceptado por «siempre»; se avisa en INVENTARIO. |
| Coherencia interna | El motivo de `*.pdf`/`*.doc`/`*.docx` en `.gitignore` («nunca deben entrar en el repositorio») contradice la regla si no se reescribe. |
| CI de doc_ia | `drift` es bloqueante: editar prompt/comando/agente deja **stale** 5 páginas selladas → re-sellar tras revisión. |

## Fases
| Fase | Ficheros | Contenido |
|---|---|---|
| F1 Producto | `.github/prompts/document_project.prompt.md`, `.claude/commands/document-project.md`, `.github/agents/documentation-generator.agent.md`, `.github/SHARED_INSTRUCTIONS.md` (fila `<origen>/md/`), `.github/DOCUMENTATION_STANDARD.md` §3.16 (una línea), `.ai/sessions/TEMPLATE/00_CONTEXT_SNAPSHOT.md` | Regla R1-R8: paso nuevo en Fase 0c, Fase 1 (INVENTARIO: sincronizados/huérfanos/migración), Fase 0b (`.gitignore` + motivo reescrito), CIERRE (commit). |
| F2 Guardas | `tests/test_docs_conformance.py` (o `tests/test_sources_folder.py`), `.claude/EDGE_CASES.md` | Test sin red: `_fuentes/` presente en prompt, comando, agente y SHARED; `.fuentes/` solo dentro de la regla de migración. Caso real `.fuentes/` vs `_fuentes/` registrado. |
| F3 Docs y contexto | `docs/functional/document_project.md` (+AC), `docs/functional/origin_types.md`, `docs/api/document_project.md`, `docs/functional/convert_to_md.md` (nota: la copia la hace el flujo, no el script), `.ai/{glossary,product,standards}.md`, `CHANGELOG.md` | Documentación del cambio; `doc_trace stamp` de las páginas selladas; `drift` = 0. |

DoD: ruff + mypy + pytest verdes; `python -m mkdocs build --strict`; `doc_trace.py drift` sin hallazgos.

## AUDIT_PLAN — GO_CONDICIONAL
| ID | Hallazgo | Severidad | Condición |
|---|---|---|---|
| A1 | D1-D3 sin confirmar | Bloqueante | Confirmación del usuario antes de F1. |
| A2 | Contradicción con el motivo del `.gitignore` | Alta | F1 reescribe el párrafo: los binarios no se versionan; su texto convertido sí, en `_fuentes/`. |
| A3 | Paso 0 solo busca `md/` en el origen | Media | Re-ejecuciones: Paso 0 también detecta `_fuentes/` existente para no recopiar y para reportar huérfanos. |
| A4 | El borrado de huérfanos o la fusión en la migración pueden perder contenido | Media | Nunca borrar ni sobrescribir sin confirmación; conflicto de hash en fusión → DETENER. |
| A5 | Drift CI bloqueante | Media | F3 incluye `stamp` + `drift` en el DoD. |
| A6 | Riesgo de que el agente vuelva a improvisar | Media | Test de coherencia (F2) + nombre literal (no descriptivo) en los 4 ficheros de instrucciones. |
| A7 | Fase 0c del prompt desfasada respecto a `convert_to_md.py` (docling es el motor por defecto; el prompt dice «markitdown principal») | Baja, fuera de alcance | Registrar como pendiente; no mezclar en este cambio. |

F1-F3 sin dependencias nuevas ni cambios en código Python de producción. Riesgo residual:
confidencialidad del texto de terceros versionado en el destino (aceptado por el requisito «siempre»).

## AUDIT_CODE — GO
| ID | Hallazgo | Resolución |
|---|---|---|
| C1 | La lista de nombres a migrar incluía `md/` en la raíz del destino: con origen = destino es la salida legítima de `convert_to_md.py` y la regla la habría movido | Retirado `md/` de las 8 apariciones (prompt ×3, comando, agente, 2 páginas, glosario, EDGE_CASES) |
| C2 | Renumeración de la Fase 0c (Paso 6 → 7) | Única referencia cruzada («se registran (Paso 7)») actualizada; «Paso 5» de Paso 0 sigue siendo correcto |
| C3 | El test solo comprueba coherencia de instrucciones, no el comportamiento del flujo | Declarado como ⚠️ en la Evidencia de `functional/document_project.md`; AC-09/AC-10 «Sin test» |

Condiciones del AUDIT_PLAN: A1 ✅ (confirmado), A2 ✅ (motivo del `.gitignore` reescrito en el comando),
A3 ✅ (Paso 0 busca `_fuentes/` en el destino), A4 ✅, A5 ✅, A6 ✅, A7 queda pendiente fuera de alcance.
