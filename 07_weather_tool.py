"""🌤️ Weather Agent - Example Tool for Weather Forecasts

This example shows how to create and integrate a custom weather tool into an Agno Agent.
This tool fetches current weather conditions for a given location using the wttr.in API.

Run `pip install httpx agno` to install dependencies.
"""

import httpx
from textwrap import dedent
import datetime

from agno.agent import Agent
from agno.models.ollama import Ollama

current_date = datetime.datetime.now().strftime("%Y-%m-%d")

def get_weather(location: str, start_date: str = None, end_date: str = None) -> str:
    """Get current weather for the specified location.

    Args:
        location (str): City or location (e.g., 'Madrid', 'New York').
        start_date (str, optional): Fecha de inicio YYYY-MM-DD para filtrar pronóstico.
        end_date (str, optional): Fecha de fin YYYY-MM-DD para filtrar pronóstico.

    Returns:
        str: JSON string with weather data.
    """
    url = f"http://wttr.in/{location}?format=j1"
    response = httpx.get(url)
    response.raise_for_status()
    return response.text


weather_agent = Agent(
    name="Weather Agent",
    role="Provide current weather information",
    model=Ollama(id="qwen3:14b-q8_0"),
    tools=[get_weather],
    instructions=dedent("""\
        Current date: {current_date}
        You are a weather agent.
        Use the tool `get_weather(location, start_date, end_date)` to fetch current weather and 7-day forecast in JSON.
        Steps:
        1. Call the tool with the provided location and optional date range.
        2. Parse JSON to extract:
           - Today's summary: temperature, description, humidity.
           - 7-day forecast from `weather` field (date, min/max temp, avg humidity, condition).
        3. Use emojis to represent conditions (e.g., ☀️ for clear, 🌧️ for rain, ❄️ for snow).
        4. Present today's summary and then a markdown table for next 7 days with columns:
           | Date | Condition | Min/Max °C | Avg Humidity |
        5. Ensure all text is in Spanish.
        6. Si la consulta incluye un rango de fechas, filtrar la tabla del pronóstico para mostrar solo esas fechas.
    """),
    show_tool_calls=True,
    markdown=True,
)

if __name__ == "__main__":
    # Example usage: obtener solo el resultado final sin pensamiento
    response = weather_agent.run(
        "Madrid desde 2025-05-28 hasta 2025-06-03",
        stream=False,
        show_tool_calls=False,
        show_reasoning=False,
        stream_intermediate_steps=False,
    )
    print(response.get_content_as_string())
