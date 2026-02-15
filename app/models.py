from dataclasses import dataclass

@dataclass
class PaymentEvent:
    event_id : str
    amount : int