from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from .custom_response import ResponseFailed

from fastapi.middleware.cors import CORSMiddleware
from .routers import apps
import logging
import logging.config
from .config import settings
from .logging_config import LOGGING_CONFIG



# Adjust logging levels based on environment
if settings.env_mood == "production":
    LOGGING_CONFIG["handlers"]["console"]["level"] = "WARNING"
    LOGGING_CONFIG["loggers"]["app"]["level"] = "INFO"

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("app")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
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

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting FastAPI application in {settings.env_mood} environment")

@app.get("/")
async def root():
    logger.debug("Processing root endpoint")
    return {"message": "Hello World"}
