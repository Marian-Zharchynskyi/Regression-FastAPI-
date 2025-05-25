import uuid
from datetime import datetime
from typing import Annotated
from fastapi import Depends, UploadFile, HTTPException
from sqlalchemy.exc import IntegrityError

from services.csv_service import CsvService
from services.regression_service import RegressionServiceDependency

from crud.analysis_repository import AnalysisRequestRepositoryDependency
from crud.regression_repository import RegressionResultRepositoryDependency

from models import AnalysisRequest

from schemas.analysis_request_config import AnalysisRequestConfig
from schemas.regression_result import RegressionResultDto


class AnalysisRequestService:
    def __init__(
        self,
        analysis_request_repository: AnalysisRequestRepositoryDependency,
        regression_result_repository: RegressionResultRepositoryDependency,
        regression_service: RegressionServiceDependency,
        csv_service: Annotated[CsvService, Depends(CsvService)],
    ):
        self.analysis_request_repository = analysis_request_repository
        self.regression_result_repository = regression_result_repository
        self.regression_service = regression_service
        self.csv_service = csv_service

    async def create_analysis_request(self, csv_file: UploadFile, config: dict) -> RegressionResultDto:
        try:
            config_model = AnalysisRequestConfig(**config)
        except ValueError as e:
            raise HTTPException(status_code=422, detail=f"Invalid config: {str(e)}")

        try:
            self.csv_service.set_file(csv_file.file)
            df = self.csv_service.read_csv()
            self.csv_service.validate_csv_data(df, config_model)
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

        request_id = uuid.uuid4()
        try:
            analysis_request = AnalysisRequest(
                id=request_id,
                created_at=datetime.now(),
                csv_filename=csv_file.filename,  
                dependent_variable=config_model.dependent_variable,
                independent_variables=config_model.independent_variables,
                formula=self.regression_service.generate_regression_formula(
                    config_model.dependent_variable, config_model.independent_variables, df
                ),
            )
            await self.analysis_request_repository.create_analysis_request(analysis_request)
        except IntegrityError as e:
            raise HTTPException(status_code=422, detail=f"Database error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

        regression_result = await self.regression_service.create_regression_result(
            request_id=request_id,
            dependent_variable=config_model.dependent_variable,
            independent_variables=config_model.independent_variables,
            df=df,
        )

        return RegressionResultDto.model_validate(regression_result)


AnalysisRequestServiceDependency = Annotated[AnalysisRequestService, Depends(AnalysisRequestService)]
