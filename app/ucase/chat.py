from fastapi import APIRouter, Depends
from app.appctx import IGetResponseBase, response
from app.presentation import request
from app import codestral

router = APIRouter()

@router.post("/chat") 
async def send_chat(payload: request.RequesChat) -> IGetResponseBase:
    result = codestral.chat(payload.chat)
    return response(
        message="Success",
        data=result
    )