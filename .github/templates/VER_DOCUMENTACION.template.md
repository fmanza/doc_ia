<!--
PLANTILLA — Fase 7c de document_project.prompt.md (Instrucciones de visualización).

Destino: <raíz del destino>/VER_DOCUMENTACION.md (idioma `en`: VIEW_DOCS.md, traducido entero).
Raíz del destino = carpeta con mkdocs.yml / zensical.toml (la misma que usan `_fuentes/` y `.ai/`).
Está FUERA de docs/: se lee sin instalar nada (editor de texto, GitHub, dentro del ZIP).
No enlazarlo desde docs/ (rompe `--strict`); citarlo como `código inline`.

Rellenar cada marcador con datos VERIFICADOS en el destino (nunca inventar):
  {proyecto}      nombre del proyecto (site_name)
  {zip_origen}    de dónde se obtiene el ZIP: página de Releases, página de descargas publicada
                  o "te lo facilita el equipo del proyecto" si no hay publicación verificable
  {zip_nombre}    patrón real del ZIP: {nombre}-docs-<versión>.zip (build_docs_zip.py) y/o
                  {nombre}-docs-latest.zip (hook)
  {url_publicada} URL del sitio publicado → solo si existen site_url Y un workflow/servicio que
                  lo publique; si no, §3 = "No aplica" con el motivo y se quita la fila
                  "enlace web" de la tabla de §0
  {repo_url}      URL de clonado del repositorio destino (git remote get-url origin); si no hay
                  remoto, "copia de la carpeta del proyecto"
  {python_min}    requires-python del destino; si no hay, el mínimo del generador
                  (mkdocs-material 9.x: 3.8; zensical: el de su versión fijada)
  {deps_file}     fichero de dependencias de docs del destino (requirements-docs.txt). Si no
                  existe → Gap V1: crearlo antes con versiones fijadas (patrón doc_ia)
  {generador}     mkdocs | zensical (módulo para `python -m {generador} serve`)

Secciones fijas: no se omiten ni se renumeran; si una no aplica, "No aplica" + motivo.
La Ruta B (doble clic en index.html) exige el plugin `offline` y el shim iframe-worker local
(Fase 0b); build_docs_zip.py se niega a empaquetar un site/ que no se abra sin servidor.
Borrar este comentario en el fichero generado.
-->
# Cómo ver la documentación de {proyecto}

Guía para ver la documentación en tu ordenador **partiendo de cero**: no hace falta saber
programar ni tener nada instalado. Hay instrucciones para **Windows, macOS y Linux**.

> Lo más sencillo: **extrae el ZIP y haz doble clic en `index.html`** (Ruta B). No necesitas
> instalar nada ni conexión a Internet.

## 0. ¿Qué tienes?

| Tienes… | Ruta | Necesitas instalar |
|---|---|---|
| Un enlace web a la documentación | Ruta A (§3) | Nada |
| Un fichero ZIP (`{zip_nombre}`) | Ruta B (§4) | Nada |
| El repositorio o la carpeta del proyecto | Ruta C (§5) | Python {python_min} o superior + dependencias |

Si dudas, usa la **Ruta B**: es la más sencilla y funciona sin conexión a Internet.

## 1. Requisitos por ruta

| Requisito | Ruta A | Ruta B | Ruta C |
|---|---|---|---|
| Navegador actual (Edge, Chrome, Firefox, Safari) | ✅ | ✅ | ✅ |
| Conexión a Internet | ✅ | Solo para descargar el ZIP | Para instalar dependencias |
| Descompresor de ZIP (incluido en Windows y macOS; `unzip` en Linux) | — | ✅ | — |
| Python | — | No (opcional: 3.7 o superior para el servidor local) | {python_min} o superior |
| Git | — | — | Opcional (para clonar) |

## 2. Instalar Python desde cero

Solo hace falta para la **Ruta C** y para la alternativa con servidor local de la Ruta B.

Comprueba primero si ya lo tienes (abre una terminal y escribe el comando):

| Sistema | Comprobar | Cómo abrir una terminal |
|---|---|---|
| Windows | `py --version` | Tecla Windows → escribe `Terminal` (o `PowerShell`) → Intro |
| macOS | `python3 --version` | Cmd + Espacio → escribe `Terminal` → Intro |
| Linux | `python3 --version` | Ctrl + Alt + T (o busca "Terminal") |

