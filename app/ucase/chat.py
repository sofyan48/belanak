from fastapi import APIRouter, Depends
from app.appctx import IGetResponseBase, response
from app.presentation import request
from app import mistral_agent
import os

router = APIRouter()

@router.post("/chat") 
async def send_chat(payload: request.RequesChat) -> IGetResponseBase:
    agent = os.environ.get("", "ag:ea58d2f9:20241212:iankai:70172da5")
    result = mistral_agent.chat(agent_id=agent, msg=payload.chat)
    reformat_result = {
        "question": {
            "content": payload.chat,
            "role": "user",
        },
        "response": {
            "content": result.choices[0].message.content,
            "role": result.choices[0].message.role,
            "reason": result.choices[0].finish_reason,
        }
        
    }
    return response(
        message="Success",
        data=reformat_result
    )