import sys
import os
import base64
from dotenv import load_dotenv
from pathlib import Path
from gvm.errors import GvmError
import typer
from typing import Optional

# Constants for paths
DATA_DIR = Path(__file__).resolve().parent.parent.parent / 'data'

# Ensure the data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Create a Typer app for the config command
app = typer.Typer()

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Load environment variables
load_dotenv()

# Import Connection modules
from cli_tool.utils.gmp_connection import GMPConnection
from cli_tool.utils.db_connection import DBConnection


def download_cvs() -> Optional[list]:
  """
  Download reports as CVS and return the list of reports.

  :return: list of reports if successful, None if connection fails.
  """
  GMP_USER = os.getenv('GMP_USER')
  GMP_PASS = os.getenv('GMP_PASS')
  if not GMP_USER or not GMP_PASS:
      print("GMP credentials are missing from environment variables.", file=sys.stderr)
      return None

  try:
    # Attempt GMP connection
    with GMPConnection.get_connection() as gmp:
      gmp.authenticate(GMP_USER, GMP_PASS)
      reports = gmp.get_reports()

      for report in reports.xpath("report"):
        report_id = report.get("id")
        # Fetch the report with the required format
        response = gmp.get_report(
          report_id,
          report_format_id="c1645568-627a-11e3-a660-406186ea4fc5",
          ignore_pagination=True,
          details=True
        )
        print(DATA_DIR)
        # Find report format and decode the base64 data
        report_format_tag = response.find('.//report_format')
        if report_format_tag is not None:
          base64_string = report_format_tag.tail.strip() if report_format_tag.tail else None
          decoded_data = base64.b64decode(base64_string)
          
          # Salve o conteúdo decodificado em um arquivo
          output_file = f'{DATA_DIR}/{report_id}.cvs'
          with open(output_file, "wb") as f:
            f.write(decoded_data)
    print("Download of reports completed successfully!")
    return reports  # Return reports list
  except GvmError as e:
      print(f"Error connecting to GMP: {e}", file=sys.stderr)
      return None


@app.command()
def import_to_db():
    """
    Import all reports into the configured database.
    """
    # Download CSV files, return if the download fails
    reports = download_cvs()
    if not reports:
        print("Failed to download reports, aborting database import.", file=sys.stderr)
        return

    # Proceed with database import (implement database import logic here)
    print(f"Successfully downloaded {len(reports)} reports. Proceeding to import them to the database.")
    # Add your database import logic here (e.g., DBConnection.import_reports(reports))
