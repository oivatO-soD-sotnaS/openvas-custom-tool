import sys

from gvm.connections import UnixSocketConnection
from gvm.errors import GvmError
from gvm.protocols.gmp import Gmp, GMP
from gvm.transforms import EtreeCheckCommandTransform
from lxml.etree import _Element


class GMPConnection:
    """
    Classe para gerenciar a conexão com o Greenbone Management Protocol (GMP).
    """

    @staticmethod
    def get_connection(path: str, username: str, password: str) -> GMP[_Element]:
        """
        Retorna uma conexão autenticada com o GMP.

        :param path: Caminho para o socket Unix.
        :param username: Nome de usuário para autenticação.
        :param password: Senha para autenticação.
        :return: Instância autenticada de Gmp.
        :raises GvmError: Caso ocorra um erro na conexão ou autenticação.
        """
        connection = UnixSocketConnection(path=path)
        transform = EtreeCheckCommandTransform()

        try:
            gmp = Gmp(connection=connection, transform=transform)
            gmp.authenticate(username, password)
            return gmp

        except GvmError as e:
            print('An error occurred during connection or authentication:', e, file=sys.stderr)
            raise

# Exemplo de uso
if __name__ == "__main__":
    path = '/var/lib/docker/volumes/greenbone-community-edition_gvmd_socket_vol/_data/gvmd.sock'
    username = 'admin'
    password = 'admin'

    try:
        with GMPConnection.get_connection(path, username, password) as gmp:
            reports = gmp.get_reports()

            for report in reports.xpath('report'):
                print(report.get('id'))

    except GvmError as e:
        print('An error occurred:', e, file=sys.stderr)
