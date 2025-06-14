# Equipo de Agentes de Investigación# Proyecto Multi-Agente de Debate y Análisis

Este repositorio contiene herramientas y scripts para la orquestación de equipos multi-agente orientados a debates mitológicos y análisis crítico de ideas de negocio, utilizando la librería `agno-agi` y modelos LLM de Gemini y Ollama.

## Estructura principal

- `09_team_mitologico.py`: Debate entre campeones de panteones mitológicos, moderado por un agente imparcial.
- `business_team.py`: Análisis crítico de ideas de negocio por un equipo de IA con roles diferenciados y un moderador.
- `research_team_ollama.py`: Ejemplo de orquestación multi-agente usando modelos Ollama locales.
- `math_debug_team.py`: Equipo de agentes para el análisis y depuración de ideas matemáticas.
- `.gitignore`: Exclusión de archivos y carpetas temporales o sensibles.
- `plan_implementacion.md`: Seguimiento de la implementación y mejoras.

## business_team.py

### ¿Qué hace?

Permite analizar cualquier idea de negocio con un equipo de **seis agentes IA especializados**:

- **El Innovador Tech**: Propone ideas audaces y tecnológicas.
- **La Analista Crítica**: Identifica riesgos, fallos y desafíos.
- **El Estratega Pragmático**: Sugiere planes de acción realistas.
- **El Investigador de Mercado**: Aporta métricas de mercado, benchmarking de competidores y tendencias, citando fuentes confiables.
- **El Consejero Legal**: Evalúa regulación, propiedad intelectual y riesgos de cumplimiento, proponiendo estrategias legales y de mitigación.
- **Moderador**: Facilita la discusión, asegura la participación equitativa y sintetiza los hallazgos en una conclusión integradora.

Todos los agentes siguen guías de comportamiento explícitas para asegurar profesionalismo, respeto y foco en el análisis constructivo.

### Ejecución

1. Instala dependencias:

   ```bash
   pip install -r requirements.txt
   ```

2. Ejecuta el script:

   ```bash
   python business_team.py
   ```

3. Ingresa una idea de negocio cuando se solicite (ejemplo: "Una app de salud mental personalizada con IA").
4. Observa el análisis multiagente y la conclusión del moderador.

### Ejemplo de ideas para probar

Puedes utilizar las siguientes ideas para analizar con `business_team.py`:

- Plataforma que conecta agricultores con consumidores urbanos.
- Red social para adultos mayores.
- Marketplace de experiencias educativas en realidad virtual/aumentada.
- App de reciclaje gamificado.
- Microcréditos blockchain para emprendedores.
- App de salud mental con IA personalizada.
- Plataforma de microcréditos blockchain.
- Servicio de suscripción de alimentos personalizados según ADN.
- Consultoría legal automatizada para pymes.
- Gestión inteligente de energía para hogares.
- Tienda online de productos artesanales con trazabilidad blockchain.
- Red de movilidad urbana con vehículos autónomos compartidos.

**Ejemplo de prompt:**

```text
Una plataforma en línea que conecta a pequeños agricultores con consumidores urbanos, permitiendo la compra directa de productos frescos y orgánicos, eliminando intermediarios.
```

### Integración ReasoningTools

El equipo utiliza ReasoningTools para potenciar el análisis, la argumentación y la generación de planes de acción.

## math_debug_team.py

### ¿Qué hace?

Permite analizar y depurar ideas, conjeturas o conceptos matemáticos con un equipo de cuatro agentes IA especializados:

- **El Teórico Formal**: Se enfoca en la rigurosidad lógica, pruebas formales, axiomas y definiciones precisas.
- **El Calculista Práctico**: Busca ejemplos, contraejemplos, realiza cálculos y verifica la idea en casos concretos.
- **El Intuitivo Creativo**: Explora conexiones con otras áreas, posibles generalizaciones, interpretaciones alternativas y la originalidad de la idea.
- **El Moderador Matemático**: Facilita la discusión entre los expertos y sintetiza los hallazgos en una conclusión clara sobre la validez y potencial de la idea matemática.

Todos los agentes están diseñados para colaborar, seguir guías de comportamiento y mantener un alto nivel de profesionalismo y respeto, enfocándose en un análisis constructivo.

