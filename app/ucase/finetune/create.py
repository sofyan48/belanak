from fastapi import (
    APIRouter, 
    File,
    UploadFile, 
    Form,
    HTTPException
)
from app.appctx import IGetResponseBase, response
from app import finetune

router = APIRouter()

@router.post("/finetune") 
async def fine_tune(model: str = Form(...),
    filename: str = Form(...),
    step: int = Form(...),
    learning_rate: float = Form(...), 
    weight: int = Form(...),
    file: UploadFile = File(...)) -> IGetResponseBase:
    
    try:
        file_content = await file.read()
        result = finetune.upload_file(filename, file_content)
        job_result = finetune.create_job(
            file_id=result.id,
            model=model,
            step=step,
            learning_rate=learning_rate,
            weight=weight,
        )
    except Exception as e:
        return response(
            status_code=500,
            message="Failed",
            data=None
        )
    
    return response(
        status_code=200,
        message="Success",
        data={
            "file": result.model_dump(),
            "job": job_result.model_dump()
        }
    )

