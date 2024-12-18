import os, sys, typer, subprocess
from typing_extensions import Annotated
from typing import Optional
from rich import print
from rich.prompt import Prompt
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv

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
        print("[cyan]Configuring GMP...[/cyan]")
        if config_gmp():
            print("[cyan bold]GMP variables updated successfully!")

    if database:
        print("[cyan]Configuring database...[/cyan]")
        if config_database():
            print("[cyan bold]Database variables updated successfully!")

    if not gmp and not database:
        print("[cyan]Configuring both GMP and database...[/cyan]")
        if config_gmp():
            print("[cyan bold]GMP variables updated successfully!")
        if config_database():
            print("[cyan bold]Database variables updated successfully!")
    typer.Exit()

def config_gmp()-> bool:
    """
    Configures the GMP environment variables in .env with user input 
    
    :return True if the gmp variables were updated successfully, False if not
    """

    username = Prompt.ask("Enter your username", default=os.getenv("GMP_USER"))
    passwd = Prompt.ask("Enter your password", default=os.getenv("GMP_PASS"), password=True)

    socket_search_type = Prompt.ask("Enter the socket search type", choices=["manual", "auto"], default="auto")
    if socket_search_type == "auto":
        socket = find_gmp_socket_with_spinner()
        if not socket:
            print("[red bold]GMP credentials not updated")
            return False
    else:
        socket = Prompt.ask("Enter the gvmd.sock file path", default="/var/run/gvmd/gvmd.sock")
    # Update GMP user    
    update_env_file("cli_tool/.env", "GMP_USER", username)

    # Update GMP user    
    update_env_file("cli_tool/.env", "GMP_PASS", passwd)

    if not socket:
        print("[red]gvmd.sock file not found")
        return False
    
    # Update GMP socket path    
    update_env_file("cli_tool/.env", "GMP_SOCKET", socket)

    print(Panel("[red]The passwords are stored unencrypted at[/red] [cyan bold]openvas-custom-tool/cli_tool/.env", title="WARNING!", border_style="bold red", title_align="left", width=80))
    
    # GMP credentials updated correctly
    return True

def config_database() -> True:
    """
    Configures the database environment variables in .env with user input 
    
    :return True if the database variables were updated successfully, False if not
    """
    db_engine = Prompt.ask("Enter the database engine", choices=["mysql", "postgres"], default="mysql")

    db_url = Prompt.ask("Enter the database URL", default=f"localhost:{"3306" if db_engine == "mysql" else "5432"}")

    db_user = Prompt.ask("Enter your username", default=os.getenv("DB_USER"))

    db_pass = Prompt.ask("Enter your password", default=os.getenv("DB_PASS"), password=True)

    db_database = Prompt.ask("Enter the database name", default=os.getenv("DB_DATABASE"))

    # update the database engine
    update_env_file("cli_tool/.env", "DB_ENGINE", db_engine)

    # update the database URL
    update_env_file("cli_tool/.env", "DB_URL", db_url)

    # update the database user
    update_env_file("cli_tool/.env", "DB_USER", db_user)
    
    # update the database password
    update_env_file("cli_tool/.env", "DB_PASS", db_pass)

    # update the database
    update_env_file("cli_tool/.env", "DB_DATABASE", db_database)

    print(Panel("[red]The passwords are stored unencrypted at[/red] [cyan bold]openvas-custom-tool/cli_tool/.env", title="WARNING!", border_style="bold red", title_align="left", width=80))
    
    # Database credentials updated correctly
    return True
    

def update_env_file(file_path: str, key: str, value: str) -> None:
    """
    Update or add a key-value pair in a .env file.

    Args:
        file_path (str): Path to the .env file.fit
    """
    # Read the .env file if it exists
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
    else:
        lines = []
    
    key_found = False
    new_lines = []
    
    for line in lines:
        if line.strip().startswith(f"{key}="):
            # Update the value for the existing key
            new_lines.append(f"{key}={value}\n")
            key_found = True
        else:
            new_lines.append(line)
    
    # Add the key-value pair if it wasn't found
    if not key_found:
        new_lines.append(f"{key}={value}\n")
    
    # Write back to the .env file
    with open(file_path, "w") as file:
        file.writelines(new_lines)


def find_gmp_socket_with_spinner() -> str | None:
    """
    Searches for the GMP socket file with a spinner while waiting.
    """
    # Check if the script is run as root
    if os.geteuid() != 0:
        print("[red]Permission denied when searching. Try running as sudo.")
        return None
    
    console = Console()
    
    
    # Start the spinner
    with console.status("[bold cyan]Searching for gvmd.sock...", spinner="bouncingBar"):
        console.print(f"[cyan]Searching for gvmd.sock...", end=" ",)
        
        try:
            # Run the find command
            result = subprocess.run(
                ["find", "/", "-name", "gvmd.sock"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False  # Don't raise error on non-zero exit status
            )


            # Display result after search
            socket_path = result.stdout.strip()
            if socket_path:
                console.print(f"[green]GMP socket found at: {socket_path}")
            else:
                console.print("[red]GMP socket not found.")
            return socket_path
        except subprocess.SubprocessError as e:
            console.print(f"[red]Error occurred: {e}")
            return None
