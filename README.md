# Proyecto Agno-Agent

Este proyecto demuestra cómo utilizar el framework [Agno](https://docs.agno.com) con modelos locales de Ollama para crear agentes de IA avanzados con distintas capacidades:

- **01.py**: Ejemplo básico de agente interactivo con Ollama.
- **02.py**: Agente con herramientas (DuckDuckGoTools) para búsquedas web.
- **03_ollama.py**: Agente con conocimiento local desde un archivo de texto.
- **03_ollama_embed.py**: Agente con búsqueda semántica usando embeddings (`nomic-embed-text`) y LanceDB.
- **04.py**: Agente con memoria y almacenamiento en SQLite, CLI interactivo.

---

## Requisitos previos

- Python 3.8 o superior
- Ollama instalado y servicio corriendo (`https://ollama.com/download`)
- Modelos Ollama descargados (por ejemplo `ollama pull qwen3:4b-fp16`)

## Instalación

1. Clona este repositorio:

   ```bash
   git clone <URL_DE_TU_REPOSITORIO>
   cd 21_aGNOaGENT
   ```

2. Crea y activa un entorno virtual:

   ```bash
   python -m venv env
   # Windows PowerShell:
   env\Scripts\Activate.ps1
   # Windows CMD:
   env\Scripts\activate.bat
   ```

3. Instala las dependencias:

   ```bash
   pip install -U agno ollama duckduckgo-search lancedb sqlalchemy nomic
   ```

4. (Opcional) Instala `python-dotenv` si usas variables de entorno:

   ```bash
   pip install python-dotenv
   ```

---

## Ejecución de ejemplos

### 1. Ejemplo básico

```bash
python 01.py
```

### 2. Agente con herramientas

```bash
python 02.py
```

### 3. Conocimiento local

```bash
python 03_ollama.py
```

### 4. Búsqueda semántica con embeddings

```bash
python 03_ollama_embed.py
```

### 5. Agente con memoria y CLI

```bash
python 04.py
```

Cada script imprime la respuesta en tiempo real (streaming) y muestra llamadas a herramientas cuando aplica.

---

## Estructura de archivos

```
21_aGNOaGENT/
├─ env/                   # Entorno virtual
├─ 01.py                  # Ejemplo básico con Ollama
├─ 02.py                  # Ejemplo con herramientas
├─ 03_ollama.py           # Agente con conocimiento local
├─ 03_ollama_embed.py     # Embeddings semánticos y LanceDB
├─ 04.py                  # Agente con memoria y CLI interactivo
├─ conocimiento.txt       # Archivo de conocimiento de ejemplo
├─ tmp/lancedb/           # Base de datos vectorial LanceDB
└─ README.md              # Documentación del proyecto
```

---

## Buenas prácticas

- Documenta cada script y función con comentarios claros.
- Respeta los principios de Clean Code.
- Mantén el entorno virtual aislado.
- Añade un archivo `.gitignore` para excluir `env/`, `tmp/lancedb/` y archivos temporales.

---

## Licencia

Este proyecto está bajo la licencia MIT. Puedes adaptarlo y reutilizarlo según tus necesidades.
