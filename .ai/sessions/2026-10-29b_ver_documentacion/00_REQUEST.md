# REQUEST

## Session metadata
- id: 2026-10-29b
- fecha: 2026-10-29
- rama: develop
- skill: new_feature (instrucciones IA del producto + tooling de ZIP)
- fase solicitada: PLAN + AUDIT_PLAN; tras «IMPLEMENT», IMPLEMENT F1-F5 + AUDIT_CODE

## Solicitud original saneada
"Es necesario crear en el destino unas instrucciones en markdown que identifiquen los requisitos
necesarios y pasos a dar para poder ver la versión de documentación, todo desde cero; es posible
que el destinatario no tenga ni Python instalado; tener en cuenta Windows, Linux y Mac.
PLAN y AUDIT_PLAN."

## Hallazgos de partida
- `use_directory_urls: true` → los enlaces del sitio son carpetas (`api/archetypes/`): abrir
  `index.html` con doble clic no navega. La «Opción B» de `docs/downloads.md` (y del Paso B3 del
  prompt, que la replica en cada destino) es falsa.
- `start-server.py` escucha en `""` (todas las interfaces).
- El ZIP versionado de `build_docs_zip.py` (el que suben las Releases) no lleva `start-server.py`
  y contiene anidado `doc_ia-docs-latest.zip`; las notas de release dicen «Open index.html».

## Objetivo operativo de esta sesión
- Fase 7c del producto: `VER_DOCUMENTACION.md` siempre en la raíz del destino, desde plantilla.
- El ZIP (latest y versionado) incluye las instrucciones y `start-server.py`, sin ZIP anidado.
- `start-server.py` solo en `127.0.0.1` y con error claro si el puerto está ocupado.
- Dogfooding en doc_ia + guardas de coherencia + docs selladas sin drift.

## Restricciones explícitas
- Sin dependencias nuevas; sin red en tests; no inventar dependencias ni URLs del destino.
- Sin commit, push ni tag hasta nueva indicación.

## Decisiones del usuario
- «IMPLEMENT» (2026-10-29): se aplican las recomendadas. D1 `VER_DOCUMENTACION.md` (`VIEW_DOCS.md`
  si idioma `en`) en la raíz del destino; D2 incluido en el ZIP; D3 Gap V1 crea
  `requirements-docs.txt`; D4 endurecer `start-server.py`; D5 (ZIP navegable sin servidor) fuera
  de alcance, como feature aparte.
