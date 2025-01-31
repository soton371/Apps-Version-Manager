from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException as StarletteHTTPException

from .core.custom_response import ResponseFailed

from fastapi.middleware.cors import CORSMiddleware
from .routers import apps,auths, audit_trails, exception_reports



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=["http://127.0.0.1:8000", "http://192.168.0.43:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return ResponseFailed(
        status_code=exc.status_code,
        message=f"{exc.detail}",
    )


app.include_router(apps.router)
app.include_router(auths.router)
app.include_router(audit_trails.router)
app.include_router(exception_reports.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}



#source .venv/bin/activate
#uvicorn app.main:app --host 192.168.0.43 --port 8000 --reload