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

    result = service.process_event(event)

    assert result.amount == 100
