from app.repository import PaymentRepository
from app.service import PaymentService

repository = PaymentRepository()

service = PaymentService(repository)

# Simulate Stripe event

stripe_events = [
    {
        "id": "evt_1",
        "type": "payment_intent.succeeded",
        "data": {"object": {"amount": 1000}}
    },
    {
        "id": "evt_2",
        "type": "payment_intent.succeeded",
        "data": {"object": {"amount": 2000}}
    },
    {
        "id": "evt_3",
        "type": "payment_intent.failed",
        "data": {"object": {"amount": 1500}}
    },
    {
        "id": "evt_4",
        "type": "payment_intent.succeeded",
        "data": {"object": {"amount": 4000}}
    }
]


service.handle_events(stripe_events)

print(f"Total Revenue: {service.get_total_revenue()}")