from fastapi import FastAPI, HTTPException, status
import aio_pika
import os
import json



from .schemas import Part

parts: list[Part] = []

app = FastAPI()

RABBIT_URL = os.getenv("RABBIT_URL")

async def publish_event(queue_name: str, payload: dict):
    connection = await aio_pika.connect_robust(RABBIT_URL)
    channel = await connection.channel()

    message = aio_pika.Message(body=json.dumps(payload).encode())

    await channel.default_exchange.publish(
        message,
        routing_key=queue_name
    )

    await connection.close()

@app.post("/api/events/test")
async def test_event(event: dict):
    await publish_event("parts_queue", event)
    return {"status": "Message sent", "event": event}

@app.post("/api/parts", status_code=status.HTTP_201_CREATED)
async def add_Part(Part: Part):
    if any(u.Part_id == Part.Part_id for u in parts):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Part_id already exists")
    parts.append(Part)

    await publish_event("parts_queue", {
        "event": "part.created",
        "part": Part.model_dump()  # if using Pydantic v2
        # if this errors, use: Part.dict()  (Pydantic v1)
    })

    return Part



@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is running, please enter the part u are searching!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/parts")
def get_parts():
    return parts

@app.get("/api/parts/{Part_id}")
def get_Part(Part_id: int):
    for u in parts:
        if u.Part_id == Part_id:
            return u
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Part not found")

@app.post("/api/parts", status_code=status.HTTP_201_CREATED)
def add_Part(Part: Part):
    if any(u.Part_id == Part.Part_id for u in parts):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Part_id already exists")
    parts.append(Part)
    return Part

@app.put("/api/parts/{Part_id}")
def update_Part(Part_id: int, updated_Part: Part):
    for index, u in enumerate(parts):
        if u.Part_id == Part_id:
            parts[index] = updated_Part
            return updated_Part
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Part not found")


@app.delete("/api/parts/{Part_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_Part(Part_id: int):
    for index, u in enumerate(parts):
        if u.Part_id == Part_id:
            parts.pop(index)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Part not found")

