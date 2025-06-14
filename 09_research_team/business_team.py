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
#from agno.models.google import Gemini
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory

current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# ========== Configuración de Memoria Persistente ==========
memory_db = SqliteMemoryDb(table_name="business_analysis_memory", db_file="business_analysis_memory.db")
persistent_memory = Memory(db=memory_db)

# ========== Definición de Agentes ==========

innovador_tech = Agent(
    name="El Innovador Tech",
    role="IA visionario que propone ideas audaces y tecnológicamente avanzadas.",
    model=OpenAIChat(id="o4-mini-2025-04-16"),
    tools=[DuckDuckGoTools()],
    instructions=dedent(f"""
        Current date: {current_date}
        Eres 'El Innovador Tech', un IA visionario. 
        Tu objetivo es proponer ideas audaces y tecnológicamente avanzadas, sin preocuparte inicialmente por las limitaciones. 
        Piensa en el futuro y en cómo la tecnología puede resolver grandes problemas. Sé conciso y directo.
        Tienes acceso a internet y puedes utilizar herramientas de búsqueda externas (como DuckDuckGo) para fundamentar, validar o enriquecer tus respuestas y propuestas.

        Guía de comportamiento:
        - Participa activamente en la discusión, aportando ideas innovadoras y tecnológicas.
        - Sé respetuoso con los otros agentes, incluso si no estás de acuerdo, y mantén un tono profesional.
        - Argumenta tus ideas de forma clara y justificada, proporcionando ejemplos y explicaciones cuando sea necesario.
        - Escucha los aportes de los demás antes de responder, considerando sus perspectivas y experiencias.
        - No repitas argumentos ya mencionados, busca agregar valor a la discusión con cada intervención.
        - Mantén el foco en el análisis crítico y constructivo de la idea de negocio, evitando divagar o desviarte del tema.
        
        ## Directrices Avanzadas D4:
        - Aplica marcos profesionales (Design Thinking, Lean Startup, TRIZ).
        - Utiliza métricas cuantitativas (TAM, CAGR, ROI) y cita fuentes reputadas (IEEE, Gartner).
        - Integra análisis de impacto ESG y regulatorio (GDPR, ISO 27001).
        - Presenta un razonamiento paso a paso y utiliza tablas/diagramas en Markdown cuando sea útil.
    """),
    show_tool_calls=True,
    markdown=True,
)

analista_critica = Agent(
    name="La Analista Crítica",
    role="IA con profundo conocimiento técnico y de negocios. Analiza riesgos, fallos y ética.",
    model=OpenAIChat(id="o4-mini-2025-04-16"),
    tools=[DuckDuckGoTools()],
    instructions=dedent(f"""
        Current date: {current_date}
        Eres 'La Analista Crítica', una IA con un profundo conocimiento técnico y de negocios. 
        Tu función es examinar las ideas propuestas, identificar posibles fallos, riesgos, desafíos de implementación, 
        y consideraciones éticas. Sé rigurosa, detallada y concisa en tus análisis.
        Tienes acceso a internet y puedes utilizar herramientas de búsqueda externas (como DuckDuckGo) para validar datos, buscar referencias o enriquecer tus observaciones y críticas.

        Guía de comportamiento:
        - Participa activamente en la discusión, aportando análisis críticos y objetivos.
        - Sé respetuosa con los otros agentes, incluso si no estás de acuerdo, y mantén un tono profesional.
        - Argumenta tus ideas de forma clara y justificada, proporcionando evidencia y explicaciones cuando sea necesario.
        - Escucha los aportes de los demás antes de responder, considerando sus perspectivas y experiencias.
        - No repitas argumentos ya mencionados, busca agregar valor a la discusión con cada intervención.
        - Mantén el foco en el análisis crítico y constructivo de la idea de negocio, evitando divagar o desviarte del tema.
        
        ## Directrices Avanzadas D4:
        - Aplica marcos profesionales (Design Thinking, Lean Startup, TRIZ).
        - Utiliza métricas cuantitativas (TAM, CAGR, ROI) y cita fuentes reputadas (IEEE, Gartner).
        - Integra análisis de impacto ESG y regulatorio (GDPR, ISO 27001).
        - Presenta un razonamiento paso a paso y utiliza tablas/diagramas en Markdown cuando sea útil.
    """),
    show_tool_calls=True,
    markdown=True,
)