Si muestra `Python 3.x.y` con una versión suficiente para tu ruta, salta a la ruta.

### Windows

1. Instala con **winget** (incluido en Windows 10/11):

    ```powershell
    winget install --id Python.Python.{python_min} -e
    ```

    Alternativa: descarga el instalador oficial desde <https://www.python.org/downloads/windows/>;
    si es el instalador clásico, marca **"Add python.exe to PATH"** en la primera pantalla.

2. **Cierra y vuelve a abrir** la terminal y comprueba: `py --version`.
3. En esta guía, en Windows se usa siempre `py`. Si `py` no existe pero `python --version`
   funciona, usa `python` en su lugar.

### macOS

1. Descarga el instalador oficial (`.pkg`) desde <https://www.python.org/downloads/macos/> y
   ábrelo con doble clic. Alternativa con Homebrew: `brew install python@{python_min}`.
2. **Cierra y vuelve a abrir** Terminal y comprueba: `python3 --version`.

> Si al escribir `python3` macOS ofrece instalar las "herramientas de desarrollo de línea de
> comandos", aceptar instala un Python de Apple válido para el servidor local de la **Ruta B**; para la Ruta C
> comprueba que la versión es {python_min} o superior.

### Linux

| Distribución | Comando |
|---|---|
| Debian / Ubuntu | `sudo apt update && sudo apt install python3 python3-venv` |
| Fedora / RHEL | `sudo dnf install python3` |
| Arch | `sudo pacman -S python` |

Comprueba: `python3 --version`. Si tu distribución trae una versión inferior a {python_min},
usa la Ruta B (no necesita Python) o instala una versión más reciente desde los
repositorios de tu distribución.

## 3. Ruta A — Documentación publicada en web

Abre {url_publicada} en el navegador. No necesitas instalar nada.

## 4. Ruta B — ZIP sin conexión

1. **Descarga** `{zip_nombre}` desde {zip_origen}. Si tu fichero lleva otra versión en el
   nombre, usa ese nombre en los comandos siguientes.
2. **(Opcional) Comprueba su integridad** si te facilitan el fichero `.sha256`:

    | Sistema | Comando (el resultado debe coincidir con el `.sha256`; mayúsculas y minúsculas dan igual) |
    |---|---|
    | Windows | `Get-FileHash .\{zip_nombre} -Algorithm SHA256` |
    | macOS | `shasum -a 256 {zip_nombre}` |
    | Linux | `sha256sum -c {zip_nombre}.sha256` |

3. **Extrae** el ZIP en una carpeta (no lo abras sin extraer):

    | Sistema | Gráfico | Terminal |
    |---|---|---|
    | Windows | Clic derecho → **Extraer todo…** | `Expand-Archive .\{zip_nombre} -DestinationPath .\{proyecto}-docs` |
    | macOS | Doble clic en el ZIP | `unzip {zip_nombre} -d {proyecto}-docs` |
    | Linux | Clic derecho → **Extraer aquí** | `unzip {zip_nombre} -d {proyecto}-docs` |

4. **Abre la documentación**: entra en la carpeta extraída y haz **doble clic en `index.html`**.
   Se abre en tu navegador con menú, búsqueda y diagramas, sin servidor y sin conexión.
   Para terminar, cierra la pestaña. Nunca cambies opciones de seguridad del navegador para
   abrirla: no hace falta.

### Alternativa: servidor local

Úsala si el doble clic no funciona en tu equipo (§6) o con ZIP generados sin el plugin `offline` (al abrirlos con doble clic se ve un listado de carpetas).
Requiere Python 3.7 o superior (§2).

1. **Abre una terminal en la carpeta extraída** (la que contiene `index.html`):
    - Windows: abre la carpeta en el Explorador → clic derecho en un hueco → **Abrir en Terminal**.
    - macOS: en Terminal escribe `cd ` (con espacio) y arrastra la carpeta a la ventana → Intro.
    - Linux: clic derecho en la carpeta → **Abrir en una terminal**.
2. **Arranca el servidor local**:

    | Sistema | Comando |
    |---|---|
    | Windows | `py start-server.py` |
    | macOS / Linux | `python3 start-server.py` |

    El navegador se abre solo en <http://127.0.0.1:8000>. Si no se abre, escribe esa dirección.
    La documentación solo es visible desde tu equipo.

