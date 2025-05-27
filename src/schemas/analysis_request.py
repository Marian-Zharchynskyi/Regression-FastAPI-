from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class AnalysisRequestDto(BaseModel):
    id: UUID
    created_at: datetime
    csv_filename: str
    dependent_variable: str
    independent_variables: dict
    formula: str

    model_config = SettingsConfigDict(from_attributes=True)
