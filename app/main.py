import asyncio
import logging

import httpx
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

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
_race_winner_cache: dict[int, dict] = {}

app = FastAPI(
    title="F1 Live API",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

@app.get("/session/{meeting_key}/{session_name}")
async def session_details(
    meeting_key: int,
    session_name: str,
):
    snapshot = state.snapshot()
    current_session = snapshot["session"]

    if (
        current_session.get("meetingKey") == meeting_key
        and current_session.get("type") == session_name
    ):
        return {
            "meetingKey": meeting_key,
            "sessionKey": current_session.get("sessionKey"),
            "session": current_session.get("name"),
            "type": current_session.get("type"),
            "meetingName": current_session.get("meetingName"),
            "location": current_session.get("location"),
            "circuit": current_session.get("circuit"),
            "startDate": current_session.get("startDate"),
            "endDate": current_session.get("endDate"),
            "status": current_session.get("status"),
        }

    schedule = await get_schedule()

    meeting = next(
        (
            meeting
            for meeting in schedule
            if meeting["meetingKey"] == meeting_key
        ),
        None,
    )

    if meeting:
        selected_session = next(
            (
                session
                for session in meeting["sessions"]
                if session["name"] == session_name
            ),
            None,
        )

        if selected_session:
            return {
                "meetingKey": meeting_key,
                "session": selected_session["name"],
                "type": selected_session["type"],
                "meetingName": meeting["name"],
                "location": meeting["location"],
                "circuit": meeting["circuit"],
                "startDate": selected_session["startDate"],
                "endDate": selected_session["endDate"],
                "status": "preview",
                "message": "Historical session data is not available yet.",
            }

    return {
        "meetingKey": meeting_key,
        "session": session_name,
        "status": "preview",
        "message": "Historical session data is not available yet.",
    }

@app.get("/race-winner/{session_key}")
async def race_winner(session_key: int):
    if session_key in _race_winner_cache:
        return _race_winner_cache[session_key]
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(
                "https://api.openf1.org/v1/session_result",
                params={"session_key": session_key},
            )

            if response.status_code == 401:
                return {
                    "status": "unavailable",
                    "message": "OpenF1 race result access is restricted.",
                }

            response.raise_for_status()

            results = response.json()

            winner = next(
                (
                    result
                    for result in results
                    if result.get("position") == 1
                ),
                None,
            )

            if not winner:
                return {
                    "status": "unavailable",
                    "message": "Race winner is not available.",
                }

            driver_number = winner.get("driver_number")

            driver_response = await client.get(
                "https://api.openf1.org/v1/drivers",
                params={
                    "session_key": session_key,
                    "driver_number": driver_number,
                },
            )

            driver_response.raise_for_status()

            drivers = driver_response.json()
            driver = drivers[0] if drivers else {}

            winner_data = {
                "status": "finished",
                "position": 1,
                "driverNumber": driver_number,
                "driverName": (
                    f"{driver.get('first_name', '')} "
                    f"{driver.get('last_name', '')}"
                ).strip(),
                "teamName": driver.get("team_name"),
                "headshotUrl": driver.get("headshot_url"),
            }

            _race_winner_cache[session_key] = winner_data

            return winner_data

    except httpx.HTTPError as error:
        logging.warning(
            "Could not load race winner for session %s: %s",
            session_key,
            error,
        )

        return {
            "status": "unavailable",
            "message": "Could not load race winner.",
        }

@app.get("/schedule", response_model=ScheduleResponse)
async def schedule():
    return {
        "meetings": await get_schedule(),
    }

@app.get("/schedule/upcoming", response_model=ScheduleResponse)
async def upcoming_schedule():
    return {
        "meetings": await get_upcoming_schedule(),
    }

@app.get("/schedule/next")
async def next_session():
    return await get_next_session()

@app.websocket("/ws/live")
async def websocket_live(websocket: WebSocket):
    await live_websocket(websocket, state)


@app.on_event("startup")
async def startup():
    asyncio.create_task(f1_client.run())


@app.on_event("shutdown")
async def shutdown():
    f1_client.stop()