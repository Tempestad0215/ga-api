from pydantic import BaseModel

from src.enums.item_enum import ItemStatusEnum


class WareHouseModel(BaseModel):
    Locked: ItemStatusEnum
    ItemCode: str
    InStock: float
    WarehouseCode: str