from sqlalchemy import Column, String, Integer, Float, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

class Vulnerability(Base):
    __tablename__ = 'vulnerabilities'

    vuln_id = Column(String(50), primary_key=True)
    name = Column(String(255), nullable=True)
    type = Column(String(50), nullable=True)
    cvss_base = Column(Float(3, 1), nullable=True)
    severity = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    scan_nvt_version = Column(DateTime, nullable=True)

    def __repr__(self):
        return (
            f"<Vulnerability(vuln_id={self.vuln_id}, name='{self.name}', "
            f"severity={self.severity}, cvss_base={self.cvss_base})>"
        )

    @classmethod
    def create(cls, session: Session, **kwargs):
        try:
            new_vulnerability = cls(**kwargs)
            session.add(new_vulnerability)
            session.commit()
            return new_vulnerability
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Erro ao criar Vulnerability: {e}")
            return None

    @classmethod
    def get_by_id(cls, session: Session, vuln_id: str):
        return session.query(cls).filter_by(vuln_id=vuln_id).first()

    @classmethod
    def get_all(cls, session: Session):
        return session.query(cls).all()

    @classmethod
    def update(cls, session: Session, vuln_id: str, **kwargs):
        try:
            vuln = session.query(cls).filter_by(vuln_id=vuln_id).first()
            if not vuln:
                print("Registro não encontrado.")
                return None

            for key, value in kwargs.items():
                if hasattr(vuln, key):
                    setattr(vuln, key, value)

            session.commit()
            return vuln
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Erro ao atualizar Vulnerability: {e}")
            return None

    @classmethod
    def delete(cls, session: Session, vuln_id: str):
        try:
            vuln = session.query(cls).filter_by(vuln_id=vuln_id).first()
            if not vuln:
                print("Registro não encontrado.")
                return False

            session.delete(vuln)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Erro ao deletar Vulnerability: {e}")
            return False
