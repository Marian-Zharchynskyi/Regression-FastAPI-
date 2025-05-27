from fastapi import FastAPI
from api.analysis_controller import analysis_request_router
from api.regression_controller import regression_router

app = FastAPI()

app.include_router(analysis_request_router)
app.include_router(regression_router)
