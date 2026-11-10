# PLAN — Origen WEB desplegada en PRE y manual de funcionamiento

> Versión inicial del plan. La versión vigente, corregida tras la auditoría, está en
> `02_AUDIT_PLAN.md` § Plan corregido.

## 1. Conclusión
Viable. Patrón de referencia: el origen BASE DE DATOS (opción `BD`): algo desplegado en un
entorno concreto, del que se toma una foto, que se **contrasta** con el CÓDIGO sin corregirlo.

Reglas para no romper los principios:
- **La navegación ocurre en el chat, nunca en `scripts/`** (igual que la adquisición remota de
  la Fase 0-pre). El tooling Python solo procesa el material capturado, sin red.
- **Lo desplegado se contrasta, no corrige**: cada discrepancia genera una ficha `COB-WEB-…`.

## 2. Encaje en el flujo
| Fase | Cambio |
|---|---|
| Inputs | Opción `WEB`: entorno, URL (no versionada), roles, modo de adquisición |
| 0-pre | Recorrido o capturas → `_staging/<nombre>/` (no versionado) |
| 0c | No aplica a imágenes; `redact_secrets.py` sobre el texto extraído |
| 1 | Pantallas × roles; versión desplegada frente a `Ref` del CÓDIGO; aviso de datos reales |
| 2-3 | Enriquece Arq. 1 §3 y 3a; contraste con el código → `COB-WEB-…` |
| Nuevo | Manual de funcionamiento |
| Incremental | Diferencias del manifiesto de pantallas entre versiones desplegadas |

## 3. Requisitos
**Acceso y seguridad**: autorización expresa del responsable de PRE; el agente nunca recibe
credenciales (el usuario inicia sesión en su navegador); red y VPN como prerrequisito;
recorrido de solo lectura (en PRE las integraciones pueden llamar a sistemas reales); sin
crawling masivo.

**Datos personales**: PRE suele contener copias de PRO; cuenta de pruebas con datos ficticios;
marca «revisada» por captura antes de publicar; `redact_secrets.py` no anonimiza imágenes:
revisión humana.

**Versión y entorno**: versión desplegada declarada y comparada con la `Ref`; el manual indica
entorno, versión y fecha; el manifiesto registra fecha, versión, rol, tamaño de ventana e idioma.

**Calidad**: texto alternativo en cada captura; secciones por rol; imágenes dentro de `docs/`
(el ZIP offline sigue funcionando); vigilar el tamaño del ZIP.

## 4. Arquetipo propuesto: Manual de funcionamiento
1. Propósito y destinatarios (roles) · 2. Requisitos de uso (navegador, permisos, acceso, red,
requisitos previos del negocio) · 3. Acceso al sistema · 4. Mapa de pantallas (Mermaid, ≤ 12
nodos) · 5. Pantallas: campos, acciones y validaciones · 6. Tareas paso a paso (enlace al 3a) ·
7. Mensajes y errores (enlace al 12) · 8. Preguntas frecuentes · 9. Evidencia plegable
(captura + `ruta::símbolo` + leyenda ✅ ⚠️ 🔍 ❌).

## 5. Entregables iniciales
ADR · tipo de origen y prioridad en el estándar, el prompt, el agente y el comando · prompt y
plantilla del arquetipo · `scripts/web_trace.py` (`init`/`ingest`/`changes`/`check`) · kit ·
`EDGE_CASES.md` · documentación propia · cierre de versión MINOR.

## 6. Decisiones abiertas
Herramienta de navegador · arquetipo nuevo o reutilizado · WEB sin CÓDIGO · acciones con efecto
en PRE · manual único o por rol.
