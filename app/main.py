from app.repository import PaymentRepository
from app.service import PaymentService

repository = PaymentRepository()

service = PaymentService(repository)

# Simulate Stripe event

event = {
    "id": "evt_1",
    "type":"payment_intent.succeeded",
    "data": {
        "object": {
            "amount": 1000
        }
    }
}

service.handle_events(event)

print(f"Total Revenue: {service.get_total_revenue()}")