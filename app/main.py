from fastapi import FastAPI

app = FastAPI(title="Service A - Greeting API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/greet/{name}")
def greet(name: str):
    return {"message": f"Hello, {name} from Service A!"}
