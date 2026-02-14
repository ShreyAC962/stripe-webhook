# Stripe sends events when the payment is successful

# Creating a webhook handler
# That recives the events
# Stores the events
# Prevents duplicate
# Calcualte the total revenue

events = []

def handle_event(event):
    if event["type"] == "payment_intent.succeeded":
        events.append(event)

def get_total_revenue():
    total = 0
    for event in events:
        total += event["data"]["object"]["amount"]
    return total