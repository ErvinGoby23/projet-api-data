from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any, List, Literal

# Transactions
class TransactionCreate(BaseModel):
    timestamp: datetime
    amount: float
    currency: str
    merchant: str
    category: Optional[str] = None
    user_id: Optional[str] = None
    meta: Optional[dict] = None  # <- au lieu de "metadata"

class TransactionRead(TransactionCreate):
    id: int
    class Config:
        from_attributes = True

# Rail events
RailEventType = Literal["ARRIVAL","DEPARTURE","DELAY","CANCEL"]

class RailEventCreate(BaseModel):
    event_time: datetime
    site_name: str
    train_no: str
    event_type: RailEventType
    delay_min: Optional[int] = None
    notes: Optional[str] = None

class RailEventRead(RailEventCreate):
    id: int
    class Config: from_attributes = True

# Pagination helper
class Page(BaseModel):
    items: list
    total: int
    page: int
    size: int
