from fastapi import FastAPI, HTTPException, status
from .schemas import Part

parts: list[Part] = []

app = FastAPI()

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

