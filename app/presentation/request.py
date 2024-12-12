from pydantic import BaseModel, constr, Field
from typing import Any, Dict


class RequesChat(BaseModel):
    chat: constr(min_length=1)

class RequestFinetune(BaseModel):
    model: constr(min_length=1)
    model: constr(min_length=1)
    step: int = Field(..., gt=0)  # gt=0 berarti nilai harus lebih besar dari 0
    learning_rate: float = Field(..., gt=0)  # gt=0 berarti nilai harus lebih besar dari 0