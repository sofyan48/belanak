from fastapi import APIRouter
from app.appctx import IGetResponseBase, response


router = APIRouter()

@router.get("/health")
async def build_retriever() -> IGetResponseBase:
    
    return response(
        status_code=200,
        message="Success",
        data= None
        
    )