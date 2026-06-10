# /document-project

Documentar un proyecto (origen → destino) orquestando los arquetipos formales. Comando de entrada único del producto doc_ia.

## Cuándo usar

- Documentar un proyecto origen externo completo aplicando los arquetipos (funcional, técnica, ejemplos, guías, ADR, landing, onboarding, normativa)
- Regenerar o actualizar la documentación propia de doc_ia (dogfooding)
- Documentar un subconjunto de módulos de un origen manteniendo `mkdocs.yml` sincronizado
- Antipatrón: NO usar para una única página suelta — aplica directamente el prompt de arquetipo correspondiente (`functional_doc`, `technical_doc`, etc.)
- Antipatrón: NO usar para cambios de código o tooling — usa `/new-feature`, `/hotfix` o `/refactor`

## Inputs requeridos (OBLIGATORIO completar TODOS)

- [ ] **Origen(es) a documentar**: Ruta(s) raíz del/los proyecto(s) (ej. `c:\repos\mi_api`)
- [ ] **Destino de la documentación**: Ruta donde se escribe (ej. `c:\repos\mi_api\docs`)
- [ ] **Generador**: `mkdocs-material` (por defecto) | `zensical`
- [ ] **Idioma**: `es` | `en` | otro
- [ ] **Tipo de cada origen** (opcional): `CÓDIGO` | `NORMATIVA` | `ESPECIFICACIÓN` | `UI/PANTALLAS` | `REFERENCIA` | `CONTRATO` | `INFRAESTRUCTURA` — autodetectado si se omite; el usuario confirma antes de continuar
- [ ] **Estrategia** (solo con ≥2 orígenes CÓDIGO): `federado` | `hub+satélite` | `monorepo` — preguntar al usuario, nunca autodetectar
- [ ] **Alcance** (opcional): módulos o subconjunto; por defecto proyecto completo
- [ ] **Arquetipos** (opcional): subconjunto; por defecto todos los aplicables **excepto 9 (Changelog) y 11 (Contribución)**, que son opt-in explícito
- [ ] **Verificación** (opcional): `--verify-tools` y/o `--verify-build [--serve]`

### ⚠️ VALIDACIÓN

Si **alguno** de los 4 campos obligatorios (Origen, Destino, Generador, Idioma) está vacío,
es ambiguo o no es verificable en disco, **DETENTE AHORA**. Pide los datos al usuario antes
de continuar. No inventes rutas ni elijas generador o idioma por el usuario. No emitas
INVENTARIO hasta que los 4 estén completos (mismo patrón de validación que `/new-feature`).

Ejemplo de detención: "Campo 'Destino' vacío → preguntar: ¿escribo en `docs/` del origen o en un repositorio aparte?"

## Política de cambios para este comando

**Obligatorio**:
- Ejecutar el flujo por fases del Documentation Generator (Fases 0-6; Fase 7 solo opt-in)
- Actualizar la navegación del generador (`mkdocs.yml`) por cada página creada, movida o retirada
- Secciones de arquetipo completas; vacías → `*No aplica para este módulo.*`
- **Al actualizar (estado B)**: leer el documento existente antes de escribir; conservar verbatim
  las secciones que siguen vigentes; actualizar solo las afectadas por cambios en el código

**Prohibido**:
- Incrustar API keys o invocar servicios IA desde código (la generación ocurre en este chat)
- Inventar módulos, APIs, salidas, errores o dependencias no presentes en el origen
- Modificar código fuente del origen (solo se escribe documentación y navegación)

**Recomendado**:
- Iterar módulo a módulo dentro de cada fase; nunca un único prompt masivo
- Cerrar con `python -m mkdocs build --strict` (o `--verify-build`) antes de publicar
- En Fase 0b, ejecutar validación de assets personalizados (ver sección "Sincronización de Configuración Visual")
- Crear siempre el artefacto `.ai/sessions/YYYY-MM-DD/` en el destino antes del commit (paso 10)

## Sincronización de Configuración Visual (Fase 0b)

**Cuándo aplica**: Si el destino tiene `mkdocs.yml` pero hereda de un generador estándar (ej. `util` heredó `mkdocs.yml` base).