3. **Para terminar**, vuelve a la terminal y pulsa `Ctrl + C`.

Si la carpeta no contiene `start-server.py` (ZIP antiguo), usa en la misma carpeta
`py -m http.server 8000 --bind 127.0.0.1` (Windows) o
`python3 -m http.server 8000 --bind 127.0.0.1` (macOS / Linux) y abre <http://127.0.0.1:8000>.

## 5. Ruta C — Desde el código fuente

Requiere Python {python_min} o superior (§2) y conexión a Internet para instalar dependencias.

1. **Obtén el código**: `git clone {repo_url}` y entra en la carpeta (`cd`). Sin Git, descarga
   el código como ZIP desde la web del repositorio y extráelo. Para instalar Git:
   `winget install --id Git.Git -e` (Windows), `xcode-select --install` (macOS),
   `sudo apt install git` / `sudo dnf install git` (Linux).
2. **Crea un entorno virtual, instala las dependencias y arranca** (desde la carpeta que
   contiene `{deps_file}`). No hace falta "activar" el entorno: se usa su Python directamente.

    **Windows** (PowerShell):

    ```powershell
    py -m venv .venv
    .venv\Scripts\python -m pip install -r {deps_file}
    .venv\Scripts\python -m {generador} serve
    ```

    **macOS / Linux**:

    ```bash
    python3 -m venv .venv
    .venv/bin/python -m pip install -r {deps_file}
    .venv/bin/python -m {generador} serve
    ```

3. Abre <http://127.0.0.1:8000>. La página se recarga sola si editas la documentación.
4. Para terminar, pulsa `Ctrl + C` en la terminal.

## 6. Problemas frecuentes

| Síntoma | Causa | Solución |
|---|---|---|
| La página sale sin estilos ni menú | Se abrió `index.html` dentro del ZIP, sin extraerlo | Extrae el ZIP completo (Ruta B, paso 3) |
| Veo un listado de carpetas o el menú no navega | ZIP antiguo, que no se abre con doble clic | Ruta B, alternativa: servidor local |
| Con doble clic, la búsqueda no devuelve nada o no salen los diagramas | El navegador o una política de la empresa bloquea los scripts de ficheros locales | Ruta B, alternativa: servidor local (no cambies opciones de seguridad del navegador) |
| En Windows, la primera página tarda unos segundos | El antivirus analiza los ficheros recién extraídos | Espera: las cargas siguientes son inmediatas |
| Windows abre Microsoft Store al escribir `python` | Alias de Windows sin Python instalado | Instala Python (§2) y usa `py` |
| `'py' no se reconoce…` / `command not found` | Python no instalado o terminal abierta antes de instalar | §2 y vuelve a abrir la terminal |
| `No se puede usar el puerto 8000` / `Address already in use` | Otro programa usa el puerto | `py start-server.py --port 8001` (o `python3 …`) y abre `http://127.0.0.1:8001` |
| `error: externally-managed-environment` | Linux/Homebrew no permiten `pip` fuera de un entorno virtual | Usa el entorno `.venv` de la Ruta C, paso 2 |
| `No module named venv` / `ensurepip is not available` | Debian/Ubuntu sin `python3-venv` | `sudo apt install python3-venv` |
| `unzip: command not found` | Linux sin `unzip` | `sudo apt install unzip` / `sudo dnf install unzip` |
| `pip` no conecta (red corporativa) | Proxy | Añade `--proxy http://proxy:puerto` al comando `pip install` |
| `No module named {generador}` | Dependencias no instaladas en `.venv` | Repite la Ruta C, paso 2 |

## 7. Detener y limpiar

- **Detener** cualquier servidor: `Ctrl + C` en su terminal (o cerrar la terminal).
- **Ruta B**: borra la carpeta extraída cuando ya no la necesites.
- **Ruta C**: borra la carpeta `.venv` para liberar espacio; se recrea con la Ruta C, paso 2.
- Python puede quedarse instalado; si quieres quitarlo, desinstálalo como cualquier otra
  aplicación (Windows: Configuración → Aplicaciones; macOS: carpeta Aplicaciones/Python;
  Linux: el gestor de paquetes).
