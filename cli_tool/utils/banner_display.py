import random, sys
from rich.console import Console
from rich.style import Style
from pathlib import Path

# Adiciona o diretório raiz ao caminho do Python
sys.path.append(str(Path(__file__).resolve().parent.parent))

from assets.banners import banners  # Importa os banners
def display_banner():
    colors = [
        "cyan",
        "magenta",
        "green",
        "blue",
        "yellow",
        "red",
        "white",
        "bright_blue",
        "bright_green",
    ]

    # Selecionar um banner e uma cor aleatória
    selected_banner = random.choice(banners)
    selected_color = random.choice(colors)

    # Configurar estilo
    base_style = Style.parse(selected_color)

    # Instanciar console e imprimir o banner
    console = Console()
    console.print(selected_banner, style=base_style)

