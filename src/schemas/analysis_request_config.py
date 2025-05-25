from typing import Any

from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class AnalysisRequestConfig(BaseModel):
    dependent_variable: str
    independent_variables: list[Any]

    model_config = SettingsConfigDict(from_attributes=True)