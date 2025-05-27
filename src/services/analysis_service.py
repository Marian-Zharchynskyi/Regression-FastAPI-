import uuid
from datetime import datetime
from typing import Annotated, List
from fastapi import Depends, UploadFile, HTTPException
from sqlalchemy.exc import IntegrityError

from services.file_service import CsvService
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
            df = self.csv_service.read_file()
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

        try:
            regression_result = await self.regression_service.create_regression_result(
                request_id=request_id,
                dependent_variable=config_model.dependent_variable,
                independent_variables=config_model.independent_variables,
                df=df,
            )

            await self.regression_result_repository.session.commit()
            
            return regression_result
        except Exception as e:
            await self.regression_result_repository.session.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to save regression result: {str(e)}")

    async def get_all_analysis_requests(self) -> List[RegressionResultDto]:
        analysis_requests = await self.analysis_request_repository.get_analysis_requests()
        results = []
        for analysis in analysis_requests:
            regression_result = await self.regression_result_repository.get_regression_result_by_request_id(analysis.id)
            if regression_result:
                try:
                    if hasattr(regression_result, 'model_summary'):
                        results.append(regression_result)
                    else:
                        results.append(RegressionResultDto.from_db_model(regression_result))
                except Exception as e:
                    print(f"Error processing analysis {analysis.id}: {str(e)}")
                    continue
        return results


AnalysisRequestServiceDependency = Annotated[AnalysisRequestService, Depends(AnalysisRequestService)]
