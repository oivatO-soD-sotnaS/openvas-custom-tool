import os, sys, typer, subprocess
from typing_extensions import Annotated
from typing import Optional
from rich import print
from rich.prompt import Prompt
from rich.console import Console
from rich.panel import Panel
from rich.padding import Padding
from dotenv import load_dotenv
from InquirerPy import inquirer

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
    Configure environment variables for GMP and database connections.

    This function updates the necessary environment variables based on user input.
    If neither --gmp nor --database is specified, both configurations will be prompted.

    Args:
        gmp (bool): Flag to configure GMP connection.
        database (bool): Flag to configure database connection.
    """
    if gmp:
        if config_gmp():
            print("[cyan bold]GMP variables updated successfully!")

    if database:
        if config_database():
            print("[cyan bold]Database variables updated successfully!")

    if not gmp and not database:
        if config_gmp():
            print("[cyan bold]GMP variables updated successfully!")
        
        if config_database():
            print("[cyan bold]Database variables updated successfully!")
    
    print(Panel("[red]The passwords are stored unencrypted at[/red] [cyan bold]openvas-custom-tool/cli_tool/.env", title="WARNING!", border_style="bold red", title_align="left", width=80))
    typer.Exit()

def config_gmp() -> bool:
    """
    Configure GMP environment variables in the .env file based on user input.

    Prompts the user for GMP credentials and socket path, and updates the .env file accordingly.

    Returns:
        bool: True if GMP variables were updated successfully, False otherwise.
    """
    print(Padding("[bold]Configuring GMP...[/bold]", (1, 1), style="on blue", expand=False))

    username = Prompt.ask("Enter your username", default=os.getenv("GMP_USER"))
    passwd = Prompt.ask("Enter your password", default=os.getenv("GMP_PASS"), password=True)

    socket_search_type = inquirer.select(
        message="Select a socket search type (up/down to select and enter to confirm):",
        choices=["Manual", "Automatic"],
        pointer=">",
        default="Automatic",
    ).execute()    
    if socket_search_type == "Automatic":
        socket = find_gmp_socket_with_spinner()
        if not socket:
            print("[red bold]GMP credentials not updated")
            return False
    else:
        socket = Prompt.ask("Enter the gvmd.sock file path", default="/var/run/gvmd/gvmd.sock")

    update_env_file("cli_tool/.env", "GMP_USER", username)
    update_env_file("cli_tool/.env", "GMP_PASS", passwd)

    if not socket:
        print("[red]gvmd.sock file not found")
        return False
    
    update_env_file("cli_tool/.env", "GMP_SOCKET", socket)
    return True

def config_database() -> bool:
    """
    Configure database environment variables in the .env file based on user input.

    Prompts the user for database details such as engine, URL, username, password, and database name.
    Updates the .env file with the provided values.

    Returns:
        bool: True if database variables were updated successfully, False otherwise.
    """
    print(Padding("[bold]Configuring database...[/bold]", (1, 1), style="on blue", expand=False))

    db_engine = inquirer.select(
        message="Select your database engine (up/down to select and enter to confirm):",
        choices=["mysql", "postgres"],
        pointer=">",  # Pointer for selection
        default="MySQL",  # Default selection
    ).execute()

    db_url = Prompt.ask("Enter the database URL", default=f"localhost:{"3306" if db_engine == "mysql" else "5432"}")
    db_user = Prompt.ask("Enter your username", default=os.getenv("DB_USER"))
    db_pass = Prompt.ask("Enter your password", default=os.getenv("DB_PASS"), password=True)
    db_database = Prompt.ask("Enter the database name", default=os.getenv("DB_DATABASE"))

    update_env_file("cli_tool/.env", "DB_ENGINE", db_engine)
    update_env_file("cli_tool/.env", "DB_URL", db_url)
    update_env_file("cli_tool/.env", "DB_USER", db_user)
    update_env_file("cli_tool/.env", "DB_PASS", db_pass)
    update_env_file("cli_tool/.env", "DB_DATABASE", db_database)
    
    return True

def update_env_file(file_path: str, key: str, value: str) -> None:
    """
    Update or add a key-value pair in the .env file.

    Reads the existing .env file (if any), updates the specified key with the given value, or adds it if not present.
    Writes the updated content back to the file.

    Args:
        file_path (str): Path to the .env file.
        key (str): Key to search and update.
        value (str): Value to assign to the key.
    """
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
    else:
        lines = []

    key_found = False
    new_lines = []

    for line in lines:
        if line.strip().startswith(f"{key}="):
            new_lines.append(f"{key}={value}\n")
            key_found = True
        else:
            new_lines.append(line)

    if not key_found:
        new_lines.append(f"{key}={value}\n")

    with open(file_path, "w") as file:
        file.writelines(new_lines)

def find_gmp_socket_with_spinner() -> Optional[str]:
    """
    Search for the GMP socket file using a spinner.

    This function attempts to locate the `gvmd.sock` file on the system, prompting the user to run the script with sudo if necessary.

    Returns:
        Optional[str]: Path to the `gvmd.sock` file if found, None otherwise.
    """
    if os.geteuid() != 0:
        print("[red]Permission denied when searching. Try running as sudo.")
        return None

    console = Console()

    with console.status("[bold cyan]Searching for gvmd.sock...", spinner="bouncingBar"):
        try:
            result = subprocess.run(
                ["find", "/", "-name", "gvmd.sock"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False 
            )

            socket_path = result.stdout.strip()
            if socket_path:
                console.print(f"[green]GMP socket found at: {socket_path}")
            else:
                console.print("[red]GMP socket not found.")
            return socket_path
        except subprocess.SubprocessError as e:
            console.print(f"[red]Error occurred: {e}")
            return None
