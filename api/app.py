from fastapi import FastAPI

app = FastAPI(description="TP5 API")

@app.get
def root():
    return {}