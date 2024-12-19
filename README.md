# Bot

Este proyecto es un bot que utiliza un modelo de lenguaje de Azure para responder a consultas. El bot está construido utilizando **FastAPI** y sigue una arquitectura modular, lo que facilita su mantenimiento y escalabilidad.

## 📑 Tabla de Contenidos

- [📂 Estructura del Proyecto](#estructura-del-proyecto)
- [🚀 Características](#características)
- [🔧 Configuración](#configuración)
  - [📋 Requisitos Previos](#requisitos-previos)
  - [🛠️ Instalación](#instalación)
  - [🗝️ Configuración de Variables de Entorno](#configuración-de-variables-de-entorno)
- [🏃‍♂️ Ejecutando la Aplicación](#ejecutando-la-aplicación)
- [🧪 Pruebas](#pruebas)
- [🛠️ Tecnologías Utilizadas](#tecnologías-utilizadas)
- [📂 Logging](#logging)
- [🌐 Creación de Entorno Virtual](#creación-de-entorno-virtual)
- [🔢 Control de Versiones](#control-de-versiones)
- [📝 Licencia](#licencia)

## 📂 Estructura del Proyecto

<details>
<summary>Ver estructura del proyecto</summary>

```plaintext
bot/
├── .gitignore
├── .bumpversion.cfg
├── requirements.txt
├── logs/
│   ├── __init__.py
│   └── logger_manager.py
├── app/
│   ├── __init__.py
│   ├── __version__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints.py
│   │   │   └── manejadores/
│   │   │       ├── __init__.py
│   │   │       └── manejadores.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user_model.py
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── succes/
│   │       ├── __init__.py
│   │       └── app_request.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── vacation.py
│   │   ├── llm.py
│   │   └── holiday.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── session.py
│   └── __version__.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_azure_service.py
│   │   ├── memory/
│   │   │   ├── __init__.py
│   │   │   └── memory_manager.py
│   │   └── tools/
│   │       ├── __init__.py
│   │       ├── base_tool.py
│   │       ├── tool_manager.py
│   │       └── functions/
│   │           ├── __init__.py
│   │           ├── api_request_tool.py
│   │           ├── semantic_search_tool.py
│   │           ├── principales/
│   │           │   ├── __init__.py
│   │           │   ├── request.py
│   │           │   └── azure_ai_search.py
│   │           └── auxiliares/
│   │               └── __init__.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_llm_service.py
│   │   └── test_api_endpoints.py

```
</details>

## 🚀 Características

- **FastAPI**: Framework moderno y de alto rendimiento para construir APIs con Python.
- **Azure OpenAI**: Integración con los modelos de lenguaje de Azure para generar respuestas inteligentes.
- **Arquitectura Modular**: Facilita el mantenimiento y la escalabilidad del proyecto.
- **Herramientas Personalizadas**: Implementación de herramientas para búsquedas semánticas y solicitudes API.
- **Gestión de Vacaciones y Festivos**: Funcionalidades para gestionar vacaciones y festivos de empleados.
- **Pruebas Automatizadas**: Conjunto de pruebas para garantizar la calidad del código.
- **Versionado Semántico**: Control de versiones utilizando SemVer.
- **Logging**: Implementación de `logging` para un mejor seguimiento y depuración.


## 🔧 Configuración

### 📋 Requisitos Previos

- **Python 3.11.8**
- **Git**

### 🛠️ Instalación

1. **Clona el repositorio:**

    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd bot
    ```

2. **Crea un entorno virtual y actívalo:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # En Windows usa `.venv\Scripts\activate`
    ```

3. **Instala las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

### 🗝️ Configuración de Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto y añade tus credenciales de Azure y otras configuraciones necesarias:

```env
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_MODEL_DEPLOYMENT_NAME=your_deployment_name
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_VERSION=your_version
AZURE_SEARCH_API_KEY=your_search_api_key
AZURE_SEARCH_ENDPOINT=your_search_endpoint
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=your_embedding_deployment
```

_Asegúrate de mantener tus credenciales seguras y no compartir este archivo públicamente._

### 🏃‍♂️ Ejecutando la Aplicación:
Desde la raíz del proyecto `bot/`, puedes ejecutar la aplicación de dos formas:

1. **Usando Uvicorn directamente:**
    ```bash
    uvicorn app.main:app --reload --port 5000
    ```

2. **Usando el script `start_app.ps1`:**
    ```powershell
    ./start_app.ps1
    ```
## 📂 Logging

El proyecto implementa un sistema de logging personalizado para proporcionar un seguimiento adecuado de las operaciones críticas y facilitar la depuración.

### 🔧 Configuración del sistema de logs
La funcionalidad de logs se implementa a través de una clase `LoggerManager` que centraliza la creación de distintos loggers, permitiendo que cada uno registre información en archivos específicos y con diferentes niveles de detalle.

Estructura de los logs:
- **logs/app.log**: Para registrar eventos generales de la aplicación, con nivel de logueo `INFO` por defecto.
- **logs/llm.log**: Para registrar las interacciones con el modelo de lenguaje (LLM), con nivel de logueo `DEBUG` por defecto para capturar más detalle en las solicitudes y respuestas del LLM.
- **logs/auth.log**: Para registrar eventos relacionados con la autenticación de usuarios, con nivel de logueo `WARNING` por defecto.

Funciones principales de logging:
- **get_app_logger**: Genera un logger para los eventos generales de la aplicación.
- **get_llm_logger**: Genera un logger especializado para las interacciones con el modelo LLM.
- **get_auth_logger**: Genera un logger para los eventos relacionados con la autenticación.
- **get_custom_logger**: Permite crear loggers personalizados para otros módulos o propósitos específicos.

Ejemplo de uso:
```bash
from logs.logger_manager import get_app_logger, get_llm_logger

# Logger general de la aplicación
app_logger = get_app_logger()

# Logger especializado para el LLM
llm_logger = get_llm_logger()

# Registrar un evento de nivel INFO en app.log
app_logger.info("La aplicación ha arrancado correctamente.")

# Registrar un evento de nivel DEBUG en llm.log
llm_logger.debug("Solicitud al LLM recibida con el siguiente contenido: {...}")

```


### 🧪 Pruebas
Las pruebas están ubicadas en la carpeta `app/tests/`. Para ejecutarlas, puedes usar `pytest`.
Asegúrate de que el entorno virtual esté activado y ejecuta:
```bash
pytest
```
Esto ejecutará todos los archivos de prueba y mostrará los resultados.

### 🛠️ Tecnologías Utilizadas
- **FastAPI:** Framework para construir APIs.
- **Uvicorn:** Servidor ASGI para ejecutar aplicaciones FastAPI.
- **Azure OpenAI:** Servicios de inteligencia artificial de Azure.
- **LangChain:** Biblioteca para construir aplicaciones de lenguaje.
- **Pydantic:** Validación de datos mediante modelos.
- **aiohttp:** Cliente HTTP asíncrono.
- **Python-dotenv:** Carga de variables de entorno desde un archivo .env.
- **tiktoken:** Tokenizador para modelos de lenguaje.
- **pytest:** Framework para realizar pruebas automatizadas.
- **Logging**: Implementación de `logging` para seguimiento y depuración.

### 🌐 Creacion de entorno virtual

Para crear un entorno virtual en Python llamado `.venv` y donde se instalarán las librerías, sigue estos pasos:

1. **Crear el entorno virtual:**

    Desde la raíz del proyecto, ejecuta:
    ```bash
    python -m venv .venv
    ```

2. **Activar el entorno virtual:**

    - En sistemas Unix o MacOS, ejecuta:
    ```bash
    source .venv/bin/activate
    ```
    - En sistemas Windows, ejecuta:
    ```bash
    .venv\Scripts\activate
    ```

3. **Instalar las dependencias:**

    Con el entorno virtual activado, instala las dependencias del proyecto:
    ```bash
    pip install -r requirements.txt
    ```

Recuerda activar el entorno virtual cada vez que trabajes en el proyecto para asegurarte de que estás utilizando las librerías y configuraciones correctas.

### 🔢 Control de Versiones
Este proyecto utiliza Versionado Semántico (SemVer) para el control de versiones, y se apoya en la herramienta `bump2version` para automatizar el proceso de actualización de versiones.
**📌 Modelo de Versionado Semántico (SemVer)**
El formato de versión es `MAJOR.MINOR.PATCH` (por ejemplo, 1.0.0):

- `MAJOR (X):` Cambios incompatibles en la API. Este incremento se realiza manualmente.
- `MINOR (Y):` Nuevas funcionalidades compatibles con versiones anteriores.
- `PATCH (Z):` Correcciones de errores compatibles con versiones anteriores.

**🛠️ Comandos para Actualizar Manualmente las Versiones**
Instalación de `bump2version`
Si aún no tienes `bump2version` instalado, puedes hacerlo ejecutando:
    ```bash
    pip install bump2version
    ```
1. Actualizar la Versión Mayor (MAJOR):
    ```bash
    bump2version major
    ```
2. Actualizar la Versión Mayor (MINOR):
    ```bash
    bump2version minor
    ```
3. Actualizar la Versión Mayor (PATCH):
    ```bash
    bump2version patch
    ```
### 📝 Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.