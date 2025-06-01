"""
Servidor MCP con integración de OpenWeatherMap.

Requiere `fastmcp`, `aiohttp`, y `python-dotenv`.
Instalar con: pip install fastmcp aiohttp python-dotenv

Ejecutar con: fastmcp run server.py (desde el directorio que contiene este archivo)

Se necesita una variable de entorno OPENWEATHERMAP_API_KEY.
Crear un archivo .env en el mismo directorio con:
OPENWEATHERMAP_API_KEY='tu_api_key_aqui'
"""

import os
import aiohttp
from datetime import datetime, timedelta
#from dotenv import load_dotenv  # Comentado para hardcodear la API key
from fastmcp import FastMCP

# Cargar variables de entorno desde .env
#load_dotenv() # Comentado para hardcodear la API key

mcp = FastMCP("weather_tools_pro")

def get_weather_emoji(description: str) -> str:
    desc = description.lower()
    if "cielo claro" in desc:
        return "☀️"
    if "sol" in desc and "nubes" in desc: # como "sol entre nubes"
        return "🌤️"
    if "algo de nubes" in desc or "nubes dispersas" in desc or "parcialmente nublado" in desc:
        return "🌥️"
    if "muy nuboso" in desc or "nublado" in desc or "nubes" in desc: # Captura general para nubes
        return "☁️"
    if "lluvia ligera" in desc or "llovizna" in desc:
        return "🌦️"
    if "lluvia" in desc:
        return "🌧️"
    if "tormenta" in desc:
        return "⛈️"
    if "nieve" in desc:
        return "❄️"
    if "niebla" in desc or "neblina" in desc:
        return "🌫️"
    return "🌡️" # Emoji por defecto

OPENWEATHERMAP_API_KEY = "5614c096d3b8f7ae1c97e2cb11a2cb83"  # API Key hardcodeada
OPENWEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

