import asyncio
import datetime
import os
from agno.agent import Agent
#from agno.models.ollama import Ollama
from agno.models.google import Gemini
from agno.tools.mcp import MCPTools
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv

# --- Constantes y Configuración ---
REPORTS_DIR = "reportes_md"
#MODEL_ID = "qwen3:4b-fp16" # Asegúrate que este modelo está disponible en tu Ollama
MODEL_ID = "gemini-2.5-flash-preview-05-20"
# --- Funciones Auxiliares ---
def get_current_datetime_for_filename() -> str:
    """Genera una cadena de fecha y hora para nombres de archivo."""
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def sanitize_filename(text: str, max_length: int = 50) -> str:
    """Limpia una cadena para usarla como parte de un nombre de archivo."""
    # Eliminar caracteres no alfanuméricos excepto espacios y guiones bajos
    sanitized = "".join(c if c.isalnum() or c in [' ', '_'] else '_' for c in text)
    # Reemplazar espacios con guiones bajos
    sanitized = sanitized.replace(' ', '_')
    # Truncar si es demasiado largo
    return sanitized[:max_length]

# --- Lógica Principal del Agente ---
async def run_agent_and_save_md(message: str) -> None:
    """
    Ejecuta el agente con el mensaje dado, imprime la respuesta
    y la guarda en un archivo Markdown.
    """
    current_date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Crear directorio de reportes si no existe
    if not os.path.exists(REPORTS_DIR):
        try:
            os.makedirs(REPORTS_DIR)
            print(f"Directorio creado: {REPORTS_DIR}")
        except OSError as e:
            print(f"Error al crear el directorio {REPORTS_DIR}: {e}")
            return

    # Inicializar el servidor MCP
    async with MCPTools(f"fastmcp run server.py") as mcp_tools:
        agent = Agent(
            model=Gemini(id=MODEL_ID),
            instructions=f"""
                        Eres un asistente amigable y servicial especializado en proporcionar información meteorológica.
                        Current date: {current_date_str} 
                        
                        Cuando presentes la información:
                        
                        - Entrega el informe en Español.
                        - Utiliza un tono conversacional y agradable.
                        - Estructura la respuesta de forma clara. Si presentas el clima actual y luego el pronóstico, sepáralos claramente, quizás con un pequeño encabezado o una frase introductoria para cada sección.
                        -El informe debe estar divido en 3 partes:
                            - La primera parte es el clima actual, con todos los detalles y emojis. Debes presentarla en tono conversacional y agregar informacion acerca de la ciudad solicitada. 
                            - La segunda parte es el pronostico de los dias siguientes 5 dias debe ser presentado en formato de tabla Markdown con las siguientes columnas: Ciudad (cuando sea mas de una ciudad), Fecha, Mínima (°C), Máxima (°C), Clima, Emoji.
                            - La tercera parte es una conclusión con recomendaciones en base a los datos obtenidos.
                            - Para esta sección, DESPUÉS de analizar el pronóstico, considera usar la herramienta de búsqueda web (Brave Search) para encontrar información adicional relevante como:
                            - Eventos locales importantes en la ciudad solicitada durante los días del pronóstico.
                            - Sugerencias de actividades específicas para la ciudad solicitada acordes al clima pronosticado (ej. "mejores museos en [Ciudad] si llueve", "parques para visitar en [Ciudad] con sol").
                            - Consejos prácticos adicionales basados en la búsqueda.
                            - Integra esta información de forma natural en tus recomendaciones, citando brevemente la utilidad de la búsqueda si es relevante.
                        - Incorpora los emojis que las herramientas proporcionan para hacer la información más visual y amigable.
                        - Utiliza markdown para mejorar la legibilidad (por ejemplo, negritas para destacar).
                        - Si el usuario pide tanto el clima actual como el pronóstico, asegúrate de que ambas partes sean completas y fáciles de entender.
                        - Si una herramienta devuelve un error, comunícalo claramente al usuario.
                        - Siempre sé cortés y finaliza con una nota amigable si es apropiado.

                        
                        """,
            tools=[mcp_tools,DuckDuckGoTools()],
            show_tool_calls=True, # Muestra las llamadas a herramientas en la consola
            markdown=True,
        )

        print(f"Enviando mensaje al agente: \"{message}\"")
        print("Esperando respuesta del agente...")

        # Usamos chat_async para obtener la respuesta completa para guardarla
        # Si quisieras ver el streaming en consola Y guardar, necesitarías capturar los tokens.
        # Por simplicidad, aquí obtenemos la respuesta completa.
        response_message = await agent.arun(
            message,
            # Los siguientes parámetros son para el streaming en consola si usaras aprint_response
            stream_intermediate_steps=True, 
            stream_tool_calls=True, 
            stream_tool_outputs=True,
            add_datetime_to_instructions=True, # Ya lo estamos haciendo manualmente arriba
        )
        
        if response_message:
            final_response_content = response_message.content
            print("\n--- Respuesta del Agente ---")
            print(final_response_content)
            print("--------------------------\n")

            # Guardar la respuesta en un archivo .md
            timestamp = get_current_datetime_for_filename()
            sanitized_message_part = sanitize_filename(message)
            filename = os.path.join(REPORTS_DIR, f"reporte_{timestamp}_{sanitized_message_part}.md")
            
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(f"# Reporte del Clima: {message}\n\n")
                    f.write(f"Generado el: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write("## Respuesta del Asistente:\n\n")
                    f.write(final_response_content)
                print(f"Respuesta guardada en: {filename}")
            except IOError as e:
                print(f"Error al guardar el archivo {filename}: {e}")
        else:
            print("No se recibió respuesta del agente.")

# --- Punto de Entrada ---
if __name__ == "__main__":
    load_dotenv() # Carga variables de .env si es necesario para las herramientas MCP

    while True:
        user_message = input("\nPor favor, introduce tu consulta de clima (o escribe 'salir' para terminar): ")
        if user_message.lower() in ['salir', 'exit', 'quit', 'no', 'n']:
            print("Hasta luego. ¡Gracias por usar el asistente de clima!")
            break
        
        print(f"Enviando mensaje al agente: \"{user_message}\"")
        asyncio.run(run_agent_and_save_md(user_message))