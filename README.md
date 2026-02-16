# Stripe sends events when the payment is successful

# Creating a webhook handler
 #### That recives the events
 #### Stores the events
 #### Prevents duplicate
 #### Calcualte the total revenue

```
events = []

def handle_event(event):
    if event["type"] == "payment_intent.succeeded":
        events.append(event)

def get_total_revenue():
    total = 0
    for event in events:
        total += event["data"]["object"]["amount"]
    return total
```

# Requirements:
 #### 1. Can stripe send duplicate events? 
 #### 2. Do events need to be persisted long term? 
 #### 3. How man events per second do we expect?  
 #### 4. Do we need to support concurrent processing?
 #### 5. Do we need observability like logging?

# Goal 
 #### 1. Stripe can send duplicates
 #### 2. Events must not be lost
 #### 3. Systems should scale
 #### 4. Logging would be useful

# Issues with current implementation:
 #### 1. Uses global variable => not thread safe, not scalable
 #### 2. No duplicate protection => if stripe sends duplicate events, we will count the revenue multiple times
 #### 3. No persistence => events can be lost if the server restarts
 #### 4. No logging => we have no visibility into what is happening
 #### 5. No structure => we have no way to query the events or calculate revenue for a specific time period

# IMPLEMENTATION
 #### 1. Introduced a PaymentEvent dataclass to improve structure and readability
 #### 2. I created a PaymentRepository class to seperate storage logic
 #### 3. I added duplicate protection using event_id as a unique identifier in the repository(Ensures Idempotency)
 #### 4. I introduced logging to provide visibility into the system's operations
 #### 5. I created the PaymentService class to handle business logic and better for testing and maintainability


# Production - How to scale this system?
 #### 1. I would not store events in memory. I would store them in a database like PostgresSQL.
 #### 2. I would also introduce message queues like Kafka or SQS to asynchronously process events and improve scalability.
 #### 3. "Stripe webhook" => API => "Message Queue"=> Worker => Database
    - Worker: A background process that consumes messages from the queue and processes them, such as saving events to the database or performing other business logic.
 #### 4. This ensures scalability and fault tolerance, as the message queue can handle spikes in traffic and the worker can be scaled horizontally to process events concurrently.
 
  Add structured logging
   #### 1. I would add structured logging
   #### 2. I would also add metrics so that we can monitor the system's performance and health.
   #### 3. Number of events processed => Failures, Duplicates => For this i would use monitoring tools like Prometheus and Grafana to visualize the metrics and set up alerts for any anomalies.





# Stripe Webhook Handler — Scalable Production Design
Initial Implementation

Stripe sends events when a payment is successful. The webhook handler receives these events, stores them, prevents duplicates, and calculates total revenue.

```
events = []

def handle_event(event):
    if event["type"] == "payment_intent.succeeded":
        events.append(event)

def get_total_revenue():
    total = 0
    for event in events:
        total += event["data"]["object"]["amount"]
    return total

```

# Requirements Clarification

    Before making changes, I would clarify the requirements:

    Can Stripe send duplicate events?
    Yes, Stripe webhooks are at-least-once delivery, so duplicates are possible.

    Do events need to be persisted long-term?
    Yes, events must not be lost.

    How many events per second do we expect?
    This helps determine scalability requirements.

    Do we need to support concurrent processing?
    Yes, production systems must handle concurrent requests safely.

    Do we need observability like logging and metrics?
    Yes, observability is critical for debugging and monitoring.

    Issues with Current Implementation

    The current implementation has several limitations:

 #### 1. Uses global variable

    Not thread-safe
    Not scalable
    Data will be lost if server restarts

 #### 2. No duplicate protection

    Stripe can resend the same event.

    This would result in revenue being counted multiple times.

 #### 3. No persistence

    Events are stored only in memory.

    If the server crashes, all data is lost.

 #### 4. No logging

    There is no visibility into:

    • What events were received
    • Whether processing failed
    • Whether duplicates occurred

 #### 5. No structure

    Events are stored as raw dictionaries.

    This makes querying and maintenance difficult.

    Improved Implementation

To address these issues, I made the following design improvements:

 #### 1. Introduced PaymentEvent Dataclass

    This improves:

    • Readability
    • Type safety
    • Maintainability

    Example:
    ```
    @dataclass
    class PaymentEvent:
        event_id: str
        amount: int
    ````

 #### 2. Created PaymentRepository

    This separates storage logic from business logic.

    Benefits:

    • Clean architecture
    • Easier testing
    • Better scalability

 #### 3. Added Duplicate Protection (Idempotency)

    Each Stripe event has a unique event_id.

    I enforce uniqueness in the repository.

    This ensures duplicate events are ignored.

    This guarantees idempotent processing, which is critical for webhook systems.

 #### 4. Introduced Logging

    I added structured logging to provide visibility.

    This helps track:

    • Events received
    • Duplicate events
    • Failures

    Example:

    event_saved
    duplicate_event
    processing_failed

 #### 5. Created PaymentService Layer

    This separates business logic from storage.

    Benefits:

    • Better organization
    • Easier testing
    • More maintainable code

# Production-Scale Design

For production scalability, I would make the following improvements:

 #### 1. Use Persistent Database (PostgreSQL)

    Instead of storing events in memory, I would store them in a database such as PostgreSQL.

    Benefits:

    • Prevents data loss
    • Supports querying and analytics
    • Ensures durability

 #### 2. Introduce Message Queue (Kafka or SQS)

    architecture:
    ```
    Stripe Webhook
        ↓
    API Service
        ↓
    Message Queue (Kafka / SQS)
        ↓
    Worker Service
        ↓
    Database
    ```

 #### 3. Worker-based Asynchronous Processing

    Worker consumes events from queue and stores them in database.

    Benefits:

    • Improves scalability
    • Improves reliability
    • Enables horizontal scaling

    Multiple workers can run in parallel.

 #### 4. Fault Tolerance

    Message queue ensures events are not lost even if worker crashes.

    Workers can resume processing later.

    Observability Improvements

    To monitor system health, I would add:

# Structured Logging

    Structured JSON logs improve debugging and tracing.

        Example:
        ```
        {
        "event_id": "evt_123",
        "status": "processed"
        }
        ```

# Metrics Monitoring

    I would track metrics such as:

    • Number of events processed
    • Number of duplicate events
    • Number of failed events
    • Processing latency

    Monitoring Tools

    I would use:

    • Prometheus → Collect metrics
    • Grafana → Visualize metrics and alerts


# Final Production Architecture
    ```
    Stripe
    ↓
    Webhook API (FastAPI)
    ↓
    Kafka / SQS
    ↓
    Worker Service
    ↓
    PostgreSQL
    ↓
    Monitoring (Prometheus + Grafana)
    ```

"I started by identifying issues in the original implementation such as lack of persistence, duplicate handling, and scalability."

"I introduced a structured PaymentEvent model and separated business logic and storage using service and repository layers."

"I added idempotency using event_id to prevent duplicate processing."

"For production scalability, I would store events in PostgreSQL and use Kafka or SQS for asynchronous processing."

"This allows horizontal scaling and ensures fault tolerance."

"I also added structured logging and metrics using Prometheus and Grafana to improve observability."

