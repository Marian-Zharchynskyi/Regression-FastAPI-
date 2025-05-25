from typing import Dict

from pydantic import BaseModel


class ModelSummaryDto(BaseModel):
    coefficients: Dict
    std_errors: Dict
    t_statistics: Dict
    p_values: Dict
    confidence_intervals: Dict


class ModelQualityDto(BaseModel):
    r_squared: float
    adj_r_squared: float
    f_statistic: float
    f_p_value: float
    n_observations: int


class RegressionResultDto(BaseModel):
    analysis_id: str  # Changed from UUID to match desired format
    model_summary: ModelSummaryDto
    model_quality: ModelQualityDto
    formula: str

    @classmethod
    def from_db_model(cls, db_model):
        return cls(
            analysis_id=str(db_model.request_id),
            model_summary=ModelSummaryDto(
                coefficients=db_model.coefficients_json,
                std_errors=db_model.std_errors_json,
                t_statistics=db_model.t_statistics_json,
                p_values=db_model.p_values_json,
                confidence_intervals=db_model.confidence_intervals,
            ),
            model_quality=ModelQualityDto(
                r_squared=db_model.r_squared,
                adj_r_squared=db_model.adj_r_squared,
                f_statistic=db_model.f_statistic,
                f_p_value=db_model.f_p_value,
                n_observations=db_model.n_observations,
            ),
            formula=db_model.formula,
        )

    class Config:
        from_attributes = True
