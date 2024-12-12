class DBConnection:
    """
    Classe para gerenciar conexões com o banco de dados.
    """

    @staticmethod
    def get_session():
        """
        Retorna uma nova sessão para interagir com o banco de dados.

        :return: Instância de sessão do SQLAlchemy.
        """
