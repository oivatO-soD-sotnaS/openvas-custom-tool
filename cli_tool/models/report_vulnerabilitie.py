from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

class ReportVulnerability(Base):
    __tablename__ = 'report_vulnerabilities'

    report_id = Column(String(36), primary_key=True)
    vuln_id = Column(String(50), primary_key=True)
    host = Column(String(100), nullable=True)
    port = Column(String(50), nullable=True)

    def __repr__(self):
        return (
            f"<ReportVulnerability(report_id={self.report_id}, vuln_id={self.vuln_id}, "
            f"host='{self.host}', port='{self.port}')>"
        )

    @classmethod
    def create(cls, session: Session, **kwargs):
        try:
            new_report_vuln = cls(**kwargs)
            session.add(new_report_vuln)
            session.commit()
            return new_report_vuln
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Erro ao criar ReportVulnerability: {e}")
            return None

    @classmethod
    def get_by_ids(cls, session: Session, report_id: str, vuln_id: str):
        return session.query(cls).filter_by(report_id=report_id, vuln_id=vuln_id).first()

    @classmethod
    def get_all(cls, session: Session):
        return session.query(cls).all()

    @classmethod
    def update(cls, session: Session, report_id: str, vuln_id: str, **kwargs):
        try:
            report_vuln = session.query(cls).filter_by(report_id=report_id, vuln_id=vuln_id).first()
            if not report_vuln:
                print("Registro não encontrado.")
                return None

            for key, value in kwargs.items():
                if hasattr(report_vuln, key):
                    setattr(report_vuln, key, value)

            session.commit()
            return report_vuln
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Erro ao atualizar ReportVulnerability: {e}")
            return None

    @classmethod
    def delete(cls, session: Session, report_id: str, vuln_id: str):
        try:
            report_vuln = session.query(cls).filter_by(report_id=report_id, vuln_id=vuln_id).first()
            if not report_vuln:
                print("Registro não encontrado.")
                return False

            session.delete(report_vuln)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Erro ao deletar ReportVulnerability: {e}")
            return False
