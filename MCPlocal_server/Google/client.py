import asyncio

import datetime
current_date = datetime.datetime.now().strftime("%Y-%m-%d")


from agno.agent import Agent
#from agno.models.groq import Groq
from agno.models.google import Gemini
from agno.tools.mcp import MCPTools
from dotenv import load_dotenv

async def run_agent(message: str) -> None:
    # Initialize the MCP server
    async with (
        MCPTools(
            f"fastmcp run server.py",  # Supply the command to run the MCP server
        ) as mcp_tools,
    ):
        agent = Agent(
            model=Gemini(id="gemini-2.0-flash-lite"),
            instructions="""
                        Eres un asistente amigable y servicial especializado en proporcionar información meteorológica.
                        Current date: {current_date} 
                        
                        Cuando presentes la información:
                        - Utiliza un tono conversacional y agradable.
                        - Estructura la respuesta de forma clara. Si presentas el clima actual y luego el pronóstico, sepáralos claramente, quizás con un pequeño encabezado o una frase introductoria para cada sección.
                        - El pronostico de los dias siguientes debe ser presentado en formato de tabla con las siguientes columnas: fecha, minima, maxima, clima. 
                        - Incorpora los emojis que las herramientas proporcionan para hacer la información más visual y amigable.
                        - Utiliza markdown para mejorar la legibilidad (por ejemplo, negritas para destacar, listas para el pronóstico).
                        - Si el usuario pide tanto el clima actual como el pronóstico, asegúrate de que ambas partes sean completas y fáciles de entender.
                        - Si una herramienta devuelve un error, comunícalo claramente al usuario.
                        - Siempre sé cortés y finaliza con una nota amigable si es apropiado.
                        """,
            tools=[mcp_tools],
            show_tool_calls=True,
            markdown=True,
        )
        await agent.aprint_response(message, 
                                    stream=True,
                                    stream_intermediate_steps=True, 
                                    stream_tool_calls=True, 
                                    stream_tool_outputs=True,
                                    add_datetime_to_instructions=True,
                                    )


# Example usage
if __name__ == "__main__":
    # Cargar variables de entorno del archivo .env
    load_dotenv()
    # --- Ejemplos de Solicitudes --- 

    # Para obtener el CLIMA ACTUAL (usará get_current_weather_owm):
    #asyncio.run(run_agent("¿cómo está el tiempo ahora en Coquimbo, Chile?  y cual es el pronostico para los proximos 5 dias"))
    # asyncio.run(run_agent("dame el clima actual en Santiago, Chile"))

    # Para obtener el PRONÓSTICO (usará get_daily_weather_forecast_owm):
    #asyncio.run(run_agent("Dame el pronóstico del tiempo para París para los próximos 3 días"))
    # asyncio.run(run_agent("¿Cuál es el pronóstico para Londres para 5 días?"))

    # --- Solicitud combinada con instrucciones de formato --- 
    asyncio.run(run_agent("¡Hola! Necesito un informe del tiempo para París. Primero, dime cómo está el clima ahora mismo, con todos los detalles y emojis. Luego, dame el pronóstico para los próximos 3 días, bien separado y claro, día por día, también con emojis. ¡Gracias!"))
    # asyncio.run(run_agent("pronóstico para Tokio, 2 días"))
