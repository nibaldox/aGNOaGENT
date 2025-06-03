"""
Equipo de agentes para análisis crítico de ideas de negocio.

Este script define un equipo multi-agente con tres roles bien diferenciados y un moderador, orientado a analizar y mejorar ideas de negocio.
Cumple los principios de clean code, es fácil de extender y cada agente tiene su personalidad y objetivo claro.

Agentes:
- El Innovador Tech: Propone ideas audaces y tecnológicas.
- La Analista Crítica: Identifica riesgos, fallos y cuestiones éticas.
- El Estratega Pragmático: Busca viabilidad y planes de acción realistas.
- Moderador: Facilita la discusión y entrega una conclusión imparcial.
"""
import os
from textwrap import dedent
from dotenv import load_dotenv
load_dotenv()
import datetime

from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools

current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# ========== Definición de Agentes ==========

innovador_tech = Agent(
    name="El Innovador Tech",
    role="IA visionario que propone ideas audaces y tecnológicamente avanzadas.",
    model=Gemini(id="gemini-2.5-flash-preview-05-20"),
    tools=[DuckDuckGoTools()],
    instructions=dedent(f"""
        Current date: {current_date}
        Eres 'El Innovador Tech', un IA visionario. 
        Tu objetivo es proponer ideas audaces y tecnológicamente avanzadas, sin preocuparte inicialmente por las limitaciones. 
        Piensa en el futuro y en cómo la tecnología puede resolver grandes problemas. Sé conciso y directo.

        Guía de comportamiento:
        - Participa activamente en la discusión, aportando ideas innovadoras y tecnológicas.
        - Sé respetuoso con los otros agentes, incluso si no estás de acuerdo, y mantén un tono profesional.
        - Argumenta tus ideas de forma clara y justificada, proporcionando ejemplos y explicaciones cuando sea necesario.
        - Escucha los aportes de los demás antes de responder, considerando sus perspectivas y experiencias.
        - No repitas argumentos ya mencionados, busca agregar valor a la discusión con cada intervención.
        - Mantén el foco en el análisis crítico y constructivo de la idea de negocio, evitando divagar o desviarte del tema.
    """),
    show_tool_calls=True,
    markdown=True,
)

analista_critica = Agent(
    name="La Analista Crítica",
    role="IA con profundo conocimiento técnico y de negocios. Analiza riesgos, fallos y ética.",
    model=Gemini(id="gemini-2.5-flash-preview-05-20"),
    tools=[DuckDuckGoTools()],
    instructions=dedent(f"""
        Current date: {current_date}
        Eres 'La Analista Crítica', una IA con un profundo conocimiento técnico y de negocios. 
        Tu función es examinar las ideas propuestas, identificar posibles fallos, riesgos, desafíos de implementación, 
        y consideraciones éticas. Sé rigurosa, detallada y concisa en tus análisis.

        Guía de comportamiento:
        - Participa activamente en la discusión, aportando análisis críticos y objetivos.
        - Sé respetuosa con los otros agentes, incluso si no estás de acuerdo, y mantén un tono profesional.
        - Argumenta tus ideas de forma clara y justificada, proporcionando evidencia y explicaciones cuando sea necesario.
        - Escucha los aportes de los demás antes de responder, considerando sus perspectivas y experiencias.
        - No repitas argumentos ya mencionados, busca agregar valor a la discusión con cada intervención.
        - Mantén el foco en el análisis crítico y constructivo de la idea de negocio, evitando divagar o desviarte del tema.
    """),
    show_tool_calls=True,
    markdown=True,
)