@mcp.tool(
    name="get_current_weather_owm",
    description="""Obtiene el clima actual detallado para una ciudad específica utilizando OpenWeatherMap.

    Args:
        city (str): El nombre de la ciudad.

    Returns:
        str: Una descripción del clima actual, temperatura, sensación térmica, humedad, velocidad del viento y nubosidad, o un mensaje de error.
    """
)
async def get_current_weather_owm(city: str) -> str:
    """Obtiene el clima actual detallado para una ciudad específica utilizando OpenWeatherMap."""
    if not OPENWEATHERMAP_API_KEY:
        return "Error: La API key de OpenWeatherMap no está configurada."

    params = {
        "q": city,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": "metric",  # Puedes cambiar a 'imperial' para Fahrenheit
        "lang": "es"      # Para respuestas en español
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(OPENWEATHER_API_URL, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    weather_main = data['weather'][0]['main']
                    weather_description = data['weather'][0]['description']
                    emoji = get_weather_emoji(weather_description)
                    temperature = data['main']['temp']
                    feels_like = data['main']['feels_like']
                    humidity = data['main']['humidity']
                    wind_speed = data['wind']['speed'] # m/s
                    clouds = data['clouds']['all'] # %

                    response_parts = [
                        f"{emoji} {city.title()}: {weather_description.capitalize()} ({weather_main}).",
                        f"🌡️ Temperatura: {temperature:.1f}°C (Sensación térmica: {feels_like:.1f}°C).",
                        f"💧 Humedad: {humidity}%.",
                        f"💨 Viento: {wind_speed} m/s.",
                        f"☁️ Nubosidad: {clouds}%."
                    ]
                    return "\n".join(response_parts)
                elif response.status == 401:
                    return f"Error: API key inválida o no autorizada. Verifica tu OPENWEATHERMAP_API_KEY."
                elif response.status == 404:
                    return f"Error: Ciudad '{city.title()}' no encontrada."
                else:
                    error_text = await response.text()
                    return f"Error al obtener el clima: {response.status} - {error_text}"
        except aiohttp.ClientConnectorError as e:
            return f"Error de conexión: No se pudo conectar a OpenWeatherMap. {e}"
        except Exception as e:
            return f"Ocurrió un error inesperado: {e}"

# Las funciones simuladas anteriores han sido eliminadas.


@mcp.tool(
    name="get_daily_weather_forecast_owm",
    description="""Obtiene el pronóstico del tiempo diario para una ciudad durante los próximos días.

    Args:
        city (str): El nombre de la ciudad.
        num_days (int): El número de días para el pronóstico (entre 1 y 5, por defecto 3).

    Returns:
        str: Un resumen del pronóstico del tiempo para cada día, o un mensaje de error.
    """
)
async def get_daily_weather_forecast_owm(city: str, num_days: int = 3) -> str:
    if not OPENWEATHERMAP_API_KEY:
        return "Error: La API key de OpenWeatherMap no está configurada."
    if not 1 <= num_days <= 5:
        return "Error: El número de días para el pronóstico debe estar entre 1 y 5."

    FORECAST_API_URL = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": "metric",
        "lang": "es",
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(FORECAST_API_URL, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    forecast_summary = []
                    daily_data = {}

                    for entry in data.get('list', []):
                        dt_object = datetime.fromtimestamp(entry['dt'])
                        date_str = dt_object.strftime("%Y-%m-%d")

                        if date_str not in daily_data:
                            daily_data[date_str] = {
                                'temps': [],
                                'weather_desc': [],
                                'weather_icons': [] # Podríamos usar esto para un resumen más inteligente
                            }
                        daily_data[date_str]['temps'].append(entry['main']['temp'])
                        daily_data[date_str]['weather_desc'].append(entry['weather'][0]['description'])
                        daily_data[date_str]['weather_icons'].append(entry['weather'][0]['icon'])
                    
                    # Ordenar por fecha y tomar los num_days solicitados
                    sorted_dates = sorted(daily_data.keys())
                    
                    # Filtrar para empezar desde mañana si el primer día es hoy y ya es tarde
                    # o si solo tenemos datos parciales de hoy.
                    today_str = datetime.now().strftime("%Y-%m-%d")
                    if sorted_dates and sorted_dates[0] == today_str:
                        # Si el primer día es hoy, y ya tenemos muchos datos de hoy,
                        # podríamos empezar desde el siguiente día para un pronóstico "limpio".
                        # Por ahora, lo incluimos si hay datos.
                        pass 

                    days_processed = 0
                    for date_key in sorted_dates:
                        if days_processed >= num_days:
                            break
                        
                        day_info = daily_data[date_key]
                        min_temp = min(day_info['temps'])
                        max_temp = max(day_info['temps'])
                        # Para la descripción, podríamos tomar la más frecuente o la del mediodía
                        # Por ahora, tomamos la descripción del mediodía como una aproximación.
                        # Una lógica más avanzada podría contar frecuencias o priorizar tipos de clima.
                        raw_weather_description = day_info['weather_desc'][len(day_info['weather_desc']) // 2]
                        weather_description_capitalized = raw_weather_description.capitalize()
                        emoji = get_weather_emoji(raw_weather_description)
                        
                        # Formatear la fecha para mostrar el nombre del día
                        date_obj_format = datetime.strptime(date_key, "%Y-%m-%d")
                        # Nombres de los días en español
                        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
                        # Nombres de los meses en español
                        meses_es = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
                        nombre_dia = dias_semana[date_obj_format.weekday()]
                        nombre_mes = meses_es[date_obj_format.month]
                        
                        forecast_summary.append(
                            f"{emoji} {nombre_dia}, {date_obj_format.day} de {nombre_mes}: Min {min_temp:.1f}°C, Max {max_temp:.1f}°C. Clima: {weather_description_capitalized}."
                        )
                        days_processed += 1
                    
                    if not forecast_summary:
                        return f"No se pudo generar un pronóstico para {city.title()} con los datos disponibles."

                    return f"Pronóstico para {city.title()}:\n" + "\n".join(forecast_summary)

                elif response.status == 401:
                    return f"Error: API key inválida o no autorizada. Verifica tu OPENWEATHERMAP_API_KEY."
                elif response.status == 404:
                    return f"Error: Ciudad '{city.title()}' no encontrada para pronóstico."
                else:
                    error_text = await response.text()
                    return f"Error al obtener el pronóstico: {response.status} - {error_text}"
        except aiohttp.ClientConnectorError as e:
            return f"Error de conexión: No se pudo conectar a OpenWeatherMap para pronóstico. {e}"
        except Exception as e:
            return f"Ocurrió un error inesperado en el pronóstico: {e}"


if __name__ == "__main__":
    if not OPENWEATHERMAP_API_KEY:
        print("ADVERTENCIA: La variable de entorno OPENWEATHERMAP_API_KEY no está configurada.")
        print("El servidor se iniciará, pero la herramienta de clima fallará.")
        print("Asegúrate de tener un archivo .env con tu API key o configúrala en tu entorno.")
    mcp.run(transport="stdio")
