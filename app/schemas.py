from dataclasses import dataclass

@dataclass
class PaymentEventSchema:
    event_id : str
    amount : int