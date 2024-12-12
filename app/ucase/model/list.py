from fastapi import APIRouter, Depends
from app.appctx import IGetResponseBase, response
from app.presentation import request
from app import mistral_agent
import os

router = APIRouter()

@router.get("/model") 
async def send_chat() -> IGetResponseBase:
    try:
        result = mistral_agent.list_model()
    except Exception as e:
        return response(
            status_code=500,
            message="Failed",
            data=None
        )
    
    return response(
        status_code=200,
        message="Success",
        data=result.model_dump()
    )