### Ejecución

1. Asegúrate de tener las dependencias instaladas (ver `requirements.txt` en el directorio raíz del proyecto, si aplica, o instala `agno-agi`, `python-dotenv`, `google-generativeai` si no lo has hecho).
2. Ejecuta el script desde el directorio raíz del proyecto (`d:\12_WindSurf\21_aGNOaGENT`):

   ```bash
   python 09_research_team/math_debug_team.py
   ```

3. Ingresa una idea o concepto matemático cuando se solicite (ejemplo: "La conjetura de Goldbach" o "Una nueva aproximación para resolver ecuaciones diferenciales parciales no lineales").
4. Observa el análisis multiagente y la conclusión del moderador.

### Ejemplo de ideas para probar

Puedes utilizar las siguientes ideas, preguntas o conceptos para analizar con `math_debug_team.py`:

- "La hipótesis de Riemann: ¿cuáles son sus implicaciones y el estado actual de la investigación?"
- "Analizar la prueba de Euclides sobre la infinitud de los números primos. ¿Es lógicamente sólida? ¿Se pueden encontrar extensiones o generalizaciones?"
- "Verificar si el número 15485863 es primo y explicar el método utilizado."
- "Explorar la secuencia de Fibonacci: generar los primeros 15 términos, discutir su fórmula cerrada (si es posible encontrarla) y visualizar su crecimiento."
- "Dada la función f(x) = x^3 - 6x^2 + 11x - 6, encontrar sus raíces y solicitar un gráfico de la función en el intervalo [-1, 4]."
- "¿Qué es un fractal? Explicar el concepto y dar ejemplos, como el conjunto de Mandelbrot. ¿Se podría generar una visualización simple de un fractal?"
- "Discutir el Último Teorema de Fermat: su enunciado, historia y la naturaleza de su prueba."
- "Un nuevo método para la factorización de números primos grandes: ¿cuáles serían sus posibles ventajas y desventajas frente a los métodos conocidos?"
- "La posible existencia de un nuevo tipo de número o estructura algebraica: ¿qué propiedades debería tener y cómo se relacionaría con las estructuras existentes?"
- "Una interpretación geométrica alternativa para los números complejos: ¿qué ventajas podría ofrecer?"
- "La aplicación de la teoría de categorías a la biología teórica: ¿qué tipo de problemas biológicos podrían modelarse mejor con este enfoque?"

**Ejemplo de prompt detallado:**

```text
Quiero analizar la siguiente idea: 'Todo número par mayor que 2 es la suma de dos números primos.' ¿Cuál es el nombre de esta conjetura? ¿Es considerada verdadera? ¿Qué tipo de pruebas o evidencias existen a su favor o en contra? ¿Podemos probarla para algunos números pares pequeños, por ejemplo, hasta 20?
```

### Características Adicionales

- **Memoria Persistente**: El equipo utiliza una base de datos SQLite (`09_research_team/math_debug_memory.db`) para recordar interacciones pasadas y mantener contexto entre sesiones.
- **Integración de Herramientas**: Al igual que otros equipos, utiliza `DuckDuckGoTools` para búsqueda de información y `ReasoningTools` para mejorar la calidad del análisis y la síntesis.

### Principios de clean code

- Código modular, documentado y fácil de entender.
- Instrucciones y prompts claros en español.
- Separación de responsabilidades y roles.
- Manejo robusto de errores y recursos.

### Requisitos

- Python 3.8+
- agno-agi
- Modelos Gemini u Ollama (configurables)
- DuckDuckGoTools y ReasoningTools

### Uso avanzado

- Puedes adaptar los roles, prompts o modelos de los agentes fácilmente.
- El sistema es extensible para otros dominios (legal, educativo, etc).

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
    - Ajusta los `system_message` para cada agente para definir sus roles.
    - Cambia el `discussion_topic`.
    - Configura los parámetros de `agno.agent.Agent` para que utilicen tu modelo Ollama (esto es crucial y depende de la API de `agno-agi`).
    - Puedes crear un archivo `.env` en la carpeta `09_research_team` para configurar `OLLAMA_BASE_URL` y `DEFAULT_OLLAMA_MODEL` si no quieres usar los valores por defecto.
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
