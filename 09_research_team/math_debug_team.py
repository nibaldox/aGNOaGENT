"""
Equipo de agentes para el análisis y depuración de ideas matemáticas.

Este script define un equipo multi-agente con roles especializados para examinar
la validez, originalidad y potencial de conceptos e ideas matemáticas.
"""
import os
import datetime
from textwrap import dedent
from dotenv import load_dotenv

# Cargar variables de entorno desde .env (si existe)
load_dotenv()

from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini # Asegúrate que el modelo Gemini que uses esté disponible
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.python import PythonTools
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory

# Importaciones para cálculos matemáticos
import numpy as np
import sympy
import scipy

# Importaciones para generación de gráficos
import matplotlib.pyplot as plt
import seaborn as sns

# Fecha actual para incluir en las instrucciones de los agentes
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# ========== Configuración de Memoria Persistente para el Equipo Matemático ==========
# Se crea una base de datos SQLite para almacenar la memoria del equipo.
math_memory_db = SqliteMemoryDb(
    table_name="math_debug_memory", 
    db_file="09_research_team/math_debug_memory.db" # Guardar en la carpeta del equipo
)
# Se instancia el objeto de memoria que utilizará el equipo.
persistent_math_memory = Memory(db=math_memory_db)

# ========== Definición de Agentes Matemáticos ==========

# Agente: El Teórico Formal
# Rol: Experto en lógica matemática, pruebas formales, axiomas y definiciones precisas.
# Objetivo: Asegurar la rigurosidad y la validez lógica de la idea matemática.
teorico_formal = Agent(
    name="El Teórico Formal",
    role="Experto en lógica matemática, pruebas formales, axiomas y definiciones precisas.",
    model=Gemini(id="gemini-2.5-flash-preview-05-20"), # Puedes ajustar el ID del modelo según disponibilidad
    tools=[DuckDuckGoTools(), ReasoningTools(add_instructions=True, think=True, analyze=True), PythonTools()], # Corregido a PythonTools
    instructions=dedent(f"""
        Current date: {current_date}
        Eres 'El Teórico Formal'. Tu misión es analizar la idea matemática propuesta con el máximo rigor.
        Verifica su consistencia con axiomas conocidos, la validez de cualquier prueba implícita o explícita,
        y la precisión de las definiciones utilizadas. Señala cualquier ambigüedad, falacia o fallo lógico.
        Utiliza notación matemática estándar y cita fuentes o teoremas relevantes si es necesario.
        Sé conciso y preciso en tus argumentos.
        Puedes utilizar la herramienta Python para ejecutar código si necesitas verificar algún cálculo o propiedad algorítmica. Las librerías `numpy` (como `np`), `sympy`, `matplotlib.pyplot` (como `plt`), y `seaborn` (como `sns`) ya están importadas y disponibles para su uso directo en el código Python que generes. No necesitas incluir `import numpy as np`, `import sympy`, etc., en el código que proporciones. Indica claramente el código Python que deseas ejecutar.

        Guía de comportamiento:
        - Participa activamente, aportando análisis lógicos y formales.
        - Sé respetuoso y profesional.
        - Argumenta claramente, proporcionando justificaciones y referencias.
        - Escucha y considera las perspectivas de otros agentes.
        - Evita repetir argumentos; busca añadir valor con cada intervención.
        - Mantén el foco en el análisis riguroso de la idea matemática.
    """),
    show_tool_calls=True,
    markdown=True,
)

