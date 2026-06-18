# REQUEST — Sesión 2026-06-18

## Objetivo

Dogfooding: revisar documentación de doc_ia contra las instrucciones IA actuales y actualizar
todo lo desactualizado. Profundizar para disponer de la mayor información posible.

## Inputs

| Parámetro | Valor |
|---|---|
| Origen(es) | `C:\Desarrollo\python\libs\doc_ia` |
| Destino | `C:\Desarrollo\python\libs\doc_ia\docs` |
| Generador | mkdocs-material |
| Idioma | es |
| Alcance | Proyecto completo + instrucciones IA |
| Verificación | `--verify-build` (ejecutado) |

## Restricciones

- No crear páginas nuevas; solo actualizar las desactualizadas
- Conservar verbatim las secciones vigentes (estado C)
- No modificar código fuente; solo documentación y contexto .ai/
