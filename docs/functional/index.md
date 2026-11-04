---
arquetipo: "1-I"
fuentes:
  docs/decisiones/sistema_decisiones.md: 10002f86c9c1
  docs/functional/archetypes.md: f3f74fa25610
  docs/functional/bootstrap.md: 2eab17244b01
  docs/functional/build_docs_zip.md: f6c11b328584
  docs/functional/check_env.md: 8f77b3becbce
  docs/functional/convert_to_md.md: ae08de56054c
  docs/functional/doc_trace.md: 3def261d69a8
  docs/functional/document_project.md: 658df1cd30a5
  docs/functional/origin_types.md: 067e6238b75b
revisado: 2026-11-04
---
# Mapa Funcional — doc_ia

Vista funcional de todo el sistema: qué capacidades ofrece doc_ia, cómo se encadenan entre sí
y qué términos comparten. Cada capacidad enlaza a su página funcional detallada.

## 1. Capacidades del Sistema

| Capacidad | Módulo(s) | Página funcional | Criterios | Tests |
|---|---|---|---|---|
| Comprobar que el entorno tiene las herramientas necesarias | Tooling determinista | [Verificación de Entorno](check_env.md) | AC-01 – AC-06 | 6/6 |
| Convertir documentos previos a Markdown para usarlos como contexto | Tooling determinista | [Conversión de Documentos a Markdown](convert_to_md.md) | AC-01 – AC-13 | 12/13 |
| Empaquetar la documentación para consulta offline con verificación de integridad | Tooling determinista | [ZIP de Documentación Offline](build_docs_zip.md) | AC-01 – AC-15 | 14/15 |
| Detectar documentación desactualizada respecto al código, cruzar criterios con tests y comprobar que las decisiones de cobertura se reflejan | Tooling determinista | [Trazabilidad Docs ↔ Código](doc_trace.md) | AC-01 – AC-27 | 27/27 |
| Documentar un proyecto completo desde una única operación de entrada | Flujos IA | [Documentar un Proyecto](document_project.md) | AC-01 – AC-12 | 1/12 |
| Clasificar cada origen (código, normativa, especificación, contrato…) y decidir su tratamiento | Flujos IA | [Catálogo de Tipos de Origen](origin_types.md) | AC-01 – AC-09 | 0/9 |
| Producir documentación con estructura fija, evidencia verificable y decisiones humanas citadas | Flujos IA | [Arquetipos Formales](archetypes.md) | AC-01 – AC-14 | 14/14 |
| Trasladar el sistema de instrucciones IA a otro proyecto | Flujos IA | [Bootstrap de Configuración IA](bootstrap.md) | AC-01 – AC-05 | 1/5 |

**Cobertura de pruebas**: 75 de 101 criterios tienen un test automatizado. Los flujos IA se
ejecutan en el chat de la plataforma IA: de ellos solo se comprueba la estructura de la
documentación resultante (Arquetipos) ⚠️.

## 2. Recorridos Transversales

### Documentar un proyecto con documentos previos

```mermaid
flowchart LR
    accTitle: Recorrido de documentos previos a ZIP offline
    accDescr: Los documentos previos se convierten a Markdown, se documenta el proyecto clasificando orígenes y aplicando arquetipos, y se construye el sitio y su ZIP offline con SHA256.
    A[Documentos previos<br/>PDF, Word, Excel…] --> B[Conversión a Markdown<br/>carpeta md/]
    B --> C[Documentar un Proyecto]
    C --> D[Clasificación de orígenes]
    D --> E[Arquetipos por módulo<br/>+ Mapa Funcional + Referencia]
    E --> F[Build del sitio]
    F --> G[ZIP offline + SHA256]
```

Los documentos que el agente IA no puede leer se convierten primero a Markdown. Después,
la documentación del proyecto copia la carpeta `md/` a `_fuentes/` del destino, clasifica cada
origen y usa esa copia como contexto.
Los arquetipos generan las páginas y la build produce el sitio, que se empaqueta en el ZIP offline.

