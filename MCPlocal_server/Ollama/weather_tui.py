import asyncio
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll, Horizontal
from textual.widgets import Header, Footer, Input, Button, Markdown
from textual.reactive import reactive

# Importar la función del backend
from client_MD import run_agent_and_save_md, load_dotenv

class WeatherTUI(App):
    """Una TUI para mostrar informes del clima."""

    CSS_PATH = "weather_tui.tcss" # Enlaza al archivo CSS

    TITLE = "Asistente de Clima Interactivo"

    # Bindings para acciones comunes
    BINDINGS = [
        ("q", "quit", "Salir"),
        ("ctrl+c", "quit", "Salir"),
        ("d", "toggle_dark", "Modo Oscuro"),
    ]

    # Variable reactiva para almacenar el contenido del informe
    report_content = reactive("### ¡Bienvenido!\n\nEscribe tu consulta de clima arriba y presiona 'Obtener Informe'.", layout=True)
    is_loading = reactive(False)

    def compose(self) -> ComposeResult:
        """Crea los widgets hijos para la aplicación."""
        yield Header()
        with Horizontal(id="input_area"):
            yield Input(placeholder="Escribe tu consulta de clima aquí...", id="query_input")
            yield Button("Obtener Informe", id="submit_button", variant="primary")
        
        with VerticalScroll(id="results_area"):
            yield Markdown(id="report_markdown") # Inicializar solo con ID
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Maneja el evento de presión del botón."""
        if event.button.id == "submit_button":
            query_input = self.query_one(Input)
            query = query_input.value
            if query:
                self.report_content = "###  Procesando tu consulta...\n\nPor favor, espera un momento."
                self.is_loading = True
                query_input.disabled = True
                event.button.disabled = True
                
                # Ejecutar la lógica del backend en un worker para no bloquear la TUI
                self.run_worker(self.fetch_weather_report(query), exclusive=True)
            else:
                self.report_content = "### Por favor, ingresa una consulta."

    async def fetch_weather_report(self, query: str) -> None:
        """Trabajador asíncrono para obtener el informe del clima."""
        try:
            # Cargar variables de entorno si es necesario para las herramientas
            load_dotenv() 
            # Llamar a la función del backend
            # asyncio.run() no es necesario aquí ya que Textual maneja el bucle de eventos
            content = await run_agent_and_save_md(query)
            self.report_content = content
        except Exception as e:
            self.report_content = f"### Ocurrió un error:\n\n```\n{e}\n```"
        finally:
            self.is_loading = False
            query_input = self.query_one(Input)
            submit_button = self.query_one("#submit_button", Button)
            query_input.disabled = False
            submit_button.disabled = False
            query_input.focus()

    def watch_report_content(self, new_content: str) -> None:
        """Actualiza el widget Markdown cuando report_content cambia."""
        # Consultar el widget Markdown por su ID para asegurar que lo encontramos
        try:
            markdown_widget = self.query_one("#report_markdown", Markdown)
            markdown_widget.update(new_content)
        except Exception as e:
            # En caso de que el widget aún no esté listo, aunque es menos probable con este cambio
            print(f"Error al actualizar Markdown: {e}")
    
    def watch_is_loading(self, loading: bool) -> None:
        """Actualiza el estado de los botones mientras se carga."""
        # Podríamos añadir un widget de carga aquí si quisiéramos
        pass

if __name__ == "__main__":
    app = WeatherTUI()
    app.run()