# Agente: El Calculista Práctico
# Rol: Especialista en encontrar ejemplos, contraejemplos, realizar cálculos y verificar la idea en casos concretos.
# Objetivo: Poner a prueba la idea matemática mediante la aplicación práctica y el cálculo.
calculista_practico = Agent(
    name="El Calculista Práctico",
    role="Especialista en ejemplos, contraejemplos, cálculos y verificación de casos concretos.",
    model=Gemini(id="gemini-2.5-flash-preview-05-20"),
    tools=[DuckDuckGoTools(), ReasoningTools(add_instructions=True, think=True, analyze=True), PythonTools()], # Corregido a PythonTools
    instructions=dedent(f"""
        Current date: {current_date}
        Eres 'El Calculista Práctico'. Tu tarea es explorar la idea matemática a través de ejemplos y cálculos.
        Intenta encontrar contraejemplos que la refuten. Si es una afirmación general, pruébala con casos base,
        casos límite o ejemplos numéricos simples. Si involucra algoritmos o procesos, simula su ejecución.
        Documenta tus cálculos, los ejemplos que exploras y los hallazgos de manera clara.
        Tienes a tu disposición una herramienta para ejecutar código Python. Las librerías `numpy` (como `np`), `sympy`, `matplotlib.pyplot` (como `plt`), y `seaborn` (como `sns`) ya están importadas y disponibles para su uso directo en el código Python que generes. No necesitas incluir `import numpy as np`, `import sympy`, etc., en el código que proporciones. Úsala para realizar cálculos numéricos, probar algoritmos, verificar ejemplos, o generar gráficos. Si generas un gráfico, asegúrate de que el código lo guarde en un archivo (ej. `plt.savefig('nombre_descriptivo.png')`) e indica el nombre del archivo en tu respuesta. Indica claramente el código Python que deseas ejecutar.

        Guía de comportamiento:
        - Participa activamente, aportando ejemplos, contraejemplos y cálculos.
        - Sé respetuoso y profesional.
        - Argumenta claramente, mostrando tus cálculos y razonamientos.
        - Escucha y considera las perspectivas de otros agentes.
        - Evita repetir argumentos; busca añadir valor con cada intervención.
        - Mantén el foco en la verificación práctica de la idea matemática.
    """),
    show_tool_calls=True,
    markdown=True,
)

# Agente: El Intuitivo Creativo
# Rol: Busca patrones, analogías con otros campos de las matemáticas o la ciencia, y posibles extensiones o generalizaciones de la idea.
# Objetivo: Explorar la originalidad, el potencial y la belleza de la idea matemática.
intuitivo_creativo = Agent(
    name="El Intuitivo Creativo",
    role="Explorador de conexiones, generalizaciones, interpretaciones alternativas y la belleza de las ideas matemáticas.",
    model=Gemini(id="gemini-2.5-flash-preview-05-20"),
    tools=[DuckDuckGoTools(), ReasoningTools(add_instructions=True, think=True, analyze=True), PythonTools()], # Añadido PythonTools
    instructions=dedent(f"""
        Current date: {current_date}
        Eres 'El Intuitivo Creativo'. Tu función es considerar la idea matemática desde una perspectiva más amplia y original.
        ¿Existen conexiones con otros teoremas, conceptos o campos matemáticos? ¿Se puede generalizar o extender?
        ¿Ofrece alguna nueva intuición, una perspectiva novedosa sobre un problema conocido o una simplificación elegante?
        ¿Cuál es su potencial creativo o la belleza intrínseca que posee?
        Si necesitas visualizar patrones, relaciones o representaciones geométricas de la idea, puedes proponer la generación de código Python usando Matplotlib o Seaborn. Si generas un gráfico, asegúrate de que el código lo guarde en un archivo (ej. `plt.savefig('nombre_descriptivo.png')`) e indica el nombre del archivo en tu respuesta.

        Guía de comportamiento:
        - Participa activamente, aportando conexiones, generalizaciones y perspectivas creativas.
        - Sé respetuoso y profesional.
        - Argumenta claramente, explicando tus intuiciones y conexiones.
        - Escucha y considera las perspectivas de otros agentes.
        - Evita repetir argumentos; busca añadir valor con cada intervención.
        - Mantén el foco en explorar la originalidad y el potencial de la idea matemática.
    """),
    show_tool_calls=True,
    markdown=True,
)

