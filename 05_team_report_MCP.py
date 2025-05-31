import os
import asyncio
import warnings
from dotenv import load_dotenv
from textwrap import dedent
import datetime

from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini 
from agno.tools.duckduckgo import DuckDuckGoTools 
from agno.tools.yfinance import YFinanceTools
from agno.tools.reasoning import ReasoningTools
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

async def execute_team_with_mcp(user_query: str):
    try:
        async with MCPTools(MCP_BRAVE_SEARCH_CMD) as mcp_tools:
            web_agent = Agent(
                name="Web Agent",
                role="Experto investigador web que utiliza Brave Search para encontrar la información más relevante y actualizada.",
                model=Gemini(id="gemini-2.5-flash-preview-05-20"), 
                tools=[mcp_tools], 
                instructions=dedent(f"""\
                    Current date: {current_date}
                    Eres un investigador web experimentado y analista de noticias. Tu herramienta principal es Brave Search.
                    Sigue estos pasos al buscar información:
                    1. Utiliza Brave Search (a través de la herramienta MCP provista) para encontrar la información más reciente y relevante.
                    2. Verifica la información cruzando múltiples fuentes si es posible.
                    3. Prioriza medios de noticias reputados y fuentes oficiales.
                    4. Cita siempre tus fuentes con enlaces URL.
                    5. Enfócate en noticias que muevan el mercado y desarrollos significativos relacionados con la consulta del usuario.

                    Tu guía de estilo:
                    - Presenta la información en un estilo periodístico claro y conciso.
                    - Utiliza viñetas para los puntos clave.
                    - Incluye citas relevantes cuando estén disponibles.
                    - Especifica la fecha de cada noticia si la encuentras.
                    - Destaca el sentimiento del mercado y las tendencias de la industria.
                    - Termina con un resumen conciso de la narrativa general.
                """),
                show_tool_calls=True,
                markdown=True,
            )

            finance_agent = Agent(
                name="Finance Agent",
                role="Analista financiero especializado en datos de mercado y rendimiento de acciones.",
                model=Gemini(id="gemini-2.5-flash-preview-05-20"), 
                tools=[YFinanceTools(), DuckDuckGoTools(), ReasoningTools()], 
                instructions=dedent(f"""\
                    Current date: {current_date}
                    Eres un analista financiero especializado. 💰
                    - Analiza datos financieros, rendimiento de acciones y tendencias del mercado.
                    - Utiliza YFinanceTools para datos específicos de acciones (precios, fundamentales, etc.).
                    - Utiliza DuckDuckGoTools para noticias financieras más amplias o datos no disponibles en YFinance.
                    - Proporciona información clara y basada en datos.
                    - Si es aplicable, correlaciona los datos financieros con las noticias obtenidas por el Web Agent.
                """),
                show_tool_calls=True,
                markdown=True,
            )

            report_agent = Agent(
                name="Report Agent",
                role="Sintetizador de información y generador de informes.",
                model=Gemini(id="gemini-2.5-flash-preview-05-20"), 
                instructions=dedent(f"""\
                    Current date: {current_date}
                    Eres un redactor de informes meticuloso y preciso. 📝
                    - Sintetiza la información proporcionada por el Web Agent y el Finance Agent.
                    - Crea un informe completo, bien estructurado y coherente en formato Markdown.
                    - Asegúrate de que el informe aborde directamente la consulta original del usuario.
                    - TODO EL INFORME DEBE ESTAR EN ESPAÑOL.
                    - Comienza con un título claro y un resumen ejecutivo.
                    - Detalla los hallazgos de la investigación web y el análisis financiero en secciones separadas y claramente marcadas.
                    - Concluye con un resumen general y perspectivas si es apropiado.
                    - Mantén un tono profesional y objetivo.
                """),
                show_tool_calls=True, 
                markdown=True,
            )

            analyst_team = Team(
                name="Analyst Team",
                agents=[web_agent, finance_agent, report_agent],
                show_tool_calls=True,
                markdown=True,
            )

            print(f"🤖 Analyst Team: Iniciando análisis para la consulta: '{user_query}'")
            response_stream = await analyst_team.arun(user_query, stream=True)
            await apprint_run_response(response_stream, markdown=True) 
            
    except Exception as e:
        print(f"Ocurrió un error al ejecutar el equipo de análisis: {e}")
    finally:
        await asyncio.sleep(0.1)


def main():
    import sys
    default_query = ("realiza un resumen del rendimiento de la empresa minera Zaldivar SPA, durante 2024, "
                     "entregando resultados operativos y financieros. E indica cual es el comportamiento "
                     "de esta empresa en lo que va del año")
    query = (" ".join(sys.argv[1:]) if len(sys.argv) > 1 else default_query)
    
    asyncio.run(execute_team_with_mcp(query))

if __name__ == "__main__":
    main()
