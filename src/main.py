from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.v1_router import v1_router
from src.core.exceptions import CustomBaseException, DatabaseException

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/call_exceptions')
async def call_exceptions():
    raise DatabaseException


@app.exception_handler(CustomBaseException)
async def custom_exception_handler(request, exc):
    error_class_name = exc.__class__.__name__
    description = exc.default_message
    error_detail = f"Custom error: {error_class_name}"
    print(exc.__dict__)
    return JSONResponse(status_code=exc.status_code, content={"detail": error_detail, "description": description})


app.include_router(v1_router, prefix='/api')
