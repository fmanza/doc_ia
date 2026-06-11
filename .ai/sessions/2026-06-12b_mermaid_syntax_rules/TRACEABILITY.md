# TRACEABILITY

## Session metadata
- id: 2026-06-12b_mermaid_syntax_rules
- fecha: 2026-06-12
- rama: develop
- skill: hotfix
- fase: RCA → FIX (socyalpro) → AGENT UPDATE (doc_ia)

## Prompt issued

```
mermaid.min.js:894 Uncaught (in promise) Error: Parse error on line 14
[...tras fix...] Parse error on line 24
```

## Context supplied

- Bloques `mermaid` de los 7 ficheros con diagramas en `C:\Desarrollo\Proyectos\socyalpro\docs\`
- `c:\Desarrollo\python\libs\doc_ia\.github\agents\documentation-generator.agent.md`
- `c:\Desarrollo\python\libs\doc_ia\.github\prompts\document_project.prompt.md`

## AI output summary

1. Escaneó los 7 ficheros con bloques mermaid; contó líneas para localizar línea 14 → `architecture.md`
   `INT[socyalpro-integration<br/>Cl@ve · Firma · SIUSS]`: `@` en label de nodo
2. Buscó `Cl@ve` en todos los docs → encontró 3 ocurrencias dentro de bloques mermaid:
   `docs/index.md:34`, `docs/architecture.md:21`, `docs/api/integrations.md:10-11`
3. Corrigió `@` → `&#64;` en los 3 ficheros (incluyendo `@firma` → `&#64;firma` en integrations.md)
4. Segundo error (línea 24): `subgraph BD[(Base de datos)]` en `architecture.md:31` —
   `[(…)]` es notación de nodo cilíndrico, inválida en declaraciones `subgraph`
5. Buscó globalmente `subgraph\s+\w*\[` → solo 1 ocurrencia; corregido a `subgraph BD[Base de datos]`
6. Añadió reglas explícitas a `documentation-generator.agent.md` y `document_project.prompt.md`:
   - Caracteres prohibidos en labels: `@` → `&#64;`, `#` → `&#35;`
   - `subgraph id[(título)]` prohibido; usar `subgraph id[título]`

## Artefactos generados

| Artefacto | Ruta | Estado |
|---|---|---|
| index.md | `C:\Desarrollo\Proyectos\socyalpro\docs\index.md` | corregido (Cl@ve → Cl&#64;ve) |
| architecture.md | `C:\Desarrollo\Proyectos\socyalpro\docs\architecture.md` | corregido (Cl@ve + subgraph BD) |
| integrations.md | `C:\Desarrollo\Proyectos\socyalpro\docs\api\integrations.md` | corregido (Cl@ve + @firma) |
| documentation-generator.agent.md | `.github/agents/documentation-generator.agent.md` | actualizado |
| document_project.prompt.md | `.github/prompts/document_project.prompt.md` | actualizado |
| 00_REQUEST.md | `.ai/sessions/2026-06-12b_mermaid_syntax_rules/00_REQUEST.md` | creado |
| TRACEABILITY.md | `.ai/sessions/2026-06-12b_mermaid_syntax_rules/TRACEABILITY.md` | creado |

## Directrices para Futuras IAs

- **[mermaid @]**: `@` dentro de labels de nodo Mermaid (`[...]`, `(...)`) causa parse error en
  Mermaid 11. El build `--strict` de MkDocs NO lo detecta. Siempre sustituir `@` → `&#64;`
  dentro de bloques ` ```mermaid ``` `.
- **[mermaid subgraph]**: `subgraph id[(título)]` causa parse error. La notación `[(…)]` solo
  es válida para nodos (cilindro/BD). En `subgraph` usar solo `subgraph título` o `subgraph id[título]`.
- **[incremental errors]**: Mermaid para en el primer error por bloque. Corrección de la línea 14
  no eliminó el error; aparece uno nuevo en línea 24. Escanear el bloque COMPLETO antes de declarar OK.

## Veredicto final

Veredicto: CLOSED  
Pendientes al cierre:
- Recargar el site de socyalpro y verificar que todos los diagramas renderizan sin errores de consola
