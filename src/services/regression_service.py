import uuid
from typing import Annotated, Dict, List
from uuid import UUID

import statsmodels.api as sm
import pandas as pd
import numpy as np
from fastapi import Depends
from sqlalchemy.orm import class_mapper

from services.csv_service import CsvService
from schemas.regression_result import RegressionResultDto
from models import RegressionResult
from crud.regression_repository import RegressionResultRepositoryDependency


def model_to_dict(obj):
    """Convert SQLAlchemy model to dictionary."""
    return {column.key: getattr(obj, column.key) for column in class_mapper(obj.__class__).columns}


class RegressionService:
    def __init__(
        self,
        regression_result_repository: RegressionResultRepositoryDependency,
        csv_service: Annotated[CsvService, Depends(CsvService)],
    ):
        self.regression_result_repository = regression_result_repository
        self.csv_service = csv_service

    async def create_regression_result(
        self, request_id: UUID, dependent_variable: str, independent_variables: List[str], df: pd.DataFrame
    ) -> RegressionResultDto:
        try:
            result = self.perform_regression_analysis(dependent_variable, independent_variables, df)
            regression_result = RegressionResult(
                id=uuid.uuid4(),
                request_id=request_id,
                coefficients_json=result["coefficients"],
                std_errors_json=result["std_errors"],
                t_statistics_json=result["t_statistics"],
                p_values_json=result["p_values"],
                confidence_intervals=result["confidence_intervals"],
                r_squared=result["r_squared"],
                adj_r_squared=result["adj_r_squared"],
                f_statistic=result["f_statistic"],
                f_p_value=result["f_p_value"],
                n_observations=result["n_observations"],
                formula=f"{dependent_variable} ~ {' + '.join(independent_variables)}", 
            )

            saved_result = await self.regression_result_repository.create_regression_result(regression_result)
            await self.regression_result_repository.session.refresh(saved_result)

            return RegressionResultDto.from_db_model(saved_result)  
        except Exception as e:
            raise ValueError("Failed to perform regression analysis") from e

    def perform_regression_analysis(
        self, dependent_variable: str, independent_variables: List[str], df: pd.DataFrame
    ) -> Dict:
        x = df[independent_variables]
        y = df[dependent_variable]

        x = sm.add_constant(x)

        model = sm.OLS(y, x).fit()

        coefficients = model.params.to_dict()
        std_errors = model.bse.to_dict()
        t_statistics = model.tvalues.to_dict()
        p_values = model.pvalues.to_dict()
        r_squared = float(np.clip(model.rsquared, 0, 1))  
        adj_r_squared = float(np.clip(model.rsquared_adj, 0, 1))  
        f_statistic = float(max(0, model.fvalue))  
        f_p_value = float(np.clip(model.f_pvalue, 0, 1))
        n_observations = int(max(1, len(y)))  

        conf_int = model.conf_int()
        confidence_intervals = {
            col: {"lower": float(conf_int.loc[col][0]), "upper": float(conf_int.loc[col][1])}
            for col in model.params.index
        }

        return {
            "coefficients": coefficients,
            "std_errors": std_errors,
            "t_statistics": t_statistics,
            "p_values": p_values,
            "confidence_intervals": confidence_intervals,
            "r_squared": r_squared,
            "adj_r_squared": adj_r_squared,
            "f_statistic": f_statistic,
            "f_p_value": f_p_value,
            "n_observations": n_observations,
        }

    def generate_regression_formula(
        self, dependent_variable: str, independent_variables: List[str], df: pd.DataFrame
    ) -> str:
        x = df[independent_variables]
        y = df[dependent_variable]

        x = sm.add_constant(x)

        model = sm.OLS(y, x).fit()

        coefficients = model.params.to_dict()

        formula = f"{dependent_variable} = {coefficients['const']}"
        for var, coef in coefficients.items():
            if var != "const":
                formula += f" + {coef} * {var}"
        return formula


RegressionServiceDependency = Annotated[RegressionService, Depends(RegressionService)]
