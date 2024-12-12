from math import ceil
from typing import Any, Generic, TypeVar
from collections.abc import Sequence
from fastapi_pagination import Params, Page
from fastapi_pagination.bases import AbstractPage, AbstractParams
from pydantic import Field
from pydantic.generics import GenericModel
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

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
    meta: dict | Any | None = {},
) -> (
    IResponseBase[DataType]
    | IGetResponseBase[DataType]
):
    if message is None:
        return {"data": data, "meta": meta}
    
    return JSONResponse(content={
        "message": message, 
        "data": data, 
        "meta": meta
    }, status_code=status_code)