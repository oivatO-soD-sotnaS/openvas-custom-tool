import os, sys, typer
from rich.console import Console
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv
from InquirerPy import inquirer

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Load environment variables
load_dotenv()

# Create a Typer app for this command
app = typer.Typer()

@app.command()
def show_vars():
  """
  Shows current set of environment variables
  """
  table = Table(title="Environment Variables")
  table.add_column("KEY", justify="left", style="cyan", no_wrap=True)
  table.add_column("VALUE", style="magenta")

  table.add_row("GMP_USER", os.getenv("GMP_USER"))
  table.add_row("GMP_PASS", os.getenv("GMP_PASS"))
  table.add_row("GMP_SOCKET", os.getenv("GMP_SOCKET"))
  table.add_row("DB_ENGINE", os.getenv("DB_ENGINE"))
  table.add_row("DB_URL", os.getenv("DB_URL"))
  table.add_row("DB_USER", os.getenv("DB_USER"))
  table.add_row("DB_PASS", os.getenv("DB_PASS"))
  table.add_row("DB_DATABASE", os.getenv("DB_DATABASE"))

  console = Console()
  console.print(table)
