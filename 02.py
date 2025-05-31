# ejemplo_agente_herramientas 02.py

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGoTools

# Creamos un agente que puede buscar en la web usando DuckDuckGo
agente = Agent(
    model=Ollama(id="qwen3:4b-fp16"),
    tools=[DuckDuckGoTools()],
    instructions=[
        "Responde de manera clara y concisa.",
        "Si no sabes la respuesta, búscala usando DuckDuckGo.",
        "Solo responde en español."
    ],
    markdown=True,
    show_tool_calls=True,
)

# Consulta que requiere búsqueda en la web
agente.print_response("¿que es agno agi agents?", stream=True, )