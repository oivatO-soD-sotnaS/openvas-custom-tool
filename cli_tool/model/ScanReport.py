from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Text

Base = declarative_base()


class ScanReport(Base):
    __tablename__ = 'scan_report'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_name = Column(String(255), nullable=False)
    host_ip = Column(String(15), nullable=False)
    hostname = Column(String(255), nullable=True)
    port = Column(String(10), nullable=False)
    severity = Column(Float, nullable=True)
    threat_level = Column(String(50), nullable=True)
    vulnerability_name = Column(Text, nullable=False)
    vulnerability_family = Column(String(100), nullable=True)
    cvss_base_score = Column(Float, nullable=True)
    solution = Column(Text, nullable=True)
    reference_links = Column(Text, nullable=True)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return (
            f"<ScanReport(id={self.id}, task_name='{self.task_name}', host_ip='{self.host_ip}', "
            f"hostname='{self.hostname}', port='{self.port}', severity={self.severity}, "
            f"threat_level='{self.threat_level}', vulnerability_name='{self.vulnerability_name}', "
            f"cvss_base_score={self.cvss_base_score})>"
        )

    @classmethod
    def create(cls, session: Session, **kwargs):
        """
        Cria um novo registro na tabela scan_report.

        :param session: Instância da sessão do SQLAlchemy.
        :param kwargs: Dados para preencher as colunas da tabela.
        :return: Instância de ScanReport criada ou None se falhar.
        """
        try:
            new_report = cls(**kwargs)
            session.add(new_report)
            session.commit()
            return new_report
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Erro ao criar ScanReport: {e}")
            return None

    @classmethod
    def get_by_id(cls, session: Session, report_id: int):
        """
        Obtém um registro da tabela scan_report pelo ID.

        :param session: Instância da sessão do SQLAlchemy.
        :param report_id: ID do registro.
        :return: Instância de ScanReport correspondente ou None se não encontrada.
        """
        return session.query(cls).filter_by(id=report_id).first()

    @classmethod
    def get_all(cls, session: Session):
        """
        Retorna todos os registros da tabela scan_report.

        :param session: Instância da sessão do SQLAlchemy.
        :return: Lista de instâncias de ScanReport.
        """
        return session.query(cls).all()

    @classmethod
    def update(cls, session: Session, report_id: int, **kwargs):
        """
        Atualiza um registro da tabela scan_report pelo ID.

        :param session: Instância da sessão do SQLAlchemy.
        :param report_id: ID do registro a ser atualizado.
        :param kwargs: Dados atualizados para o registro.
        :return: Instância de ScanReport atualizada ou None se falhar.
        """
        try:
            report = session.query(cls).filter_by(id=report_id).first()
            if not report:
                print("Registro não encontrado.")
                return None

            for key, value in kwargs.items():
                if hasattr(report, key):
                    setattr(report, key, value)

            session.commit()
            return report
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Erro ao atualizar ScanReport: {e}")
            return None

    @classmethod
    def delete(cls, session: Session, report_id: int):
        """
        Exclui um registro da tabela scan_report pelo ID.

        :param session: Instância da sessão do SQLAlchemy.
        :param report_id: ID do registro a ser excluído.
        :return: True se bem-sucedido, False se falhar.
        """
        try:
            report = session.query(cls).filter_by(id=report_id).first()
            if not report:
                print("Registro não encontrado.")
                return False

            session.delete(report)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Erro ao deletar ScanReport: {e}")
            return False
