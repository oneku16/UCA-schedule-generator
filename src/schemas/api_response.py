from typing import Any, Generic, Optional, TypeVar

from pydantic import ConfigDict
# from pydantic.generics import GenericModel
from pydantic import BaseModel


T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    message: Optional[Any]
    data: Optional[T]

    model_config = ConfigDict(extra='ignore', from_attributes=True)
