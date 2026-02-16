from app.queue import consume
from app.repository import PaymentRepository
from app.service import PaymentService
from app.metrics import events_processed

repository = PaymentRepository()
service = PaymentService()

def run_worker():
    while True:
        stripe_event = consume() # Consume the next event from the queue
        print("Event received:", stripe_event)
        event = service.process_event(stripe_event) # Process the event to extract relevant data
        repository.save_event(event) # Save the processed event to the database
        events_processed.inc() # Increment the Prometheus counter for processed events
