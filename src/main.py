from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api.analysis_controller import analysis_request_router

app = FastAPI()

app.include_router(analysis_request_router, prefix="/v1")


@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")
