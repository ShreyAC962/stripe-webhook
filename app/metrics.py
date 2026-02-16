from prometheus_client import Counter

events_processed = Counter(
    "events_processed",
    "Total processed events"
)