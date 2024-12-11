from fastapi import APIRouter
from app.appctx import IGetResponseBase, response


router = APIRouter()

@router.get("/health")
async def build_retriever() -> IGetResponseBase:
    
    return response(
        message="Success",
        data= None
        
    )