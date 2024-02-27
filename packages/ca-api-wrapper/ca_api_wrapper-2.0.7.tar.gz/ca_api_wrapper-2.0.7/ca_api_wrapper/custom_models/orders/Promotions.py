from typing import List, Optional
from pydantic import BaseModel, validator, ValidationError

class Promotions(BaseModel): 
    Code: Optional[str]
    Amount: Optional[float]
