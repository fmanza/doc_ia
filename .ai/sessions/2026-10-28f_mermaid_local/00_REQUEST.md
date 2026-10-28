# REQUEST

## Session metadata
- id: 2026-10-28f
- fecha: 2026-10-28
- rama: develop
- skill: new_feature
- fase solicitada: IMPLEMENT completo (L1–L3) tras PLAN + AUDIT_PLAN aprobados ("GO entero")

## Solicitud original saneada
1. "Dime F10, que sigue esperando a la fase F8, el motivo"
2. "No entiendo, no salen ahora los Mermaid si lo ejecuto"
3. Propuesta aceptada: Mermaid en local como fase independiente de F8. "PLAN de esa fase".
4. "GO entero."

## Decisiones del usuario (AskUserQuestion)
- Versión: 12.2.0.
- Alcance: doc_ia + producto (Fase 0b).
- Obtención: commit del fichero + test de versión.

## Objetivo operativo de esta sesión
- Los diagramas del sitio y del ZIP offline se dibujan sin conexión, con la misma versión exacta
  en MkDocs Material y Zensical.
- El producto (`/document-project`, Fase 0b) lleva Mermaid local a los destinos.
- Un test sin red mantiene coherentes fichero, `mkdocs.yml`, plantilla y CI.

## Restricciones explícitas
- Sin dependencias Python nuevas; tests sin red.
- Sin push ni tag.

## Resultado esperado
- Commits L1, L2, L3 en `develop` con DoD verde; TRACEABILITY e INDEX.