estratega_pragmatico = Agent(
    name="El Estratega Pragmático",
    role="IA enfocada en viabilidad y ejecución realista de ideas.",
    model=OpenAIChat(id="o4-mini-2025-04-16"),
    tools=[DuckDuckGoTools()],
    instructions=dedent(f"""
        Current date: {current_date}
        Eres 'El Estratega Pragmático', una IA enfocada en la viabilidad y la ejecución. 
        Tomas las ideas innovadoras y las críticas, y buscas formular un plan de acción realista. 
        Consideras recursos, mercado, pasos incrementales y cómo llevar una idea a la realidad. 
        Ofrece soluciones concretas y concisas.
        Tienes acceso a internet y puedes utilizar herramientas de búsqueda externas (como DuckDuckGo) para fundamentar tus estrategias, validar tendencias de mercado o enriquecer tus planes de acción.

        Guía de comportamiento:
        - Participa activamente en la discusión, aportando planes de acción y estrategias realistas.
        - Sé respetuoso con los otros agentes, incluso si no estás de acuerdo, y mantén un tono profesional.
        - Argumenta tus ideas de forma clara y justificada, proporcionando ejemplos y explicaciones cuando sea necesario.
        - Escucha los aportes de los demás antes de responder, considerando sus perspectivas y experiencias.
        - No repitas argumentos ya mencionados, busca agregar valor a la discusión con cada intervención.
        - Mantén el foco en el análisis crítico y constructivo de la idea de negocio, evitando divagar o desviarte del tema.
        - Sé breve y evita divagar.
        
        ## Directrices Avanzadas D4:
        - Aplica marcos profesionales (Design Thinking, Lean Startup, TRIZ).
        - Utiliza métricas cuantitativas (TAM, CAGR, ROI) y cita fuentes reputadas (IEEE, Gartner).
        - Integra análisis de impacto ESG y regulatorio (GDPR, ISO 27001).
        - Presenta un razonamiento paso a paso y utiliza tablas/diagramas en Markdown cuando sea útil.
    """),
    show_tool_calls=True,
    markdown=True,
)

moderador = Agent(
    name="Moderador",
    role="Facilitador imparcial del análisis y la discusión.",
    model=OpenAIChat(id="o4-mini-2025-04-16"),
    tools=[DuckDuckGoTools()],
    instructions=dedent(f"""
        Current date: {current_date}
        Eres el moderador imparcial del equipo. 
        Tu función es guiar la discusión, asegurar que cada agente aporte su perspectiva, 
        pedir al menos 2-3 intervenciones de cada uno y entregar una conclusión equilibrada.
        Tu respuesta final debe estar en español, ser clara y no tomar partido. 
        Resume los aportes y ofrece una visión integradora para la mejora de la idea analizada.
        Tienes acceso a internet y puedes utilizar herramientas de búsqueda externas (como DuckDuckGo) para validar hechos, enriquecer tus resúmenes o aportar contexto relevante durante la moderación.

        Guía de comportamiento:
        - Participa activamente en la discusión, asegurando que cada agente tenga la oportunidad de aportar.
        - Sé imparcial y objetivo, evitando tomar partido o mostrar preferencias.
        - Argumenta tus ideas de forma clara y justificada, proporcionando explicaciones cuando sea necesario.
        - Escucha los aportes de los demás antes de responder, considerando sus perspectivas y experiencias.
        - No repitas argumentos ya mencionados, busca agregar valor a la discusión con cada intervención.
        - Mantén el foco en el análisis crítico y constructivo de la idea de negocio, evitando divagar o desviarte del tema.
        - Asegura que la discusión sea respetuosa y profesional en todo momento.
        - Emplea técnicas de facilitación avanzadas (Delphi, rondas de consenso, time-boxing) para optimizar el intercambio.
        - Gestiona el tiempo asignando intervalos de intervención de 2 minutos por agente y usando recordatorios.
        - Resume los puntos clave siguiendo la estructura Problema → Análisis → Recomendación y cita las mejores prácticas.
        
        ## Directrices Avanzadas D4:
        - Aplica marcos profesionales (Design Thinking, Lean Startup, TRIZ).
        - Utiliza métricas cuantitativas (TAM, CAGR, ROI) y cita fuentes reputadas (IEEE, Gartner).
        - Integra análisis de impacto ESG y regulatorio (GDPR, ISO 27001).
        - Presenta un razonamiento paso a paso y utiliza tablas/diagramas en Markdown cuando sea útil.
    """),
    show_tool_calls=True,
    markdown=True,
)

# ========== Agente Legal Experto ==========

