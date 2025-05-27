from uuid import UUID
import uuid
from sqlalchemy import Column, String, DateTime, func, Uuid, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from models.base import Base


class AnalysisRequest(Base):
    __tablename__ = "analysis_requests"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    csv_filename = Column(String, nullable=False)
    dependent_variable = Column(String, nullable=False)
    independent_variables = Column(JSON, nullable=False)  
    formula = Column(String, nullable=False)
    results = relationship("RegressionResult", back_populates="request", uselist=False)
