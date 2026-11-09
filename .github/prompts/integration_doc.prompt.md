# Prompt: integration_doc — Integraciones (Arquetipo 14)

Genera o actualiza la documentación de las **integraciones** de un proyecto origen: con qué
sistemas intercambia datos, en qué sentido, cuándo, con qué contrato y qué efecto tiene cada
intercambio sobre el dominio. Solo con información verificable del código, la configuración
(nombres de clave, nunca valores) y el material de diseño técnico de integraciones.

**Diferencia con otros arquetipos**: el Arquetipo 2 documenta la API interna de un módulo y en su
§4 **enlaza** a la integración que usa; el Arquetipo 12 §5 **lista** las interfaces que el sistema
publica. El Arquetipo 14 describe **el intercambio** completo, en dos vistas: funcional
(`index.md`, estructura del Arquetipo 1) y técnica (`externas.md` / `internas.md`, estructura del
Arquetipo 2). Norma: `DOCUMENTATION_STANDARD.md` §3.19.

## Instrucción al modelo

```
Actúa como arquitecto de integración y technical writer.

1. INVENTARIO de integraciones — busca en el código real:
   - Clientes HTTP/REST/SOAP (RestTemplate, WebClient, @FeignClient, HttpClient, requests, httpx,
     fetch, axios, WSDL), mensajería (JMS, Kafka, AMQP), FTP/SFTP, ficheros intercambiados.
   - Quién lanza cada integración: cron, @Scheduled, Quartz, tablas de planificador, otro sistema.
   - Identidad federada (OAuth2/OIDC, SAML, LDAP/AD) y cómo se corresponde el usuario externo con
     el interno.
   - Endpoints que el proyecto ofrece a terceros (exportaciones, webhooks, callbacks).
   - Componentes internos del producto usados en proceso o por base de datos compartida.
   - Material ESPECIFICACIÓN de diseño técnico de integraciones (contratos, periodicidad).
   Clasifica cada una como externa o interna y como entrante, saliente o bidireccional.
   Las que no alimentan el ámbito documentado van a «Fuera de alcance» (una línea cada una).

2. VISTA FUNCIONAL → docs/integraciones/index.md, con la estructura del Arquetipo 1:
# Integraciones
## 1. Objetivo y Descripción
   Contexto de negocio + tabla | Integración | Sistema | Sentido | Qué aporta al dominio |
## 2. Precondiciones
   Orden de ejecución (qué debe cargarse antes), credenciales disponibles, datos previos.
### Actores y permisos
## 3. Flujo Principal
   sequenceDiagram con el orden y la periodicidad (§3.17: accTitle/accDescr, ≤ 12 participantes
   y mensajes legibles) + párrafo por paso, sin jerga técnica.
## 4. Postcondiciones y Efectos
## 5. Reglas de Negocio
   Tabla | Regla | Descripción | Impacto si se viola |: altas, bajas lógicas, modificaciones,
   efecto sobre procesos en curso, salvaguardas ante respuestas incompletas, prioridad entre
   fuentes que comparten datos.
## 6. Límites, Flujos Alternativos y Casos Especiales
### Qué NO hace esta funcionalidad   ← incluye «Fuera de alcance»
### Flujos alternativos               (relanzar a mano, cargas completas frente a incrementales)
### Casos especiales
## 7. Criterios de Aceptación          | ID | Dado | Cuando | Entonces | Test |
## 8. Glosario de Dominio
??? note "Evidencia"

3. VISTA TÉCNICA → docs/integraciones/externas.md (y internas.md si hay dependencias internas
   relevantes), con la estructura del Arquetipo 2:
# Integraciones externas | # Integraciones internas
[Una frase: responsabilidad.]
## 1. Arquitectura y Diseño
   Diagrama (flowchart, ≤ 12 nodos) + tabla OBLIGATORIA:
   | Integración | Sentido | Mecanismo | Autenticación | Periodicidad | Datos | Destino | Errores |
## 2. Modelo de Datos / Contratos
### API pública          (endpoint u operación, firma, servicio que invoca, destino)
### Contrato de entrada  (parámetros; credenciales solo por nombre)
### Contrato de salida   (correspondencia campo origen → tabla/campo destino, histórico, logs)
### Errores y casos especiales  (errores silenciados, reintentos, transacciones, salvaguardas)
## 3. Componentes y Clases
## 4. Dependencias y Requisitos
## 5. Ejemplos Relacionados   ← enlace bidireccional con un ejemplo del Arquetipo 4
## 6. Verificación y Tests
??? note "Evidencia"
```

## Restricciones

- No inventes sistemas, endpoints, periodicidades, campos ni contratos. Lo que solo consta en el
  diseño técnico o en una wiki y no se ve en el código: 🔍 al final de la celda o frase.
- **Credenciales**: nombra la clave o el fichero; **nunca** el valor, ni URLs con secretos. Las
  credenciales en URL, sin verificar o en claro en documentos son hallazgos ⚠️ (y fichas `COB-INTEG`
  si el destino adopta el registro de decisiones).
- Si el planificador vive fuera del código (tabla de base de datos, servidor), dilo y márcalo 🔍.
- Discrepancias entre el diseño técnico y el código: manda el código; la diferencia se registra.
- Secciones vacías: `*No aplica para este módulo.*`. Evidencia con `ruta::símbolo` en código inline.
- Responde solo con el Markdown de cada página.

## Cuándo aplica

Solo si el INVENTARIO detecta al menos una señal de integración (`DOCUMENTATION_STANDARD.md`
§3.19). Sin señales, `docs/integraciones/` no se crea.

## Cómo usar este prompt

### Claude Code

```
Inventaría las integraciones de [proyecto] y genera docs/integraciones/{index,externas,internas}.md
siguiendo .github/prompts/integration_doc.prompt.md. Añade la sección «Integraciones» a mkdocs.yml
(pestaña propia si quedan pestañas libres; si no, dentro de «Técnica»).
```

### Copilot Chat

```
#file:.github/prompts/integration_doc.prompt.md
#file:[controlador o cliente de integración]

Genera la documentación de integraciones siguiendo las instrucciones del prompt.
```

## Output esperado

Tres páginas Markdown (`index.md`, `externas.md` y, si aplica, `internas.md`) con las secciones de
los arquetipos 1 y 2 numeradas, la tabla de inventario y el bloque `??? note "Evidencia"` final.
