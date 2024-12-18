import typer
from commands.config import app as config_app  # Import the config subcommand app
from commands.fetch import app as import_reports_app  # Import the config subcommand app
from utils.banner_display import display_banner # Import the display banner 
from utils.verify_vars import check_env_variables # Import 


# Main app
app = typer.Typer()

# Add the config subcommand to the main app
app.add_typer(config_app)
app.add_typer(import_reports_app)

if __name__ == "__main__":
    display_banner()
    check_env_variables()
    app()
