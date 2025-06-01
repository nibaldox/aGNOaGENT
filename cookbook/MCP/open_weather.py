"""🏠 MCP OpenWeather Agent - Search for weather listings!

Este script muestra cómo configurar un agente Agno que utiliza MCPTools y Ollama
para buscar alojamientos en Airbnb de forma programática.

Requisitos:
  - Node.js y @openbnb/mcp-server-open-weather instalado (o configurable vía ENV)
  - Crear variable de entorno `MCP_OPENWEATHER_CMD` para personalizar el comando.
  - `pip install google-genai mcp agno python-dotenv`
"""
import os
import warnings
import asyncio
from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.ollama import Ollama
from agno.tools.mcp import MCPTools
from agno.utils.pprint import apprint_run_response
from textwrap import dedent

import datetime
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

load_dotenv()

# Supresión de warnings de recursos no cerrados
warnings.filterwarnings("ignore", category=ResourceWarning)
warnings.simplefilter("ignore", ResourceWarning)

# Comando MCP configurable mediante variable de entorno
MCP_OPENWEATHER_CMD = os.getenv(
    "MCP_OPENWEATHER_CMD",
    r"npx -y D:/12_WindSurf/21_aGNOaGENT/MCP_Server/postman-mcp-server/mcpServer.js",
)

async def run_agent(message: str) -> None:
    """Ejecuta un agente MCP para buscar información en la web."

    Args:
        message (str): Consulta de búsqueda en texto libre, p.ej.,
            "quiero viajar a colombia, la proxima semana, por favor muetrame 5 opciones".

    Returns:
        None: Imprime el flujo de respuesta mediante `apprint_run_response`.
    """
    try:
        async with MCPTools(MCP_OPENWEATHER_CMD) as mcp_tools:
            agent = Agent(
                name="Buscador Avanzado",
                role="Agente de búsqueda avanzada en la web usando MCPTools",
                model=Gemini(id="gemini-2.0-flash-lite"),
                #model=Ollama(id="qwen3:14b-q8_0"),
                instructions=dedent("""\
                    Current date: {current_date} 
                    Eres un agente de búsqueda avanzada en la web.
                    Sigue estos pasos:
                    1. Interpreta y refina la consulta del usuario para mejorar relevancia.
                    2. Llama a la herramienta MCP con la consulta refinada.
                    3. Para cada resultado, extrae:
                       - Título
                       - URL
                       - Fragmento relevante (2-3 frases)
                       - Fecha de publicación (si está disponible)
                    4. Ordena los resultados por nivel de relevancia.
                    5. Presenta una tabla Markdown con columnas: Título | URL | Fragmento.
                    6. Luego, genera un informe narrativo y extenso consolidado en español que resuma los hallazgos y aporte contexto.
                    7. Si no hay resultados, responde: "No se encontraron resultados relevantes".
                    8. Mantén todo el texto en español y formatea en Markdown.
                """),
                tools=[mcp_tools],
                markdown=True,
            )

            response_stream = await agent.arun(message, stream=True)
            await apprint_run_response(response_stream, markdown=True)
    except Exception as e:
        print(f"Error al ejecutar MCPTools: {e}")
    await asyncio.sleep(0.1)

def main():
    """Punto de entrada principal del script."""
    import sys
    # Construir consulta desde argumentos o usar default
    query = (" ".join(sys.argv[1:]) if len(sys.argv) > 1 else
             "dime el clima en New York, de esta semana")
    asyncio.run(run_agent(query))

if __name__ == "__main__":
    main()
