from pathlib import Path

from agno.agent import Agent
from agno.media import Image
from agno.models.ollama import Ollama

agent = Agent(model=Ollama(id="gemma3:4b-it-qat"), markdown=True)

image_path = Path(__file__).parent.joinpath("super-agents.png")
agent.print_response(
    "describe la imagen, en español",
    images=[Image(filepath=image_path)],
    stream=True,
)
