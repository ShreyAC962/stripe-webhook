from fastapi import FastAPI
from app.queue import publish

from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

app = FastAPI() # Initialize FastAPI application

@app.get("/")
def root():
    return {"message": "Welcome to the Stripe Webhook Processor!"} # Basic root endpoint for testing

@app.post("/webhook")
async def stripe_webhook(event: dict):
    publish(event) # Publish the incoming Stripe event to the queue for processing
    return {"status": "accepted"} # Return a response indicating the event was accepted for processing

@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(), # Generate the latest Prometheus metrics
        media_type=CONTENT_TYPE_LATEST # Set the content type for Prometheus metrics
    )