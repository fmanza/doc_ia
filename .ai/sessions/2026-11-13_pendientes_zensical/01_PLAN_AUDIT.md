# PLAN + AUDIT_PLAN — Pendientes de la migración a Zensical (v0.13.0)

## Situación (2026-11-13)
- v0.12.0 publicada (`f5d9b69`). En `develop`, después: `4702805` (publicación) y `b3190ba`
  (COB-BUILDZIP-001 reclasificada, Z4 cerrada). Solo documentación.
- C3 cerrada: el usuario confirmó la búsqueda en el ZIP (doc_ia y UFV) por `file://`.
- `--builder`: lo citan `scripts/build_docs_zip.py` (`LEGACY_BUILDER_FLAG`), 2 tests, ADR-003,
  `docs/{api,functional,examples}/build_docs_zip.md`, `docs/reference/index.md` (sinopsis, código
  de salida 2, evidencia), `docs/guides/troubleshooting.md`, `EDGE_CASES.md:388` (histórico),
  `bootstrap_ai_config.prompt.md:142`, `document_project.prompt.md:785`. Los destinos llevan copia
  del script (UFV la regeneró desde 0.12.0, con `--builder`).
- Releases por versión (desde v0.11.1, dos por versión):
  - `docs-vX.Y.Z` ← `docs-zip-release.yml` (push a `main` con cambios en `docs/`, `mkdocs.yml` o
    `pyproject.toml`): ZIP + `.sha256` + `CHECKSUMS.txt`.
  - `vX.Y.Z` ← `docs-release.yml` (tag `v*`): solo el ZIP, construido otra vez.
  - Mismo nombre de fichero, huellas distintas: quien combine el ZIP de una con el `.sha256` de la
    otra ve un fallo de integridad (pasó al verificar v0.12.0).
- **Spike** (sin tocar el repo): dos builds del mismo commit con un minuto de diferencia dan un
  `site/` idéntico (97 ficheros, 0 diferencias). La diferencia de huella sale solo del ZIP
  (fecha de cada entrada) → con fecha fija el ZIP es **reproducible**.
- Zensical: versión exacta en `requirements-docs.txt` y `requirements.txt` (dos sitios, sin guarda
  de coherencia). `CONTRIBUTING.md` tiene «Actualizar Mermaid» e «Actualizar iframe-worker», pero
  no «Actualizar Zensical». Guardas existentes: `test_zensical_compat.py` (plugins, enlaces al
  ZIP), `test_mermaid_assets.py::test_theme_bundle_uses_global_mermaid[zensical]`,
  `test_no_mkdocs.py`.

## Decisiones propuestas
- **D1 — ZIP reproducible** (resuelve el punto 4 de raíz): `build_docs_zip.py::_zip` y
  `mkdocs_hooks.py::on_post_build` escriben cada entrada con `ZipInfo` y fecha fija (la del commit
  `HEAD` si hay git; si no, 1980-01-01), orden ya determinista y permisos fijos. Mismo commit →
  mismos bytes → misma huella en las dos releases. Se mantienen los dos mecanismos (regla de
  `CLAUDE.md` § Descarga offline).
- **D2 — `.sha256` también en `vX.Y.Z`**: `docs-release.yml` adjunta `dist/*.zip.sha256`.
- **D3 — `--builder` fuera en v0.13.0** (BREAKING en 0.x → versión menor): se quitan la opción, la
  constante y sus tests. Sin la opción, argparse rechaza `--builder` con código 2 («unrecognized
  arguments»); el mensaje explicativo de ADR-003 se pierde y se documenta en troubleshooting.
- **D4 — Actualizar Zensical**: sección «Actualizar Zensical» en `CONTRIBUTING.md` (paso a paso) y
  guarda de una sola versión: test que exige `zensical` y `zensical-ui` iguales en
  `requirements-docs.txt` y `requirements.txt`.

## Fases

### Q1 · `feat(build): ZIP de documentación reproducible`
- `scripts/build_docs_zip.py`: `_zip` con `ZipInfo` (fecha `_zip_date()`: `git log -1 --format=%ct`
  si hay repo, si no 1980-01-01; `external_attr` fijo; `ZIP_DEFLATED`).
- `mkdocs_hooks.py`: la misma escritura (sin importar el script: el módulo se copia a destinos y
  debe seguir siendo autónomo, stdlib).
- Tests: dos ZIP del mismo `site/` con distinta hora del sistema → mismos bytes; entradas con la
  fecha fijada; el ZIP `latest` y el versionado contienen lo mismo.
- Docs: `api/functional/examples` de `build_docs_zip` (regla «ZIP reproducible», AC nuevo),
  `docs/downloads.md` (las dos releases traen el mismo fichero y la misma huella).
- EDGE_CASES: entrada «Dos releases con el mismo ZIP y huellas distintas (RESUELTO)».

### Q2 · `ci(release): la release del tag adjunta el .sha256`
- `docs-release.yml`: `files:` con `dist/doc_ia-docs-*.zip` y `dist/doc_ia-docs-*.zip.sha256`.
- Verificación tras publicar: la huella de `vX.Y.Z` = la de `docs-vX.Y.Z`.

