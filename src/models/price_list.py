from typing import Optional

from pydantic import BaseModel


class PriceListModel(BaseModel):
    Price: float
    Currency: Optional[str] = None
    PriceList: int
