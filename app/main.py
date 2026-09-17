from fastapi import FastAPI


app = FastAPI(
    title="F1 Live API",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "name": "F1 Live API",
        "status": "ok",
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
    }
