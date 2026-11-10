# Prompt: user_manual_doc — Manual de Funcionamiento (Arquetipo 15)

Genera o actualiza el **manual de funcionamiento** de una aplicación tal como está **desplegada**
en un entorno (p. ej. PRE): qué puede hacer cada rol, qué necesita antes de empezar y cómo se usa
cada pantalla. Parte de las capturas del origen WEB (material `UI/PANTALLAS`) y del código, que
sustenta lo que se afirma. Norma: `DOCUMENTATION_STANDARD.md` §3.20.

**Diferencia con otros arquetipos**: el Arquetipo 1 explica qué hace un módulo y sus reglas, para
producto; el 3a resuelve una tarea concreta. El Arquetipo 15 recorre la aplicación desplegada
pantalla a pantalla para quien la usa, y enlaza a ambos en lugar de repetirlos.

## Instrucción al modelo

```
Actúa como technical writer de manuales de usuario y analista funcional.

0. ENTRADA — origen WEB ya adquirido (document_project.prompt.md § Origen WEB):
   - Capturas revisadas y publicadas en docs/assets/manual/<origen>/ (web_captures.py publish).
   - .ai/captures.json: entorno, versión desplegada, rol de cada captura.
   - Origen CÓDIGO: menús, rutas, controladores, formularios, validaciones, mensajes, permisos.
   - Notas del recorrido de solo lectura (modo navegador), si las hay.

1. MAPA — áreas funcionales (menú o módulo de la aplicación) × roles × pantallas, a partir del
   menú del código y de las capturas. Una página por área.

2. PORTADA → docs/manual/index.md
# Manual de funcionamiento — [Aplicación]
## 1. Propósito y Destinatarios
   Para qué sirve la aplicación (2-3 frases) + tabla | Rol | Qué puede hacer | Áreas |
## 2. Requisitos de Uso
   Navegador soportado, permisos y roles, acceso y red (VPN, certificados, inicio de sesión),
   requisitos previos del negocio (datos o procesos que deben existir), y una nota con el
   entorno, la versión desplegada y la fecha de las capturas. Nunca la URL del entorno.
## 3. Acceso al Sistema
## 4. Mapa de Pantallas
   flowchart de navegación (§3.17: accTitle/accDescr, ≤ 12 nodos) + lista de áreas enlazadas.
??? note "Evidencia"

3. ÁREA → docs/manual/<área>.md
# [Área]
## 1. Para Qué Sirve
## 2. Antes de Empezar          (rol, permisos, datos que deben existir)
## 3. Pantallas
   Por pantalla: ### [Pantalla] + captura con texto alternativo
   ![Descripción de lo que muestra](../assets/manual/<origen>/<fichero>.png)
   + tabla | Campo / acción | Descripción | Obligatorio |
## 4. Tareas Paso a Paso       (### [Tarea] *(Rol)* + pasos numerados; enlace al 3a si existe)
## 5. Mensajes y Errores       | Mensaje | Cuándo aparece | Qué hacer |  (enlace al Arq. 12)
## 6. Preguntas Frecuentes
??? note "Evidencia"
   | Afirmación | Fuente | Confianza |
   Fuente: la captura (docs/assets/manual/<origen>/<fichero>) y, si se verifica, `ruta::símbolo`.

4. FRONTMATTER de cada página: arquetipo "15" y en fuentes: las capturas que cita y los ficheros
   de código que la sustentan (doc_trace.py stamp <página> --source …).
```

## Restricciones

- No inventes pantallas, campos, botones, mensajes ni permisos. Lo visto en la captura sin
  código localizado: 🔍. Lo que está en el código y no aparece en la web (o al revés), o un
  literal distinto: ⚠️ y ficha `COB-WEB-<NNN>` (Arquetipo 13); la decisión es humana.
- **Solo lectura**: los flujos con escritura se describen con las capturas que aporta el usuario;
  nunca se ejecutan en el entorno para documentarlos.
- **Datos personales**: los valores de ejemplo en tablas y pasos son ficticios evidentes. Si una
  captura publicada muestra datos reales, se detiene la página y se avisa: debe retirarse y
  sustituirse (`web_captures.py publish` con la nueva), nunca recortarse en el texto.
- **La URL del entorno no se escribe** en ninguna página: se nombra el entorno (PRE) y la versión.
- Cada captura citada lleva texto alternativo que describe lo que muestra (no «captura 1»).
- Lenguaje de usuario: sin nombres de clases, tablas ni endpoints en el cuerpo; solo en la
  Evidencia.
- Secciones vacías: `*No aplica para esta área.*`.
- Responde solo con el Markdown de cada página.

## Cuándo aplica

Solo con la opción `WEB` de `/document-project` y un origen `CÓDIGO` (`DOCUMENTATION_STANDARD.md`
§3.20). Sin `WEB`, `docs/manual/` no se crea.

## Cómo usar este prompt

### Claude Code

```
Genera el manual de funcionamiento de [aplicación] en docs/manual/ siguiendo
.github/prompts/user_manual_doc.prompt.md, con las capturas de docs/assets/manual/<origen>/ y el
código de [origen]. Añade la sección «Manual» a mkdocs.yml (pestaña propia si quedan pestañas
libres; si no, dentro de «Guías») y termina con web_captures.py check.
```

### Copilot Chat

```
#file:.github/prompts/user_manual_doc.prompt.md
#file:.ai/captures.json
#file:[menú o controlador del área]

Genera la página del área siguiendo las instrucciones del prompt.
```

## Output esperado

`docs/manual/index.md` y una página por área, con las secciones numeradas del Arquetipo 15,
capturas con texto alternativo y el bloque `??? note "Evidencia"` final; `web_captures.py check`
sin hallazgos.
