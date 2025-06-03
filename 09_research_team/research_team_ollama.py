import asyncio
import os
import datetime
from dotenv import load_dotenv

# Intenta importar Agent de agno_agi. Si no está directamente en el path,
# esto podría fallar o necesitar ajustes en PYTHONPATH.
try:
    from agno.agent import Agent
    from agno.models.ollama import Ollama # Importar la clase de modelo Ollama
    from ollama import Client as OllamaClient # Importar el cliente de Ollama
    AGNO_AVAILABLE = True
    print("INFO: `agno.agent.Agent` y `agno.models.ollama.Ollama` importados correctamente.")
except ImportError:
    print("ADVERTENCIA: No se pudo importar 'agno.agent.Agent'. Se usará una clase Placeholder.")
    print("           Asegúrate de que agno-agi esté instalado y en tu PYTHONPATH.")
    AGNO_AVAILABLE = False

    class Agent: # Placeholder si agno-agi no está disponible
        """
        Clase Placeholder para simular agno.agent.Agent cuando no está disponible.
        Permite probar el flujo de la discusión.
        """
        def __init__(self, system_message: str, agent_name: str, llm_config: dict = None):
            """
            Inicializa el agente placeholder.
            :param system_message: Mensaje de sistema que define el rol del agente.
            :param agent_name: Nombre del agente.
            :param llm_config: Configuración simulada del LLM (ej. para Ollama).
            """
            self.system_message = system_message
            self.name = agent_name
            self.llm_config = llm_config if llm_config else {}
            model_name = self.llm_config.get('model', 'desconocido')
            print(f"  [Placeholder Agent] '{self.name}' inicializado.")
            print(f"    Rol: {self.system_message[:70]}...")
            print(f"    Modelo (simulado): {model_name}")

        async def arun(self, message: str, **kwargs) -> str:
            """
            Simula la ejecución asíncrona del agente y genera una respuesta.
            :param message: Mensaje de entrada para el agente.
            :param kwargs: Argumentos adicionales (ignorados en placeholder).
            :return: Respuesta simulada del agente.
            """
            print(f"\n--- {self.name} (Placeholder) procesando --- ")
            print(f"Input: '{message[:100]}...' ")
            # print(f"Config LLM (simulada): {self.llm_config}")
            
            response_prefix = f"Como {self.name} (usando el modelo simulado {self.llm_config.get('model', 'placeholder')}), considero que "
            if "Innovador" in self.name:
                response = response_prefix + f"deberíamos enfocarnos en las posibilidades ilimitadas y las tecnologías emergentes relacionadas con '{message[:50]}...' para romper paradigmas."
            elif "Crítica" in self.name or "Crítico" in self.name:
                response = response_prefix + f"es imperativo analizar con detenimiento los riesgos inherentes, las posibles fallas y las implicaciones éticas de '{message[:50]}...' antes de cualquier avance."
            elif "Pragmático" in self.name or "Pragmática" in self.name:
                response = response_prefix + f"necesitamos un plan de acción tangible y eficiente, evaluando los recursos, el mercado y la implementación paso a paso para '{message[:50]}...' con realismo."
            else:
                response = response_prefix + f"mi perspectiva sobre '{message[:50]}...' es compleja y requiere más análisis."
            
            await asyncio.sleep(0.2) # Simular una pequeña demora de "pensamiento"
            return response

# Cargar variables de entorno desde .env si existe en esta carpeta
# Útil para OLLAMA_BASE_URL, DEFAULT_OLLAMA_MODEL, o API keys si fueran necesarias
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print("INFO: Archivo .env local cargado.")

# --- Configuración Específica para Ollama ---
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_OLLAMA_MODEL = os.getenv("DEFAULT_OLLAMA_MODEL", "qwen3:4b-fp16") # o llama3, mistral, phi3, etc.

def get_ollama_llm_config(model_name: str = DEFAULT_OLLAMA_MODEL) -> dict:
    """
    Prepara la configuración del LLM para un agente que usará Ollama.
    LA ESTRUCTURA DE ESTE DICCIONARIO ES UNA SUPOSICIÓN y debe ser adaptada
    a cómo `agno.agent.Agent` espera la configuración del LLM.

    Podría ser que `agno.agent.Agent` espere un objeto LLM instanciado de una clase
    compatible con Ollama (similar a `langchain_community.llms.Ollama`)
    o un diccionario de parámetros.

    Ejemplo de suposición para un diccionario de configuración:
    {
        "provider": "ollama", // Identificador para agno-agi
        "model": "llama3:latest", // Nombre del modelo en Ollama
        "base_url": "http://localhost:11434", // URL de la API de Ollama
        "temperature": 0.7, // Parámetro de inferencia
        // Otros parámetros como system_prompt, max_tokens, etc.
    }
    """
    return {
        "provider": "ollama",  # Suposición, verificar con la documentación de agno-agi
        "model": model_name,
        "base_url": OLLAMA_BASE_URL, # agno-agi podría tener esto como default
        "temperature": 0.7,
        # "max_tokens": 2048, # Ejemplo
        # "system_prompt": "..." # Generalmente el system_message del Agent tiene precedencia
    }

