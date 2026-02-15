from app.models import PaymentEvent

class PaymentService:

    def __init__(self, repository):
        self.repository = repository # Dependency injection of the repository

    def handle_events(self, stripe_event):
        if stripe_event["type"] != "payment_intent.succeeded":
            return
        payment_event = PaymentEvent(
            event_id = stripe_event["id"],
            amount = stripe_event["data"]["object"]["amount"]
        )
        self.repository.save_event(payment_event)

    def get_total_revenue(self):
        events = self.repository.get_all_events()
        return sum(event.amount for event in events)

