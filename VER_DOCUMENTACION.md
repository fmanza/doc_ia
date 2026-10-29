# Cómo ver la documentación de doc_ia

Guía para ver la documentación en tu ordenador **partiendo de cero**: no hace falta saber
programar ni tener nada instalado. Hay instrucciones para **Windows, macOS y Linux**.

> Lo más sencillo: **extrae el ZIP y haz doble clic en `index.html`** (Ruta B). No necesitas
> instalar nada ni conexión a Internet.

## 0. ¿Qué tienes?

| Tienes… | Ruta | Necesitas instalar |
|---|---|---|
| Un fichero ZIP (`doc_ia-docs-0.3.0.zip`) | Ruta B (§4) | Nada |
| El repositorio o la carpeta del proyecto | Ruta C (§5) | Python 3.12 o superior + dependencias |

Si dudas, usa la **Ruta B**: es la más sencilla y funciona sin conexión a Internet.

## 1. Requisitos por ruta

| Requisito | Ruta A | Ruta B | Ruta C |
|---|---|---|---|
| Navegador actual (Edge, Chrome, Firefox, Safari) | ✅ | ✅ | ✅ |
| Conexión a Internet | ✅ | Solo para descargar el ZIP | Para instalar dependencias |
| Descompresor de ZIP (incluido en Windows y macOS; `unzip` en Linux) | — | ✅ | — |
| Python | — | No (opcional: 3.7 o superior para el servidor local) | 3.12 o superior |
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
    winget install --id Python.Python.3.12 -e
    ```

    Alternativa: descarga el instalador oficial desde <https://www.python.org/downloads/windows/>;
    si es el instalador clásico, marca **"Add python.exe to PATH"** en la primera pantalla.

2. **Cierra y vuelve a abrir** la terminal y comprueba: `py --version`.
3. En esta guía, en Windows se usa siempre `py`. Si `py` no existe pero `python --version`
   funciona, usa `python` en su lugar.

### macOS

1. Descarga el instalador oficial (`.pkg`) desde <https://www.python.org/downloads/macos/> y
   ábrelo con doble clic. Alternativa con Homebrew: `brew install python@3.12`.
2. **Cierra y vuelve a abrir** Terminal y comprueba: `python3 --version`.

> Si al escribir `python3` macOS ofrece instalar las "herramientas de desarrollo de línea de
> comandos", aceptar instala un Python de Apple válido para el servidor local de la **Ruta B**; para la Ruta C
> comprueba que la versión es 3.12 o superior.

### Linux

| Distribución | Comando |
|---|---|
| Debian / Ubuntu | `sudo apt update && sudo apt install python3 python3-venv` |
| Fedora / RHEL | `sudo dnf install python3` |
| Arch | `sudo pacman -S python` |

Comprueba: `python3 --version`. Si tu distribución trae una versión inferior a 3.12,
usa la Ruta B (no necesita Python) o instala una versión más reciente desde los
repositorios de tu distribución.

## 3. Ruta A — Documentación publicada en web

No aplica: `mkdocs.yml` declara `site_url` (`https://fmanza.github.io/doc_ia/`), pero ningún
workflow del repositorio publica el sitio (ni GitHub Pages ni `mkdocs gh-deploy`). Usa la Ruta B
o la Ruta C.

## 4. Ruta B — ZIP sin conexión

1. **Descarga** `doc_ia-docs-0.3.0.zip` desde la sección **Assets** de la release más reciente en <https://github.com/fmanza/doc_ia/releases>. Si tu fichero lleva otra versión en el
   nombre, usa ese nombre en los comandos siguientes.
2. **(Opcional) Comprueba su integridad** si te facilitan el fichero `.sha256`:

    | Sistema | Comando (el resultado debe coincidir con el `.sha256`; mayúsculas y minúsculas dan igual) |
    |---|---|
    | Windows | `Get-FileHash .\doc_ia-docs-0.3.0.zip -Algorithm SHA256` |
    | macOS | `shasum -a 256 doc_ia-docs-0.3.0.zip` |
    | Linux | `sha256sum -c doc_ia-docs-0.3.0.zip.sha256` |

3. **Extrae** el ZIP en una carpeta (no lo abras sin extraer):

    | Sistema | Gráfico | Terminal |
    |---|---|---|
    | Windows | Clic derecho → **Extraer todo…** | `Expand-Archive .\doc_ia-docs-0.3.0.zip -DestinationPath .\doc_ia-docs` |
    | macOS | Doble clic en el ZIP | `unzip doc_ia-docs-0.3.0.zip -d doc_ia-docs` |
    | Linux | Clic derecho → **Extraer aquí** | `unzip doc_ia-docs-0.3.0.zip -d doc_ia-docs` |

4. **Abre la documentación**: entra en la carpeta extraída y haz **doble clic en `index.html`**.
   Se abre en tu navegador con menú, búsqueda y diagramas, sin servidor y sin conexión.
   Para terminar, cierra la pestaña. Nunca cambies opciones de seguridad del navegador para
   abrirla: no hace falta.

### Alternativa: servidor local

Úsala si el doble clic no funciona en tu equipo (§6) o con los ZIP de doc_ia 0.3.0 y anteriores, que no se abren con doble clic.
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

Si la carpeta no contiene `start-server.py` (los ZIP de las releases 0.3.0 y anteriores no lo
incluyen), usa en la misma carpeta
`py -m http.server 8000 --bind 127.0.0.1` (Windows) o
`python3 -m http.server 8000 --bind 127.0.0.1` (macOS / Linux) y abre <http://127.0.0.1:8000>.

## 5. Ruta C — Desde el código fuente

Requiere Python 3.12 o superior (§2) y conexión a Internet para instalar dependencias.

1. **Obtén el código**: `git clone https://github.com/fmanza/doc_ia.git` y entra en la carpeta
   (`cd doc_ia`). Sin Git, descarga el código como ZIP desde la web del repositorio y extráelo. Para instalar Git:
   `winget install --id Git.Git -e` (Windows), `xcode-select --install` (macOS),
   `sudo apt install git` / `sudo dnf install git` (Linux).
2. **Crea un entorno virtual, instala las dependencias y arranca** (desde la carpeta que
   contiene `requirements-docs.txt`). No hace falta "activar" el entorno: se usa su Python directamente.

    **Windows** (PowerShell):

    ```powershell
    py -m venv .venv
    .venv\Scripts\python -m pip install -r requirements-docs.txt
    .venv\Scripts\python -m mkdocs serve
    ```

    **macOS / Linux**:

    ```bash
    python3 -m venv .venv
    .venv/bin/python -m pip install -r requirements-docs.txt
    .venv/bin/python -m mkdocs serve
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
| `No module named mkdocs` | Dependencias no instaladas en `.venv` | Repite la Ruta C, paso 2 |

## 7. Detener y limpiar

- **Detener** cualquier servidor: `Ctrl + C` en su terminal (o cerrar la terminal).
- **Ruta B**: borra la carpeta extraída cuando ya no la necesites.
- **Ruta C**: borra la carpeta `.venv` para liberar espacio; se recrea con la Ruta C, paso 2.
- Python puede quedarse instalado; si quieres quitarlo, desinstálalo como cualquier otra
  aplicación (Windows: Configuración → Aplicaciones; macOS: carpeta Aplicaciones/Python;
  Linux: el gestor de paquetes).
