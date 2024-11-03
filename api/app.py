from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI()

@app.get("/")
async def read_root():
    return {}

@app.get("/miscellaneous/addition")
async def addition(a: Optional[float] = None, b: Optional[float] = None):
    if a is None or b is None:
        raise HTTPException(status_code=400, detail="Both query parameters 'a' and 'b' are required")
    return {"result": a + b}