**Qué sincronizar** (universal, aplicable a todos los proyectos MkDocs):
- `theme.features` — Ver tabla de compatibilidad más abajo; algunas requieren decisión
- `markdown_extensions` críticas — `pymdownx.snippets` (para `--8<--`), `pymdownx.superfences` (Mermaid), `pymdownx.emoji`
- `extra_javascript` y `extra_css` — Assets personalizados (ej. `sidebar-toggle.js`, `nav.css`)
- `extra.social` — Enlaces de redes sociales (si aplica)

**Tabla de `theme.features` — copiables vs decisión**:

| Feature | Acción | Razón |
|---|---|---|
| `navigation.tabs`, `navigation.tabs.sticky` | ✅ Copiar | Universal |
| `navigation.top`, `navigation.footer` | ✅ Copiar | Universal |
| `search.suggest`, `search.highlight` | ✅ Copiar | Universal |
| `content.code.copy`, `content.code.annotate`, `content.tabs.link` | ✅ Copiar | Universal |
| `toc.follow` | ✅ Copiar | Universal |
| **`navigation.sections`** | ⚠️ **NO copiar si `nav.css` presente** | Activa grupos estáticos: desactiva `.md-nav__item--nested` → sidebar sin colapso |
| `navigation.expand` | ⚠️ Decisión | Expande todo por defecto; puede no ser deseado |
| `navigation.prune` | ⚠️ Decisión | Solo recomendado en navs muy grandes |

**Regla crítica**: Si `nav.css` está en `extra_css` → `navigation.sections` debe estar **ausente** de `theme.features`.

**Qué NO sincronizar** (específico del proyecto, nunca copiar ciegamente):
- `plugins` — Solo sincronizar si el destino lo necesita (ej: `mkdocstrings` es para proyectos con código; no para doc_ia)
- `site_name`, `site_description`, `site_author`, `site_url`, `repo_url` — Específicos del proyecto
- `site_dir`, `docs_dir` — Usar defaults o configuración destino

**Proceso**:
1. Si destino NO tiene `mkdocs.yml` → copiar completo de origen
2. Si destino tiene `mkdocs.yml` incompleto → sincronizar secciones "universal" del origen
3. Si destino tiene `mkdocs.yml` personalizado → verificar assets personalizados existen en disco

**Validación de Assets**:
```bash
# Verificar que los archivos referenciados en extra_javascript y extra_css existen
ls {destino}/docs/assets/js/*.js
ls {destino}/docs/assets/css/*.css

# Si faltan, copiar desde origen (si es proyecto hermano) o crear vacíos
cp -r {origen}/docs/assets/* {destino}/docs/assets/
```

**Commit de referencia**: En doc_ia → origin, origen de la configuración visual

---

## Devuelve en este orden

1. **VALIDACIÓN DE INPUTS**
   - Tabla: | Parámetro | Valor | Estado (✅/❌) |
   - Si hay ❌ → detenerse y preguntar

2. **CLASIFICACIÓN DE ORÍGENES** (solo con ≥2 orígenes, o si el único origen no es CÓDIGO)
   - Tabla: | Origen | Tipo detectado | Señales | Rol |
   - Tipos posibles:
     - `CÓDIGO` — archivos fuente (`.py`, `.js`, `.ts`, `.cs`, `.java`, `.go`, `.rs`, …), `pyproject.toml`, `package.json`, `pom.xml`, `src/`, `tests/` presentes → documentar como proyecto (arquetipos 1–7)
     - `NORMATIVA` — PDFs/docs con nombres que contienen `ley`, `decreto`, `directiva`, `rgpd`, `gdpr`, `une`, `iso`, `reglamento` → activar Arquetipo 8; enriquece §2 Arquetipo 1 del proyecto principal
     - `ESPECIFICACIÓN` — Word/PDF de requisitos, user stories, pliego, ficheros `.feature`; carpetas `specs/`, `requirements/`, `ux/` → enriquece Arquetipo 1 §2+§3+§4 del proyecto principal
     - `UI/PANTALLAS` — wireframes, mockups, capturas (`.png`, `.jpg`, `.pdf` de diseño); carpetas `mockups/`, `figma-exports/` → enriquece Arquetipo 1 §3 y Arquetipo 3
     - `REFERENCIA` — manuales de **terceros**, RFCs, especificaciones de protocolo **ajenas al proyecto** → enriquece Arquetipo 2 §4 o Arquetipo 5
     - `CONTRATO` — especificaciones machine-readable del **propio proyecto**: `openapi:` / `asyncapi:` YAML, `.graphql`, `.proto`, `.sql` DDL, `.dbml`; carpetas `api/`, `schemas/`, `proto/` → enriquece Arquetipo 2 §1 (interfaces) y §2 (contratos/datos)
     - `INFRAESTRUCTURA` — IaC y despliegue: `.tf`, `Dockerfile`, `docker-compose.yml`, K8s YAML en `k8s/`/`deploy/`/`helm/`, Ansible → enriquece Arquetipo 2 §4 y Arquetipo 6D (vista despliegue)
   - Si hay ≥2 orígenes `CÓDIGO` → preguntar estrategia (nunca autodetectar):
     - `federado`: cada proyecto documenta de forma independiente (docs/ propio, mkdocs.yml propio)
     - `hub+satélite`: un proyecto "hub" es el destino; los demás se documentan como secciones dentro de él
     - `monorepo`: un mkdocs.yml raíz agrupa secciones por proyecto
   - **Caso degenerado**: si no hay ningún origen `CÓDIGO` → **DETENER**: "No se detecta ningún proyecto de desarrollo. `/document-project` requiere al menos un origen de tipo CÓDIGO. Para documentar solo normativa o especificación, usa directamente `normative_traceability.prompt.md` o `functional_doc.prompt.md`."
   - ⚠️ **Confirmar clasificación con el usuario antes de continuar al INVENTARIO.**