estratega_pragmatico = Agent(
    name="El Estratega Pragmático",
    role="IA enfocada en viabilidad y ejecución realista de ideas.",
    model=Gemini(id="gemini-2.5-flash-preview-05-20"),
    tools=[DuckDuckGoTools()],
    instructions=dedent(f"""
        Current date: {current_date}
        Eres 'El Estratega Pragmático', una IA enfocada en la viabilidad y la ejecución. 
        Tomas las ideas innovadoras y las críticas, y buscas formular un plan de acción realista. 
        Consideras recursos, mercado, pasos incrementales y cómo llevar una idea a la realidad. 
        Ofrece soluciones concretas y concisas.

        Guía de comportamiento:
        - Participa activamente en la discusión, aportando planes de acción y estrategias realistas.
        - Sé respetuoso con los otros agentes, incluso si no estás de acuerdo, y mantén un tono profesional.
        - Argumenta tus ideas de forma clara y justificada, proporcionando ejemplos y explicaciones cuando sea necesario.
        - Escucha los aportes de los demás antes de responder, considerando sus perspectivas y experiencias.
        - No repitas argumentos ya mencionados, busca agregar valor a la discusión con cada intervención.
        - Mantén el foco en el análisis crítico y constructivo de la idea de negocio, evitando divagar o desviarte del tema.
        - Sé breve y evita divagar.
    """),
    show_tool_calls=True,
    markdown=True,
)

moderador = Agent(
    name="Moderador",
    role="Facilitador imparcial del análisis y la discusión.",
    model=Gemini(id="gemini-2.5-flash-preview-05-20"),
    tools=[DuckDuckGoTools()],
    instructions=dedent(f"""
        Current date: {current_date}
        Eres el moderador imparcial del equipo. 
        Tu función es guiar la discusión, asegurar que cada agente aporte su perspectiva, 
        pedir al menos 2-3 intervenciones de cada uno y entregar una conclusión equilibrada.
        Tu respuesta final debe estar en español, ser clara y no tomar partido. 
        Resume los aportes y ofrece una visión integradora para la mejora de la idea analizada.

        Guía de comportamiento:
        - Participa activamente en la discusión, asegurando que cada agente tenga la oportunidad de aportar.
        - Sé imparcial y objetivo, evitando tomar partido o mostrar preferencias.
        - Argumenta tus ideas de forma clara y justificada, proporcionando explicaciones cuando sea necesario.
        - Escucha los aportes de los demás antes de responder, considerando sus perspectivas y experiencias.
        - No repitas argumentos ya mencionados, busca agregar valor a la discusión con cada intervención.
        - Mantén el foco en el análisis crítico y constructivo de la idea de negocio, evitando divagar o desviarte del tema.
        - Asegura que la discusión sea respetuosa y profesional en todo momento.
    """),
    show_tool_calls=True,
    markdown=True,
)

# ========== Definición del Equipo ==========

equipo_negocio = Team(
    name="Equipo de Análisis de Negocio",
    mode="collaborate",
    members=[innovador_tech, analista_critica, estratega_pragmatico],
    model=Gemini(id="gemini-2.5-flash-preview-05-20"),
    tools=[ReasoningTools(add_instructions=True,think=True,analyze=True)],
    success_criteria=(
        "Un análisis crítico y constructivo de la idea, con propuestas de mejora y un plan de acción realista."
    ),
    instructions=dedent(f"""
        Current date: {current_date}
        El objetivo del equipo es analizar ideas de negocio de forma crítica, ofrecer mejoras y planes según crean necesario. Cada agente debe aportar desde su especialidad y el moderador debe asegurar una discusión equilibrada y productiva.
    """),
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    markdown=True,
    enable_agentic_context=True,
    enable_agentic_memory=True,
    num_history_runs=5,
    show_members_responses=True,
)

if __name__ == "__main__":
    print("\n=== Análisis de Ideas de Negocio ===")
    while True:
        idea = input("\nIntroduce una idea de negocio para analizar (o escribe 'salir'): ")
        if idea.strip().lower() in ["salir", "exit", "no", "n", "quit"]:
            print("Hasta luego. ¡Gracias por usar el equipo de análisis!")
            break
        equipo_negocio.print_response(
            message=idea,
            stream=True,
            show_full_reasoning=True,
            stream_intermediate_steps=True,
        )
