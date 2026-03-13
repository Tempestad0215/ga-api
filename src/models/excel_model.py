from typing import Optional

from pydantic import BaseModel



class ItemExcelModel(BaseModel):
    ItemCode: str
    ItemName: str
    WarehouseCode: str
    InStock: float
    Price: float
    DesiredInventory: float
    MinInventory: float
    MaxInventory: float
    BarCode: Optional[str] = None