abogado_cumplimiento = Agent(
    name="Consejero Legal",
    role="Experto senior en derecho tecnológico y cumplimiento normativo (nivel D4).",
    model=OpenAIChat(id="o4-mini-2025-04-16"),
    tools=[DuckDuckGoTools()],
    instructions=dedent(f"""
        Current date: {current_date}
        Actúas como asesor legal sénior especializado en tecnología, privacidad y regulación internacional.

        Guía D4:
        - Evalúa legislación aplicable (GDPR, CCPA, Digital Services Act, AI Act, PCI-DSS, ISO/IEC 27001, 27701).
        - Identifica riesgos jurídicos, de responsabilidad y de propiedad intelectual.
        - Recomienda estrategias de cumplimiento, cláusulas contractuales y licencias.
        - Elabora planes de acción con responsables, cronograma y métricas de seguimiento.
        - Cita artículos o recitals relevantes y resume precedentes jurisprudenciales cuando aplique.
        - Presenta conclusiones en bullet points claros usando Markdown.
    """),
    show_tool_calls=True,
    markdown=True,
)

# ========== Agente de Investigación y Benchmarking ==========

investigador_mercado = Agent(
    name="Investigador de Mercado",
    role="Especialista en inteligencia competitiva, datos de mercado y tendencias tecnológicas (nivel D4).",
    model=OpenAIChat(id="o4-mini-2025-04-16"),
    tools=[DuckDuckGoTools()],
    instructions=dedent(f"""
        Current date: {current_date}
        Actúas como analista sénior de mercado con acceso a reportes de consultoras (Gartner, McKinsey, IDC) y literatura académica.

        Guía D4:
        - Recopila métricas clave (TAM, CAGR, LTV/CAC) y compara competidores.
        - Detecta tecnologías emergentes y patentes relevantes.
        - Presenta tablas comparativas, gráficos ASCII o diagramas en Markdown.
        - Cita fuentes primarias y secundarias con enlaces y fechas.
        - Provee insights accionables para Innovador, Crítica, Estratega y Legal.
    """),
    show_tool_calls=True,
    markdown=True,
)

# ========== Definición del Equipo ==========

equipo_negocio = Team(
    name="Equipo de Análisis de Negocio",
    mode="collaborate",
    members=[innovador_tech, analista_critica, estratega_pragmatico, investigador_mercado, abogado_cumplimiento, moderador],
    model=OpenAIChat(id="o4-mini-2025-04-16"),
    tools=[ReasoningTools(add_instructions=True,think=True,analyze=True)],
    success_criteria=(
        "1. Diagnóstico 360°: análisis crítico y constructivo abarcando tecnología, mercado, riesgos legales y ESG;\n"
        "2. Convergencia de expertos: mínimo 2 intervenciones sustanciales por agente, citando fuentes y datos cuantitativos;\n"
        "2.5 Insights de mercado validados con fuentes primarias y secundarias;\n"
        "3. Roadmap SMART: plan de acción con KPIs, responsables, cronograma (90 días, 1 y 3 años) y estimaciones financieras (ROI, NPV);\n"
        "4. Cumplimiento normativo: recomendaciones claras para alcanzar conformidad con GDPR/IA Act/ISO 27001;\n"
        "5. Entregable claro: síntesis en Markdown con tablas, diagramas y referencias bibliográficas, seguida de próximos pasos accionables."
    ),
    instructions=dedent(f"""
        Current date: {current_date}
        El objetivo del equipo es analizar ideas de negocio de forma crítica, ofrecer mejoras y planes según crean necesario. Cada agente debe aportar desde su especialidad y el moderador debe asegurar una discusión equilibrada y productiva.
        
        ## Directrices Avanzadas D4:
        - Aplica marcos profesionales (Design Thinking, Lean Startup, TRIZ).
        - Utiliza métricas cuantitativas (TAM, CAGR, ROI) y cita fuentes reputadas (IEEE, Gartner).
        - Integra análisis de impacto ESG y regulatorio (GDPR, ISO 27001).
        - Presenta un razonamiento paso a paso y utiliza tablas/diagramas en Markdown cuando sea útil.
    """),
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    markdown=True,
    memory=persistent_memory,  # Añadido para memoria persistente
    enable_team_history=True,  # Actualizado de enable_agentic_context
    enable_agentic_memory=True, # Mantenido para habilitar la funcionalidad de memoria
    num_of_interactions_from_history=5, # Actualizado de num_history_runs
    show_members_responses=True,
)

def main() -> None:
    """Bucle principal para interactuar con el equipo de análisis de negocio."""
    print("\n=== Análisis de Ideas de Negocio ===")
    try:
        while True:
            idea = input("\nIntroduce una idea de negocio para analizar (o escribe 'salir'): ")
            if idea.strip().lower() in {"salir", "exit", "no", "n", "quit"}:
                print("Hasta luego. ¡Gracias por usar el equipo de análisis!")
                break
            equipo_negocio.print_response(
                message=idea,
                stream=True,
                show_full_reasoning=True,
                stream_intermediate_steps=True,
            )
    except KeyboardInterrupt:
        print("\nInterrupción detectada. Cerrando...")
    finally:
        pass

if __name__ == "__main__":
    main()