async def simulate_agent_discussion(topic: str, agents_config: list[dict], rounds: int = 2):
    global AGNO_AVAILABLE # Declarar que usaremos la variable global
    """
    Simula una discusión entre varios agentes sobre un tema dado.

    :param topic: El tema inicial de la discusión.
    :param agents_config: Lista de diccionarios, cada uno con 'name', 'system_message' y 'llm_config'.
    :param rounds: Número de rondas completas de discusión (cada agente habla una vez por ronda).
    """
    print(f"\n{'='*15} Iniciando Discusión {'='*15}")
    print(f"Tema: {topic}")
    print(f"Usando: {'agno.agent.Agent' if AGNO_AVAILABLE else 'Placeholder Agent'}")
    if not AGNO_AVAILABLE:
        print("ADVERTENCIA: `agno.agent.Agent` no disponible. Las interacciones con Ollama NO ocurrirán.")
    else:
        print(f"INFO: Configurado para usar Ollama en {OLLAMA_BASE_URL} con modelo por defecto {DEFAULT_OLLAMA_MODEL}")
        print("       Asegúrate de que Ollama esté en ejecución y el modelo esté disponible.")
        print("       (ej. `ollama pull {DEFAULT_OLLAMA_MODEL}`)")
    
    agents = []
    print("\n--- Configurando Agentes ---")
    for config in agents_config:
        # Aquí es donde se instancia el Agent real de agno-agi.
        # La clave es cómo `agno.agent.Agent` acepta la configuración de Ollama.
        # Puede ser a través de un parámetro `llm`, `model_config`, `llm_params`,
        # o configurando variables de entorno que `agno-agi` lea.
        # O podría requerir un objeto LLM específico de `agno-agi` o compatible.
        
        # Para el placeholder, pasamos agent_name y llm_config directamente.
        # Para el Agent real, esto dependerá de su constructor.
        # Ejemplo de cómo podría ser con agno.agent.Agent (SUPOSICIÓN):
        # agent = Agent(
        #     system_message=config["system_message"],
        #     name=config["name"], # o role=config["name"]
        #     llm_configuration=config["llm_config"] # o llm=OllamaCompatibleLLM(**config["llm_config"])
        # )
        # Almacenamos una tupla: (nombre_configurado, instancia_agente)
        # Esto nos permite mantener nuestro nombre de agente si Agent() no lo soporta.
        try:
            ollama_client_instance = OllamaClient(host=OLLAMA_BASE_URL)
            model_config = config["llm_config"]
            ollama_model_instance = Ollama(
                id=model_config.get("model", DEFAULT_OLLAMA_MODEL),
                client=ollama_client_instance,
                options={"temperature": model_config.get("temperature", 0.7)}
            )
            agent_instance = Agent(
                system_message=config["system_message"],
                model=ollama_model_instance
            )
            agents.append({"name": config["name"], "instance": agent_instance, "llm_config": config["llm_config"]})
            print(f"  Agente '{config['name']}' instanciado con `agno.agent.Agent`.")
        except TypeError as e:
            print(f"  ERROR al instanciar `agno.agent.Agent` para '{config['name']}': {e}")
            print(f"  Revisar los parámetros esperados por Agent.__init__ de agno-agi.")
            print(f"  Usando Placeholder para '{config['name']}' como fallback.")
            # Fallback al placeholder si la instanciación del Agent real falla
            placeholder_agent = globals()['Agent']( # Accede al Agent placeholder global
                system_message=config["system_message"]
                # agent_name y llm_config no son parte del constructor del placeholder
            )
            agents.append({"name": config["name"], "instance": placeholder_agent, "llm_config": config["llm_config"], "is_placeholder": True})
            print("INFO: Fallback a Placeholder Agent. AGNO_AVAILABLE se establecerá en False.")
            AGNO_AVAILABLE = False # Modificar la variable global


    current_message = topic
    discussion_history = [f"# Discusión sobre: {topic}\n"]

    # Agregar detalles de los agentes configurados al historial
    discussion_history.append("**Agentes Configurados:**")
    for ag_info in agents: # 'agents' está poblado en este punto
        _llm_c = ag_info.get("llm_config", {})
        _model_n = _llm_c.get("model", DEFAULT_OLLAMA_MODEL)
        _is_ph = ag_info.get("is_placeholder", False)
        _type_d = "Placeholder" if _is_ph else _model_n
        discussion_history.append(f"- {ag_info['name']} (Modelo: {_type_d})")
    discussion_history.append("\n---\n")

    for i in range(rounds):
        print(f"\n--- Ronda de Discusión {i+1} / {rounds} ---")
        for agent_idx, agent_dict in enumerate(agents):
            agent_name = agent_dict["name"]
            agent_instance = agent_dict["instance"]
            agent_llm_config = agent_dict["llm_config"]
            is_placeholder = agent_dict.get("is_placeholder", not AGNO_AVAILABLE)

            agent_model_info = agent_llm_config.get('model', 'N/A')
            print(f"\nTurno de: {agent_name} (Modelo: {agent_model_info}{' - Placeholder' if is_placeholder else ''})")
            
            input_message_for_agent = current_message
            
            try:
                response = await agent_instance.arun(input_message_for_agent)
                
                if hasattr(response, 'content'):
                    response_content = response.content
                elif isinstance(response, str):
                    response_content = response
                else:
                    print(f"ADVERTENCIA: Tipo de respuesta inesperado de {agent_name}: {type(response)}")
                    response_content = str(response)

            except Exception as e:
                print(f"ERROR: Excepción durante la ejecución del agente {agent_name}: {e}")
                import traceback
                traceback.print_exc()
                response_content = f"(Error al generar respuesta para {agent_name}: {type(e).__name__})"

            print(f"Respuesta de {agent_name}: {response_content}")
            discussion_history.append(f"\n## Ronda {i+1} / {rounds}")
            discussion_history.append(f"### Turno: {agent_name} (Modelo: {agent_model_info}{' - Placeholder' if is_placeholder else ''})\n")
            if not (i == 0 and agent_idx == 0):
                discussion_history.append(f"**Mensaje Recibido:**\n```text\n{input_message_for_agent}\n```\n")
            else:
                discussion_history.append("**Inicio con el Tema Principal.**\n")
            discussion_history.append(f"**Respuesta Generada:**\n```text\n{response_content}\n```\n---\n")

            current_message = response_content


    print(f"\n{'='*15} Fin de la Discusión {'='*15}")
    # --- Guardar discusión en archivo Markdown ---
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Sanitizar el tema para usarlo en el nombre del archivo (simple sanitización)
    safe_topic = "".join(c if c.isalnum() else "_" for c in topic[:40]).rstrip("_")
    output_filename = f"discussion_log_{safe_topic}_{timestamp}.md"
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write("\n".join(discussion_history))
        print(f"\nINFO: La discusión completa ha sido guardada en: {output_filename}")
    except IOError as e:
        print(f"ERROR: No se pudo guardar la discusión en {output_filename}: {e}")
    
    print("\n\n=============== Historial Completo de la Discusión ===============")
    for entry_idx, entry in enumerate(discussion_history):
        print(f"{entry_idx}. {entry}")

