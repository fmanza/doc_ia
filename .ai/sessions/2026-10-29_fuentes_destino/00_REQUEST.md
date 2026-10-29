# REQUEST

## Session metadata
- id: 2026-10-29
- fecha: 2026-10-29
- rama: develop
- skill: new_feature (instrucciones IA del producto)
- fase solicitada: PLAN + AUDIT_PLAN; tras «Confirmo», IMPLEMENT F1-F3 + AUDIT_CODE

## Solicitud original saneada
"Se ha detectado que cuando se convierten los archivos se ha tomado como nombre `.fuentes/` y
`_fuentes/` en el destino; se tiene que normalizar desde las instrucciones. El destino debe
recibir siempre estos archivos. Dime impacto del cambio. PLAN y AUDIT_PLAN."

## Hallazgo de partida
- `scripts/convert_to_md.py` escribe siempre en `<origen>/md/` (`md_root = source_root / "md"`).
- Ninguna instrucción (prompt, comando, agente, SHARED_INSTRUCTIONS) dice si los convertidos van
  al destino ni con qué nombre → el agente improvisó `.fuentes/` y `_fuentes/` en sesiones distintas.
- No hay carpetas `.fuentes/` ni `_fuentes/` bajo `C:\Desarrollo` (búsqueda hasta 9 niveles):
  los destinos afectados están en otra ruta.

## Restricciones explícitas
- Normalizar desde las instrucciones (no se pide cambiar `convert_to_md.py`).
- El destino recibe siempre los convertidos.
- Sin IMPLEMENT hasta aprobación.

## Decisiones del usuario
- «Confirmo» (2026-10-29): D1 `_fuentes/`, D2 copiar también si origen = destino, D3 ruta sin cambios.
- Sin commit, push ni tag hasta nueva indicación.
