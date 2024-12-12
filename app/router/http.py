# from fastapi import APIRouter
from fastapi import APIRouter
from app.ucase import health

from app.ucase import finetune
from app.ucase import chat

routerIn = APIRouter(prefix="/in")
routerIn.include_router(health.router)

routerV1 = APIRouter(prefix="/v1")
routerV1.include_router(chat.chat.router)
routerV1.include_router(finetune.create.router)
routerV1.include_router(finetune.list.router)
routerV1.include_router(finetune.cancel.router)
routerV1.include_router(finetune.start.router)
