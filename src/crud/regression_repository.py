from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select

from db import SessionContext
from models import RegressionResult


class RegressionResultRepository:
    def __init__(self, session: SessionContext):
        self.session = session

    async def get_regression_results(self):
        query = select(RegressionResult)
        result = await self.session.scalars(query)

        return result.all()

    async def get_regression_result_by_id(self, regression_result_id: UUID):
        query = select(RegressionResult).where(RegressionResult.id == regression_result_id)
        result = await self.session.scalars(query)

        return result.one_or_none()

    async def create_regression_result(self, regression_result: RegressionResult) -> RegressionResult:
        try:
            self.session.add(regression_result)
            await self.session.flush()  # This ensures the object is saved and IDs are generated
            return regression_result
        except Exception as e:
            await self.session.rollback()
            raise ValueError(f"Failed to create regression result: {str(e)}")

    async def get_regression_result_by_request_id(self, request_id: UUID):
        query = select(RegressionResult).where(RegressionResult.request_id == request_id)
        result = await self.session.scalars(query)
        return result.one_or_none()


RegressionResultRepositoryDependency = Annotated[RegressionResultRepository, Depends(RegressionResultRepository)]
