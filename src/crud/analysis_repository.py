from typing import Annotated
from uuid import UUID 

from fastapi import Depends
from sqlalchemy import select

from db import SessionContext
from models import AnalysisRequest


class AnalysisRequestRepository:
    def __init__(self, session: SessionContext):
        self.session = session

    async def get_analysis_requests(self):
        query = select(AnalysisRequest)
        result = await self.session.scalars(query)

        return result.all()

    async def get_analysis_request_by_id(self, analysis_request_id: UUID): 
        query = select(AnalysisRequest).where(AnalysisRequest.id == analysis_request_id)
        result = await self.session.scalars(query)

        return result.one_or_none()

    async def create_analysis_request(self, analysis_request: AnalysisRequest):
        self.session.add(analysis_request)
        await self.session.commit()

        return analysis_request


AnalysisRequestRepositoryDependency = Annotated[AnalysisRequestRepository, Depends(AnalysisRequestRepository)]
