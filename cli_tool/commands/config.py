import os, sys, typer
from typing_extensions import Annotated
from typing import Optional
from rich import print
from rich.prompt import Prompt
from rich.prompt import Confirm
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv, set_key

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Load environment variables
load_dotenv()

# Create a Typer app for this command
app = typer.Typer()

@app.command()
def configure(
    gmp: Annotated[Optional[bool], typer.Option("--gmp", help="Configure GMP connection")] = False,
    database: Annotated[Optional[bool], typer.Option("--database", help="Configure database connection")] = False,
) -> None:
    """
    Configure environment variables. --gmp to configure GMP, --database to configure database.
    
    Args:
        gmp: Whether to configure GMP connection (default is False).
        database: Whether to configure database connection (default is False).
    """
    if gmp:
        print("[green]Configuring GMP...[/green]")
        config_gmp()

    if database:
        print("[green]Configuring database...[/green]")
        config_database()

    if not gmp and not database:
        print("[green]Configuring both GMP and database...[/green]")
        config_gmp()
        config_database()

def config_gmp():
    username = Prompt.ask("Enter your username", default="admin")
    passwd = Prompt.ask("Enter your password", default="admin")

    table = Table(title="GMP openvas", caption="credentials")

    table.add_column("username", justify="right", style="cyan", no_wrap=True)
    table.add_column("passord", style="magenta")

    table.add_row(username, passwd)

    console = Console()
    console.print(table)
    
    print("GMP configured!")

def config_database():
    print("Database configured!")


print(os.getenv('GMP_USER'))

