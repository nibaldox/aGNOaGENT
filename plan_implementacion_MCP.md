# Plan de Implementación: Integración de OpenWeatherMap en Servidor MCP Python

## Objetivo

Integrar la funcionalidad de obtención de datos meteorológicos de OpenWeatherMap (actualmente en un servidor MCP JavaScript) en el servidor MCP Python existente (`agno/cookbook/tools/mcp/local_server/server.py`).

## Pasos de Implementación

1. **Configuración Inicial**
    * [ ] Crear/Actualizar archivo `plan_implementacion_MCP.md` (este archivo).
    * [ ] Confirmar la estrategia de reimplementación en Python.
    * [ ] Decidir el método de gestión de la API Key de OpenWeatherMap (se usará variable de entorno `OPENWEATHERMAP_API_KEY`).

2. **Desarrollo del Servidor (`server.py` en `agno/cookbook/tools/mcp/local_server/`)**
    * [ ] Importar librerías necesarias: `aiohttp` para peticiones HTTP asíncronas, `os` para variables de entorno, `json` para manejar respuestas.
    * [ ] Implementar la función `get_current_weather_owm(city: str)`:
        * [ ] Leer la `OPENWEATHERMAP_API_KEY` desde las variables de entorno.
        * [ ] Construir la URL para la API de OpenWeatherMap (endpoint de clima actual por nombre de ciudad).
        * [ ] Realizar la petición GET asíncrona usando `aiohttp`.
        * [ ] Manejar posibles errores de la petición (HTTP status codes, excepciones de red).
        * [ ] Parsear la respuesta JSON.
        * [ ] Extraer y devolver la información relevante (e.g., temperatura, descripción del clima, ciudad).
    * [ ] Registrar `get_current_weather_owm` como una herramienta MCP usando el decorador `@mcp.tool()` con nombre, descripción y esquema de parámetros adecuados.
    * [ ] Comentar o eliminar las funciones simuladas `get_weather` y `get_temperature`.

3. **Gestión de Dependencias**
    * [ ] Crear/Actualizar `requirements.txt` en la raíz del proyecto o en `agno/cookbook/tools/mcp/local_server/` para incluir `fastmcp`, `aiohttp`, `python-dotenv`.

4. **Documentación**
    * [ ] Actualizar `README.md` (general del proyecto o específico del cookbook) para:
        * [ ] Explicar la nueva funcionalidad del servidor MCP.
        * [ ] Instrucciones sobre cómo configurar la variable de entorno `OPENWEATHERMAP_API_KEY`.
        * [ ] Ejemplo de cómo llamar a la nueva herramienta desde un cliente.
    * [ ] Añadir comentarios relevantes en el código de `server.py`.

5. **Configuración de Entorno**
    * [ ] Crear un archivo `.env.example` con `OPENWEATHERMAP_API_KEY="TU_API_KEY_AQUI"`.
    * [ ] Añadir `.env` al archivo `.gitignore` para evitar subir la API key real al repositorio.

6. **Pruebas (`client.py` en `agno/cookbook/tools/mcp/local_server/`)**
    * [ ] Modificar `client.py` para que:
        * [ ] Utilice `python-dotenv` para cargar variables de entorno si se está desarrollando localmente.
        * [ ] El mensaje enviado al agente sea para probar la nueva herramienta `get_current_weather_owm` (e.g., "What is the current weather in London?").
    * [ ] Ejecutar `client.py` y verificar que:
        * [x] El servidor `server.py` se inicia correctamente.
        * [x] El agente llama a la herramienta `get_current_weather_owm` (verificado con API key hardcodeada).
        * [x] Se obtiene una respuesta real de OpenWeatherMap (verificado con API key hardcodeada).

7. **(Opcional) Implementación de Herramientas Adicionales**
    * [ ] `get_weather_forecast_owm`: Para obtener el pronóstico del tiempo.
    * [ ] `get_weather_history_owm`: Para obtener datos históricos (considerar la complejidad y si es realmente necesario para el proyecto de sismógrafos).

## Próximos Pasos Inmediatos

* Comenzar con el Paso 2: Modificación de `server.py`.
