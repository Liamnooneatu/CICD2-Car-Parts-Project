from fastapi import FastAPI, HTTPException, status
from .schemas import Part
import aio_pika
import os
import json

from .schemas import Part

app = FastAPI(title="Service A - Parts API")

parts: list[Part] = []

@app.get("/health")
def health():
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
def add_part(part: Part):
    if any(p.Part_id == part.Part_id for p in parts):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Part_id already exists")
    parts.append(part)
    return part

@app.put("/api/parts/{Part_id}")
def update_part(Part_id: int, updated_part: Part):
    for i, p in enumerate(parts):
        if p.Part_id == Part_id:
            parts[i] = updated_part
            return updated_part
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Part not found")

@app.delete("/api/parts/{Part_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_part(Part_id: int):
    for i, p in enumerate(parts):
        if p.Part_id == Part_id:
            parts.pop(i)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Part not found")
