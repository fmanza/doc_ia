# ADR-001: MkDocs Material como generador por defecto

## 1. Contexto y Problema

doc_ia se creó mediante bootstrap desde util_bbdd, cuyo generador por defecto era
**Zensical**. doc_ia necesita un generador estático para su propio sitio y como
recomendación por defecto al documentar proyectos origen. Mantener Zensical como
defecto implicaba una dependencia adicional no declarada en `requirements.txt` y un
ecosistema de plugins más joven.

## 2. Decisión

**MkDocs + Material for MkDocs es el generador por defecto** de doc_ia. Zensical queda
como alternativa **recíprocamente compatible** sobre el mismo `mkdocs.yml`, disponible
vía `python scripts/build_docs_zip.py --builder zensical`, pero no es dependencia del
proyecto. `mkdocs.yml` es la fuente única de configuración (no existe `zensical.toml`).

## 3. Consecuencias

- Ventajas: una sola dependencia documental (`mkdocs-material` en `requirements.txt`),
  ecosistema maduro (snippets, superfences/Mermaid, búsqueda), build estricto estable
  en CI y en `build_docs_zip.py`.
- Compromisos: el flag `--builder zensical` se mantiene sin test de integración (Zensical
  no está instalado); deuda aceptada hasta que haya un caso de uso real.

## 4. Alternativas Consideradas

| Alternativa | Pros | Contras | Motivo de rechazo |
|---|---|---|---|
| Zensical por defecto (como el origen) | Continuidad con util_bbdd | Dependencia extra; ecosistema más joven | doc_ia no hereda las necesidades del origen |
| Doble configuración (mkdocs.yml + zensical.toml) | Soporte explícito de ambos | Dos fuentes de verdad que divergen | Viola la regla de fuente única |
| Sphinx | Potente para API Python | Stack reST distinto; rompe los arquetipos Markdown/Mermaid | Incompatible con el estándar documental |

## 5. Estado y Revisión

Estado: **ACEPTADO**
Fecha de última revisión: 2026-06-10
