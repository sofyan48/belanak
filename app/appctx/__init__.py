from math import ceil
from typing import Any, Generic, TypeVar
from collections.abc import Sequence
from fastapi_pagination import Params, Page
from fastapi_pagination.bases import AbstractPage, AbstractParams
from pydantic import Field
from pydantic.generics import GenericModel
from fastapi.responses import JSONResponse

from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from app import app

DataType = TypeVar("DataType")
T = TypeVar("T")

class PageBase(Page[T], Generic[T]):
    previous_page: int | None = Field(
        None, description="Page number of the previous page"
    )
    next_page: int | None = Field(None, description="Page number of the next page")


class IResponseBase(GenericModel, Generic[T]):
    message: str = ""
    meta: dict = {}
    data: T | None


class IGetResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str | None = "Data got correctly"
    status_code: int | None = None


def response(
    status_code: int,
    data: DataType | None = None,
    message: str | None = None,
    meta: dict | Any | None = {}) -> ( IResponseBase[DataType]
    | IGetResponseBase[DataType]):
    try:
        if message is None:
            return {"data": data, "meta": meta}
        
        return JSONResponse(content={
            "message": message, 
            "data": data, 
            "meta": meta
        }, status_code=status_code)
    except Exception as e:
        return JSONResponse(content={
            "message": str(e),
            "data": None,
        }, status_code=500)

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