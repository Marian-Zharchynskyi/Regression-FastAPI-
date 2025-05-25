from typing import Annotated, Union, BinaryIO

import pandas as pd
from fastapi import Depends

from schemas.analysis_request_config import AnalysisRequestConfig


class CsvService:
    def __init__(self):
        self.file = None

    def set_file(self, file: Union[str, BinaryIO]):
        self.file = file

    def read_csv(self) -> pd.DataFrame:
        if not self.file:
            raise ValueError("No file has been set")
            
        try:
            return pd.read_csv(self.file)
        except Exception as e:
            raise ValueError(f"Failed to read CSV file: {e}")

    def validate_csv_data(self, df: pd.DataFrame, config: AnalysisRequestConfig) -> bool:
        if config.dependent_variable not in df.columns:
            raise ValueError(f"Dependent variable column '{config.dependent_variable}' not found in CSV file")

        for independent_variable in config.independent_variables:
            if independent_variable not in df.columns:
                raise ValueError(f"Independent variable column '{independent_variable}' not found in CSV file")

        if config.dependent_variable in config.independent_variables:
            raise ValueError("Dependent variable cannot be in the list of independent variables")

        return True


CsvServiceDependency = Annotated[CsvService, Depends(CsvService)]