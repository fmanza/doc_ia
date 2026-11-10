---
arquetipo: "1"
fuentes:
  .claude/commands/document-project.md: f82478174881
  .github/DOCUMENTATION_STANDARD.md: 015af37230ba
  .github/prompts/document_project.prompt.md: 03e2d68949a7
  .github/templates/kit/documentar.command.md: 44364ebb0ca8
  CLAUDE.md: 466e411d7ddb
  scripts/db_trace.py: c337133736ca
  scripts/kit.py: 432af520016f
  scripts/redact_secrets.py: d0cbb8ed3fbf
  scripts/snapshot_sources.py: f9dd29bea432
  scripts/web_captures.py: 53972c5aa039
decisiones:
  ../decisiones/docproj_decisiones.md: ace9e2e187df
revisado: 2026-11-10
---
# Documentar un Proyecto

## 1. Objetivo y Descripción

La documentación de un proyecto con doc_ia parte de una única operación de entrada:
indicar el origen (o los orígenes) a documentar, el destino donde se escribirá la
documentación, el generador de sitio y el idioma. A partir de estos cuatro parámetros,
el flujo de trabajo clasifica los orígenes según su naturaleza (código fuente, normativa,
especificación, pantallas…), orquesta el inventario del proyecto, la generación de
documentación por arquetipos formales y la sincronización de la navegación del sitio.

La usan los desarrolladores y technical writers que quieren documentar desde cero un
proyecto existente, o actualizar y completar su documentación a medida que el código
evoluciona. También cubre casos donde la fuente documental incluye material
heterogéneo: normativa de referencia, capturas de pantalla o especificaciones de
requisitos que enriquecen la documentación del proyecto principal.

Su valor está en que un único punto de entrada cubre todo el ciclo
(inventariar → generar → revisar → publicar) sin necesidad de coordinar prompts ni
decidir manualmente qué arquetipo aplicar a cada módulo.

## 2. Precondiciones

- Una plataforma IA con acceso al repositorio doc_ia: Claude Code (comando `/document-project`)
  o Gemini, Copilot, Cursor y Codex (prompt `document_project.prompt.md`). En un destino que ya
  tiene el [kit de documentación](kit.md), basta con abrirlo y lanzar `/documentar`: la
  metodología está en su carpeta `.doc_ia/` y los parámetros en su prompt de instancia.
- Los cuatro parámetros obligatorios: **origen(es)**, **destino**, **generador**
  (`mkdocs-material` por defecto, o `zensical`) e **idioma**.
- Cada origen indicado existe y es legible. Además de una carpeta local, un origen puede ser
  un fichero con la versión en el nombre (patrón con `{ver}`), una carpeta de red, una
  biblioteca de SharePoint sincronizada con OneDrive o un repositorio remoto con su rama,
  etiqueta o commit.
- Al menos uno de los orígenes es de tipo CÓDIGO.
- Opcionales: tipo de cada origen, estrategia (solo con ≥2 orígenes CÓDIGO), alcance,
  exportación de la base de datos (`BD`, ver [Trazabilidad con la Base de Datos](db_trace.md)),
  subconjunto de arquetipos, verificación (`--verify-tools`, `--verify-build`) y modo
  (`incremental` por defecto si el destino ya se documentó con baseline; `completo`).
- Para la verificación de build: el generador elegido instalado en el entorno.

## 3. Flujo Principal

```mermaid
sequenceDiagram
    accTitle: Documentar un proyecto desde el chat
    accDescr: El usuario invoca el flujo con cuatro parámetros; el agente valida, pide confirmar la clasificación si hay varios orígenes o ninguno es código, inventaría el origen frente a la documentación existente, genera las páginas en el destino y devuelve un resumen con la trazabilidad y una propuesta de commit.
    actor U as Usuario
    participant A as Agente
    participant O as Origen
    participant D as Destino
    U->>A: Origen(es), destino, generador e idioma
    alt Falta algún parámetro
        A-->>U: Se detiene y pregunta
    end
    opt Varios orígenes o el único no es código
        A-->>U: Clasificación de orígenes propuesta
        U->>A: Confirma
    end
    A->>D: Sincroniza la configuración visual
    A->>O: Inventaría módulos
    A->>D: Compara con la documentación existente (A, B o C)
    A->>D: Crea o actualiza páginas por arquetipo y la navegación
    A->>D: Revisa y actualiza la página de descargas y las instrucciones para verla
    A-->>U: Resumen, trazabilidad de la sesión y propuesta de commit
```

