import logging

from app.models import PaymentEvent

logging.basicConfig(level = logging.INFO)

class PaymentRepository:
    def __init__(self):
        self.events = {}
        logging.info("Payment Repository initialized")

    def save_event(self, payment_event : PaymentEvent):
        if payment_event.event_id in self.events:
            logging.warning(f"Duplicate event detected: {payment_event.event_id}")
            return 
        self.events[payment_event.event_id] = payment_event
        logging.info(f"Event saved: {payment_event.event_id}")
    
    def get_all_events(self):
        return list(self.events.values())

