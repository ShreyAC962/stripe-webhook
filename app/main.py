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

# Requirements:
# 1. Can stripe send duplicate events? 
# 2. Do events need to be persisted long term? 
# 3. How man events per second do we expect?  
# 4. Do we need to support concurrent processing?
# 5. Do we need observability like logging?

# Goal 
# 1. Stripe can send duplicates
# 2. Events must not be lost
# 3. Systems should scale
# 4. Logging would be useful

# Issues with current implementation:
# 1. Uses global variable => not thread safe, not scalable
# 2. No duplicate protection => if stripe sends duplicate events, we will count the revenue multiple times
# 3. No persistence => events can be lost if the server restarts
# 4. No logging => we have no visibility into what is happening
# 5. No structure => we have no way to query the events or calculate revenue for a specific time period



