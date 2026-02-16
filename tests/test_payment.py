from app.service import PaymentService

def test_payment_event():
    service = PaymentService()

    event = [
            {
                "id": "evt_test_1",
                "data": {
                    "object": {
                        "amount": 5000
                }
            }
        }
    ]

    service.handle_events(event)

    assert service.get_total_revenue() == 5000
