"""🏠 MCP Airbnb Agent - Search for Airbnb listings!

Este script muestra cómo configurar un agente Agno que utiliza MCPTools y Ollama
para buscar alojamientos en Airbnb de forma programática.

Requisitos:
  - Node.js y @openbnb/mcp-server-airbnb instalado (o configurable vía ENV)
  - Crear variable de entorno `MCP_AIRBNB_CMD` para personalizar el comando.
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

load_dotenv()

# Supresión de warnings de recursos no cerrados
warnings.filterwarnings("ignore", category=ResourceWarning)
warnings.simplefilter("ignore", ResourceWarning)

# Comando MCP configurable mediante variable de entorno
MCP_AIRBNB_CMD = os.getenv(
    "MCP_AIRBNB_CMD",
    "npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt",
)

async def run_agent(message: str) -> None:
    """Ejecuta un agente MCP para buscar alojamientos en Airbnb.

    Args:
        message (str): Consulta de búsqueda en texto libre, p.ej.,
            "listings available in Paris for 2 people...".

    Returns:
        None: Imprime el flujo de respuesta mediante `apprint_run_response`.
    """
    try:
        async with MCPTools(MCP_AIRBNB_CMD) as mcp_tools:
            agent = Agent(
                name="Airbnb Agent",
                role="Buscar alojamientos en Airbnb usando MCPTools",
                model=Gemini(id="gemini-2.5-flash-preview-04-17"),
                #model=Ollama(id="qwen3:14b-q8_0"),
                instructions=dedent("""\
                    Eres un agente especializado en buscar alojamientos en Airbnb.
                    Sigue estos pasos:
                    1. Llama a la herramienta MCP con la consulta proporcionada.
                    2. Del resultado, extrae para cada alojamiento: nombre, precio total, rating y enlace.
                    3. Muestra la información en una tabla Markdown con columnas: Nombre | Precio | Rating | Enlace.
                    4. Si no hay resultados, responde: 'No se encontraron alojamientos relevantes'.
                    5. Mantén todo el texto en español.
                """),
                tools=[mcp_tools],
                markdown=True,
            )

            response_stream = await agent.arun(message, stream=True)
            await apprint_run_response(response_stream, markdown=True)
    except Exception as e:
        print(f"Error al ejecutar MCPTools: {e}")

def main():
    """Punto de entrada principal del script."""
    import sys
    # Construir consulta desde argumentos o usar default
    query = (" ".join(sys.argv[1:]) if len(sys.argv) > 1 else
             "What listings are available in Paris for 1 person for 3 nights from 1 to 4 August 2025?")
    asyncio.run(run_agent(query))

if __name__ == "__main__":
    main()
