from typing import Any, Optional

from pydantic import BaseModel, ConfigDict



class APIResponse(BaseModel):
    message: Optional[Any]
    data: Optional[Any] = None

    model_config = ConfigDict(extra='ignore', from_attributes=True)
