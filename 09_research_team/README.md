# Equipo de Agentes de Investigación con `agno-agi` y Ollama

Este proyecto demuestra cómo crear un equipo de agentes de IA que pueden discutir un tema entre ellos. Utiliza la biblioteca `agno-agi` para la gestión de los agentes y Ollama para servir modelos de lenguaje grandes (LLMs) localmente durante las pruebas iniciales.

## Descripción

El script principal, `research_team_ollama.py`, configura múltiples agentes, cada uno con un rol o "personalidad" distinta definida a través de un mensaje de sistema. Estos agentes luego participan en una discusión por turnos sobre un tema predefinido. La salida de un agente se convierte en la entrada para el siguiente, simulando una conversación.

Este ejemplo sirve como base para explorar arquitecturas multi-agente más complejas.

## Características

* Múltiples agentes configurables.
* Roles de agente personalizables mediante prompts de sistema.
* Discusión secuencial por rondas.
* Integración con `agno-agi`.
* Diseñado para pruebas iniciales con Ollama.

## Requisitos Previos

* Python 3.8+
* La biblioteca `agno-agi` (asegúrate de que esté instalada y accesible en tu entorno).
* Ollama instalado y en ejecución.
* Un modelo LLM descargado en Ollama (por ejemplo, `ollama pull llama3` o `ollama pull mistral`).

## Instalación

1. **Clona el repositorio (si aplica) o asegúrate de tener esta carpeta de proyecto.**
2. **Instala `agno-agi`**: Sigue las instrucciones de instalación de la biblioteca `agno-agi`. Si es parte de este mismo proyecto, asegúrate de que tu `PYTHONPATH` esté configurado correctamente.
3. **Instala otras dependencias (si las hubiera)**:

    ```bash
    pip install -r requirements.txt 
    ```

    *(Nota: `requirements.txt` se creará si se identifican dependencias específicas además de `agno-agi`, como `python-dotenv`)*

## Configuración de Ollama

1. Asegúrate de que Ollama esté corriendo en tu sistema. Generalmente se accede a través de `http://localhost:11434`.
2. Descarga un modelo si aún no lo has hecho:

    ```bash
    ollama pull nombre_del_modelo_deseado 
    ```

    (e.g., `llama3`, `mistral`, `phi3`)
3. El script `research_team_ollama.py` deberá ser configurado para apuntar a tu modelo Ollama. Esto generalmente implica especificar el nombre del modelo y, posiblemente, la URL base de la API de Ollama si `agno-agi` lo requiere.

## Uso

1. Modifica el script `research_team_ollama.py` si es necesario:
    * Ajusta los `system_message` para cada agente para definir sus roles.
    * Cambia el `discussion_topic`.
    * Configura los parámetros de `agno.agent.Agent` para que utilicen tu modelo Ollama (esto es crucial y depende de la API de `agno-agi`).
    * Puedes crear un archivo `.env` en la carpeta `09_research_team` para configurar `OLLAMA_BASE_URL` y `DEFAULT_OLLAMA_MODEL` si no quieres usar los valores por defecto.
2. Ejecuta el script:

    ```bash
    python research_team_ollama.py
    ```

3. Observa la salida en la consola, que mostrará la discusión entre los agentes.

## Estructura del Proyecto

```text
09_research_team/
├── .env (opcional, para configuraciones)
├── .gitignore
├── plan_implementacion.md
├── README.md
├── research_team_ollama.py  # Script principal de la simulación
└── (posibles archivos de configuración o módulos adicionales)
```

## Próximos Pasos y Mejoras

Consultar `plan_implementacion.md` para ver las fases de desarrollo y posibles mejoras futuras.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request.
