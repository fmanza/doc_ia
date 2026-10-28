# Glosario — doc_ia

> Contexto persistente para agentes IA. Actualizado: 2026-06-18.

| Término | Definición |
|---|---|
| **Arquetipo documental** | Plantilla formal de documentación con secciones fijas numeradas. doc_ia define 12: Funcional (1), Técnica/API (2), How-to (3a), Tutorial (3b), Ejemplos (4), ADR/MADR 4.0 (5), Navegación Principal (6, 4 variantes), Onboarding (7), Trazabilidad Normativa (8, condicional), Changelog (9, opt-in), Config IA (10), Contribución (11, opt-in), Referencia del Sistema (12, condicional). Ver `.github/DOCUMENTATION_STANDARD.md`. |
| **Proyecto origen** | Proyecto de desarrollo externo que se quiere documentar. Parámetro obligatorio de cada ejecución documental. |
| **Destino de la documentación** | Carpeta o repositorio donde se escribe la documentación generada. Parámetro obligatorio. |
| **Tipo de origen** | Naturaleza del origen que determina su tratamiento documental. 8 tipos: `CÓDIGO`, `NORMATIVA`, `ESPECIFICACIÓN`, `UI/PANTALLAS`, `REFERENCIA`, `CONTRATO`, `INFRAESTRUCTURA`, `MANUAL`. Los tipos no-CÓDIGO se agrupan como MATERIAL. |
| **Bloque Evidencia** | Bloque plegable `??? note "Evidencia"` sin número de sección que cierra las páginas de los Arquetipos 1, 2 y 12. Tabla `Elemento \| Fuente \| Confianza` con citas `ruta::símbolo` en código inline. Ver `DOCUMENTATION_STANDARD.md` §3.16. |
| **Leyenda de confianza** | ✅ verificado · ⚠️ parcial · 🔍 inferido · ❌ gap. Nacida en el Arquetipo 8 y generalizada a todos los arquetipos en 2026-10-28. ✅ es implícito en el cuerpo de la página. |
| **MATERIAL** | Término colectivo para orígenes no-CÓDIGO. Su contenido enriquece secciones de los arquetipos del proyecto CÓDIGO principal sin generar páginas propias. |
| **CONTRATO** | Tipo de origen: especificaciones machine-readable del proyecto (OpenAPI, AsyncAPI, GraphQL, Protobuf, SQL DDL, DBML). Enriquece Arquetipo 2 §1 y §2. |
| **INFRAESTRUCTURA** | Tipo de origen: artefactos IaC y de despliegue (Terraform, Kubernetes, Docker, Ansible). Enriquece Arquetipo 2 §4 y Arquetipo 6D. |
| **MANUAL** | Tipo de origen: documentación narrativa del propio proyecto (manuales, guías, runbooks). Enriquece Arquetipos 3a, 3b, 6 y 7. |
| **Ejecución en chat** | Principio del producto: la generación documental ocurre en el chat de la plataforma IA (Claude Code, Gemini, Copilot, Cursor, Codex), nunca en código que invoque APIs. |
| **Tooling determinista** | Código Python de `scripts/` y `hooks/` sin dependencias de servicios IA: mismo input → mismo output, validable en CI. |
| **Flujo canónico** | Ciclo `PLAN → AUDIT_PLAN → IMPLEMENT → AUDIT_CODE → VERSION` que estructura cualquier cambio no trivial. |
| **Fase 0a** | Paso de clasificación de orígenes ejecutado antes del inventario cuando hay ≥2 orígenes o el único no es CÓDIGO. Requiere confirmación del usuario. |
| **Fase 0b** | Sincronización visual obligatoria al inicio de toda sesión `/document-project`: verificar assets (nav.css, mermaid.css, sidebar-toggle.js, mermaid.js), `mkdocs.yml` (sin `navigation.sections` si `nav.css` presente), `.gitignore`. |
| **Carpeta `md/`** | Artefactos generados por `scripts/convert_to_md.py`: versiones `.md` de documentos binarios del origen. El agente los usa como contexto de primera clase en Fases 2-4 sin re-conversión. |
| **Estado A/B/C** | Clasificación del inventario: A = sin documentación (CREAR), B = desactualizado (ACTUALIZAR), C = vigente (OMITIR). |
| **Bootstrap (modelo PULL)** | Traslado del sistema de instrucciones IA a otro proyecto, invocado **desde el destino** con el origen como plantilla de solo lectura. Ver `bootstrap_ai_config.prompt.md`. |
| **Capas A/B/C/D** | Clasificación de activos en el bootstrap: A metodología (verbatim), B especialización (reescribir dominio), C contexto (regenerar), D excluir. |
| **Entry point** | Fichero de instrucciones específico de una plataforma IA (`CLAUDE.md`, `GEMINI.md`, `.cursorrules`, `copilot-instructions.md`); siempre subordinado al canónico `SHARED_INSTRUCTIONS.md`. |
| **Canónico** | `.github/SHARED_INSTRUCTIONS.md`: fuente única de reglas comunes; los entry points solo añaden especialización (regla DRY). |
| **MADR 4.0** | Formato para Architecture Decision Records: frontmatter YAML con status/date/deciders + título "Use X for Y". Usado en Arquetipo 5. |
| **ZIP offline** | Paquete distribuible del sitio de docs con checksum SHA256. Mecanismo dual: `scripts/build_docs_zip.py` (versionado en `dist/`) y `mkdocs_hooks.py` (latest en `site/`). |
| **Hook MkDocs** | `mkdocs_hooks.py` en la raíz del proyecto: genera `{nombre}-docs-latest.zip` en `site/` en cada build. Sin instalación (no requiere pip install). |
| **sync_root_docs** | `hooks/sync_root_docs.py`: copia CHANGELOG.md y CONTRIBUTING.md de la raíz a `docs/`. Funciona como hook MkDocs y PostToolUse. |
| **Enlace bidireccional** | Obligación de los arquetipos 2 (Técnica §5) y 4 (Ejemplos §5) de enlazarse mutuamente. |
| **Dogfooding** | El sitio `docs/` de doc_ia se genera aplicando sus propios 12 arquetipos (33 páginas). |
| **Sesión** | Unidad de trabajo registrada en `.ai/sessions/<fecha>/` con REQUEST, CONTEXT_SNAPSHOT y TRACEABILITY (plantilla en `.ai/sessions/TEMPLATE/`). |
| **Cierre de sesión** | Paso final obligatorio de `/document-project`: crea artefactos `.ai/sessions/YYYY-MM-DD/` en el destino y propone commit Conventional Commits `docs(<scope>):`. |
| **Directrices para Futuras IAs** | Sección obligatoria del TRACEABILITY.md al cerrar sesión: hechos verificables que evitan repetir análisis. |
| **Estrategia multi-CÓDIGO** | Forma de documentar ≥2 orígenes CÓDIGO: `federado`, `hub+satélite` o `monorepo`. Nunca se autodetecta; el usuario elige. |
| **`downloads.md`** | Página obligatoria en todo destino documentado. Variante A (con ZIP script) o Variante B (sin script, solo instrucciones). |
| **`start-server.py`** | Servidor HTTP local para navegación offline incluido en el ZIP generado por `mkdocs_hooks.py`. |
