import typer
from commands.config import app as config_app  # Import the config subcommand app
from commands.import_reports import app as import_reports_app  # Import the config subcommand app
# Main app
app = typer.Typer()

# Add the config subcommand to the main app
app.add_typer(config_app)
app.add_typer(import_reports_app)

if __name__ == "__main__":
    app()
