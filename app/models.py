from sqlalchemy import Column, String, Integer

from app.database import Base

class PaymentEvent(Base):
    __tablename__ = "payment_events"
    event_id = Column(String, primary_key=True)
    amount = Column(Integer)