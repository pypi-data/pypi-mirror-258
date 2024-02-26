from typing import List, Optional
from pydantic import BaseModel
from .Promotions import Promotions
class OrderItem(BaseModel):
    Sku: str
    Quantity: int
    UnitPrice: float
    TaxPrice: float
    ShippingPrice: float
    ShippingTaxPrice: float
    SiteListingID: Optional[str] = None
    HarmonizedCode: Optional[str] = None
    Promotions: Optional[List[Promotions]] = None