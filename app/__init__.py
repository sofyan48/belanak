import os 
from fastapi import (
    FastAPI
)
from bootstrap import (
    mistral
)
from app.core import settings
from starlette.middleware.cors import CORSMiddleware


APP_ROOT = os.path.join(os.path.dirname(__file__), '..')

# bootstaping
mistral_client = mistral.mistral_client()
codestral = mistral.codestral_client(mistral)
finetune = mistral.fine_tuning(mistral_client)

# Core Application Instance
app = FastAPI()
# Set all CORS origins enabled
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Routers
from app.router.http import routerV1, routerIn
app.include_router(router=routerIn)
app.include_router(router=routerV1, prefix="/ex")