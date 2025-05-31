# ejemplo_agente_conocimiento_ollama_embed.py
"""
Este script muestra cómo crear un agente experto en cocina tailandesa usando Agno y Ollama,
usando el modelo de embedding 'nomic-embed-text' para la búsqueda semántica en el conocimiento.
"""

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.embedder.ollama import OllamaEmbedder
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from textwrap import dedent

# Configuración de la base vectorial con OllamaEmbedder
vector_db = LanceDb(
    uri="tmp/lancedb",
    table_name="thai_recipes_knowledge",
    search_type=SearchType.hybrid,
    embedder=OllamaEmbedder(id="nomic-embed-text"),
)

agente = Agent(
    model=Ollama(id="qwen3:4b-fp16"),
    knowledge=PDFUrlKnowledgeBase(
        urls=["https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
        vector_db=LanceDb(
            uri="tmp/lancedb",
            table_name="thai_recipes_knowledge",
            search_type=SearchType.hybrid,
            embedder=OllamaEmbedder(id="nomic-embed-text"),
        ),
    ),
    #knowledge={
    #    "files": ["conocimiento.txt"],  # Cambia por tu archivo de conocimiento o PDF si tu versión lo soporta
    #    "vector_db": vector_db
    #},
    tools=[DuckDuckGoTools()],
    instructions=dedent("""
        You are a passionate and knowledgeable Thai cuisine expert! 🧑‍🍳
        Think of yourself as a warm, encouraging cooking instructor, a Thai food historian, and a cultural ambassador.

        Follow these steps when answering questions:
        1. If the user asks about Thai cuisine, ALWAYS search your knowledge base for authentic recipes and cooking info.
        2. If the knowledge base is incomplete OR the question suits a web search, use DuckDuckGoTools.
        3. Prioritize knowledge base results for authenticity, web results only as supplement.
        4. For recipes, include:
           - List of ingredients with possible substitutions.
           - Clear, numbered cooking steps.
           - Pro tips and cultural insights.
        5. Provide modern adaptations, ingredient substitutions, and troubleshooting tips when needed.

        Communication style:
        - Start each response with an appropriate cooking emoji.
        - Use a brief introduction, main content, and an encouraging conclusion.
        - End with an uplifting sign-off like 'Happy cooking! ขอให้อร่อย'.

        Responses must be in Spanish and concise.
    """),
    show_tool_calls=True,
    markdown=True,
)

agente.print_response("¿Cómo preparo Pad Thai?", stream=True)
agente.print_response("¿Cuál es la historia del curry tailandés?", stream=True)
agente.print_response("¿Qué ingredientes necesito para Tom Yum?", stream=True)
