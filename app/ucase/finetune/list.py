from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.appctx import IGetResponseBase, response
from app.presentation import request
from app import finetune
import json

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
    result = job_list.model_dump()
    return response(
        status_code=200,
        message="Success",
        data= result["data"],
        meta= {
            "total": result["total"]
        }
    )

