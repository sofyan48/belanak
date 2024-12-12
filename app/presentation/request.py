from pydantic import BaseModel, constr, conint


class RequesChat(BaseModel):
    chat: constr(min_length=1)


class ParamsListFinetuneJobs(BaseModel):
    page: conint(ge=1)
    limit: conint(ge=1)

class PayloadCancelFineTune(BaseModel):
    id: constr(min_length=1)

class PayloadStartJobFineTune(BaseModel):
    id: constr(min_length=1)
