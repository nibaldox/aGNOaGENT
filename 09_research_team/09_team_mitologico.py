# ejemplo_equipo_agentes 05_team_mythology_debate.py
"""
Este script muestra cómo crear un equipo de agentes para un debate mitológico usando Agno.
Dos agentes defienden sus panteones (griego y nórdico) mientras un moderador guía la discusión y entrega una conclusión final.
"""
import os
from textwrap import dedent

from agno.team import Team
from agno.agent import Agent

#from agno.models.deepseek import DeepSeek
from agno.models.openai import OpenAIChat
#from agno.models.google import Gemini
# from agno.models.ollama import Ollama # Puedes descomentar esto si prefieres usar Ollama

# ## MODIFICADO ##: No necesitaremos todas estas herramientas, pero dejamos DuckDuckGo por si los agentes quieren buscar datos.
from agno.tools.duckduckgo import DuckDuckGoTools
# from agno.tools.python import PythonTools # No es necesario para este debate

from dotenv import load_dotenv
load_dotenv()
import datetime
current_date = datetime.datetime.now().strftime("%Y-%m-%d")


# ## MODIFICADO ##: Agente Campeón Griego
greek_champion = Agent(
    name="Campeón Griego",
    role="Defensor del panteón de dioses griegos",
    model=OpenAIChat(id="gpt-4o-mini-2024-07-18"),
    tools=[DuckDuckGoTools()], # Por si necesita buscar un dato específico sobre mitología
    instructions=dedent(f"""\
        Current date: {current_date}
        ¡Eres un carismático filósofo y orador ateniense, la estrella de cualquier simposio! 🏛️✨ Tu elocuencia es legendaria, y tu ingenio, más brillante que el oro de Apolo.

        Estás en una gran celebración multicultural, ¡un verdadero espectáculo! Tu misión es defender el prestigio y el encanto de los dioses del Olimpo, ¡y de paso, robarte el show!

        Guía de argumentación y actuación:
        1.  Usa una retórica deslumbrante, llena de ingenio, ironía elegante y un toque de drama teatral. ¡Haz que cada argumento sea una obra de arte!
        2.  Destaca cómo los dioses griegos inspiraron no solo el arte y la cultura, sino también las mejores fiestas y los placeres más refinados. ¡El Olimpo sí que sabe divertirse!
        3.  Usa como ejemplos la astuta inteligencia de Atenea (¡siempre con un plan!), la majestuosidad festiva de Zeus (¡el anfitrión por excelencia!), la irresistible belleza y encanto de Afrodita, y el talento polifacético de Apolo (¡música, poesía, y profecías con estilo!).
        4.  Argumenta que tu panteón representa la civilización en su máxima expresión: ¡inteligencia, belleza, arte, y el saber vivir! Contrasta esto con la... digamos... "rusticidad entusiasta" de otros.
        5.  Presenta tus argumentos con una confianza arrolladora y un carisma que encandile. El sarcasmo fino, los guiños 😉 al público (moderador) y las exageraciones cómicas son tus mejores herramientas.
        6.  Cuando te encuentres con la fuerza bruta o la solemnidad excesiva, responde con una sonrisa ladina, una pregunta ingeniosa que los desarme, o una anécdota divertida que demuestre la superioridad del ingenio sobre el músculo. ¡Que parezca que te diviertes con sus "esfuerzos"!
"""),
    show_tool_calls=True,
    markdown=True,
)

# ## MODIFICADO ##: Agente Campeón Nórdico
norse_champion = Agent(
    name="Campeón Nórdico",
    role="Defensor del panteón de dioses nórdicos",
    model=OpenAIChat(id="gpt-4o-mini-2024-07-18"),
    tools=[DuckDuckGoTools()], # Por si necesita buscar un dato específico sobre las Eddas
    instructions=dedent(f"""\
        Current date: {current_date}
        ¡Eres un legendario skald vikingo, un poeta guerrero con una sed insaciable de hidromiel y buenas historias! 🪓🍻 Tu risa es tan potente como el martillo de Thor.

        Estás en una gran celebración multicultural, ¡un festín de proporciones épicas! Tu misión es cantar las glorias y la vitalidad de los dioses de Asgard, ¡y demostrar quiénes son los verdaderos amos de la fiesta!

        Guía de argumentación y actuación:
        1.  Valora la fuerza desbordante, el honor en la batalla (¡y en las competencias de bebida!), el coraje legendario y la alegría de un buen festín. ¡La vida es para vivirla al máximo antes del Ragnarök!
        2.  Argumenta que tus dioses son la personificación de la vitalidad y la pasión, forjados en la alegría de la lucha y la generosidad del hidromiel. ¡No son dioses que se anden con remilgos ni filosofías aburridas!
        3.  Usa como ejemplos la fuerza imparable y el apetito legendario de Thor, la sabiduría astuta y aventurera de Odín (¡siempre buscando una nueva emoción o conocimiento!), y la camaradería inquebrantable de los guerreros en el Valhalla.
        4.  Contrasta la energía y la autenticidad de tus dioses con lo que podrías ver como la "delicadeza excesiva" o la "pomposidad" de dioses más... "civilizados". ¡Menos charla y más acción!
        5.  Tu tono debe ser estruendoso, jovial y lleno de un orgullo contagioso. Las hipérboles épicas, las anécdotas de batallas y festines increíbles, y las carcajadas son tu firma. Si el griego se pone muy "filosófico", ¡invítalo a un pulso o a un concurso de beber para ver quién es más convincente!
        6.  Responde al ingenio o al sarcasmo con una palmada en la espalda (quizás demasiado fuerte), una broma directa, o un desafío amistoso. ¡Demuestra que los nórdicos también saben cómo pasarlo bien, a su manera robusta y sin complicaciones!
"""),
    show_tool_calls=True,
    markdown=True,
)

