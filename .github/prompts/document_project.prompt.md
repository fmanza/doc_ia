# Prompt: document_project — Punto de entrada único para documentar un proyecto

## Objetivo

Documentar un proyecto de desarrollo (un proyecto origen externo o el propio doc_ia) aplicando
los **arquetipos formales** de `.github/DOCUMENTATION_STANDARD.md` mediante el flujo por fases
del agente **Documentation Generator**. Los orígenes y el destino son **parámetros obligatorios**
de cada ejecución: nunca constantes asumidas.

Este prompt es el **comando de entrada único** del producto doc_ia. No uses prompts de arquetipo
sueltos para documentar un proyecto completo: invoca este flujo y deja que orqueste los arquetipos.

## Contexto a completar (OBLIGATORIO — validar antes de empezar)

- [ ] **Origen(es) a documentar**: ruta(s) raíz del/los proyecto(s) (ej. `c:\repos\mi_api`)
- [ ] **Destino de la documentación**: ruta donde se escribe (ej. `c:\repos\mi_api\docs` o repo aparte)
- [ ] **Generador**: `mkdocs-material` (por defecto en doc_ia) | `zensical`
- [ ] **Idioma**: `es` | `en` | otro

Opcionales:

- **Tipo de cada origen**: `CÓDIGO` | `NORMATIVA` | `ESPECIFICACIÓN` | `UI/PANTALLAS` | `REFERENCIA` | `CONTRATO` | `INFRAESTRUCTURA` — autodetectado si se omite; se confirma con el usuario antes de continuar
- **Estrategia** (solo con ≥2 orígenes CÓDIGO): `federado` | `hub+satélite` | `monorepo` — siempre preguntar al usuario, nunca autodetectar
- **Alcance**: módulos o subconjunto a documentar (por defecto: proyecto completo)
- **Arquetipos**: subconjunto a aplicar (por defecto: todos los aplicables según inventario)
- **Verificación**: `--verify-tools` y/o `--verify-build [--serve]` (opt-in, nunca automáticos)

## ⚠️ VALIDACIÓN (bloqueante)

Si **alguno** de los 4 campos obligatorios está vacío, es ambiguo o no es verificable,
**DETENTE AHORA**. Pide los datos al usuario antes de continuar. **No inventes rutas, no asumas
destino, no elijas generador ni idioma por el usuario.** Mismo patrón de validación que
`new_feature`: sin contexto completo no se emite ninguna fase.

Ejemplos de detención:

- "Falta **Destino** → preguntar: ¿la documentación se escribe en `docs/` del propio origen o en otro repositorio?"
- "Origen `c:\repos\mi_api` no existe o no es legible → preguntar ruta correcta antes de inventariar."
- "Generador no indicado → preguntar: ¿MkDocs Material (por defecto) o Zensical?"

## Política innegociable (de `SHARED_INSTRUCTIONS.md` § Principios)

1. **Prohibido incrustar API keys**: ninguna credencial de servicios IA se configura, versiona
   ni incrusta en código, prompts o workflows.
2. **La ejecución IA ocurre siempre en el chat** de la plataforma (Claude Code, Gemini, Copilot,
   Cursor, Codex), guiada por estas instrucciones.
3. **El código Python nunca invoca servicios IA**: `scripts/` es tooling determinista
   (build, ZIP, validaciones). Si una fase parece requerir generación programática vía API,
   la respuesta es NO: se genera en este chat.

## Flujo orquestado (Documentation Generator)

Aplica el flujo por fases de `.github/agents/documentation-generator.agent.md` sobre el
**origen** indicado, escribiendo en el **destino** indicado:

```
Fase 0a — Clasificación de orígenes (solo con ≥2 orígenes, o si el único origen no es CÓDIGO):
         1. Para cada origen, detectar tipo por señales del sistema de ficheros:
            - CÓDIGO         : archivos fuente (.py, .js, .ts, .cs, .java, .go, .rs, …),
                               pyproject.toml, package.json, pom.xml, Cargo.toml, go.mod,
                               src/, tests/ presentes
            - NORMATIVA      : PDFs/docs con palabras clave en nombre o carpeta:
                               ley, decreto, directiva, rgpd, gdpr, une, iso, reglamento, compliance
            - ESPECIFICACIÓN : Word/PDF de requisitos, user stories, pliego, ficheros .feature (BDD);
                               carpetas specs/, requirements/, ux/, user-stories/
            - UI/PANTALLAS   : wireframes, mockups, capturas (.png, .jpg, .pdf de diseño);
                               carpetas mockups/, screens/, wireframes/, figma-exports/
            - REFERENCIA     : manuales de TERCEROS, RFCs, especificaciones de protocolo AJENAS al proyecto
            - CONTRATO       : especificaciones machine-readable del PROPIO proyecto:
                               .yaml/.json con clave openapi: o asyncapi:; .graphql/.gql; .proto; .avsc;
                               .sql DDL en db//migrations/; .dbml; carpetas api/, contracts/, schemas/, proto/
            - INFRAESTRUCTURA: IaC y despliegue: .tf (Terraform); Dockerfile, docker-compose.yml;
                               YAML en k8s/, deploy/, manifests/, helm/; playbooks Ansible en roles//ansible/
         2. Presentar tabla: | Origen | Tipo detectado | Señales encontradas | Rol propuesto |
         3. DETENER y pedir confirmación al usuario antes de continuar.
         4. Si hay ≥2 orígenes CÓDIGO → preguntar estrategia al usuario:
            - federado     : cada proyecto con docs/ y mkdocs.yml propios, independientes
            - hub+satélite : un proyecto "hub" concentra el destino; los demás son secciones
            - monorepo     : mkdocs.yml raíz único agrupa secciones por proyecto
         5. Caso degenerado — ningún origen CÓDIGO → DETENER con mensaje:
            "No se detecta ningún proyecto de desarrollo. /document-project requiere al menos
             un origen de tipo CÓDIGO. Para documentar solo normativa o especificación,
             usa directamente normative_traceability.prompt.md o functional_doc.prompt.md."
         Mapeo MATERIAL → arquetipos (para orígenes no-CÓDIGO):
            NORMATIVA        → Arquetipo 8 + enriquece §2 (Reglas de Negocio) del Arquetipo 1
            ESPECIFICACIÓN   → enriquece Arquetipo 1 §2+§3+§4 del proyecto principal
            UI/PANTALLAS     → enriquece Arquetipo 1 §3 (Casos de Uso) y Arquetipo 3
            REFERENCIA       → enriquece Arquetipo 2 §4 (Dependencias) o Arquetipo 5 (ADR)
            CONTRATO         → enriquece Arquetipo 2 §1 (Arquitectura/interfaces) y §2 (Modelo de Datos/Contratos)
            INFRAESTRUCTURA  → enriquece Arquetipo 2 §4 (Dependencias) y Arquetipo 6D §3 (vista despliegue)

Fase 0 — Detección de normativa: si el origen referencia normativa de obligado cumplimiento,
         ofrecer Arquetipo 8 (normative_traceability.prompt.md). Si no hay, omitir.
         Nota: si la Fase 0a ya clasificó un origen como NORMATIVA, este paso está cubierto.
Fase 1 — Inventariar y clasificar:
         Leer árbol real del origen (README, código, docs/, mkdocs.yml del destino).
         Para cada módulo del origen y cada página existente en el destino, asignar estado:
           ESTADO A — sin doc: no existe página en docs/ para este módulo.
           ESTADO B — desactualizado: página existe pero al menos uno de los siguientes:
             · firma de función/clase pública cambiada (parámetro, nombre o tipo de retorno)
             · nuevo símbolo público en el código no documentado en la página
             · símbolo documentado ya no existe en el módulo actual
             · tests actuales contradicen el comportamiento descrito en la documentación
             · sección marcada "Pendiente de verificación" ya verificable en código actual
           ESTADO C — vigente: página existe y código coincide con lo documentado.
         Acción derivada: A → CREAR | B → ACTUALIZAR | C → OMITIR.
         Prioridad de ejecución: A antes que B; C no se toca.
Fase 2 — Mapeo funcional (functional_doc.prompt.md) → [destino]/functional/
Fase 3 — Documentación técnica con Mermaid (technical_doc.prompt.md) → [destino]/api/
Fase 4 — Ejemplos verificables (example_doc.prompt.md) → [destino]/examples/
         Guías y landing según inventario: guide_doc, landing_doc, onboarding_dev, architecture_doc.
Fase 5 — Sincronizar navegación del generador (mkdocs.yml del destino): añadir/mover/retirar entradas.
Fase 6 — Revisión final: Markdown, enlaces relativos, sintaxis Mermaid, secciones de arquetipo completas.
Fase 7 — Verificación de build (solo con --verify-build): build --strict del generador + lectura del HTML.
```

