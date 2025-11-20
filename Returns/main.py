from fastapi import FastAPI, HTTPException, status
from .schemas import Return

Returns: list[Return] = []

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is running, please enter the product you want to return!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/Returns")
def get_Returns():
    return Returns

@app.get("/api/Returns/{Return_id}")
def get_Return(Return_id: int):
    for u in Returns:
        if u.Return_id == Return_id:
            return u
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Return Item not found")


#@app.post("/api/Returns", status_code=status.HTTP_201_CREATED)
#def add_Return(Return: Return):
   # if any(u.Return_id == Return.Return_id for u in Returns):
  #      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This Return_id already exists")
  #  Returns.append(Return)
  #  return Return

@app.put("/api/Returns/{Return_id}")
def update_Return(Return_id: int, updated_Return: Return):
    for index, u in enumerate(Returns):
        if u.Return_id == Return_id:
            Returns[index] = updated_Return
            return updated_Return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Return not found")


@app.delete("/api/Returns/{Return_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_Return(Return_id: int):
    for index, u in enumerate(Returns):
        if u.Return_id == Return_id:
            Returns.pop(index)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Return not found")

