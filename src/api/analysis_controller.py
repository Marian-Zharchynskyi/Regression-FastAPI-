import json

from fastapi import APIRouter, UploadFile, Form

from services.analysis_service import AnalysisRequestServiceDependency

analysis_request_router = APIRouter(prefix="/analysis-requests")


@analysis_request_router.post("/analyse-regression")
async def analyse_regression(
    csv_file: UploadFile,
    analysis_request_service: AnalysisRequestServiceDependency,
    config: str = Form(...),
):
    config_dict = json.loads(config)  # Parse JSON string to dictionary
    return await analysis_request_service.create_analysis_request(csv_file, config_dict)