from datetime import datetime

import uuid
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Uuid, JSON, String, DateTime
from models.base import Base


class AnalysisRequest(Base):
    __tablename__ = "analysis_requests"

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True, native_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    csv_filename: Mapped[str] = mapped_column(String(200), nullable=False)  # Змінено з csv_name
    dependent_variable: Mapped[str] = mapped_column(String(300), nullable=False)
    independent_variables: Mapped[list] = mapped_column(JSON, nullable=False)
    formula: Mapped[str] = mapped_column(String(1000), nullable=False)
