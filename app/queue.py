import queue

event_queue = queue.Queue()

def publish(event):
    event_queue.put(event) # Add the event to the queue for processing

def consume():
    return event_queue.get() # Get the next event from the queue for processing