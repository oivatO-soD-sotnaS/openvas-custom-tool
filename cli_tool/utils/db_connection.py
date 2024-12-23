import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from rich import print
from rich.panel import Panel

# Carregar variáveis de ambiente
from pathlib import Path
load_dotenv()

Base = declarative_base()  # Base for all models

class DBConnection:
    @staticmethod
    def get_engine():
        """
        Retorna uma instância do engine do SQLAlchemy.
        """
        
        DB_URL = os.getenv('DB_URL')
        DB_ENGINE = os.getenv('DB_ENGINE')
        DB_DATABASE = os.getenv('DB_DATABASE')
        DB_USER = os.getenv('DB_USER')
        DB_PASS = os.getenv('DB_PASS')

        if not all([DB_URL, DB_ENGINE, DB_DATABASE, DB_USER, DB_PASS]):
            raise ValueError("Variáveis de ambiente para a conexão com o banco estão incompletas.")

        if DB_ENGINE == 'postgres':
            return create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_URL}/{DB_DATABASE}')
        elif DB_ENGINE == 'mysql':
            return create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_URL}/{DB_DATABASE}')
        else:
            raise ValueError("DB_ENGINE inválido. Use 'postgres' ou 'mysql'.")

    @staticmethod
    def get_session(engine):
        """
        Retorna uma nova sessão para interagir com o banco de dados.
        """
        Session = sessionmaker(bind=engine)
        return Session()

    @staticmethod
    def create_tables(engine):
        """
        Cria todas as tabelas definidas nos modelos.
        """
        Base.metadata.create_all(bind=engine)

    @staticmethod
    def test_connection(session):
        """
        Testa a conexão com o banco de dados.

        :return: True se a conexão for bem-sucedida, False caso contrário.
        """
        try:
            result = session.execute(text("SELECT 1")).scalar()
            return True
        except OperationalError as e:
            print(Panel(f"[red]Erro ao conectar ao banco de dados:[/red] [cyan bold]{e}", title="WARNING!", border_style="bold red", title_align="left", width=140))
            return False

if __name__ == "__main__":
    DBConnection.test_connection()
