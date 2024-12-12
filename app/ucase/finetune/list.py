from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.appctx import IGetResponseBase, response
from app.presentation import request
from app import finetune

router = APIRouter()

@router.get("/finetune") 
async def fine_tune(params: request.ParamsListFinetuneJobs = Query(...)) -> IGetResponseBase:
    try:
        job_list = finetune.list_job(params.limit, params.page)
    except Exception as e:
        return response(
            status_code=500,
            message="Failed:"+str(e)
        )
    return response(
        status_code=200,
        message="Success",
        meta= {
            "total": job_list.total
        },
        data=job_list.data
    )

