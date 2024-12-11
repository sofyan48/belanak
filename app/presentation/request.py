from pydantic import BaseModel, constr
from typing import Any, Dict


class RequesChat(BaseModel):
    chat: constr(min_length=1)
