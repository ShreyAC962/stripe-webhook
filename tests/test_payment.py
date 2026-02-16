from app.repository import PaymentRepository
from app.service import PaymentService

def test_payment_event():
    repo = PaymentRepository()
    service = PaymentService(repo)

    event = [
            {
                "id": "evt_test_1",
                "type":"payment_intent.succeeded",
                "data": {
                    "object": {
                        "amount": 5000
                }
            }
        }
    ]

    service.handle_events(event)

    assert service.get_total_revenue() == 5000
