# Plan de Implementación: Equipo de Agentes de Investigación con Ollama

Este documento sigue el progreso de la implementación de un sistema de múltiples agentes de IA que discuten una idea, utilizando `agno-agi` y Ollama para las pruebas iniciales.

## Objetivos del Proyecto

1. Crear un script en Python que simule una discusión entre 2-3 agentes de IA.
2. Cada agente tendrá un rol o personalidad definida.
3. Los agentes interactuarán secuencialmente, respondiendo al output del agente anterior.
4. Utilizar la biblioteca `agno-agi` para la creación y gestión de agentes.
5. Configurar los agentes para que utilicen un modelo LLM servido a través de Ollama para las pruebas iniciales.
6. Proporcionar un historial claro de la discusión generada.

## Fases de Implementación

### Fase 1: Configuración Inicial y Estructura del Proyecto (En Progreso)

* [x] Definición del plan inicial y ejemplo de código conceptual. (Realizado en conversación previa)
* [x] Creación de la carpeta del proyecto: `09_research_team`.
* [x] Creación de este archivo `plan_implementacion.md`.
* [x] Creación de `README.md` con la descripción del proyecto.
* [x] Creación de `.gitignore`.
* [ ] Creación del script principal `research_team_ollama.py`.
  * [ ] Implementación de la clase `Agent` o uso directo de `agno.agent.Agent`.
  * [ ] Configuración de los agentes para usar Ollama.
  * [ ] Lógica para la orquestación de la discusión.
* [ ] Pruebas iniciales de funcionamiento con Ollama.

### Fase 2: Refinamiento y Pruebas

* [ ] Ajustar los prompts de sistema de los agentes para mejorar la calidad de la discusión.
* [ ] Implementar un manejo de errores más robusto.
* [ ] Probar con diferentes modelos de Ollama (si están disponibles).
* [ ] Evaluar la coherencia y relevancia de las respuestas de los agentes.

### Fase 3: (Opcional) Expansión

* [ ] Permitir más rondas de discusión.
* [ ] Introducir un "moderador" o un agente "resumidor".
* [ ] Guardar el historial de la discusión en un archivo.
* [ ] Explorar formas más complejas de interacción entre agentes (ej. no solo secuencial).

## Tecnologías Clave

* Python
* `agno-agi` (biblioteca para agentes de IA)
* Ollama (para servir modelos LLM localmente)
* (Opcional) Streamlit (si se decide añadir una UI en el futuro)

## Notas Adicionales

* Asegurarse de que Ollama esté en ejecución y el modelo deseado esté descargado (`ollama pull <nombre_del_modelo>`).
* La configuración de `agno-agi` para conectarse a Ollama podría requerir especificar el endpoint (ej. `http://localhost:11434`) y el nombre del modelo.
