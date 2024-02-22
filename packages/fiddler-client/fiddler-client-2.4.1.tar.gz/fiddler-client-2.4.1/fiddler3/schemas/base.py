from pydantic import BaseModel as _BaseModel
from pydantic import Extra


class BaseModel(_BaseModel):
    class Config:
        extra = Extra.ignore
        arbitrary_types_allowed = True
