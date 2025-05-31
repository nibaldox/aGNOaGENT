import os
import asyncio
import warnings
from dotenv import load_dotenv
from textwrap import dedent
import datetime

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.mcp import MCPTools
from agno.utils.pprint import apprint_run_response

load_dotenv()
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

warnings.filterwarnings("ignore", category=ResourceWarning)
warnings.simplefilter("ignore", ResourceWarning)

MCP_BRAVE_SEARCH_CMD = os.getenv(
    "MCP_BRAVE_SEARCH_CMD",
    "npx -y @modelcontextprotocol/server-brave-search --ignore-robots-txt",
)

async def simple_mcp_test(user_query: str):
    print(f"--- Iniciando prueba simple con MCP para: '{user_query}' ---")
    try:
        async with MCPTools(MCP_BRAVE_SEARCH_CMD) as mcp_tools:
            print("MCPTools inicializado.")
            web_agent = Agent(
                name="Test Web Agent",
                role="Agente de prueba usando MCPTools para Brave Search",
                model=Gemini(id="gemini-2.5-flash-preview-05-20"), # Ajusta el modelo si es necesario
                tools=[mcp_tools],
                instructions=dedent(f"""
                    Current date: {current_date}
                    Realiza una búsqueda web para: {user_query}
                """),
                show_tool_calls=True,
                markdown=True,
            )
            print("Agente de prueba creado. Ejecutando web_agent.arun()...")
            response_stream = await web_agent.arun(user_query, stream=True)
            print("web_agent.arun() completado. Procesando respuesta con apprint_run_response...")
            await apprint_run_response(response_stream, markdown=True)
            print("Respuesta procesada.")
            
    except asyncio.CancelledError:
        print("!!! ATENCIÓN: Prueba simple cancelada (asyncio.CancelledError detectado explícitamente) !!!")
        # Es importante relanzar para ver si el RuntimeError sigue ocurriendo después
        raise
    except Exception as e:
        print(f"!!! ERROR en prueba simple: {type(e).__name__}: {e} !!!")
        import traceback
        traceback.print_exc()
    finally:
        print("--- Finalizando prueba simple con MCP (bloque finally alcanzado) ---")
        # Una pequeña pausa puede ayudar a que las tareas de fondo se cierren.
        await asyncio.sleep(0.5) # Aumentado ligeramente por si acaso

def main():
    import sys
    # Puedes cambiar la consulta de prueba aquí si lo deseas
    query = (" ".join(sys.argv[1:]) if len(sys.argv) > 1 else "estado del tiempo en Marte")
    
    print(f"Ejecutando simple_mcp_test con la consulta: '{query}'")
    asyncio.run(simple_mcp_test(query))

if __name__ == "__main__":
    main()