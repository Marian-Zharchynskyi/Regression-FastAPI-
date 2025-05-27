from typing import List
from fastapi import APIRouter

from services.regression_service import RegressionServiceDependency
from schemas.regression_result import RegressionResultDto

regression_router = APIRouter(prefix="/regression-results")


@regression_router.get("/", response_model=List[RegressionResultDto])
async def get_all_regression_results(
    regression_service: RegressionServiceDependency,
):
    return await regression_service.get_all_regression_results()
