from typing import Annotated

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

    async def create_regression_result(self, regression_result: RegressionResult) -> RegressionResult:
        self.session.add(regression_result)
        await self.session.flush()  # Add this line to ensure all fields are populated

        return regression_result

    async def delete_regression_result(self, regression_result: RegressionResult):
        await self.session.delete(regression_result)
        await self.session.commit()

        return regression_result


RegressionResultRepositoryDependency = Annotated[RegressionResultRepository, Depends(RegressionResultRepository)]
