# Glosario — doc_ia

> Contexto persistente para agentes IA. Regenerado en el bootstrap (2026-06-10).

| Término | Definición |
|---|---|
| **Arquetipo documental** | Plantilla formal de documentación con secciones fijas numeradas. doc_ia define 7 (+1 condicional): Funcional, Técnica/API, Guía, Ejemplos, ADR, Navegación Principal, Onboarding, Trazabilidad Normativa. Ver `.github/DOCUMENTATION_STANDARD.md`. |
| **Proyecto origen** | Proyecto de desarrollo externo que se quiere documentar. Parámetro obligatorio de cada ejecución documental. |
| **Destino de la documentación** | Carpeta o repositorio donde se escribe la documentación generada. Parámetro obligatorio. |
| **Ejecución en chat** | Principio del producto: la generación documental ocurre en el chat de la plataforma IA (Claude Code, Gemini, Copilot, Cursor, Codex), nunca en código que invoque APIs. |
| **Tooling determinista** | Código Python de `scripts/` sin dependencias de servicios IA: mismo input → mismo output, validable en CI. |
| **Flujo canónico** | Ciclo `PLAN → AUDIT_PLAN → IMPLEMENT → AUDIT_CODE → VERSION` que estructura cualquier cambio no trivial. |
| **Bootstrap (modelo PULL)** | Traslado del sistema de instrucciones IA a otro proyecto, invocado **desde el destino** con el origen como plantilla de solo lectura. Ver `bootstrap_ai_config.prompt.md`. |
| **Capas A/B/C/D** | Clasificación de activos en el bootstrap: A metodología (verbatim), B especialización (reescribir dominio), C contexto (regenerar), D excluir. |
| **Entry point** | Fichero de instrucciones específico de una plataforma IA (`CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `copilot-instructions.md`); siempre subordinado al canónico `SHARED_INSTRUCTIONS.md`. |
| **Canónico** | `.github/SHARED_INSTRUCTIONS.md`: fuente única de reglas comunes; los entry points solo añaden especialización (regla DRY). |
| **ZIP offline** | Paquete distribuible del sitio de docs (`dist/doc_ia-docs-{version}.zip`) con checksum SHA256, generado por `scripts/build_docs_zip.py`. |
| **Enlace bidireccional** | Obligación de los arquetipos 2 (Técnica §5) y 4 (Ejemplos §5) de enlazarse mutuamente. |
| **Dogfooding** | El sitio `docs/` de doc_ia se genera aplicando sus propios arquetipos. |
| **Sesión** | Unidad de trabajo registrada en `.ai/sessions/<fecha>/` con REQUEST, CONTEXT_SNAPSHOT y TRACEABILITY (plantilla en `.ai/sessions/TEMPLATE/`). |
| **Directrices para Futuras IAs** | Sección obligatoria del TRACEABILITY.md al cerrar sesión: hechos verificables que evitan repetir análisis. |
