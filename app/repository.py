from sqlalchemy import IntergrityError
from app.database import SessionLocal
from app.models import PaymentEvent

from app.logging_config import logger



class PaymentRepository:
    def save(self, event_schema):
        session = SessionLocal() 
        try:
            event = PaymentEvent(
                event_id = event_schema.event_id,
                amount = event_schema.amount
            )
            session.add(event) # Add the event to the session
            session.commit() # Commit the transaction to save it to the database
            logger.info(f"Saved event {event_schema.event_id} to the database.", extra={"event_id": event_schema.event_id})
        except IntergrityError:
            session.rollback() # Rollback the transaction if there's an integrity error (e.g., duplicate event_id)
            logger.warning(f"Event {event_schema.event_id} already exists in the database. Skipping.", extra={"event_id": event_schema.event_id})
        finally:
            session.close() # Close the session