from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

class Report(Base):
    __tablename__ = 'reports'

    report_id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=True)
    creation_time = Column(DateTime, nullable=True)
    modification_time = Column(DateTime, nullable=True)
    owner_name = Column(String(50), nullable=True)
    scan_start = Column(DateTime, nullable=True)
    scan_end = Column(DateTime, nullable=True)
    scan_status = Column(String(20), nullable=True)
    severity = Column(Float(4, 1), nullable=True)
    result_count = Column(Integer, nullable=True)

    def __repr__(self):
        return (
            f"<Report(report_id={self.report_id}, name='{self.name}', "
            f"owner_name='{self.owner_name}', severity={self.severity})>"
        )

    @classmethod
    def create(cls, session: Session, **kwargs):
        try:
            new_report = cls(**kwargs)
            session.add(new_report)
            session.commit()
            return new_report
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Erro ao criar Report: {e}")
            return None

    @classmethod
    def get_by_id(cls, session: Session, report_id: str):
        return session.query(cls).filter_by(report_id=report_id).first()

    @classmethod
    def get_all(cls, session: Session):
        return session.query(cls).all()

    @classmethod
    def update(cls, session: Session, report_id: str, **kwargs):
        try:
            report = session.query(cls).filter_by(report_id=report_id).first()
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
            print(f"Erro ao atualizar Report: {e}")
            return None

    @classmethod
    def delete(cls, session: Session, report_id: str):
        try:
            report = session.query(cls).filter_by(report_id=report_id).first()
            if not report:
                print("Registro não encontrado.")
                return False

            session.delete(report)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Erro ao deletar Report: {e}")
            return False