El usuario invoca el flujo con los cuatro parámetros; si falta alguno, el flujo se detiene y
pregunta. Con varios orígenes, o si el único no es código, se clasifican primero y el usuario
confirma la clasificación. Después se sincroniza la configuración visual del destino y se
inventaría el origen: cada módulo y página recibe un estado (A sin documentación, B
desactualizada, C vigente) que decide la acción del plan (crear, actualizar u omitir). La
generación recorre los arquetipos módulo a módulo —funcional y mapa funcional, técnica,
referencia del sistema si hay superficie de usuario, ejemplos y guías—, se sincroniza la
navegación, se revisa el resultado, se genera o actualiza la página de descargas, se escriben en la raíz del destino las
instrucciones para ver la documentación desde cero (`VER_DOCUMENTACION.md`) y se cierra
la sesión con su artefacto de trazabilidad y una propuesta de commit.

## 4. Postcondiciones y Efectos

- Las páginas en estado A existen en el destino; las de estado B están actualizadas
  conservando las secciones vigentes; las de estado C no se han modificado.
- Las páginas con bloque "Evidencia" declaran sus fuentes en el frontmatter; si el destino
  dispone del tooling de trazabilidad, quedan selladas y sin desactualizaciones.
- Si hay registro de decisiones de cobertura (siempre con normativa), las decisiones que las
  personas han tomado ya se reflejan en las páginas, enlazadas a su ficha; los apartados nuevos
  parciales, sin cubrir o por verificar tienen ficha pendiente, y el resumen lista las
  preguntas concretas para quien decide.
- La navegación del generador en el destino (`mkdocs.yml`) incluye todas las páginas nuevas
  en 9 pestañas como máximo (descargas dentro de «Inicio») y la configuración estándar
  verificada (tema, assets, Mermaid).
- `docs/downloads.md` existe en el destino (variante A o B) y los huecos de distribución
  offline quedan reportados en el resumen.
- `VER_DOCUMENTACION.md` existe en la raíz del destino, fuera de `docs/`, con los requisitos y
  pasos para ver la documentación desde cero en Windows, macOS y Linux, y viaja dentro del ZIP.
- El destino tiene los seis recursos visuales en `docs/assets/`, entre ellos su propia copia de Mermaid y el shim de búsqueda para ficheros locales, y su configuración genera URLs `*.html` con el plugin `offline`: el ZIP se abre con doble clic en `index.html`, con búsqueda y diagramas, sin servidor ni conexión. Tiene además un `.gitignore` con los
  patrones estándar.
- Si algún origen no era una carpeta local de trabajo, su copia está en `_staging/<nombre>/`
  de la raíz del destino, excluida del control de versiones, y los orígenes de documentos
  quedan registrados con su versión e historial en `.ai/sources.json`; el origen no se ha
  modificado.
- Con origen BASE DE DATOS (parámetro `BD`): el destino tiene la sección generada `docs/bd/`
  con las páginas de los objetos del alcance, el catálogo de ese subconjunto en
  `_fuentes/<nombre>/`, una ficha `COB-DATOS-…` por discrepancia entre el código y la base de
  datos, y `.ai/trace_map.toml` regenerado al cerrar la sesión.
- Con origen WEB (opción `WEB`): el destino tiene el manual de funcionamiento en `docs/manual/`
  (Arquetipo 15), las capturas revisadas en `docs/assets/manual/<origen>/` registradas en
  `.ai/captures.json` con entorno, versión y rol, y una ficha `COB-WEB-…` por diferencia entre la
  aplicación desplegada y el código. La dirección del entorno no aparece en ningún fichero.
- Si el origen tiene documentos convertidos a Markdown, el destino tiene su copia en
  `_fuentes/`, fuera de `docs/` y versionada, y ninguna carpeta con otro nombre para ellos.
- El destino lleva el [kit de documentación](kit.md) al día con la versión de doc_ia de la
  sesión: la metodología y las herramientas en `.doc_ia/` (con su registro `kit.lock.json`), los
  lanzadores `/documentar` para cada plataforma IA y `DOCUMENTAR.md` en su raíz; los ficheros
  del kit editados en el destino o ajenos con el mismo nombre no se han tocado y figuran en el
  resumen. El prompt de instancia `.ai/prompts/documentar.prompt.md` recoge los parámetros y
  las decisiones de la sesión, y en la primera sesión `DOCUMENTAR.md` incluye ejemplos reales
  del proyecto.
- Existe `.ai/sessions/YYYY-MM-DD/` en el destino con `00_REQUEST.md`,
  `00_CONTEXT_SNAPSHOT.md` y `TRACEABILITY.md`; en la primera sesión se crean además los
  cinco ficheros de contexto `.ai/*.md`, con las secciones fijas de las plantillas de doc_ia
  (`.github/templates/ai_context/`) y solo con datos de los orígenes del proyecto.
- Se **propone** un commit `docs(<scope>): …`; el flujo no lo ejecuta por sí mismo.
- Con `--verify-build`: el sitio se ha construido en modo estricto y el resultado figura en
  el informe.

## 5. Reglas de Negocio

