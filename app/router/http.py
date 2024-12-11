# from fastapi import APIRouter
from fastapi import APIRouter
from app.ucase import (
    health,
    chat,
    finetune
)
routerIn = APIRouter(prefix="/in")
routerIn.include_router(health.router)


routerV1 = APIRouter(prefix="/v1")
routerV1.include_router(chat.router)
routerV1.include_router(finetune.router)
# routerV1.include_router(retriever.router)
# routerV1.include_router(datasheet.router)
# routerV1.include_router(webhook.router)