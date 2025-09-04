from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, JSON, Enum
from .db import Base, engine
import enum

print("🔨 Création des tables…")
Base.metadata.create_all(bind=engine)
print("✅ Tables créées")

class RailEventType(str, enum.Enum):
    ARRIVAL="ARRIVAL"; DEPARTURE="DEPARTURE"; DELAY="DELAY"; CANCEL="CANCEL"

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    amount = Column(DECIMAL(10,2), nullable=False)
    currency = Column(String(3), nullable=False, default="EUR")
    merchant = Column(String(120), nullable=False)
    category = Column(String(60), nullable=True)
    user_id = Column(String(64), nullable=True)
    meta = Column(JSON, nullable=True)  # <- au lieu de "metadata"

class RailEvent(Base):
    __tablename__ = "rail_events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_time = Column(DateTime, nullable=False)
    site_name = Column(String(80), nullable=False)
    train_no = Column(String(20), nullable=False)
    event_type = Column(Enum(RailEventType), nullable=False)
    delay_min = Column(Integer, nullable=True)
    notes = Column(String(255), nullable=True)