### Llevar doc_ia a otro proyecto y documentarlo

```mermaid
flowchart LR
    accTitle: Recorrido de bootstrap en un proyecto destino
    accDescr: El proyecto destino recibe la configuración IA, verifica su entorno y documenta su proyecto aplicando los arquetipos.
    A[Proyecto destino] --> B[Bootstrap de Configuración IA]
    B --> C[Destino con prompts,<br/>agentes y comandos]
    C --> D[Verificación de Entorno]
    D --> E[Documentar un Proyecto<br/>desde el destino]
    E --> F[Arquetipos aplicados]
```

El bootstrap copia al proyecto destino las instrucciones de doc_ia, incluidos los prompts de
arquetipos. A partir de ahí el destino verifica su entorno y se documenta a sí mismo con el
mismo flujo de entrada.

## 3. Actores y Permisos

*No aplica para este sistema.* doc_ia no distingue roles ni permisos: cualquier usuario con
acceso al repositorio y a una plataforma IA puede usar todas las capacidades.

## 4. Glosario Global

| Término | Definición |
|---|---|
| Origen | Lo que se documenta o se toma como fuente: el proyecto a documentar en *Documentar un Proyecto*; doc_ia como plantilla en el *Bootstrap* |
| Destino | Carpeta o repositorio donde se escriben la documentación o la configuración generadas |
| Arquetipo | Plantilla formal de documentación con secciones fijas, audiencia y ubicación definidas |
| Tipo de origen | Naturaleza de un origen (`CÓDIGO`, `NORMATIVA`, `ESPECIFICACIÓN`, `UI/PANTALLAS`, `REFERENCIA`, `CONTRATO`, `INFRAESTRUCTURA`, `MANUAL`) que decide su tratamiento |
| MATERIAL | Cualquier origen que no es código; enriquece las páginas del proyecto principal sin generar páginas propias |
| Contrato propio | Especificación de las APIs o datos del propio proyecto (`CONTRATO`); los contratos de terceros son `REFERENCIA` |
| Carpeta `md/` | Resultado de la conversión a Markdown, junto a los documentos originales |
| `_fuentes/` | Copia de las carpetas `md/` en el proyecto documentado; sirve como contexto al documentarlo y queda versionada con él |

??? note "Evidencia"

    | Elemento | Fuente | Confianza |
    |---|---|---|
    | Capacidad «Verificación de Entorno» y 6/6 tests | `docs/functional/check_env.md::§7` | ✅ |
    | Capacidad «Conversión a Markdown» y 12/13 tests | `docs/functional/convert_to_md.md::§7` | ✅ |
    | Capacidad «ZIP offline» y 14/15 tests | `docs/functional/build_docs_zip.md::§7` | ✅ |
    | Capacidad «Trazabilidad» y 27/27 tests | `docs/functional/doc_trace.md::§7` | ✅ |
    | Capacidad «Documentar un Proyecto» y 1/12 tests | `docs/functional/document_project.md::§7` | ✅ |
    | Capacidad «Tipos de Origen» y 0/9 tests | `docs/functional/origin_types.md::§7` | ✅ |
    | Capacidad «Arquetipos» y 14/14 tests | `docs/functional/archetypes.md::§7` | ✅ |
    | Capacidad «Bootstrap» y 1/5 tests | `docs/functional/bootstrap.md::§7` | ✅ |
    | Recorrido «documentos previos» | `docs/functional/convert_to_md.md::§1`, `docs/functional/document_project.md::§3` | ✅ |
    | [COB-SISTEMA-002](../decisiones/sistema_decisiones.md#cob-sistema-002) · Recorrido «bootstrap → documentar» | `docs/functional/bootstrap.md::§4`, `docs/functional/document_project.md::§2` | 🔍 |
    | Sin roles ni permisos | Ninguna página funcional define «Actores y permisos» | ✅ |
    | Doble sentido de «Origen» | `docs/functional/bootstrap.md::§8`, `docs/functional/document_project.md::§8` | ✅ |
