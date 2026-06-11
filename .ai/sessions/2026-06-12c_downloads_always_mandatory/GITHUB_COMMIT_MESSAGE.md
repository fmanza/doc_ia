# Commit — doc_ia (rama develop)

```
fix(agents): downloads.md siempre obligatorio — Variante A/B según presencia de ZIP script

RCA: DOCUMENTATION_STANDARD.md §4.1 marcaba downloads.md como condicional; los agentes
lo omitían en proyectos sin build_docs_zip.py (observado en socyalpro).

Cambios:
- document_project.prompt.md: Fase 1 (TIENE_ZIP_SCRIPT) + Fase 7b reescrita (A/B siempre)
- documentation-generator.agent.md: Fase 4 — downloads.md SIEMPRE obligatorio
- DOCUMENTATION_STANDARD.md: §4.1 nav comentario + §3.9 tabla guías adicionales
- .ai/sessions/2026-06-12c_downloads_always_mandatory/ (trazabilidad)
```

---

# Commit — socyalpro (repositorio aparte)

```
docs(downloads): añadir página de descargas offline (Variante B)

Página downloads.md ausente en la documentación generada; añadida con
instrucciones de build local + tabla placeholder para futura publicación
automática. Entrada añadida en mkdocs.yml nav.
```
