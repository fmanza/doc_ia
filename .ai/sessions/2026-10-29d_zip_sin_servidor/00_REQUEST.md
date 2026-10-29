# REQUEST

## Session metadata
- id: 2026-10-29d
- fecha: 2026-10-29
- rama: develop
- skill: new_feature (build + tooling de ZIP + instrucciones IA del producto)
- fase solicitada: PLAN + AUDIT_PLAN (sin implementar)

## Solicitud original saneada
"ZIP que se abra sin Python ni servidor, con doble clic en index.html y con búsqueda. Lo dejé
fuera a propósito (decisión D5 del plan) porque afecta al build, a los dos generadores y a sus
tests. Es la única forma de que «sin Python» funcione de verdad; propongo hacerlo como feature
aparte. PLAN y AUDIT_PLAN."

## Antecedente
- Sesión `2026-10-29b_ver_documentacion`, decisión D5: ZIP navegable sin servidor fuera de
  alcance. Allí se retiró la «Opción B: abrir `index.html`» por falsa (`use_directory_urls: true`)
  y se añadió `test_downloads_never_offers_opening_index_html`.

## Spike (scratchpad, sin tocar el repo)
- MkDocs 1.6.1 + Material 9.8.0 y Zensical 0.0.73 con el plugin `offline`: ambos fuerzan
  `use_directory_urls: false` y escriben el índice de búsqueda como JS (MkDocs:
  `search/search_index.js`; Zensical: `search.js` en la raíz). Los dos bundles lo cargan con
  `<script>` cuando `location.protocol === "file:"`.
- Ambos inyectan `https://unpkg.com/iframe-worker/shim` en `extra.polyfills` salvo que ya exista
  una entrada que contenga `iframe-worker`. Con `extra.polyfills: [assets/vendor/iframe-worker/shim.js]`
  los dos emiten la ruta relativa correcta por página y no añaden unpkg.
- Sitios generados: 0 enlaces relativos a carpeta y 0 `<script src="http…">` en ambos.
- Zensical exige `site_dir` dentro del proyecto. El índice JS añade ~420 KB sin comprimir.
- No verificado: búsqueda real en navegador por `file://` (solo a nivel de build).

## Restricciones explícitas
- Sin dependencias Python nuevas; sin red en tests; `start-server.py` se mantiene.
- Sin commit, push ni tag hasta nueva indicación.
