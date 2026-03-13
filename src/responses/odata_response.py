from typing import List, TypeVar, Generic, Optional

from pydantic import BaseModel, Field

T = TypeVar('T')

class ODataResponse(BaseModel, Generic[T]):
    odata_context: Optional[str]  = Field(default=None, alias="@odata.context")
    odata_next_link: Optional[str] = Field(default=None, alias="@odata.nextLink")
    value: List[T]