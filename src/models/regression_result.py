import uuid
from uuid import UUID
from sqlalchemy import Uuid, JSON, ForeignKey, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class RegressionResult(Base):
    __tablename__ = "regression_results"

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    request_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("analysis_requests.id"))
    coefficients_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    std_errors_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    t_statistics_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    p_values_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    r_squared: Mapped[float] = mapped_column(Float, nullable=False)
    adj_r_squared: Mapped[float] = mapped_column(Float, nullable=False)
    f_statistic: Mapped[float] = mapped_column(Float, nullable=False)
    f_p_value: Mapped[float] = mapped_column(Float, nullable=False)
    n_observations: Mapped[int] = mapped_column(Integer, nullable=False)
    confidence_intervals: Mapped[dict] = mapped_column(JSON, nullable=False)
    formula: Mapped[str] = mapped_column(String(1000), nullable=False)
    request = relationship("AnalysisRequest", back_populates="results")