async def main():
    """
    Función principal para configurar y ejecutar la simulación de discusión.
    """
    # 1. Definición de Agentes: Nombres, roles (system_message) y configuración del LLM
    agents_configuration = [
        {
            "name": "El Innovador Tech",
            "system_message": "Eres 'El Innovador Tech', un IA visionario. Tu objetivo es proponer ideas audaces y tecnológicamente avanzadas, sin preocuparte inicialmente por las limitaciones. Piensa en el futuro y en cómo la tecnología puede resolver grandes problemas. Sé conciso y directo.",
            "llm_config": get_ollama_llm_config(model_name=os.getenv("INNOVATOR_MODEL", DEFAULT_OLLAMA_MODEL))
        },
        {
            "name": "La Analista Crítica",
            "system_message": "Eres 'La Analista Crítica', una IA con un profundo conocimiento técnico y de negocios. Tu función es examinar las ideas propuestas, identificar posibles fallos, riesgos, desafíos de implementación, y consideraciones éticas. Sé rigurosa, detallada y concisa.",
            "llm_config": get_ollama_llm_config(model_name=os.getenv("CRITIC_MODEL", DEFAULT_OLLAMA_MODEL))
        },
        {
            "name": "El Estratega Pragmático",
            "system_message": "Eres 'El Estratega Pragmático', una IA enfocada en la viabilidad y la ejecución. Tomas las ideas innovadoras y las críticas, y buscas formular un plan de acción realista. Consideras recursos, mercado, pasos incrementales y cómo llevar una idea a la realidad. Ofrece soluciones concretas y concisas.",
            "llm_config": get_ollama_llm_config(model_name=os.getenv("PRAGMATIST_MODEL", DEFAULT_OLLAMA_MODEL))
        }
    ]

    # 2. Tema de Discusión
    discussion_topic = "Idea Central: Impacto de la IA Generativa en el Empleo: Analizar los posibles cambios en el mercado laboral, nuevas profesiones que podrían surgir y cómo la sociedad puede adaptarse."

    # 3. Orquestar la Discusión
    await simulate_agent_discussion(topic=discussion_topic, agents_config=agents_configuration, rounds=5)

if __name__ == "__main__":
    print("INFO: Iniciando script de simulación de equipo de investigación...")
    # Manejo para ejecutar asyncio en diferentes entornos (script vs Jupyter)
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "asyncio.run() cannot be called from a running event loop" in str(e):
            print("INFO: Detectado loop de eventos existente. Agendando main() como tarea.")
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(main())
            else: # No debería ocurrir si el error anterior fue lanzado
                print("ERROR: Loop de eventos no está corriendo a pesar del error. Re-lanzando.")
                raise
        else:
            print(f"ERROR: Ocurrió un RuntimeError inesperado: {e}")
            raise
    except Exception as e:
        print(f"ERROR: Ocurrió una excepción no manejada en el nivel superior: {e}")
        import traceback
        traceback.print_exc()

    print("INFO: Script de simulación finalizado.")