### Q3 · `feat(build)!: retirar la opción obsoleta --builder`
- `scripts/build_docs_zip.py`: fuera `LEGACY_BUILDER_FLAG`, el argumento y la comprobación;
  `BUILDER` se mantiene.
- Tests: fuera `test_legacy_builder_flag_zensical_is_accepted`; `test_mkdocs_builder_is_rejected`
  pasa a comprobar código 2 y «unrecognized arguments» con `--builder` (cualquier valor).
- Docs: ADR-003 (nota: retirada en 0.13.0), `api/functional/examples` (AC-16 reescrito),
  `reference/index.md`, `troubleshooting.md`; prompts de producto (`bootstrap_ai_config` §142,
  `document_project` §785: «sin `--builder`»). `EDGE_CASES:388` es histórico (sección MkDocs).
- Producto: la Fase 0b, al regenerar el script del destino desde doc_ia, ya no lleva `--builder`.

### Q4 · `docs(contributing): procedimiento para actualizar Zensical` + guarda
- `CONTRIBUTING.md` § «Actualizar Zensical»: leer notas de versión; cambiar las dos versiones
  exactas (`zensical`, `zensical-ui`); revisar `ZENSICAL_SUPPORTED_PLUGINS` y `hooks:`; build y
  comparación de rutas con la versión anterior; Mermaid sin conexión (C9) y búsqueda por `file://`;
  CHANGELOG. Sincronizado a `docs/contributing.md` por el hook.
- `tests/test_zensical_compat.py`: `zensical` y `zensical-ui` con la misma versión exacta en
  `requirements-docs.txt` y `requirements.txt`.

### VERSION v0.13.0
- Incluye `4702805`, `b3190ba` y Q1-Q4. Release en `develop`, CI verde, merge a `main` con
  confirmación, CI verde, tag sobre el merge verificado, push del tag por separado (memoria
  «release-steps-separate»). Comprobación final: huellas iguales en `v0.13.0` y `docs-v0.13.0`.

## AUDIT_PLAN

| # | Hallazgo | Severidad | Tratamiento |
|---|---|---|---|
| A1 | El spike de reproducibilidad es local (Windows) y entre dos builds seguidas; las dos releases se construyen en runners Linux distintos, en momentos distintos. | Media | Q1 fija la fecha y el orden; el contenido de `site/` ya es estable. Verificación obligatoria en la propia release v0.13.0 (huellas iguales). Si difieren, D2 sigue dando a cada release su `.sha256` correcto: el usuario nunca combina huellas cruzadas sin aviso. |
| A2 | La versión de zlib puede cambiar entre imágenes del runner y alterar los bytes comprimidos. | Baja | Ambos workflows usan `ubuntu-latest` en minutos de diferencia; documentar el límite en EDGE_CASES. No se promete reproducibilidad entre sistemas. |
| A3 | `mkdocs_hooks.py` se copia a destinos y no puede depender del script. | Media | Implementación propia de 5-6 líneas en el módulo (stdlib); test para cada uno. |
| A4 | Fecha del commit: en el ZIP del CI con `fetch-depth: 0` hay git; en un ZIP construido fuera de un repo (destino sin git) no. | Baja | Fallback 1980-01-01 (mínimo de ZIP). Test de los dos caminos. |
| A5 | Quitar `--builder` rompe llamadas existentes, incluidas las copias del script en destinos (UFV). | Media | BREAKING declarado en v0.13.0 (CHANGELOG, commit `!`). Los destinos se actualizan en su Fase 0b; el error de argparse (código 2) es explícito. |
| A6 | Al quitar la opción se pierde el mensaje que remite a ADR-003. | Baja | `troubleshooting.md` y `reference/index.md` documentan «unrecognized arguments: --builder» → quitar la opción. |
| A7 | La guarda de una versión no cubre `docs/downloads.md` («Zensical 0.1.1») ni `ADR-003`, que citan la versión en prosa. | Baja | La sección de CONTRIBUTING lista esos sitios; no se automatiza (prosa). |
| A8 | Q1 cambia la huella de todo ZIP futuro respecto a builds anteriores (fecha de entradas). | Informativo | Esperado; no afecta a releases ya publicadas. |
| A9 | Los dos workflows siguen construyendo dos veces el mismo sitio. | Informativo | Se mantiene a propósito (regla de `CLAUDE.md`: los dos mecanismos deben existir). Reutilizar el ZIP de `docs-v*` en la release del tag sería otra opción, más frágil (dependencia entre workflows y filtro `paths`). |

**DoD**: ruff, mypy strict, pytest; `build_docs_zip.py` con exit 0; dos ejecuciones seguidas →
ZIP idéntico (`cmp`); `doc_trace` drift/decisions/llms/matrix sin hallazgos; `test_no_mkdocs.py`;
CI verde.

## Veredicto
- **Q1: GO** (verificación de A1 en la release).
- **Q2: GO.**
- **Q3: GO** (BREAKING en v0.13.0).
- **Q4: GO.**
- **VERSION v0.13.0: GO_CONDICIONAL** a confirmar merge, tag y push en cada paso.
