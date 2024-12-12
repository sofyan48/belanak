from fastapi import (
    APIRouter
)
from app.presentation import request
from app.appctx import IGetResponseBase, response
from app import finetune

router = APIRouter()

@router.post("/finetune/job") 
async def start_job(payload : request.PayloadStartJobFineTune) -> IGetResponseBase:
    try:
        result = finetune.start_job(
            job_id=payload.id
        )
    except Exception as e:
        return response(
            status_code=500,
            message=str(e),
            data=None
        )
    print()
    return response(
        status_code=200,
        message="Success",
        data=result.model_dump()
    )

