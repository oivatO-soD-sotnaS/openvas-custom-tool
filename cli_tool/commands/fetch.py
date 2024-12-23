import sys
import os
import base64
import typer
import csv
from typing import Optional, List, Dict
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from rich import print
from rich.padding import Padding
from rich.panel import Panel
from gvm.errors import GvmError
from cli_tool.utils.gmp_connection import GMPConnection
from cli_tool.utils.db_connection import DBConnection
from models import Report, Vulnerability, ReportVulnerability

# Constants
DATA_DIR = Path(__file__).resolve().parent.parent.parent / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Load environment variables
load_dotenv()

# Typer CLI app
app = typer.Typer()

# Ensure parent directories are in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

@app.command()
def fetch() -> None:
    """
    Fetch OpenVAS reports into the local database.
    """
    engine = DBConnection.get_engine()
    session = DBConnection.get_session(engine=engine)

    if not DBConnection.test_connection(session=session):
        typer.Exit()

    fetch_reports(session)

    session.close()
    typer.Exit()

def download_reports_from_gmp() -> Optional[List[Dict]]:
    """
    Download reports from GMP in CSV format.

    Returns:
        List of report metadata if successful, None otherwise.
    """
    gmp_user = os.getenv('GMP_USER')
    gmp_pass = os.getenv('GMP_PASS')

    try:
        with GMPConnection.get_connection() as gmp:
            gmp.authenticate(gmp_user, gmp_pass)
            reports = []

            for report in gmp.get_reports().xpath("report"):
                report_id = report.get("id")
                reports.append(report)
                response = gmp.get_report(
                    report_id,
                    report_format_id="c1645568-627a-11e3-a660-406186ea4fc5",
                    ignore_pagination=True,
                    details=True
                )

                save_report_as_csv(report_id, response)

            return reports
    except GvmError as e:
        print(f"[red]Error connecting to GMP: {e}", file=sys.stderr)
        return None

def save_report_as_csv(report_id: str, response) -> None:
    """
    Save a report as a CSV file.

    Args:
        report_id: The ID of the report.
        response: The report data in XML format.
    """
    report_format_tag = response.find('.//report_format')
    if report_format_tag is not None:
        base64_string = report_format_tag.tail.strip() if report_format_tag.tail else None
        if base64_string:
            decoded_data = base64.b64decode(base64_string)
            output_file = DATA_DIR / f"{report_id}.csv"
            with open(output_file, "wb") as f:
                f.write(decoded_data)

def parse_report_metadata(report) -> Dict:
    """
    Extract metadata from a report.

    Args:
        report: Report XML element.

    Returns:
        A dictionary containing report metadata.
    """
    return {
        "report_id": report.get('id'),
        "name": report.find('.//task/name').text,
        "creation_time": datetime.fromisoformat(report.find('.//creation_time').text.replace("Z", "+00:00")),
        "modification_time": datetime.fromisoformat(report.find('.//modification_time').text.replace("Z", "+00:00")),
        "owner_name": report.find('.//owner/name').text,
        "scan_start": datetime.fromisoformat(report.find('.//scan_start').text.replace("Z", "+00:00")),
        "scan_end": datetime.fromisoformat(report.find('.//scan_end').text.replace("Z", "+00:00")),
        "scan_status": report.find('.//scan_run_status').text,
        "severity": float(report.find('.//severity/filtered').text),
        "result_count": int(report.find('.//result_count/filtered').text)
    }

def process_csv_file(report_id: str, session) -> None:
    """
    Process a CSV file and insert its data into the database.

    Args:
        report_id: The ID of the report.
        session: Database session.
    """
    csv_file = DATA_DIR / f"{report_id}.csv"
    with open(csv_file) as file:
        reader = csv.reader(file)
        next(reader)  # Skip header

        for row in reader:
            vulnerability_data = parse_vulnerability_data(row)
            Vulnerability.create(session, **vulnerability_data)

            vulnerability_id = Vulnerability.get_by_name(session, name=vulnerability_data["name"]).vulnerability_id

            report_vulnerability_data = parse_report_vulnerability_data(report_id, row, vulnerability_id)
            ReportVulnerability.create(session, **report_vulnerability_data)

def parse_vulnerability_data(row: List[str]) -> Dict:
    """
    Parse vulnerability data from a CSV row.

    Args:
        row: CSV row containing vulnerability data.

    Returns:
        A dictionary containing vulnerability data.
    """
    return {
      "nvt_oid": row[11].strip(), #csv
      "name": row[8].strip(), # csv
      "cvss_base": float(row[4]), # csv
      "severity": row[5].strip(), # csv
      "solution_type": row[7].strip(), # csv
      "summary": row[9].strip(), # csv
      "CVEs": row[12].strip(), # csv
      "solution": row[18].strip(), # csv
      "affected_software_os": row[19].strip(), # csv
      "vulnerability_insight": row[20].strip(), # csv
    }

def parse_report_vulnerability_data(report_id: str, row: List[str], vulnerability_id: int) -> Dict:
    """
    Parse report-vulnerability mapping data from a CSV row.

    Args:
        report_id: The ID of the report.
        row: CSV row containing mapping data.
        vulnerability_id: The ID of the vulnerability.

    Returns:
        A dictionary containing report-vulnerability mapping data.
    """
    return {
        "report_id": report_id,
        "vulnerability_id": vulnerability_id,
        "ip": row[0].strip(),
        "hostname": row[1].strip(),
        "port": row[2].strip(),
        "protocol": row[3].strip(),
        "QoD": row[6].strip(),
        "specific_result": row[10].strip(),
        "detection_method": row[21].strip(),
    }

def fetch_reports(session) -> bool:
    """
    Fetch and process reports into the database.

    Args:
        session: Database session.

    Returns:
        True if successful, False otherwise.
    """
    print(Padding("[bold]Fetching reports...[/bold]", (1, 1), style="on cyan", expand=False))

    reports = download_reports_from_gmp()
    if reports is None:
        print("[red]Failed to download reports. Aborting.", file=sys.stderr)
        return False

    print(f"[bold]Downloaded {len(reports)} reports. Processing...")

    for report in reports:
        report_metadata = parse_report_metadata(report)
        Report.create(session, **report_metadata)
        process_csv_file(report_metadata["report_id"], session)

    print(Panel("[bold yellow]Reports and vulnerabilities updated!", title="SUCCESS", border_style="bold green", width=140))
    return True
