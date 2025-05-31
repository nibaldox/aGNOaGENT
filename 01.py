# ejemplo_agente_basico 01.py

from agno.agent import Agent
#from agno.models.openai import OpenAI
from agno.models.ollama import Ollama

# Creamos un agente simple usando un modelo de OpenAI (puedes cambiarlo por otro si tienes clave API)
agente = Agent(
    model=Ollama(id="gemma3:4b-it-qat"),  # Asegúrate de tener tu API Key configurada
    instructions=[
        "Responde de manera clara y concisa.",
        "Solo responde en español."
    ],
    markdown=True,
)

# Realizamos una consulta al agente
agente.print_response("cuentame una historia de ciencia ficcion divida en 10 capitulos", 
                        stream=True)
