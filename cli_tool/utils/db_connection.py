import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# Carregar variáveis de ambiente
from pathlib import Path
load_dotenv()

class DBConnection:
    """
    Classe para gerenciar conexões com o banco de dados.
    """

    @staticmethod
    def get_session() -> sessionmaker:
        """
        Retorna uma nova sessão para interagir com o banco de dados.

        :return: Instância de sessão do SQLAlchemy.
        :raises ValueError: Se as variáveis de ambiente estiverem faltando.
        """
        DB_URL = os.getenv('DB_URL')
        DB_ENGINE = os.getenv('DB_ENGINE')
        DB_DATABASE = os.getenv('DB_DATABASE')
        DB_USER = os.getenv('DB_USER')
        DB_PASS = os.getenv('DB_PASS')

        if not all([DB_URL, DB_ENGINE, DB_DATABASE, DB_USER, DB_PASS]):
            raise ValueError("Variáveis de ambiente para a conexão com o banco estão incompletas.")

        if DB_ENGINE == 'postgres':
            engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_URL}/{DB_DATABASE}')
        elif DB_ENGINE == 'mysql':
            engine = create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_URL}/{DB_DATABASE}')
        else:
            raise ValueError("DB_ENGINE inválido. Use 'postgres' ou 'mysql'.")

        Session = sessionmaker(bind=engine)
        return Session

    @staticmethod
    def test_connection():
        """
        Testa a conexão com o banco de dados.

        :return: True se a conexão for bem-sucedida, False caso contrário.
        """
        try:
            Session = DBConnection.get_session()
            with Session().bind.connect() as connection:
                result = connection.execute(text("SELECT 1")).scalar()
                print("Conexão bem-sucedida!" if result == 1 else "Falha ao executar consulta.")
                return True
        except OperationalError as e:
            print("Erro ao conectar ao banco de dados:", e)
            return False

# Testando a conexão
if __name__ == "__main__":
    DBConnection.test_connection()