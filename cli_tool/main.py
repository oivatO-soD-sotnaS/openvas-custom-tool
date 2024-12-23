import typer
from commands.config import app as config_app  # Import the config subcommand app
from commands.fetch import app as import_reports_app  # Import the fetch subcommand app
from commands.show_vars import app as show_vars_app  # Import the show-vars subcommand app
from utils.banner_display import banner # Import the display banner 
from utils.verify_vars import check_env_variables # Import 
from utils.db_connection import DBConnection


# Main app
app = typer.Typer()

# Add the config subcommand to the main app
app.add_typer(config_app)
app.add_typer(import_reports_app)
app.add_typer(show_vars_app)

if __name__ == "__main__":
    # Displat random banner
    banner()
    
    # check environment variables under .env
    if check_env_variables():
        
        # makes sure all tables are initialized correctly 
        engine = DBConnection.get_engine()
        DBConnection.create_tables(engine=engine)
        
        # starts app
        app()
