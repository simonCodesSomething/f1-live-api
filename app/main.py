import asyncio
import logging

from fastapi import FastAPI, WebSocket

from app.f1_client import F1LiveClient
from app.models import F1Snapshot, ScheduleResponse
from app.schedule import (
    get_schedule,
    get_upcoming_schedule,
    get_next_session,
)
from app.state import F1State
from app.websocket import live_websocket, manager

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="F1 Live API",
    version="0.1.0",
)

def handle_f1_message(message: dict):
    state.update(message)

    snapshot = state.snapshot()

    print(
        f"Broadcasting: "
        f"{snapshot['session']['lap']}/"
        f"{snapshot['session']['totalLaps']} "
        f"drivers={len(snapshot['drivers'])}"
    )

    asyncio.create_task(manager.broadcast(snapshot))


state = F1State()
f1_client = F1LiveClient(handle_f1_message)


@app.get("/")
async def root():
    return {
        "name": "F1 Live API",
        "status": "ok",
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/snapshot", response_model=F1Snapshot)
async def snapshot():
    return state.snapshot()

@app.get("/schedule", response_model=ScheduleResponse)
async def schedule():
    return {
        "meetings": get_schedule(),
    }

@app.get("/schedule/upcoming", response_model=ScheduleResponse)
async def upcoming_schedule():
    return {
        "meetings": get_upcoming_schedule(),
    }

@app.get("/schedule/next")
async def next_session():
    return get_next_session()

@app.websocket("/ws/live")
async def websocket_live(websocket: WebSocket):
    await live_websocket(websocket, state)


@app.on_event("startup")
async def startup():
    asyncio.create_task(f1_client.run())


@app.on_event("shutdown")
async def shutdown():
    f1_client.stop()