from pydantic import BaseModel, constr, conint
from typing import Any, Dict


class RequesChat(BaseModel):
    chat: constr(min_length=1)


class ParamsListFinetuneJobs(BaseModel):
    page: conint(ge=1)
    limit: conint(ge=1)
