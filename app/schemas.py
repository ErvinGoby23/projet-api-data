from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Literal


# Transactions
class TransactionBase(BaseModel):
    timestamp: Optional[datetime] = None
    amount: float
    currency: str
    merchant: str
    category: Optional[str] = None
    user_id: Optional[str] = None
    meta: Optional[dict] = None

class TransactionCreate(TransactionBase):
    timestamp: datetime   # obligatoire à la création

class TransactionRead(TransactionBase):
    id: int
    class Config:
        from_attributes = True


# Rail events
RailEventType = Literal["ARRIVAL", "DEPARTURE", "DELAY", "CANCEL"]

class RailEventCreate(BaseModel):
    event_time: datetime
    site_name: str
    train_no: str
    event_type: RailEventType
    delay_min: Optional[int] = None
    notes: Optional[str] = None

class RailEventRead(RailEventCreate):
    id: int
    class Config:
        from_attributes = True


# Pagination helper
class Page(BaseModel):
    items: List[TransactionRead]
    total: int
    page: int
    size: int
