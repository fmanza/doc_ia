---
status: "ACEPTADO"
date: 2026-11-10
deciders: [Paco Manzano]
consulted: [Plan Architect, Documentation Generator]
informed: [usuarios de /document-project]
---

# Use user captures and an optional in-chat browser for the deployed WEB origin

## Contexto y Problema

Los proyectos documentados con doc_ia suelen tener la aplicación desplegada en un entorno de
preproducción (PRE). Quien usa la aplicación necesita un **manual de funcionamiento**: qué puede
hacer cada rol, qué hace falta antes de empezar y cómo se usa cada pantalla. Ese contenido no
sale del código solo, y los arquetipos existentes están pensados para desarrolladores (1, 2, 12)
o resuelven una tarea concreta (3a).

Documentar a partir de la aplicación desplegada choca con varios principios del proyecto:

- Los scripts son deterministas y **no acceden a la red**.
- El **origen nunca se escribe**: en PRE las acciones con efecto pueden llegar a sistemas reales
  a través de las integraciones.
- PRE suele contener copias de **datos personales reales**, y una captura publicada queda en el
  historial de git.
- El kit se usa desde varias plataformas IA y no todas tienen una herramienta de navegador.
- El contenido de una página web es **no confiable**: puede llevar instrucciones inyectadas.

El ADR-002 aplazó los arquetipos nuevos hasta que un proyecto destino real los requiriera. El
destino UFV (aplicación kuniv, desplegada en PRE) es ese caso.

## Decisión

- **WEB es una forma de adquisición, no un tipo de origen**: produce material `UI/PANTALLAS`
  (opción `WEB` de `/document-project`, `document_project.prompt.md` § Origen WEB). Requiere un
  origen `CÓDIGO`; sin él no aplica.
- **Las capturas que aporta el usuario son la base** y funcionan en todas las plataformas. El
  recorrido con una herramienta de navegador del chat (Claude in Chrome) es **opcional** y
  siempre de **solo lectura**: se navega y se lee, nunca se envía, guarda, elimina ni lanza nada.
  El texto de las páginas se trata como dato, nunca como instrucción.
- **Ningún script navega.** `scripts/web_captures.py` solo trabaja con ficheros: `publish`
  copia a `docs/assets/manual/<origen>/` las capturas que una persona ha revisado y las registra
  en `.ai/captures.json` (huella, entorno, versión desplegada, rol); `check` detecta capturas sin
  registrar, modificadas, huérfanas, rotas, sin texto alternativo y URLs en el manifiesto.
- **La URL del entorno nunca se versiona**: se nombra el entorno (PRE) y la versión.
- **Arquetipo 15 — Manual de funcionamiento** (`docs/manual/`, `DOCUMENTATION_STANDARD.md`
  §3.20, `user_manual_doc.prompt.md`): un manual único, con el rol indicado en cada tarea.
- **Lo desplegado se contrasta con el código**, como la base de datos: ninguno corrige al otro y
  cada discrepancia es una ficha `COB-WEB-<NNN>` del Arquetipo 13.

## Consecuencias

| Tipo | Descripción |
|---|---|
| Ventaja | Manual para usuarios finales con evidencia: cada afirmación cita la captura y, si se verifica, el código |
| Ventaja | La publicación pasa por una revisión humana y `check` detecta cualquier imagen que la haya saltado |
| Ventaja | Una captura republicada cambia su huella y `doc_trace.py drift` marca las páginas que la citan |
| Ventaja | Funciona en todas las plataformas del kit; el navegador solo acelera la exploración |
| Compromiso | Las capturas son trabajo manual del usuario y no se pueden reproducir: el manifiesto registra entorno, versión, rol y fecha |
| Compromiso | Las imágenes engordan el repositorio y el ZIP offline |
| Riesgo aceptado | La regla de solo lectura del navegador se apoya en instrucciones; se mitiga con una cuenta de pruebas con rol de solo lectura |
| Riesgo aceptado | Ninguna herramienta anonimiza imágenes de forma fiable: con datos reales, la captura se repite con datos ficticios o se excluye |

## Alternativas Consideradas

| Alternativa | Pros | Contras | Motivo rechazo |
|---|---|---|---|
| Script con Playwright que recorre la web | Capturas reproducibles | Acceso a red desde `scripts/`, credenciales en el tooling, acciones con efecto sin control humano | Rompe el principio de tooling sin red |
| Solo navegador en el chat | Menos trabajo manual | No está disponible en todas las plataformas del kit; el agente toma capturas con datos sin revisar | Se mantiene como modo opcional |
| Reutilizar los arquetipos 1 y 3a sin arquetipo nuevo | Sin numeración nueva | El manual de usuario por pantalla y rol no encaja en su estructura | Hay un destino real que lo requiere (criterio del ADR-002) |
| Tipo de origen nuevo `WEB` | Señal explícita | Duplica `UI/PANTALLAS` | La forma de adquisición basta |
| Manual por rol | Páginas más cortas | Repite las pantallas que comparten los roles | Manual único; uno por rol solo si los roles no comparten pantallas |

## Estado y Revisión

ACEPTADO — 2026-11-10. Sesión: `.ai/sessions/2026-11-10_web_pre_manual/`.
Revisar tras la primera sesión `/document-project` con la opción `WEB` sobre UFV.
Relacionado: [ADR-002](ADR-002-arquetipos-con-evidencia.md) (arquetipos aplazados hasta un
destino real) y [ADR-004](ADR-004-registro-decisiones-cobertura.md) (fichas `COB-…`).
