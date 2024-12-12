from typing import Any, TypeVar
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any, Dict, TypeVar, Optional

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from app import app

DataType = TypeVar("DataType")

class IResponseBase(BaseModel):
    message: str = ""
    meta: Dict[str, Any] = {}
    data: Optional[DataType] = None

class IGetResponseBase(IResponseBase):
    message: str = "Data got correctly"
    status_code: int = 200

def response(
    data: DataType,
    message: str = "Success",
    meta: Dict[str, Any] = {},
    status_code: int = 200
) -> JSONResponse:
    response_content = {
        "message": message,
        "meta": meta,
        "data": data
    }
    return JSONResponse(content=response_content, status_code=status_code)
    
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        error_detail = {
            "type": error["type"],
            "loc": error["loc"],
            "msg": error["msg"],
            "input": error.get("input")
        }
        errors.append(error_detail)
    return response(
        status_code=400,
        data=error,
        message="validation Failed"
    )

@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    errors = []
    for error in exc.errors():
        error_detail = {
            "type": error["type"],
            "loc": error["loc"],
            "msg": error["msg"],
            "input": error.get("input")
        }
        errors.append(error_detail)
    return response(
        status_code=400,
        data=error,
        message="validation Failed"
    )