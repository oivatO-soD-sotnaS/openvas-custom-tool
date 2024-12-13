import sys, os, base64
from dotenv import load_dotenv
from pathlib import Path

from gvm.errors import GvmError

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Load environment variables
load_dotenv()

# Import Connection modules
from cli_tool.utils.gmp_connection import GMPConnection
from cli_tool.utils.db_connection import DBConnection

def download_cvs():
  GMP_USER = os.getenv('GMP_USER')
  GMP_PASS = os.getenv('GMP_PASS')
  try:
    with GMPConnection.get_connection() as gmp:
      gmp.authenticate(GMP_USER, GMP_PASS)
      reports = gmp.get_reports()

      for report in reports.xpath("report"):
          report_id = report.get("id")
          response: get_reports_response = gmp.get_report(
              report_id,
              report_format_id="c1645568-627a-11e3-a660-406186ea4fc5",
              ignore_pagination=True,
              details=True
          )
          
          
          # Localize a tag <report_format> e acesse o texto logo após ela
          report_format_tag = response.find('.//report_format')
          if report_format_tag is not None:
              base64_string = report_format_tag.tail.strip() if report_format_tag.tail else None
              decoded_data = base64.b64decode(base64_string)
              
              # Salve o conteúdo decodificado em um arquivo
              output_file = f'../../data/{report_id}.cvs'
              with open(output_file, "wb") as f:
                  f.write(decoded_data)
      print("Download dos reports concluído com sucesso!")
      return True
  except GvmError as e:
    print("Erro ao testar conexão com o GMP:", e, file=sys.stderr)
    return False
        

def import_to_db():
   
   pass
def main():
  download_cvs()
  import_to_db()
  pass


if __name__ == "__main__":
  download_cvs()