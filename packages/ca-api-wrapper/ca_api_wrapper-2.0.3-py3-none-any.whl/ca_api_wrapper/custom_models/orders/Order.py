from typing import List, Optional
from pydantic import BaseModel
from .OrderItem import OrderItem
from .PaymentStatus import PaymentStatus

    

class Order(BaseModel):
    ProfileID: int
    
    #Order Data: 
    SiteOrderID: str
    SiteName: str
    siteID: Optional[int]
    
    #Order Amounts: 
    TotalPrice: float
    TotalTaxPrice: float
    TotalShippingPrice: float
    TotalShippingTaxPrice: float
    
    #Shipping Status
    ShippingStatus: str
    EstimatedShipDateUtc: Optional[str] = None

    #Payment Status:
    CheckoutStatus: str
    PaymentStatus: PaymentStatus
    
    #Shipping Service:
    RequestedShippingCarrier: Optional[str] = None
    RequestedShippingClass: Optional[str] = None
    
    #Buyer:
    BuyerUserId: Optional[str] = None
    BuyerEmailAddress: str
    PaymentMethod: str
    PaymentCreditCardLast4: Optional[str] = None
    PaymentMerchantReferenceNumber: Optional[str] = None
    
    #Shipping:
    ShippingTitle: Optional[str] = None
    ShippingFirstName: str
    ShippingLastName: str
    ShippingSuffix: Optional[str] = None
    ShippingCompanyName: Optional[str] = None
    ShippingCompanyJobTitle: Optional[str] = None
    ShippingDaytimePhone: str
    ShippingEveningPhone: Optional[str] = None
    ShippingAddressLine1: str
    ShippingAddressLine2: Optional[str] = None
    ShippingCity: str
    ShippingStateOrProvince: str
    ShippingPostalCode: str
    ShippingCountry: str
    
    #Billing: 
    BillingTitle: Optional[str] = None
    BillingFirstName: str
    BillingLastName: str
    BillingSuffix: Optional[str] = None
    BillingCompanyName: Optional[str] = None
    BillingCompanyJobTitle: Optional[str] = None
    BillingDaytimePhone: str
    BillingEveningPhone: Optional[str] = None
    BillingAddressLine1: str
    BillingAddressLine2: Optional[str] = None
    BillingCity: str
    BillingStateOrProvince: str
    BillingPostalCode: str
    BillingCountry: str
    
    #PrivateNotes: 
    PrivateNotes: Optional[str] = None
    
    #Items
    Items: List[OrderItem]

class Root(BaseModel):
    Order: Order