3. **INVENTARIO** (Fases 0-1)
   - Normativa de referencia (Arquetipo 8) si aplica
   - Tabla con 4 columnas: | Módulo / Página | Estado | Acción | Arquetipos / Secciones |
     - Estado A — sin doc → CREAR
     - Estado B — desactualizado → ACTUALIZAR (indicar qué secciones)
     - Estado C — vigente → OMITIR
   - Criterios estado B: firma cambiada · símbolo nuevo no documentado · símbolo retirado
     del módulo · tests contradicen docs · sección "Pendiente de verificación" verificable ya

4. **PLAN_DOC**
   - Orden de ejecución: CREAR (A) antes que ACTUALIZAR (B); OMITIR (C) no se toca
   - Por cada página: acción + secciones afectadas + impacto en navegación
   - Con múltiples orígenes CÓDIGO: indicar estrategia elegida y qué proyecto es el hub (si aplica)

5. **GENERACIÓN** (Fases 2-4)
   - Funcional → técnica → ejemplos → guías/landing según inventario
   - Para estado B: leer página existente completa → actualizar solo secciones afectadas
     → conservar verbatim las vigentes → nunca borrar "Pendiente de verificación" sin verificar
   - Orígenes MATERIAL: usar como fuente de enriquecimiento de las secciones mapeadas (ver CLASIFICACIÓN); no crear páginas propias para ellos

6. **SYNC NAV** (Fase 5)
   - Diff de `mkdocs.yml` del destino

7. **REVISIÓN** (Fase 6)
   - Markdown, enlaces, Mermaid, secciones de arquetipo

8. **BUILD** (Fase 7, solo con `--verify-build`)

9. **RESUMEN**
   - Archivos generados/actualizados, entradas de nav, pendientes de verificación humana

10. **CIERRE DE SESIÓN** (siempre obligatorio)

    **a) Artefacto `.ai/sessions/`** — crear en el **destino** (no en doc_ia), en la ruta
    `{destino}/../.ai/sessions/YYYY-MM-DD/` con tres ficheros:

    - `00_REQUEST.md` — inputs recibidos (origen, destino, generador, idioma, alcance,
      arquetipos, verificación) + objetivo operativo de la sesión
    - `00_CONTEXT_SNAPSHOT.md` — ficheros leídos antes de la primera fase, estado git
      (rama, cambios pre-existentes, último commit), estado de build (si se ejecutó)
    - `TRACEABILITY.md` — resumen cronológico de acciones, tabla de artefactos generados
      (`| Artefacto | Ruta | Estado |`), directrices para IAs futuras, veredicto final
      (`GO` / `GO_CONDICIONAL` / `NO_GO` / `CLOSED`)

    Usar como plantilla los ficheros de `.ai/sessions/TEMPLATE/` de doc_ia.
    Si `.ai/sessions/` no existe en el destino, crearlo (es el primer uso del sistema de sesiones
    en ese proyecto).

    **b) Commit** — una vez escritos los artefactos y verificado el build (si aplica), proponer
    el siguiente commit en el repositorio **destino**:

    ```
    docs(<scope>): <resumen de lo documentado>

    Sesión: .ai/sessions/YYYY-MM-DD/
    Arquetipos: <lista de arquetipos generados/actualizados>
    Páginas: <N> creadas · <M> actualizadas · <K> omitidas
    ```

    - `<scope>` = nombre corto del origen (ej. `util_bbdd`, `mi_api`)
    - Conventional Commits: usar `docs:` para sesiones de documentación pura
    - No hacer `git push`: solo proponer el mensaje y ejecutar `git add` + `git commit`
      si el usuario confirma
    - Si el destino es el propio doc_ia, hacer el commit en doc_ia

