from app.schemas import PaymentEventSchema

class PaymentService:

    def __init__(self, repository):
        self.repository = repository # Dependency injection of the repository

    def handle_events(self, stripe_event):
        for event in stripe_event:
            if event["type"] != "payment_intent.succeeded":
                continue
            payment_event = PaymentEventSchema(
                event_id = event["id"],
                amount = event["data"]["object"]["amount"]
            )
            self.repository.save_event(payment_event)

    def get_total_revenue(self):
        events = self.repository.get_all_events()
        return sum(event.amount for event in events)

