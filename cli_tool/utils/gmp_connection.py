import sys
import os

from gvm.connections import UnixSocketConnection
from gvm.errors import GvmError
from gvm.protocols.gmp import Gmp, GMP
from gvm.transforms import EtreeCheckCommandTransform
from lxml.etree import _Element

# Carregar variáveis de ambiente
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()


class GMPConnection:
    """
    Classe para gerenciar a conexão com o Greenbone Management Protocol (GMP).
    """

    @staticmethod
    def get_connection() -> GMP[_Element]:
        """
        Retorna uma conexão autenticada com o GMP.

        :return: Instância autenticada de Gmp.
        :raises GvmError: Caso ocorra um erro na conexão ou autenticação.
        """

        GMP_SOCKET = os.getenv('GMP_SOCKET')

        connection = UnixSocketConnection(path=GMP_SOCKET)
        transform = EtreeCheckCommandTransform()

        try:
            gmp = Gmp(connection=connection, transform=transform)
            return gmp

        except GvmError as e:
            print('An error occurred during connection or authentication:', e, file=sys.stderr)
            raise

    @staticmethod
    def test_connection() -> bool:
        """
        Testa a conexão com o GMP.

        :return: True se a conexão for bem-sucedida, False caso contrário.
        """

        GMP_USER = os.getenv('GMP_USER')
        GMP_PASS = os.getenv('GMP_PASS')

        try:
            with GMPConnection.get_connection() as gmp:
                gmp.authenticate(GMP_USER, GMP_PASS)
                print("Conexão com o GMP bem-sucedida!")
                return True
        except GvmError as e:
            print("Erro ao testar conexão com o GMP:", e, file=sys.stderr)
            return False

if __name__ == "__main__":
    GMPConnection.test_connection()
