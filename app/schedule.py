from __future__ import annotations

from datetime import datetime, timezone, timedelta
import logging

import httpx


OPENF1_BASE_URL = "https://api.openf1.org/v1"

_schedule_cache: dict[int, tuple[float, list[dict]]] = {}
SCHEDULE_CACHE_TTL = 3600  # 1 hour

logger = logging.getLogger(__name__)


def _to_local_datetime(
    value: str | None,
    gmt_offset: str | None,
) -> str | None:
    if not value:
        return None

    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    if gmt_offset:
        sign = -1 if gmt_offset.startswith("-") else 1
        offset = gmt_offset.lstrip("+-")

        hours, minutes = offset.split(":")[:2]

        dt = dt.astimezone(
            timezone(
                sign * timedelta(
                    hours=int(hours),
                    minutes=int(minutes),
                )
            )
        )

    return dt.isoformat(timespec="seconds")


async def get_schedule(year: int | None = None) -> list[dict]:
    if year is None:
        year = datetime.now().year

    now = datetime.now(timezone.utc).timestamp()

    cached = _schedule_cache.get(year)

    if cached and now - cached[0] < SCHEDULE_CACHE_TTL:
        return cached[1]

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            meetings_response = await client.get(
                f"{OPENF1_BASE_URL}/meetings",
                params={"year": year},
            )

            if meetings_response.status_code == 401:
                logger.warning(
                    "OpenF1 schedule temporarily unavailable: "
                    "API access is restricted."
                )

                if cached:
                    logger.warning(
                        "Using stale cached schedule for %s.",
                        year,
                    )
                    return cached[1]

                return []

            meetings_response.raise_for_status()

            sessions_response = await client.get(
                f"{OPENF1_BASE_URL}/sessions",
                params={"year": year},
            )

            if sessions_response.status_code == 401:
                logger.warning(
                    "OpenF1 sessions temporarily unavailable: "
                    "API access is restricted."
                )

                if cached:
                    logger.warning(
                        "Using stale cached schedule for %s.",
                        year,
                    )
                    return cached[1]

                return []

            sessions_response.raise_for_status()

    except httpx.HTTPError as error:
        logger.warning(
            "OpenF1 schedule request failed: %s",
            error,
        )

        if cached:
            logger.warning(
                "Using stale cached schedule for %s.",
                year,
            )
            return cached[1]

        return []

    meetings = meetings_response.json()
    sessions = sessions_response.json()

    sessions_by_meeting: dict[int, list[dict]] = {}

    for session in sessions:
        if session.get("is_cancelled"):
            continue

        meeting_key = session.get("meeting_key")

        if meeting_key is None:
            continue

        sessions_by_meeting.setdefault(
            meeting_key,
            []
        ).append(session)

    schedule = []

    for meeting in meetings:
        if meeting.get("is_cancelled"):
            continue

        meeting_key = meeting["meeting_key"]

        meeting_sessions = sessions_by_meeting.get(
            meeting_key,
            []
        )

        meeting_sessions.sort(
            key=lambda session: session.get(
                "date_start",
                ""
            )
        )

        formatted_sessions = []

        for session in meeting_sessions:
            formatted_sessions.append(
                {
                    "sessionKey": session.get("session_key"),
                    "name": session.get("session_name"),
                    "type": session.get("session_type"),
                    "startDate": _to_local_datetime(
                        session.get("date_start"),
                        session.get("gmt_offset"),
                    ),
                    "endDate": _to_local_datetime(
                        session.get("date_end"),
                        session.get("gmt_offset"),
                    ),
                }
            )

        if not formatted_sessions:
            continue

        schedule.append(
            {
                "meetingKey": meeting_key,
                "name": meeting.get("meeting_name"),
                "officialName": meeting.get(
                    "meeting_official_name"
                ),
                "location": meeting.get("location"),
                "country": meeting.get("country_name"),
                "countryCode": meeting.get(
                    "country_code"
                ),
                "circuit": meeting.get(
                    "circuit_short_name"
                ),
                "round": None,
                "gmtOffset": meeting.get(
                    "gmt_offset"
                ),
                "sessions": formatted_sessions,
            }
        )

    schedule.sort(
        key=lambda meeting: (
            meeting["sessions"][0]["startDate"]
            if meeting["sessions"]
            else ""
        )
    )

    _schedule_cache[year] = (now, schedule)

    return schedule


async def get_upcoming_schedule() -> list[dict]:
    schedule = await get_schedule()

    now = datetime.now(timezone.utc)

    upcoming = []

    for meeting in schedule:
        future_sessions = [
            session
            for session in meeting["sessions"]
            if session.get("startDate")
            and datetime.fromisoformat(
                session["startDate"]
            ) >= now
        ]

        if future_sessions:
            upcoming.append(
                {
                    **meeting,
                    "sessions": future_sessions,
                }
            )

    return upcoming


async def get_next_session() -> dict | None:
    schedule = await get_schedule()

    now = datetime.now(timezone.utc)

    future_sessions = []

    for meeting in schedule:
        for session in meeting["sessions"]:
            start_date = session.get("startDate")

            if not start_date:
                continue

            session_start = datetime.fromisoformat(start_date)

            if session_start >= now:
                future_sessions.append(
                    {
                        **session,
                        "meetingKey": meeting["meetingKey"],
                        "meetingName": meeting["name"],
                        "location": meeting["location"],
                        "country": meeting["country"],
                        "circuit": meeting["circuit"],
                    }
                )

    if not future_sessions:
        return None

    future_sessions.sort(
        key=lambda session: session["startDate"]
    )

    return future_sessions[0]