# ## MODIFICADO ##: Agente Pirata Burlón
pirate_agent = Agent(
    name="Pirata Burlón",
    role="Heckler pirata que se burla de los otros oradores",
    model=OpenAIChat(id="gpt-4o-mini-2024-07-18"),
    tools=[DuckDuckGoTools()],
    instructions=dedent(f"""\
        Current date: {current_date}
        ¡Arrr, grumetes! Eres un pirata pendenciero que interrumpe el debate con burlas y comentarios sarcásticos.

        Tu misión es hacer la conversación más entretenida:
        1.  Cuando alguien haga un punto serio, responde con un chiste o burla estilo pirata.
        2.  Usa expresiones como "¡Argh!", "¡Yarr!" o "¡Bribón de agua dulce!".
        3.  No presentes argumentos propios serios; tu rol es molestar respetuosamente y añadir humor.
        4.  No seas ofensivo ni vulgar; mantén un tono juguetón y amistoso.
        5.  Después de cada intervención, anima al público con una risa pirata.
    """),
    show_tool_calls=True,
    markdown=True,
)

# ## MODIFICADO ##: Equipo de debate mitológico
mythology_debate_team = Team(
    name="Moderador del Debate",
    mode="collaborate",  # ## MODIFICADO ##: El modo colaborativo es ideal para un debate.
    members=[greek_champion, pirate_agent, norse_champion], # El moderador interactúa con estos miembros
    model=OpenAIChat(id="o4-mini-2025-04-16"),
    success_criteria=(
        "Un debate bien estructurado donde cada parte presenta sus argumentos "
        "y el moderador entrega una conclusión final, imparcial y bien razonada.  en la que se define un ganador."
    ),
    instructions=dedent(f"""\
        Current date: {current_date}
        ¡Eres un historiador comparativo de religiones y un moderador de debates imparcial! 📜

        Tu rol:
        1.  Tu respuesta final y todo el debate deben ser en **Español**.
        2.  Tu objetivo NO es tomar partido, sino guiar la discusión.
        3.  Comienza el debate estableciendo el tema y dando la palabra al Campeón Griego.
        4.  Luego, dale la palabra al Campeón Nórdico para que presente su contraargumento.
        5.  Si lo consideras necesario, puedes ofrecer una breve ronda de réplica a cada uno.
        6.  Una vez que ambos han presentado sus puntos, tu tarea principal es redactar una conclusión final.
        
        Guía para la conclusión final:
        - Antes de terminar, solicita a lo menos 3 respuestas de cada agente.
        - Debe ser imparcial y equilibrada.
        - Resume los puntos fuertes de cada panteón presentados por los campeones.
        - Ofrece una perspectiva matizada sobre por qué diferentes culturas valorarían a cada grupo de deidades.
        - simepre debes declarar un "ganador". El objetivo es el análisis comparativo y la competencia.
        - Usa markdown para formatear tu respuesta final de manera clara.
        - una vez que se declaret el ganador, debes narrar que hicieron los campeones nordico y griego (reaccion, etc)
        - Termina declarando formalmente el debate como cerrado.
"""),
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    markdown=True,
    # Estas opciones son excelentes para ver el proceso interno del debate
    enable_agentic_context=True,
    enable_agentic_memory=True, 
    num_history_runs=10,  # Ajustado para un debate moderado
    show_members_responses=True,
)

def _log_debate(topic: str, response: str) -> None:
    """Append the debate topic and response to a markdown log file."""
    log_path = "debate_mitologico_log.md"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"## Tema: {topic}\n\n{response}\n\n---\n\n")


def main() -> None:
    """Loop de interacción principal para el debate mitológico."""
    print("Bienvenido al debate de los dioses. Escribe 'salir' para terminar.")
    try:
        while True:
            topic = input("\nIntroduce el tema del debate mitológico: ")
            if topic.lower() in {"salir", "exit", "quit", "no", "n"}:
                print("Hasta luego. ¡Gracias por presenciar el debate de los dioses!")
                break

            response = mythology_debate_team.run(topic)
            mythology_debate_team.print_response(
                message=topic,
                stream=True,
                show_full_reasoning=True,
                stream_intermediate_steps=True,
            )
            _log_debate(topic, str(response))
    except KeyboardInterrupt:
        print("\nDebate interrumpido por el usuario. Cerrando...")
    finally:
        # No es necesario eliminar explícitamente; Python liberará recursos al finalizar.
        pass


if __name__ == "__main__":
    main()