## Ejemplo de entrada — origen único

```
Origen(es): c:\Desarrollo\python\libs\doc_ia
Destino: c:\Desarrollo\python\libs\doc_ia\docs
Generador: mkdocs-material
Idioma: es
Alcance: scripts/ completo (check_env.py, build_docs_zip.py)
Arquetipos: funcional, técnica, ejemplos
Verificación: --verify-build
```

## Ejemplo de entrada — múltiples orígenes heterogéneos

```
Origen(es):
  - c:\repos\mi_api                  (proyecto principal)
  - c:\docs\normativa\ley_39.pdf     (ley de referencia)
  - c:\docs\pantallas\mockups\       (capturas de pantalla)
Destino: c:\repos\mi_api\docs
Generador: mkdocs-material
Idioma: es
Tipo de cada origen: mi_api=CÓDIGO, ley_39.pdf=NORMATIVA, mockups=UI/PANTALLAS
```

## Ejemplo de entrada — múltiples proyectos de código

```
Origen(es):
  - c:\repos\mi_api    (backend Python)
  - c:\repos\mi_web    (frontend React)
Destino: c:\repos\mi_api\docs
Generador: mkdocs-material
Idioma: es
Estrategia: hub+satélite  (mi_api es el hub)
```

## Ejemplo de salida esperada (VALIDACIÓN + CLASIFICACIÓN + INVENTARIO)

```markdown
## VALIDACIÓN DE INPUTS

| Parámetro | Valor | Estado |
|---|---|---|
| Origen(es) | c:\Desarrollo\python\libs\doc_ia | ✅ existe y es legible |
| Destino | c:\Desarrollo\python\libs\doc_ia\docs | ✅ existe |
| Generador | mkdocs-material | ✅ mkdocs.yml presente |
| Idioma | es | ✅ |

## CLASIFICACIÓN DE ORÍGENES

(origen único — fase omitida; tipo detectado: CÓDIGO)

## INVENTARIO

| Módulo / Página | Estado | Acción | Arquetipos / Secciones |
|---|---|---|---|
| scripts/check_env.py | A — sin doc | CREAR | funcional + técnica + ejemplo |
| scripts/build_docs_zip.py | B — desactualizado | ACTUALIZAR §3 §5 | técnica (firma `--builder` cambiada) |
| docs/index.md | C — vigente | OMITIR | — |

Normativa de referencia: no detectada → Arquetipo 8 omitido.
```

## Qué hacer si falla

- **"Origen no legible o fuera del workspace"** → pedir al usuario que añada el directorio como working dir adicional o confirme la ruta
- **"mkdocs build advierte sobre assets CSS/JS no encontrados"** → Verificar que `extra_javascript` y `extra_css` en `mkdocs.yml` referencian archivos existentes en `docs/assets/`. Si faltan, sincronizarlos desde origen o crearlos vacíos.
- **"mkdocs build --strict falla tras SYNC NAV"** → ver `.claude/TESTING_GUIDE.md`; revisar páginas huérfanas o rotas en `nav:`
- **"Contexto perdido entre fases"** → ver `.claude/EDGE_CASES.md`; retomar desde el RESUMEN parcial de la última fase completada
- **"El usuario pide generar vía API externa"** → rechazar: principio innegociable (SHARED_INSTRUCTIONS § Principios)

## Referencias

- `.github/prompts/document_project.prompt.md` → prompt equivalente multiplataforma
- `.github/agents/documentation-generator.agent.md` → flujo por fases que orquesta este comando
- `.github/DOCUMENTATION_STANDARD.md` → arquetipos formales (estructuras obligatorias)
- `.github/instructions/docs.instructions.md` → reglas operativas (Mermaid, Markdown, snippets)
