from typing import Optional, List

from pydantic import BaseModel, Field

from src.enums.item_enum import ItemStatusEnum
from src.models.price_list import PriceListModel
from src.models.warehouse_model import WareHouseModel


class ItemModel(BaseModel):
    ItemCode: str
    ItemName: str
    ItemsGroupCode: int
    Valid: ItemStatusEnum
    ItemWarehouseInfoCollection: List[WareHouseModel]
    ItemPrices: List[PriceListModel]
    InventoryItem: ItemStatusEnum
    DesiredInventory: float
    PurchaseItem: ItemStatusEnum
    SalesItem: ItemStatusEnum
    MinInventory: float
    MaxInventory: float
    BarCode: Optional[str] = None
    # CreateDate: Optional[datetime] = None

class ItemStockLow(BaseModel):
    Codigo: str
    Descripcion: str
    Id_Adicional: Optional[str] = None
    Disponible: float
    CompraMinima: float
    StockMinimo: float
    StockMaximo: float
    Almacen: str
    CantidadUltimaCompra: Optional[float] = None
    CostoUltimaCompra: Optional[float] = None
    FechaUltimaCompra: Optional[str] = None


class UpdateStockLimitByWarehouse(BaseModel):
    WarehouseCode: str
    MinimalStock: float
    MaximalStock: float
    MinimalOrder: float




