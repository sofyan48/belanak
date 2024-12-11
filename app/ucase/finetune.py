from fastapi import APIRouter, File, UploadFile
from app.appctx import IGetResponseBase, response
from app.presentation import request
from app import finetune
import pandas, json, io

router = APIRouter()

@router.post("/finetune") 
async def fine_tune(file: UploadFile = File(...)) -> IGetResponseBase:
    # Membaca konten file secara asinkron
    file_content = await file.read()

    result = finetune.upload_file("testing.jsonl", file_content)
   
    finetune.create_job(
        file_id=result.id,
        model="open-mistral-7b",
        step=10,
        learning_rate=0.0001,
        weight=1,
    )
    return response(
        message="Success",
        data=result
    )