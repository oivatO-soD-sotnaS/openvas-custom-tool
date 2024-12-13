from utils.db_connection import DBConnection
from models.scan_report import ScanReport, Base

def criar_tabelas():
    """
    Cria as tabelas no banco de dados, caso não existam.
    """
    Session = DBConnection.get_session()
    engine = Session().bind  # Recupera o engine configurado
    print("Verificando e criando tabelas, se necessário...")
    Base.metadata.create_all(engine)
    print("Tabelas verificadas/criadas com sucesso!")

def main():
    # Criar tabelas no banco
    criar_tabelas()

    # Testar a conexão
    if not DBConnection.test_connection():
        print("Falha na conexão com o banco. Verifique as configurações.")
        return

    # Obter uma sessão
    Session = DBConnection.get_session()
    session = Session()

    # Criar um novo registro na tabela scan_report
    novo_registro = {
        "task_name": "Scan de Rede",
        "host_ip": "192.168.0.1",
        "hostname": "servidor_local",
        "port": "22",
        "severity": 7.5,
        "threat_level": "Alto",
        "vulnerability_name": "Falha SSH",
        "vulnerability_family": "Autenticação",
        "cvss_base_score": 7.5,
        "solution": "Atualizar para versão mais recente.",
        "reference_links": "https://exemplo.com/solucao",
        "description": "Uma vulnerabilidade no serviço SSH foi detectada."
    }

    try:
        # Criar um novo ScanReport
        report = ScanReport.create(session, **novo_registro)
        if report:
            print(f"Registro criado com sucesso: {report}")

        # Buscar todos os registros
        todos_registros = ScanReport.get_all(session)
        print("Registros no banco de dados:")
        for registro in todos_registros:
            print(registro)

    except Exception as e:
        print(f"Erro durante a execução: {e}")
    finally:
        # Fechar a sessão
        session.close()

if __name__ == "__main__":
    main()