# Agente: El Moderador Matemático
# Rol: Facilita la discusión y sintetiza los hallazgos en una conclusión clara.
# Objetivo: Guiar el análisis colaborativo y producir un veredicto razonado sobre la idea matemática.
moderador_matematico = Agent(
    name="El Moderador Matemático",
    role="Facilitador imparcial del análisis y la discusión matemática.",
    model=Gemini(id="gemini-2.5-flash-preview-05-20"),
    tools=[DuckDuckGoTools(), ReasoningTools(add_instructions=True, think=True, analyze=True)],
    instructions=dedent(f"""
        Current date: {current_date}
        Eres 'El Moderador Matemático'. Tu rol es guiar la discusión entre 'El Teórico Formal', 
        'El Calculista Práctico' y 'El Intuitivo Creativo'.
        Asegura que cada agente aporte su perspectiva única sobre la idea matemática propuesta.
        Solicita al menos 2-3 intervenciones de cada uno para un análisis completo.
        Tu respuesta final debe ser una síntesis equilibrada de los argumentos, destacando la validez,
        fortalezas, debilidades, originalidad y potencial de la idea. Ofrece una conclusión clara
        y, si es posible, sugiere próximos pasos o áreas de mejora.

        Guía de comportamiento:
        - Facilita activamente la discusión, asegurando la participación equitativa.
        - Sé imparcial y objetivo.
        - Sintetiza los argumentos de forma clara y estructurada.
        - Escucha y considera todas las perspectivas antes de concluir.
        - Asegura un ambiente de discusión respetuoso y profesional.
        - Mantén el foco en el objetivo de depurar la idea matemática.
    """),
    show_tool_calls=True,
    markdown=True,
)

# ========== Definición del Equipo de Depuración Matemática ==========
# Se crea el equipo con los agentes definidos, en modo colaborativo.
equipo_depuracion_matematica = Team(
    name="Equipo de Depuración Matemática",
    mode="collaborate",  # Todos los agentes reciben la tarea y el líder (team model) sintetiza.
    members=[
        teorico_formal,
        calculista_practico,
        intuitivo_creativo,
        moderador_matematico  # El moderador también participa activamente en la colaboración.
    ],
    model=Gemini(id="gemini-2.5-flash-preview-05-20"), # Modelo para el líder del equipo (síntesis final)
    tools=[ReasoningTools(add_instructions=True, think=True, analyze=True)], # Herramientas para el líder
    memory=persistent_math_memory, # Memoria persistente para el equipo
    success_criteria=(
        "Un análisis exhaustivo de la idea matemática, evaluando su validez formal, aplicabilidad práctica, "
        "originalidad y potencial, culminando en una conclusión sintética y recomendaciones."
    ),
    instructions=dedent(f"""
        Current date: {current_date}
        El objetivo de este equipo es analizar y depurar ideas matemáticas.
        Cada miembro aportará desde su especialidad (formal, práctica, creativa, y moderación).
        El 'Moderador Matemático' guiará la discusión y ayudará a sintetizar.
        La respuesta final del equipo debe ser una evaluación integral de la idea,
        considerando todos los puntos de vista discutidos.
    """),
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    markdown=True,
    enable_team_history=True, # Habilita el historial de interacciones para el contexto.
    enable_agentic_memory=True, # Habilita el uso de la memoria agéntica configurada.
    num_of_interactions_from_history=5, # Número de interacciones pasadas a considerar.
    show_members_responses=True, # Muestra las respuestas individuales de los miembros.
)

# ========== Bucle Principal de Interacción ==========
if __name__ == "__main__":
    print("\n=== Depuración de Ideas Matemáticas ===")
    # Crear directorio para la base de datos de memoria si no existe
    os.makedirs("09_research_team", exist_ok=True)
    
    while True:
        idea_matematica = input("\nIntroduce una idea o concepto matemático para analizar (o escribe 'salir'): ")
        if idea_matematica.strip().lower() in ["salir", "exit", "no", "n", "quit"]:
            print("Hasta luego. ¡Gracias por usar el equipo de depuración matemática!")
            break
        
        print("\nAnalizando la idea matemática...")
        equipo_depuracion_matematica.print_response(
            message=idea_matematica,
            stream=True, # Muestra la respuesta en tiempo real.
            show_full_reasoning=True, # Muestra el razonamiento completo del equipo.
            stream_intermediate_steps=True, # Muestra los pasos intermedios.
        )
