from app.schemas import PaymentEventSchema

class PaymentService:
    def process_event(self, strip_event):
        return PaymentEventSchema(
            event_id = strip_event['id'],
            amount= strip_event['data']['object']['amount']
        )