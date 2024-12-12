from pydantic import BaseModel, constr, conint


class RequesChat(BaseModel):
    chat: constr(min_length=1)


class ParamsListFinetuneJobs(BaseModel):
    page: conint(ge=1)
    limit: conint(ge=1)

# class BodyFinetune(BaseModel):
#     model: constr(min_length=1)
#     filename: constr(min_length=1)
#     step: conint(ge=1)
#     learning_rate: float
#     weight: int = conint(ge=1)