| Regla | Descripción | Impacto si se viola |
|---|---|---|
| Cuatro parámetros obligatorios | Origen(es), Destino, Generador e Idioma son requeridos; el flujo se detiene y pregunta si falta alguno | Se documentaría un proyecto equivocado, en la ruta incorrecta o con el generador inadecuado |
| Adquisición de orígenes (Fase 0-pre) | El origen nunca se escribe. Lo que no es una carpeta local de trabajo se copia antes a `_staging/<nombre>/` del destino, ignorada por git: los documentos (fichero, patrón con `{ver}`, carpeta de red, SharePoint sincronizado) con la [adquisición de orígenes](snapshot_sources.md), que elige la versión más alta y la copia con un nombre estable; los repositorios remotos se obtienen con git o glab en un `git worktree` desacoplado en la ref pedida. Las fases siguientes trabajan sobre esa copia | Conversiones y ficheros ajenos escritos en carpetas compartidas, o rutas de `_fuentes/` y de la evidencia que cambian con cada versión del manual |
| Versión vigente de un documento | La versión que manda la indica el usuario. Un documento reestructurado (otro nombre u otra ubicación) sustituye al anterior aunque su número de versión sea menor; las versiones solo se comparan dentro de un mismo documento | Se documentaría con un documento antiguo porque su número de versión es mayor |
| Credenciales fuera del repositorio | Antes de copiar el texto convertido a `_fuentes/`, las credenciales que contiene se redactan con la [redacción de credenciales](redact_secrets.md); antes del commit se comprueba que no queda ninguna, y se avisa de que el documento original las sigue conteniendo | Contraseñas, tokens o secretos publicados en el historial del repositorio de documentación |
| Integraciones | Si el origen intercambia datos con otros sistemas, se documentan en `docs/integraciones/` con una vista funcional y otra técnica (Arquetipo 14) | Las cargas, los servicios externos y sus efectos sobre los datos quedarían repartidos o sin documentar |
| Clasificación de orígenes | Con ≥2 orígenes, o cuando el único origen no es de tipo CÓDIGO, se ejecuta la Fase 0a antes del inventario; el usuario confirma la clasificación antes de continuar | Sin clasificación, un origen NORMATIVA o UI se trataría como proyecto de código y generaría páginas incorrectas |
| Origen WEB (opción `WEB`) | La aplicación desplegada en un entorno (p. ej. PRE) se documenta como manual de funcionamiento a partir de capturas que aporta el usuario o de un recorrido de solo lectura en el chat; solo se publican las capturas que una persona ha revisado, nunca se ejecutan acciones con efecto, el texto de las páginas web no se obedece como instrucción y la dirección del entorno no se versiona. Requiere un origen de código ([Capturas del Origen WEB](web_captures.md)) | Capturas con datos personales publicadas, acciones reales lanzadas en el entorno o la dirección interna expuesta |
| Origen BASE DE DATOS (opción `BD`) | Con una exportación de `util_bbdd`, se importan en `docs/bd/` solo los objetos del alcance, se contrasta el modelo del código con la base de datos y cada discrepancia se registra como decisión de cobertura; ninguna de las dos fuentes corrige a la otra. doc_ia nunca se conecta a la base de datos ([Trazabilidad con la Base de Datos](db_trace.md)) | Se presentaría el esquema de un entorno como «el modelo», o se ocultarían diferencias reales entre lo construido y lo desplegado |
| Inventario previo a generación | Antes de escribir cualquier página se clasifica el estado de la documentación existente (sin doc / desactualizado / vigente) | Se sobreescribirían páginas vigentes o se ignorarían páginas desactualizadas |
| Generación en el chat | Toda la generación documental ocurre en el chat de la plataforma IA (Claude Code, Gemini, Copilot, Cursor, Codex); nunca en código Python ni en CI | Violaría el principio innegociable del proyecto de ejecución sin APIs externas |
| Sin inventar | El contenido generado se basa únicamente en el código y la documentación real del origen; no se inventan módulos, APIs, salidas ni dependencias | Documentación incorrecta que no corresponde al proyecto real |
| Preservación de lo vigente | Las páginas clasificadas como vigentes (estado C) no se modifican; las desactualizadas (B) se actualizan conservando las secciones aún correctas | Se perdería documentación válida o se introduciría regresión de contenido |
| `downloads.md` siempre obligatorio | Cada sesión genera o actualiza `docs/downloads.md` en el destino (Fase 7b); el flujo detecta tres señales de distribución offline (`TIENE_ZIP_SCRIPT`, `TIENE_MKDOCS_PLUGIN`, `TIENE_WORKFLOW_GITHUB`) y reporta los huecos | El destino quedaría sin una página de descarga offline o con datos desactualizados |
| Instrucciones de visualización siempre | Cada sesión genera o actualiza `VER_DOCUMENTACION.md` en la raíz del destino (Fase 7c) desde una plantilla con secciones fijas: qué ruta seguir (web, ZIP, código fuente), cómo abrir el ZIP con doble clic tras extraerlo, el servidor local como alternativa, cómo instalar Python para la ruta de código fuente y problemas frecuentes; los valores (versión de Python, dependencias, nombre del ZIP, publicación) salen del destino | Quien recibe la documentación sin conocimientos técnicos no sabría verla |
| Relanzar solo sobre lo cambiado | Al cerrar cada sesión se guarda el punto del historial de cada proyecto documentado; al relanzar, el inventario parte de los ficheros cambiados desde ese punto y de las páginas que los citan, y el resto se da por vigente sin releerlo. Si no hay punto guardado, el proyecto no usa Git, el punto ya no existe o cambió la versión de doc_ia, la sesión es completa | Releer todo el proyecto en cada actualización, o dar por vigente una página cuyo código cambió |
| [COB-DOCPROJ-001](../decisiones/docproj_decisiones.md#cob-docproj-001) · Sincronización visual obligatoria (Fase 0b) | Al inicio de toda sesión se verifican: assets CSS/JS en `docs/assets/`, configuración de `mkdocs.yml` (sin `navigation.sections` si `nav.css` presente), `.gitignore` con patrones estándar (`site/`, `*.pdf`, `*.doc`, `*.docx`). Aplica tanto en creación como en actualización ✅ | El destino tendría assets desincronizados, menú lateral sin colapso o binarios versionados por error |
| Zensical sin pérdidas silenciosas | Con generador Zensical, que no ejecuta `hooks:` ni los plugins que no soporta, el flujo detecta si el script de build del destino ejecuta él mismo esos pasos (`TIENE_PIPELINE_SIN_HOOKS`), reporta el Gap A4 si no lo hace y señala los plugins no soportados; nunca crea `zensical.toml` | El destino perdería sin aviso la sincronización de ficheros raíz, el ZIP "latest" o la función de un plugin |
| Documentos pre-convertidos (`md/`) | Si el origen contiene carpetas `md/` (generadas por `convert_to_md.py`), se usan como contexto de primera clase en Fases 2-4 sin re-conversión; no generan páginas propias ni reciben estado A/B/C | Se perdería contexto valioso de documentos binarios o se intentaría re-convertir innecesariamente |
| Fuentes convertidas en `_fuentes/` | El destino recibe siempre una copia de los documentos convertidos en `_fuentes/<origen>/…`, con la misma ruta que en el origen, aunque origen y destino sean el mismo repositorio. Es el único nombre válido: otro nombre existente se migra a `_fuentes/` con confirmación, y nada se borra sin confirmar. Su texto se versiona en el destino; los binarios, no | Cada sesión elegiría un nombre distinto (`.fuentes/`, `_fuentes/`), la evidencia apuntaría a rutas fuera del repositorio y la trazabilidad no detectaría cambios en esos documentos |
| Independencia entre proyectos | Todo lo que se escribe en el destino se deriva de doc_ia (scripts, plantillas, recursos) y de los orígenes del propio proyecto. Otro proyecto documentado con doc_ia no es plantilla ni fuente de decisiones: su clasificación de orígenes, su alcance, sus fichas de cobertura o sus ADR no se aplican aquí, aunque el stack coincida. Lo que otro proyecto resolvió y el estándar no cubría se incorpora primero a doc_ia | Un proyecto heredaría decisiones que nadie tomó para él, y cada destino copiado de otro acumularía sus errores y versiones antiguas de los scripts |
| Kit de documentación en el destino | Al inicio de toda sesión, también en destinos ya creados, se instala o actualiza el [kit de documentación](kit.md) desde doc_ia; un fichero del kit editado en el destino o un lanzador ajeno es un conflicto que se informa y nunca se fuerza sin que lo pida el usuario. Sin doc_ia accesible, solo se comprueba el kit y se avisa en el resumen. El cierre crea o actualiza el prompt de instancia con los parámetros y decisiones de la sesión, para que `/documentar` la repita sin preguntar, y el commit propuesto incluye el kit, los lanzadores, `DOCUMENTAR.md` y ese prompt | Quien recibe el repositorio de documentación no podría relanzarla sin doc_ia ni sin repetir las preguntas de la primera sesión |
| Contexto persistente `.ai/*.md` | En la primera sesión de un destino nuevo (o si faltan), se crean los 5 ficheros de contexto raíz: `product.md`, `architecture.md`, `glossary.md`, `runtime.md`, `standards.md`; en sesiones posteriores se actualizan si el inventario detecta cambios relevantes | Una IA futura no tendría el snapshot del proyecto para su `00_CONTEXT_SNAPSHOT` |

## 6. Límites, Flujos Alternativos y Casos Especiales

### Qué NO hace esta funcionalidad

- No genera contenido mediante APIs de IA ni desde código: todo ocurre en el chat.
- No documenta orígenes compuestos solo por MATERIAL (sin ningún proyecto de código).
- No decide la estrategia con varios proyectos de código: siempre la pregunta.
- No modifica páginas vigentes (estado C).
- No ejecuta el build del sitio salvo que se pida `--verify-build`.
- No está pensado para una sola página suelta: para eso se aplica directamente el prompt
  del arquetipo correspondiente.
- No hace el commit: lo propone al cierre de la sesión.

### Flujos alternativos

- **Parámetro faltante o ambiguo**: el flujo se detiene y pregunta al usuario antes de
  inventariar. No se asume destino ni idioma por defecto.
- **Relanzamiento sobre un destino ya documentado**: si el destino guarda el punto del historial
  de cada proyecto, el inventario solo revisa lo cambiado desde ese punto; con `Modo: completo`,
  o si ese punto no sirve (proyecto sin Git, punto inexistente, otra versión de doc_ia), se
  revisa todo y el motivo aparece en el inventario.
- **Origen no legible**: si la ruta indicada no existe o no es accesible, se pide
  confirmación antes de continuar.
- **Orígenes heterogéneos**: con ≥2 orígenes o cuando el único origen no es CÓDIGO, la
  Fase 0a detecta el tipo de cada uno (ver [Tipos de Origen](origin_types.md)) y presenta
  una tabla al usuario para confirmación antes de inventariar. Los orígenes de tipo MATERIAL
  no generan páginas propias: su contenido enriquece secciones concretas de los arquetipos
  del proyecto CÓDIGO principal.
- **Estrategia multi-CÓDIGO**: con ≥2 orígenes de tipo CÓDIGO, el flujo pregunta la
  estrategia de documentación (`federado`, `hub+satélite`, `monorepo`); nunca se
  autodetecta porque depende del contexto organizacional.
- **Sin origen CÓDIGO**: si todos los orígenes son MATERIAL, el flujo se detiene e
  informa que `/document-project` requiere al menos un origen de tipo CÓDIGO.
- **Verificación de build**: paso opcional (`--verify-build`) que construye el sitio en
  modo estricto al final y confirma que compila sin errores.
- **Generador Zensical**: la configuración y los assets son los mismos (Zensical lee el mismo
  `mkdocs.yml`). Cambian el build, que se hace a través del script del destino para que se
  ejecuten los pasos que Zensical ignora, la comprobación de plugins soportados y la señal
  adicional del pipeline en la página de descargas.

- **Relanzamiento desde el destino con `/documentar`**: el lanzador lee el prompt de instancia
  y aplica la metodología de `.doc_ia/` con esos parámetros; modos opcionales `incremental`
  (por defecto), `completo`, `verificar`, `aplicar-decisiones` y `zip`. Si falta el prompt de
  instancia, se crea pidiendo al usuario los parámetros obligatorios.

### Casos especiales

- **Documentación parcialmente existente**: el inventario clasifica cada módulo y página
  de forma independiente; las páginas vigentes no se tocan.
- **Alcance restringido**: se puede indicar un subconjunto de módulos o un subconjunto de
  arquetipos; el resto queda fuera del plan de generación.
- **Normativa detectada**: si el origen referencia normativa de obligado cumplimiento, el
  flujo ofrece el Arquetipo 8 junto con su registro de decisiones (Arquetipo 13); si no, los
  omite.
- **Registro de decisiones ya editado**: las decisiones tomadas se aplican antes de regenerar
  las páginas de su ámbito; las fichas incompletas o inválidas no se aplican y se informan en
  el resumen. El flujo nunca escribe la decisión de una persona.
- **Carpetas `md/` pre-convertidas**: se reutilizan como contexto sin volver a convertir.
- **Destino con fuentes bajo otro nombre** (`.fuentes/` o `fuentes/` en su raíz): el
  inventario propone migrarlas a `_fuentes/` y actualizar las páginas que las citan; si una misma
  fuente difiere entre las dos carpetas, el flujo se detiene y pregunta.

## 7. Criterios de Aceptación

| ID | Dado | Cuando | Entonces | Test |
|---|---|---|---|---|
| AC-01 | Un proyecto con código fuente sin documentación previa | Se invoca el flujo con los cuatro parámetros completos | Se genera documentación para cada módulo detectado, el sitio compila sin errores, la navegación está actualizada y existe el artefacto `.ai/sessions/YYYY-MM-DD/` en el destino | Sin test |
| AC-02 | Un proyecto con documentación existente, parte vigente y parte desactualizada | Se invoca el flujo | Se actualiza solo lo desactualizado; lo vigente se conserva verbatim; no se crea contenido duplicado | Sin test |
| AC-03 | Un flujo invocado con el parámetro Destino vacío | Se inicia la ejecución | El flujo se detiene, informa del campo faltante y pide al usuario que lo complete antes de continuar | Sin test |
| AC-04 | Un proyecto con un módulo ya documentado que no ha cambiado | Se ejecuta el inventario | El módulo recibe estado C (vigente) y no se genera ni modifica ninguna página para él | Sin test |
| AC-05 | Dos orígenes: un proyecto Python y un PDF de normativa | Se invoca el flujo | La Fase 0a presenta una tabla con los tipos detectados (CÓDIGO y NORMATIVA), el usuario confirma, y el PDF enriquece las reglas de negocio de la documentación funcional sin generar página propia | Sin test |
| AC-06 | Todos los orígenes indicados son MATERIAL (sin ningún proyecto de código) | Se inicia la ejecución | El flujo se detiene con un mensaje que informa que se requiere al menos un origen de tipo CÓDIGO y orienta al prompt de arquetipo directo | Sin test |
| AC-07 | Cualquier sesión de `/document-project` completada | El flujo llega al RESUMEN | Existe el artefacto `.ai/sessions/YYYY-MM-DD/` con los tres ficheros obligatorios (`00_REQUEST.md`, `00_CONTEXT_SNAPSHOT.md`, `TRACEABILITY.md`) y se propone un commit Conventional Commits | Sin test |
| AC-08 | Un destino con generador Zensical, `hooks:` en `mkdocs.yml` y un script de build que no ejecuta esos hooks | Se ejecuta el flujo | El inventario y DOWNLOADS reportan `TIENE_PIPELINE_SIN_HOOKS = false` y el Gap A4 con la acción de actualizar el script; los plugins no soportados aparecen como hallazgo en RESUMEN; no se crea `zensical.toml` | Sin test |
| AC-09 | Un origen con PDFs convertidos en `md/`, documentado en su propio repositorio o en uno aparte | Se ejecuta el flujo | Los `.md` convertidos quedan copiados en `_fuentes/<origen>/…` de la raíz del destino, fuera de `docs/`; el inventario los lista y el commit propuesto los incluye | Sin test |
| AC-10 | Un destino que ya guarda fuentes convertidas en `.fuentes/` | Se ejecuta el flujo y el usuario confirma la migración | Las fuentes pasan a `_fuentes/`, las páginas que las citaban apuntan a la nueva ruta y no queda ninguna carpeta `.fuentes/` | Sin test |
| AC-11 | Un destino documentado con el generador por defecto, sin publicación web | Se completa el flujo | Existe `VER_DOCUMENTACION.md` en la raíz del destino con las secciones fijas 0-7, sin marcadores por rellenar, con la ruta web marcada "No aplica" y los comandos para Windows, macOS y Linux | `tests/test_docs_conformance.py::test_view_instructions_filled_for_doc_ia` |
| AC-12 | Un destino ya documentado, con su punto de historial guardado, cuyo proyecto cambia en un solo módulo | Se relanza el flujo sin indicar modo | El inventario se limita a los ficheros cambiados y a las páginas que los citan (más sus ejemplos), el resto queda vigente sin leerse, y el cierre guarda el nuevo punto en `.ai/doc_state.json` | Sin test |

Verificación: ejecutar `/document-project` (Claude Code) o
`Lee y aplica .github/prompts/document_project.prompt.md` con los cuatro parámetros en
cualquier plataforma IA soportada. El flujo se ejecuta en el chat y no tiene tests
automatizados.

## 8. Glosario de Dominio

| Término | Definición |
|---|---|
| Origen | Ruta raíz del proyecto cuyo código y estructura se van a documentar; puede ser único o múltiple |
| Destino | Ruta donde se escriben los archivos de documentación generados |
| Estado A | Módulo sin página de documentación existente; acción derivada: CREAR |
| Estado B | Módulo con página existente pero desactualizada respecto al código actual; acción derivada: ACTUALIZAR |
| Estado C | Módulo con página existente y vigente; acción derivada: OMITIR |
| Arquetipo formal | Plantilla de documentación con estructura fija y audiencia definida (ver [Arquetipos Formales](archetypes.md)) |
| Generador | Herramienta de sitio estático que construye el HTML a partir de los archivos Markdown (`mkdocs-material` por defecto) |
| Tipo de origen | Naturaleza del origen; determina el tratamiento documental. Nueve tipos: `CÓDIGO`, `NORMATIVA`, `ESPECIFICACIÓN`, `UI/PANTALLAS`, `REFERENCIA`, `CONTRATO`, `INFRAESTRUCTURA`, `MANUAL`, `BASE DE DATOS`. Catálogo completo: [Tipos de Origen](origin_types.md) |
| MATERIAL | Término colectivo para orígenes que no son de tipo CÓDIGO; su contenido enriquece secciones de los arquetipos del proyecto CÓDIGO principal sin generar páginas propias |
| `CONTRATO` | Especificaciones machine-readable de las APIs y modelos de datos del propio proyecto (OpenAPI, AsyncAPI, GraphQL, Protobuf, SQL DDL, DBML…); enriquece Arquetipo 2 §1 y §2 y Arquetipo 12 §5 |
| `INFRAESTRUCTURA` | Artefactos IaC y de despliegue del propio proyecto (Terraform, Kubernetes, Docker, Ansible…); enriquece Arquetipo 2 §4 y Arquetipo 6C §3 › Despliegue |
| `MANUAL` | Documentación narrativa ya escrita para el propio proyecto (manuales de usuario, guías de administrador, runbooks…); enriquece Arquetipos 3a, 3b, 6 y 7 |
| Fase 0-pre | Adquisición de orígenes: copia a `_staging/` del destino lo que no es una carpeta local de trabajo (documentos con versión, carpetas de red, SharePoint sincronizado, repositorios remotos) antes de clasificarlo |
| Fase 0a | Paso de clasificación de orígenes ejecutado antes del inventario cuando hay ≥2 orígenes o el único origen no es CÓDIGO; requiere confirmación del usuario antes de continuar |
| Fase 0b | Sincronización visual obligatoria al inicio de toda sesión: verificar assets CSS/JS, `mkdocs.yml` (sin `navigation.sections`), `.gitignore` con patrones estándar |
| Carpeta `md/` | Artefactos generados por `convert_to_md.py` en la Fase 0c: versiones Markdown de documentos binarios del origen. No generan páginas propias |
| `_fuentes/` | Copia de las carpetas `md/` en la raíz del destino, fuera de `docs/`; es lo que se lee como contexto en Fases 2-4 y lo que cita la evidencia. Único nombre válido |
| Contexto `.ai/*.md` | Ficheros de contexto persistente del proyecto (`product.md`, `architecture.md`, `glossary.md`, `runtime.md`, `standards.md`); creados en la primera sesión de un destino nuevo |
| Estrategia | Forma de documentar múltiples orígenes de tipo CÓDIGO: `federado` (cada proyecto independiente), `hub+satélite` (un proyecto concentra el destino), `monorepo` (un `mkdocs.yml` raíz agrupa secciones); nunca se autodetecta |
| Kit de documentación | Lo que deja doc_ia en el destino para relanzar su documentación: `.doc_ia/`, lanzadores `/documentar`, `DOCUMENTAR.md` y su registro. Ver [Kit de Documentación](kit.md) |
| Prompt de instancia | `.ai/prompts/documentar.prompt.md` del destino: parámetros y decisiones del proyecto que `/documentar` aplica; lo mantiene el cierre de sesión |
| Cierre de sesión | Paso final obligatorio del flujo: crea los artefactos `.ai/sessions/YYYY-MM-DD/` en el destino, actualiza o crea `.ai/*.md` si es primera sesión, y propone un commit Conventional Commits con el resumen de la sesión |

??? note "Evidencia"

    | Elemento | Fuente | Confianza |
    |---|---|---|
    | Regla «Cuatro parámetros obligatorios» | `.github/prompts/document_project.prompt.md::VALIDACIÓN (bloqueante)` | ✅ |
    | Regla «Adquisición de orígenes (Fase 0-pre)», precondición de formas de origen y postcondición de `_staging/` | `.github/prompts/document_project.prompt.md::Fase 0-pre`, `scripts/snapshot_sources.py::sync_source`, `::resolve` | ✅ |
    | Regla «Clasificación de orígenes» | `.github/prompts/document_project.prompt.md::Fase 0a` | ✅ |
    | Regla «Inventario previo a generación» | `.github/prompts/document_project.prompt.md::Fase 1` | ✅ |
    | Regla «Generación en el chat» | `.github/prompts/document_project.prompt.md::Política innegociable` | ✅ |
    | Regla «Sin inventar» | `CLAUDE.md::Contrato documental obligatorio` | ✅ |
    | Regla «Preservación de lo vigente» | `.github/prompts/document_project.prompt.md::Protocolo ACTUALIZAR (estado B)` | ✅ |
    | Regla «`downloads.md` siempre obligatorio» | `.github/prompts/document_project.prompt.md::Fase 7b` | ✅ |
    | [COB-DOCPROJ-002](../decisiones/docproj_decisiones.md#cob-docproj-002) · Regla «Instrucciones de visualización siempre» y AC-11 | `.github/prompts/document_project.prompt.md::Fase 7c`, `.github/templates/VER_DOCUMENTACION.template.md`, `tests/test_docs_conformance.py::test_view_instructions_rule_everywhere` (coherencia de las instrucciones; el resultado solo se comprueba sobre doc_ia) | ⚠️ (decisión: Aceptar riesgo) |
    | [COB-DOCPROJ-003](../decisiones/docproj_decisiones.md#cob-docproj-003) · Regla «Relanzar solo sobre lo cambiado» y AC-12 | `.github/prompts/document_project.prompt.md::Fase 1` (modo incremental), `::Devuelve en este orden` (punto 10, Baseline), `scripts/doc_trace.py::check_changes`, `tests/test_docs_conformance.py::test_incremental_mode_rule_everywhere` (coherencia de las instrucciones; el flujo completo no tiene test) | ⚠️ (decisión: Aceptar riesgo) |
    | Regla «Sincronización visual (Fase 0b)» | `.claude/commands/document-project.md::Sincronización de Configuración Visual (Fase 0b)`, `.github/prompts/document_project.prompt.md::Fase 0b` | ✅ |
    | Reglas «Versión vigente de un documento», «Credenciales fuera del repositorio» e «Integraciones» | `.github/prompts/document_project.prompt.md::Fase 0-pre` (Versión vigente), `::Fase 0c — Paso 4b`, `::Fase 3b`, `scripts/snapshot_sources.py::replace_source`, `scripts/redact_secrets.py::redact_tree` | ✅ |
    | Regla «Documentos pre-convertidos (`md/`)» | `.github/prompts/document_project.prompt.md::Fase 0c — Paso 0` | ✅ |
    | [COB-DOCPROJ-004](../decisiones/docproj_decisiones.md#cob-docproj-004) · Regla «Fuentes convertidas en `_fuentes/`», AC-09 y AC-10 | `.github/prompts/document_project.prompt.md::Fase 0c — Paso 5`, `tests/test_docs_conformance.py::test_sources_folder_is_canonical` (coherencia de las instrucciones, no del resultado) | ⚠️ (decisión: Aceptar riesgo) |
    | Regla «Origen BASE DE DATOS», precondición `BD` y postcondición `docs/bd/` | `.github/prompts/document_project.prompt.md::Origen BASE DE DATOS (opción BD)`, `::Devuelve en este orden` (Trazabilidad para la BD), `.claude/commands/document-project.md` (Inputs requeridos), `scripts/db_trace.py::import_pages`, `::build_tracemap` | ✅ |
    | Regla «Origen WEB» y postcondición `docs/manual/` | `.github/prompts/document_project.prompt.md::Origen WEB (opción WEB)`, `::Fase 3c`, `::Devuelve en este orden` (CIERRE «Capturas»), `.claude/commands/document-project.md` (Inputs requeridos), `scripts/web_captures.py::publish`, `::check` | ✅ |
    | Regla «Kit de documentación en el destino», postcondición del kit y flujo `/documentar` | `.github/prompts/document_project.prompt.md::Kit de documentación en el destino y <doc_ia>`, `::Fase 0b` (Kit de lanzamiento), `::Devuelve en este orden` (puntos 9 y 10), `.claude/commands/document-project.md::Sincronización de Configuración Visual (Fase 0b)`, `.github/templates/kit/documentar.command.md`, `scripts/kit.py::sync` | ✅ |
    | Regla «Contexto persistente `.ai/*.md`» | `.claude/commands/document-project.md::Devuelve en este orden` (tabla de ficheros `.ai/`) | ✅ |
    | Postcondición y caso «registro de decisiones» | `.github/prompts/document_project.prompt.md::Fase 3` (Decisiones de cobertura), `::Devuelve en este orden` (punto 9), `.github/DOCUMENTATION_STANDARD.md::3.18` | ✅ |
    | Precondición «generador instalado para `--verify-build`» | `.github/prompts/document_project.prompt.md::Fase 7` | ✅ |
    | Postcondición «commit propuesto, no ejecutado» | `.github/prompts/document_project.prompt.md::Devuelve en este orden` (punto 10) | ✅ |
    | [COB-DOCPROJ-005](../decisiones/docproj_decisiones.md#cob-docproj-005) · AC-01 | `.github/prompts/document_project.prompt.md::Devuelve en este orden` | 🔍 → ⚠️ (decisión: Reclasificar) |
    | AC-02 | `.github/prompts/document_project.prompt.md::Protocolo ACTUALIZAR (estado B)` | ✅ |
    | AC-03 | `.github/prompts/document_project.prompt.md::VALIDACIÓN (bloqueante)` | ✅ |
    | AC-04 | `.github/prompts/document_project.prompt.md::Fase 1` | ✅ |
    | AC-05 | `.github/prompts/document_project.prompt.md::Fase 0a` | ✅ |
    | AC-06 | `.github/DOCUMENTATION_STANDARD.md::3.10 Documentación con Múltiples Orígenes` (caso degenerado) | ✅ |
    | AC-07 | `.github/prompts/document_project.prompt.md::Devuelve en este orden` (punto 10) | ✅ |
    | Regla «Zensical sin pérdidas silenciosas» y AC-08 | `.github/prompts/document_project.prompt.md::Reglas por generador: Zensical` | ✅ |
