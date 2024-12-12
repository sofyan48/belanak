from fastapi import (
    APIRouter
)
from app.presentation import request
from app.appctx import IGetResponseBase, response
from app import finetune

router = APIRouter()

@router.post("/finetune/job/cancel") 
async def cancel_job(payload : request.PayloadCancelFineTune) -> IGetResponseBase:
    try:
        result = finetune.cancel_job(
            job_id=payload.id
        )
    except Exception as e:
        return response(
            status_code=500,
            message="Failed",
            data=None
        )
    print()
    return response(
        status_code=200,
        message="Success",
        data=result.model_dump()
    )