**Protocolo ACTUALIZAR (estado B) — obligatorio en Fases 2-4:**
1. Leer el documento existente completo antes de escribir cualquier línea.
2. Comparar sección a sección con el código actual del origen.
3. Actualizar solo las secciones afectadas; copiar verbatim las que siguen vigentes.
4. Nunca eliminar una sección "Pendiente de verificación" sin haberla verificado en el código.
5. Si un símbolo documentado ya no existe en el módulo: retirar su sección y documentar el reemplazo si lo hay.

Reglas transversales: idioma indicado en todo el contenido generado; no inventar módulos,
APIs ni capacidades; secciones vacías → `*No aplica para este módulo.*`; reglas operativas de
`.github/instructions/docs.instructions.md`.

## Devuelve en este orden

1. **VALIDACIÓN DE INPUTS** — tabla: | Parámetro | Valor | Estado (✅/❌) | — si hay ❌, detenerse aquí.
2. **CLASIFICACIÓN DE ORÍGENES** (Fase 0a) — solo con ≥2 orígenes o si el único no es CÓDIGO:
   - Tabla: | Origen | Tipo detectado | Señales | Rol |
   - Si hay ≥2 orígenes CÓDIGO: indicar estrategia elegida por el usuario.
   - ⚠️ Confirmar con el usuario antes de continuar.
3. **INVENTARIO** (Fase 0+1) — tabla: | Módulo / Página | Estado (A/B/C) | Acción (CREAR/ACTUALIZAR/OMITIR) | Arquetipos / Secciones afectadas |
   - Con múltiples orígenes CÓDIGO: un sub-inventario por proyecto.
4. **PLAN_DOC** — orden de generación con columnas CREAR / ACTUALIZAR (indicar secciones) / OMITIR; impacto en navegación.
5. **GENERACIÓN** (Fases 2-4) — por fases e iterando módulo a módulo; nunca un único prompt masivo.
   - Orígenes MATERIAL: usar como fuente de enriquecimiento de las secciones mapeadas (ver Fase 0a); no crear páginas propias para ellos.
6. **SYNC NAV** (Fase 5) — diff de `mkdocs.yml` (o config del generador) del destino.
7. **REVISIÓN** (Fase 6) — checklist de validación + hallazgos.
8. **BUILD** (Fase 7, solo opt-in) — resultado de `--verify-build`.
9. **RESUMEN** — archivos generados/actualizados, entradas de nav, pendientes de verificación humana.
10. **CIERRE DE SESIÓN** (siempre obligatorio) — crear artefacto `.ai/sessions/YYYY-MM-DD/` en el
    destino (`00_REQUEST.md`, `00_CONTEXT_SNAPSHOT.md`, `TRACEABILITY.md`) y proponer commit
    `docs(<scope>): <resumen>` con recuento de páginas creadas/actualizadas/omitidas.

## Ejemplo de entrada

```
Origen(es): c:\Desarrollo\python\libs\doc_ia
Destino: c:\Desarrollo\python\libs\doc_ia\docs
Generador: mkdocs-material
Idioma: es
Alcance: scripts/ completo (check_env.py, build_docs_zip.py)
Arquetipos: funcional, técnica, ejemplos
Verificación: --verify-build
```

## Invocación por plataforma

- **Claude Code**: `/document-project` (slash command) o "Lee y aplica `.github/prompts/document_project.prompt.md`"
- **Copilot Chat**: `/runSubagent Documentation Generator` proporcionando los 4 parámetros obligatorios
- **Gemini / Cursor / Codex**: "Lee y aplica `.github/prompts/document_project.prompt.md` con [parámetros]"
