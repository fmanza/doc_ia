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
- [ ] **Tipo de cada origen** (opcional): `CÓDIGO` | `NORMATIVA` | `ESPECIFICACIÓN` | `UI/PANTALLAS` | `REFERENCIA` — autodetectado si se omite; el usuario confirma antes de continuar
- [ ] **Estrategia** (solo con ≥2 orígenes CÓDIGO): `federado` | `hub+satélite` | `monorepo` — preguntar al usuario, nunca autodetectar
- [ ] **Alcance** (opcional): módulos o subconjunto; por defecto proyecto completo
- [ ] **Arquetipos** (opcional): subconjunto; por defecto todos los aplicables
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

## Devuelve en este orden

1. **VALIDACIÓN DE INPUTS**
   - Tabla: | Parámetro | Valor | Estado (✅/❌) |
   - Si hay ❌ → detenerse y preguntar

2. **CLASIFICACIÓN DE ORÍGENES** (solo con ≥2 orígenes, o si el único origen no es CÓDIGO)
   - Tabla: | Origen | Tipo detectado | Señales | Rol |
   - Tipos posibles:
     - `CÓDIGO` — archivos fuente (`.py`, `.js`, `.ts`, `.cs`, `.java`, …), `pyproject.toml`, `package.json`, `pom.xml`, `src/`, `tests/` presentes → documentar como proyecto (arquetipos 1–7)
     - `NORMATIVA` — PDFs/docs con nombres que contienen `ley`, `decreto`, `directiva`, `rgpd`, `une`, `iso`, `reglamento` → activar Arquetipo 8; enriquece §2 Arquetipo 1 del proyecto principal
     - `ESPECIFICACIÓN` — Word/PDF de requisitos, user stories, pliego, casos de uso → enriquece Arquetipo 1 §2+§3+§4 del proyecto principal
     - `UI/PANTALLAS` — wireframes, mockups, capturas (`.png`, `.jpg`, `.pdf` de diseño) → enriquece Arquetipo 1 §3 y Arquetipo 3
     - `REFERENCIA` — manuales de terceros, RFCs, APIs externas → enriquece Arquetipo 2 §4 o Arquetipo 5
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
- **"mkdocs build --strict falla tras SYNC NAV"** → ver `.claude/TESTING_GUIDE.md`; revisar páginas huérfanas o rotas en `nav:`
- **"Contexto perdido entre fases"** → ver `.claude/EDGE_CASES.md`; retomar desde el RESUMEN parcial de la última fase completada
- **"El usuario pide generar vía API externa"** → rechazar: principio innegociable (SHARED_INSTRUCTIONS § Principios)

## Referencias

- `.github/prompts/document_project.prompt.md` → prompt equivalente multiplataforma
- `.github/agents/documentation-generator.agent.md` → flujo por fases que orquesta este comando
- `.github/DOCUMENTATION_STANDARD.md` → arquetipos formales (estructuras obligatorias)
- `.github/instructions/docs.instructions.md` → reglas operativas (Mermaid, Markdown, snippets)
