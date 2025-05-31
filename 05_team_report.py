# ejemplo_equipo_agentes 05_team.py
"""
Este script muestra cómo crear un equipo de agentes con Agno y Ollama.
Un agente busca en la web y datos sobre un tema definido por el usuario, otro lo transforma a un informe, coordinados para generar un informe completo.
"""
import os
from textwrap import dedent

from agno.team import Team
from agno.agent import Agent

from agno.models.ollama import Ollama
from agno.models.google import Gemini
#from agno.tools.serpapi import SerpApiTools

from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.python import PythonTools
from agno.tools.mcp import MCPTools


from dotenv import load_dotenv
load_dotenv()
import datetime
current_date = datetime.datetime.now().strftime("%Y-%m-%d")


# Agente especializado en búsquedas web
web_agent = Agent(
    name="Web Agent",
    role="deep web search for information",
    #model=Gemini(id="gemini-2.5-flash-preview-05-20"),
    model=Ollama(id="qwen3:14b-q8_0"),
    tools=[DuckDuckGoTools()],
    instructions=dedent(f"""\
    Current date: {current_date} 
    You are an experienced web researcher and news analyst! 🔍

    Follow these steps when searching for information:
    1. Use only the most recent and relevant sources, avoiding outdated content.
    2. Cross-reference information from multiple sources.
    3. Prioritize reputable news outlets and official sources.
    4. Apply date filters to restrict results to the period defined by Lider (e.g., using tbs parameters in Google).
    5. Always cite your sources with links.
    6. Focus on market-moving news and significant developments.
 

    Your style guide:
    - Present information in a clear, journalistic style.
    - Use bullet points for key takeaways.
    - Include relevant quotes when available.
    - Specify the date and time for each piece of news.
    - Highlight market sentiment and industry trends.
    - End with a concise summary of the overall narrative.
"""),
    show_tool_calls=True,
    markdown=True,
)

# Agente especializado en datos financieros
finance_agent = Agent(
    name="Finance Agent",
    role="deep financial data analysis",
    #model=Gemini(id="gemini-2.5-flash-preview-05-20"),
    model=Ollama(id="qwen3:14b-q8_0"),
    tools=[YFinanceTools(stock_price=True, 
                        analyst_recommendations=True, 
                        company_info=True,
                        stock_fundamentals=True,
                        technical_indicators=True,
                        historical_prices=True,
                        enable_all=True)],
    instructions=dedent(f"""\
    Current date: {current_date}
    You are a skilled financial analyst with expertise in market data! 📊

    Follow these steps when analyzing financial data:
    1. Start with the latest stock price, trading volume, and daily range.
    2. Present detailed analyst recommendations and consensus target prices.
    3. Include key metrics: P/E ratio, market cap, 52-week range.
    4. Analyze trading patterns and volume trends.
    5. Compare performance against relevant sector indices.

    Your style guide:
    - Use tables for structured data presentation.
    - Include clear headers for each data section.
    - Add brief explanations for technical terms.
    - Highlight notable changes with emojis.
    - Use bullet points for quick insights.
    - Compare current values with historical averages.
    - End with a data-driven financial outlook.
"""),
    show_tool_calls=True,
    markdown=True,
)

# Equipo de agentes coordinados
agent_team = Team(
    name="Lider",
    #role="lead editor of a prestigious financial news desk!",
    mode="coordinate",  # modes: route, collaborate, coordinate
    members=[web_agent, finance_agent],
    tools=[ReasoningTools(add_instructions=True), PythonTools()],   
    #model=Gemini(id="gemini-2.5-flash-preview-05-20"),
    model=Ollama(id="qwen3:14b-q8_0"),
    success_criteria=(
        "A comprehensive report with clear sections "
        "and data-driven insights."
    ),
    instructions=dedent(f"""\
    Current date: {current_date}
    You are the lead editor of a prestigious news desk! 📰

    Your role:
    1. the final report must be in Spanish.
    2. Coordinate between the web researcher and financial analyst, if they are needed.
    3. Combine their findings into a compelling narrative.
    4. Ensure all information is properly sourced and verified.
    5. Present a balanced view of both news and data.
    6. Highlight key risks and opportunities.
    7. Generate report in Spanish.
    8. Use markdown to format the report.
    9. Highlight notable changes with emojis.
    10. Use bullet points for quick insights.
    11. Use tables for structured data presentation.
    12. Include clear headers for each data section.
    13. Add brief explanations for technical terms.
    14. Highlight market sentiment and industry trends.
    15. End with a concise summary of the overall narrative.

    Your style guide:
    - use a narrative tone in the report. 
    - Start with an attention-grabbing headline and value of stock price.
    - Begin with a powerful executive summary.
    - Present data first, followed by news context.
    - Use clear section breaks between different types of information.
    - Include relevant charts or tables when available.
    - Add a 'Market Sentiment' section with current mood.
    - Include a 'Key Takeaways' section at the end.
    - End with 'Risk Factors' when appropriate.
    - Generate report in Spanish.
    - Use markdown to format the report.
    - Highlight notable changes with emojis.
    - Use bullet points for quick insights.
    - Use tables for structured data presentation.
    - Include clear headers for each data section.
    - Add brief explanations for technical terms.
    - Highlight market sentiment and industry trends.
    - End with a concise summary of the overall narrative.
"""),
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    markdown=True,
    enable_agentic_context=True,
    enable_agentic_memory=True,
    num_history_runs=3,
    show_members_responses=True,
    
)

while True:
    user_message = input("\nPor favor, introduce tu consulta para el equipo de agentes (o escribe 'salir' para terminar): ")
    if user_message.lower() in ['salir', 'exit', 'quit', 'no', 'n']:
        print("Hasta luego. ¡Gracias por usar el equipo de agentes!")
        # Intentar liberar recursos explícitamente
        try:
            del web_agent
            del finance_agent
            del agent_team
            import gc
            gc.collect()
            print("Recursos de agentes liberados.")
        except NameError:
            # En caso de que los agentes no se hayan definido por alguna razón
            pass 
        break

    agent_team.print_response(
        message=user_message,
        stream=False,
        #show_full_reasoning=True,
        #stream_intermediate_steps=True,
    )

    # Opcional: Preguntar explícitamente si desea continuar, aunque el prompt ya lo sugiere.
    # continue_chat = input("¿Deseas hacer otra consulta? (s/n): ")
    # if continue_chat.lower() != 's':
    #     print("Hasta luego. ¡Gracias por usar el equipo de agentes!")
    #     break

# Código comentado original:
#agent_team.print_response(
#   message="What's the market outlook and financial performance of cooper mining companies? and generate report in Spanish",
#   stream=True,
#)
#agent_team.print_response(
#    message="Analyze recent developments and financial performance of TSLA and generate report in Spanish",
#    stream=True,
#)
