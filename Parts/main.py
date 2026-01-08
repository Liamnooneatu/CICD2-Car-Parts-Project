from fastapi import FastAPI, HTTPException, status
import aio_pika
import os
import json

from .schemas import Part

app = FastAPI(title="Service A - Parts API")
parts: list[Part] = []

RABBIT_URL = os.getenv("RABBIT_URL")
EXCHANGE_NAME = "events_topic"


async def publish_topic_event(routing_key: str, payload: dict):
    """
    Publish an event to a RabbitMQ topic exchange.
    """
    if not RABBIT_URL:
        raise RuntimeError("RABBIT_URL is not set. Run: set -a; source .env; set +a")

    conn = await aio_pika.connect_robust(RABBIT_URL)
    ch = await conn.channel()

    ex = await ch.declare_exchange(EXCHANGE_NAME, aio_pika.ExchangeType.TOPIC)

    msg = aio_pika.Message(body=json.dumps(payload).encode())
    await ex.publish(msg, routing_key=routing_key)

    await conn.close()


@app.get("/")
def read_root():
    return {"message": "Service A running - Parts API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/parts")
def get_parts():
    return parts


@app.get("/api/parts/{Part_id}")
def get_part(Part_id: int):
    for p in parts:
        if p.Part_id == Part_id:
            return p
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Part not found")


@app.post("/api/parts", status_code=status.HTTP_201_CREATED)
async def add_part(part: Part):
    if any(p.Part_id == part.Part_id for p in parts):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Part_id already exists")

    parts.append(part)

    # Publish RabbitMQ topic event
    await publish_topic_event(
        "part.created",
        {"event": "part.created", "part": part.model_dump()}  # if this fails, use part.dict()
    )

    return part


@app.put("/api/parts/{Part_id}")
async def update_part(Part_id: int, updated_part: Part):
    for i, p in enumerate(parts):
        if p.Part_id == Part_id:
            parts[i] = updated_part

            # Publish update event (optional but useful for Part B demo)
            await publish_topic_event(
                "part.updated",
                {"event": "part.updated", "part": updated_part.model_dump()}
            )

            return updated_part

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Part not found")


@app.delete("/api/parts/{Part_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_part(Part_id: int):
    for i, p in enumerate(parts):
        if p.Part_id == Part_id:
            deleted = parts.pop(i)

            # Publish delete event (optional)
            await publish_topic_event(
                "part.deleted",
                {"event": "part.deleted", "part": deleted.model_dump()}
            )

            return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Part not found")


# Simple manual test publisher (optional)
@app.post("/api/events/test")
async def test_event(event: dict):
    await publish_topic_event("part.test", event)
    return {"status": "Message sent", "event": event}
