# Prompt: reference_doc — Referencia del Sistema (Arquetipo 12)

Genera o actualiza la **referencia consultable** de **doc_ia** (o de un proyecto origen) usando
solo información verificable del código, `pyproject.toml`, ficheros de configuración, README y
material de tipo `CONTRATO`.

**Cuadrante Diátaxis**: *Reference* — información para consultar, no para leer de principio a fin.
Cada entrada se localiza por su nombre (clave, comando, código de error) y se describe de forma
seca, completa y uniforme.

**Diferencia con el Arquetipo 2 (`technical_doc`)**: el Arquetipo 2 documenta la **API interna de
un módulo** (funciones, clases, contratos para quien integra código). El Arquetipo 12 documenta la
**superficie que ve el usuario u operador de todo el sistema**: configuración, comandos,
códigos de salida, eventos e interfaces publicadas. El Arquetipo 2 enlaza aquí; no duplica.

## Instrucción al modelo

```
Actúa como technical writer especializado en documentación de referencia de herramientas
de línea de comandos, servicios y librerías.

Analiza el código real del sistema completo (no módulo a módulo): parsers de argumentos
(argparse, click, typer, commander, picocli…), lecturas de variables de entorno, ficheros de
configuración, `sys.exit`/códigos de retorno, excepciones públicas, productores/consumidores de
mensajes y especificaciones CONTRATO (OpenAPI, AsyncAPI, .proto, GraphQL).
No asumas opciones, valores por defecto ni códigos que no aparezcan en el código.

Genera la referencia en Markdown siguiendo el Arquetipo 12 con estas secciones en este orden exacto:

# Referencia — [Nombre del sistema o ámbito]

[Una frase: qué superficie cubre esta referencia y a quién va dirigida.]

## 1. Configuración
Tabla: | Clave | Origen | Tipo | Por defecto | Descripción |
Origen: `env` (variable de entorno), `fichero` (ruta del fichero de configuración) o `flag`.
Para secretos (tokens, contraseñas, claves): documenta nombre, tipo y obligatoriedad;
en "Por defecto" escribe "—" y NUNCA el valor.
Si el sistema no lee configuración: "*No aplica para este sistema.*"

## 2. CLI y Comandos
Una subsección `### <comando>` por cada punto de entrada ejecutable, con:
- Sinopsis en bloque fenced (`python scripts/x.py [opciones] <arg>`).
- Tabla: | Opción / Argumento | Tipo | Por defecto | Descripción |
Orden de las subsecciones: alfabético por nombre de comando.
Si el sistema no tiene CLI: "*No aplica para este sistema.*"

## 3. Errores y Códigos de Salida
Tabla: | Código / Error | Origen | Cuándo ocurre | Acción recomendada |
Incluye códigos de salida de proceso, excepciones públicas y códigos de error de API.
Ordena por comando y después por código ascendente.

## 4. Eventos y Mensajes
Tabla: | Evento / Mensaje | Productor | Consumidor | Payload / formato |
Colas, webhooks, eventos de dominio, hooks del sistema o mensajes de log con contrato estable.
Si no hay: "*No aplica para este sistema.*"

## 5. Interfaces Publicadas
Tabla: | Interfaz | Tipo | Contrato fuente | Descripción |
Tipo: HTTP, gRPC, GraphQL, fichero de salida, formato de intercambio.
Contrato fuente: ruta como código inline al material CONTRATO (no copies la especificación
completa; resume operaciones y enlaza a la página de docs/ si existe).
Si no hay interfaces publicadas: "*No aplica para este sistema.*"

## 6. Datos
SOLO con persistencia propia (ORM, DDL, migraciones, `.dbml`, `.avsc`) o ficheros con formato
propio que el sistema lee y escribe. Fuentes: código + material CONTRATO.
- `erDiagram` global (máx. 12 entidades; si hay más, agrupa por agregado y lista el resto).
- Tabla: | Entidad | Campo | Tipo | Restricción | Sensibilidad |
  Sensibilidad: pública / interna / personal / secreta. Campos personales → marcar "personal"
  aunque no haya normativa (alimenta el Arquetipo 8 si se activa).
- Entidades con estados: `stateDiagram-v2` con las transiciones reales del código.
Si no hay persistencia ni formatos propios: "*No aplica para este sistema.*"

??? note "Evidencia"
    Bloque plegable final, sin número de sección (DOCUMENTATION_STANDARD.md §3.16).
    Tabla: | Elemento | Fuente | Confianza |
    Una fila por clave, comando, código y interfaz.
    Fuente como código inline `ruta::símbolo` (fallback `ruta:línea`), nunca como enlace.
    Confianza: ✅ verificado · ⚠️ parcial · 🔍 inferido · ❌ gap.

---

Restricciones:
- Si una sección queda vacía, escribe "*No aplica para este sistema.*" — nunca omitas la sección
- Estilo de referencia: frases cortas, sin narrativa, sin "por qué" (eso es Explanation: ADR / 6C)
- Toda opción, valor por defecto y código debe existir en el código; si no se puede verificar,
  márcalo con 🔍 al final de la celda
- NUNCA escribas el valor de un secreto ni URLs internas; cita la ubicación
- Valores por defecto copiados literalmente del código (no parafrasear `None` como "vacío")
- NO uses la directiva --8<--; embebe sinopsis y ejemplos en bloques fenced
- Si falta información, añade subsección "### Pendiente de verificación" con preguntas concretas
- Responde SOLO con el Markdown, sin texto introductorio ni cierre
```

## Cuándo aplica

Siempre que el INVENTARIO detecte al menos una de estas señales; si no detecta ninguna,
el arquetipo no aplica y `docs/reference/` no se crea:

| Señal | Sección que alimenta |
|---|---|
| Lecturas de entorno (`os.environ`, `getenv`, `process.env`), ficheros `.env`, `*.toml`/`*.yaml`/`*.ini` de configuración | §1 |
| Parsers de CLI o `[project.scripts]` / `bin` en el manifiesto | §2 |
| `sys.exit(n)`, `process.exit(n)`, excepciones públicas exportadas | §3 |
| Colas, webhooks, buses de eventos, hooks | §4 |
| Material `CONTRATO` (OpenAPI, AsyncAPI, `.proto`, `.graphql`) | §5 |
| ORM, DDL, migraciones, `.dbml`, `.avsc`, ficheros con formato propio | §6 |

## Cómo usar este prompt

### Modo sistema completo — Claude Code

```
Lee los puntos de entrada y ficheros de configuración de [proyecto] y genera la referencia
del sistema usando .github/prompts/reference_doc.prompt.md.
Guarda en docs/reference/index.md (o docs/reference/[ámbito].md si la página supera ~300 líneas)
y añade la entrada "Referencia del Sistema" en mkdocs.yml (tras "Referencia Técnica").
No inventes opciones ni valores por defecto; márcalos con 🔍 si no son verificables.
```

### Modo sistema completo — Copilot Chat

```
#file:.github/prompts/reference_doc.prompt.md
#file:pyproject.toml
#file:[punto_de_entrada]

Genera la referencia del sistema siguiendo las instrucciones del prompt.
```

## Output esperado

Markdown con título H1 `# Referencia — …`, frase introductoria, las 6 secciones del
Arquetipo 12 numeradas (`## 1.`–`## 6.`) y el bloque plegable `??? note "Evidencia"` final.
Secciones vacías con `*No aplica para este sistema.*`.
