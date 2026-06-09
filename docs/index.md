# doc_ia

Proyecto IA para documentar cualquier proyecto de desarrollo mediante instrucciones IA
ejecutadas en los chats de los servicios contratados.

!!! note "Estado: esqueleto inicial (Fase 0)"
    Esta documentación se generará con las propias instrucciones del proyecto
    (dogfooding) tras completar el bootstrap de configuración IA.
    Pendiente: arquetipos funcional, técnico, guía de usuario y ejemplos.

## Principios

- Los **orígenes a documentar** y el **destino de la documentación** son parámetros
  obligatorios de cada ejecución.
- **Sin API keys** de servicios IA en el proyecto.
- **Sin componentes programáticos IA**: el código Python es tooling determinista
  (build, ZIP offline, validación).
