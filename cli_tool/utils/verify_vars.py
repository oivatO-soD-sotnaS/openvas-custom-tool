import os, sys

from dotenv import load_dotenv
from rich import print
from rich.panel import Panel
from commands import configure

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Load environment variables
load_dotenv()


def check_env_variables() -> bool:
  required_vars = ["GMP_USER",
                  "GMP_PASS",
                  "GMP_SOCKET",
                  "DB_ENGINE",
                  "DB_URL",
                  "DB_USER",
                  "DB_PASS",
                  "DB_DATABASE"]
  missing_vars = [var for var in required_vars if not os.getenv(var)]

  if len(missing_vars) > 0:
    print(Panel(f"[red]{", ".join(missing_vars)} is missing, run[/red] [bold cyan]sudo main.py[/bold cyan][red] configure to configure all of them!", title="WARNING!", border_style="bold red", title_align="left", width=90))
    configure(True, True)
    return False
  return True
