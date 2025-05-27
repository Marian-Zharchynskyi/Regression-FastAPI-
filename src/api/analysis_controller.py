import json
from uuid import UUID
from typing import List

from fastapi import APIRouter, UploadFile, Form, HTTPException

from services.analysis_service import AnalysisRequestServiceDependency
from schemas.regression_result import RegressionResultDto

analysis_request_router = APIRouter(prefix="/analysis-requests")


@analysis_request_router.post("/analyse-regression")
async def analyse_regression(
    csv_file: UploadFile,
    analysis_request_service: AnalysisRequestServiceDependency,
    config: str = Form(...),
):
    config_dict = json.loads(config)
    return await analysis_request_service.create_analysis_request(csv_file, config_dict)


@analysis_request_router.get("/", response_model=List[RegressionResultDto])
async def get_all_analyses(
    analysis_request_service: AnalysisRequestServiceDependency,
):
    analyses = await analysis_request_service.get_all_analysis_requests()
    return analyses


@analysis_request_router.get("/{analysis_id}", response_model=RegressionResultDto)
async def get_analysis_by_id(
    analysis_id: UUID,
    analysis_request_service: AnalysisRequestServiceDependency,
):
    analysis = await analysis_request_service.get_analysis_request_by_id(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis