from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from utils.db_connection import Base

class Report(Base):
    __tablename__ = 'report'

    report_id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    creation_time = Column(DateTime, nullable=False)
    modification_time = Column(DateTime, nullable=False)
    owner_name = Column(String(50), nullable=False)
    scan_start = Column(DateTime, nullable=False)
    scan_end = Column(DateTime, nullable=False)
    scan_status = Column(String(20), nullable=False)
    severity = Column(Float(4, 1), nullable=False)
    result_count = Column(Integer, nullable=False)

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
            return None

