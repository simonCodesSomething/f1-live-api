from __future__ import annotations

from datetime import datetime, timezone


SCHEDULE = [
    {
        "meetingKey": 15,
        "name": "Azerbaijan Grand Prix",
        "officialName": "FORMULA 1 QATAR AIRWAYS AZERBAIJAN GRAND PRIX 2026",
        "location": "Baku",
        "country": "Azerbaijan",
        "countryCode": "AZE",
        "circuit": "Baku City Circuit",
        "round": 15,
        "gmtOffset": "+04:00",
        "sessions": [
            {
                "name": "Practice 1",
                "type": "Practice",
                "startDate": "2026-09-24T12:30:00",
                "endDate": "2026-09-24T13:30:00",
            },
            {
                "name": "Practice 2",
                "type": "Practice",
                "startDate": "2026-09-24T16:00:00",
                "endDate": "2026-09-24T17:00:00",
            },
            {
                "name": "Practice 3",
                "type": "Practice",
                "startDate": "2026-09-25T12:30:00",
                "endDate": "2026-09-25T13:30:00",
            },
            {
                "name": "Qualifying",
                "type": "Qualifying",
                "startDate": "2026-09-25T16:00:00",
                "endDate": "2026-09-25T17:00:00",
            },
            {
                "name": "Race",
                "type": "Race",
                "startDate": "2026-09-26T15:00:00",
                "endDate": "2026-09-26T17:00:00",
            },
        ],
    },
    {
        "meetingKey": 16,
        "name": "Bahrain Grand Prix",
        "officialName": "FORMULA 1 GULF AIR BAHRAIN GRAND PRIX IN MALAYSIA 2026",
        "location": "Sepang",
        "country": "Malaysia",
        "countryCode": "MYS",
        "circuit": "Sepang International Circuit",
        "round": 16,
        "gmtOffset": "+08:00",
        "sessions": [
            {
                "name": "Practice 1",
                "type": "Practice",
                "startDate": "2026-10-02T18:30:00",
                "endDate": "2026-10-02T19:30:00",
            },
            {
                "name": "Practice 2",
                "type": "Practice",
                "startDate": "2026-10-02T22:00:00",
                "endDate": "2026-10-02T23:00:00",
            },
            {
                "name": "Practice 3",
                "type": "Practice",
                "startDate": "2026-10-03T19:00:00",
                "endDate": "2026-10-03T20:00:00",
            },
            {
                "name": "Qualifying",
                "type": "Qualifying",
                "startDate": "2026-10-03T23:00:00",
                "endDate": "2026-10-04T00:00:00",
            },
            {
                "name": "Race",
                "type": "Race",
                "startDate": "2026-10-04T23:00:00",
                "endDate": "2026-10-05T01:00:00",
            },
        ],
    },
    {
        "meetingKey": 17,
        "name": "Singapore Grand Prix",
        "officialName": "FORMULA 1 SINGAPORE AIRLINES SINGAPORE GRAND PRIX 2026",
        "location": "Singapore",
        "country": "Singapore",
        "countryCode": "SGP",
        "circuit": "Marina Bay Street Circuit",
        "round": 17,
        "gmtOffset": "+08:00",
        "sessions": [
            {
                "name": "Practice 1",
                "type": "Practice",
                "startDate": "2026-10-09T16:30:00",
                "endDate": "2026-10-09T17:30:00",
            },
            {
                "name": "Sprint Qualifying",
                "type": "Sprint Qualifying",
                "startDate": "2026-10-09T20:30:00",
                "endDate": "2026-10-09T21:14:00",
            },
            {
                "name": "Sprint",
                "type": "Sprint",
                "startDate": "2026-10-10T17:00:00",
                "endDate": "2026-10-10T17:30:00",
            },
            {
                "name": "Qualifying",
                "type": "Qualifying",
                "startDate": "2026-10-10T21:00:00",
                "endDate": "2026-10-10T22:00:00",
            },
            {
                "name": "Race",
                "type": "Race",
                "startDate": "2026-10-11T20:00:00",
                "endDate": "2026-10-11T22:00:00",
            },
        ],
    },
    {
        "meetingKey": 18,
        "name": "United States Grand Prix",
        "officialName": "FORMULA 1 MSC CRUISES UNITED STATES GRAND PRIX 2026",
        "location": "Austin",
        "country": "United States",
        "countryCode": "USA",
        "circuit": "Circuit of The Americas",
        "round": 18,
        "gmtOffset": "-05:00",
        "sessions": [
            {
                "name": "Practice 1",
                "type": "Practice",
                "startDate": "2026-10-23T12:30:00",
                "endDate": "2026-10-23T13:30:00",
            },
            {
                "name": "Practice 2",
                "type": "Practice",
                "startDate": "2026-10-23T16:00:00",
                "endDate": "2026-10-23T17:00:00",
            },
            {
                "name": "Practice 3",
                "type": "Practice",
                "startDate": "2026-10-24T12:30:00",
                "endDate": "2026-10-24T13:30:00",
            },
            {
                "name": "Qualifying",
                "type": "Qualifying",
                "startDate": "2026-10-24T16:00:00",
                "endDate": "2026-10-24T17:00:00",
            },
            {
                "name": "Race",
                "type": "Race",
                "startDate": "2026-10-25T15:00:00",
                "endDate": "2026-10-25T17:00:00",
            },
        ],
    },
    {
        "meetingKey": 19,
        "name": "Mexico City Grand Prix",
        "officialName": "FORMULA 1 GRAN PREMIO DE LA CIUDAD DE MÉXICO 2026",
        "location": "Mexico City",
        "country": "Mexico",
        "countryCode": "MEX",
        "circuit": "Autódromo Hermanos Rodríguez",
        "round": 19,
        "gmtOffset": "-06:00",
        "sessions": [
            {
                "name": "Practice 1",
                "type": "Practice",
                "startDate": "2026-10-30T12:30:00",
                "endDate": "2026-10-30T13:30:00",
            },
            {
                "name": "Practice 2",
                "type": "Practice",
                "startDate": "2026-10-30T16:00:00",
                "endDate": "2026-10-30T17:00:00",
            },
            {
                "name": "Practice 3",
                "type": "Practice",
                "startDate": "2026-10-31T11:30:00",
                "endDate": "2026-10-31T12:30:00",
            },
            {
                "name": "Qualifying",
                "type": "Qualifying",
                "startDate": "2026-10-31T15:00:00",
                "endDate": "2026-10-31T16:00:00",
            },
            {
                "name": "Race",
                "type": "Race",
                "startDate": "2026-11-01T14:00:00",
                "endDate": "2026-11-01T16:00:00",
            },
        ],
    },
    {
        "meetingKey": 20,
        "name": "São Paulo Grand Prix",
        "officialName": "FORMULA 1 MSC CRUISES GRANDE PRÊMIO DE SÃO PAULO 2026",
        "location": "São Paulo",
        "country": "Brazil",
        "countryCode": "BRA",
        "circuit": "Interlagos",
        "round": 20,
        "gmtOffset": "-03:00",
        "sessions": [
            {
                "name": "Practice 1",
                "type": "Practice",
                "startDate": "2026-11-06T12:30:00",
                "endDate": "2026-11-06T13:30:00",
            },
            {
                "name": "Sprint Qualifying",
                "type": "Sprint Qualifying",
                "startDate": "2026-11-06T16:00:00",
                "endDate": "2026-11-06T16:44:00",
            },
            {
                "name": "Sprint",
                "type": "Sprint",
                "startDate": "2026-11-07T11:30:00",
                "endDate": "2026-11-07T12:00:00",
            },
            {
                "name": "Qualifying",
                "type": "Qualifying",
                "startDate": "2026-11-07T15:00:00",
                "endDate": "2026-11-07T16:00:00",
            },
            {
                "name": "Race",
                "type": "Race",
                "startDate": "2026-11-08T14:00:00",
                "endDate": "2026-11-08T16:00:00",
            },
        ],
    },
    {
        "meetingKey": 21,
        "name": "Las Vegas Grand Prix",
        "officialName": "FORMULA 1 HEINEKEN LAS VEGAS GRAND PRIX 2026",
        "location": "Las Vegas",
        "country": "United States",
        "countryCode": "USA",
        "circuit": "Las Vegas Strip Circuit",
        "round": 21,
        "gmtOffset": "-08:00",
        "sessions": [
            {
                "name": "Practice 1",
                "type": "Practice",
                "startDate": "2026-11-19T16:30:00",
                "endDate": "2026-11-19T17:30:00",
            },
            {
                "name": "Practice 2",
                "type": "Practice",
                "startDate": "2026-11-19T20:00:00",
                "endDate": "2026-11-19T21:00:00",
            },
            {
                "name": "Practice 3",
                "type": "Practice",
                "startDate": "2026-11-20T16:30:00",
                "endDate": "2026-11-20T17:30:00",
            },
            {
                "name": "Qualifying",
                "type": "Qualifying",
                "startDate": "2026-11-20T20:00:00",
                "endDate": "2026-11-20T21:00:00",
            },
            {
                "name": "Race",
                "type": "Race",
                "startDate": "2026-11-21T20:00:00",
                "endDate": "2026-11-21T22:00:00",
            },
        ],
    },
    {
        "meetingKey": 22,
        "name": "Qatar Grand Prix",
        "officialName": "FORMULA 1 QATAR AIRWAYS QATAR GRAND PRIX 2026",
        "location": "Lusail",
        "country": "Qatar",
        "countryCode": "QAT",
        "circuit": "Lusail International Circuit",
        "round": 22,
        "gmtOffset": "+03:00",
        "sessions": [
            {
                "name": "Practice 1",
                "type": "Practice",
                "startDate": "2026-11-27T16:30:00",
                "endDate": "2026-11-27T17:30:00",
            },
            {
                "name": "Practice 2",
                "type": "Practice",
                "startDate": "2026-11-27T20:00:00",
                "endDate": "2026-11-27T21:00:00",
            },
            {
                "name": "Practice 3",
                "type": "Practice",
                "startDate": "2026-11-28T17:30:00",
                "endDate": "2026-11-28T18:30:00",
            },
            {
                "name": "Qualifying",
                "type": "Qualifying",
                "startDate": "2026-11-28T21:00:00",
                "endDate": "2026-11-28T22:00:00",
            },
            {
                "name": "Race",
                "type": "Race",
                "startDate": "2026-11-29T19:00:00",
                "endDate": "2026-11-29T21:00:00",
            },
        ],
    },
    {
        "meetingKey": 23,
        "name": "Abu Dhabi Grand Prix",
        "officialName": "FORMULA 1 ETIHAD AIRWAYS ABU DHABI GRAND PRIX 2026",
        "location": "Abu Dhabi",
        "country": "United Arab Emirates",
        "countryCode": "UAE",
        "circuit": "Yas Marina Circuit",
        "round": 23,
        "gmtOffset": "+04:00",
        "sessions": [
            {
                "name": "Practice 1",
                "type": "Practice",
                "startDate": "2026-12-04T13:30:00",
                "endDate": "2026-12-04T14:30:00",
            },
            {
                "name": "Practice 2",
                "type": "Practice",
                "startDate": "2026-12-04T17:00:00",
                "endDate": "2026-12-04T18:00:00",
            },
            {
                "name": "Practice 3",
                "type": "Practice",
                "startDate": "2026-12-05T14:30:00",
                "endDate": "2026-12-05T15:30:00",
            },
            {
                "name": "Qualifying",
                "type": "Qualifying",
                "startDate": "2026-12-05T18:00:00",
                "endDate": "2026-12-05T19:00:00",
            },
            {
                "name": "Race",
                "type": "Race",
                "startDate": "2026-12-06T17:00:00",
                "endDate": "2026-12-06T19:00:00",
            },
        ],
    },
]


def get_schedule() -> list[dict]:
    return SCHEDULE


def get_upcoming_schedule() -> list[dict]:
    now = datetime.now(timezone.utc)

    upcoming = []

    for meeting in SCHEDULE:
        future_sessions = []

        offset = meeting.get("gmtOffset", "+00:00")

        for session in meeting["sessions"]:
            start = datetime.fromisoformat(
                session["startDate"] + offset
            )

            if start >= now:
                future_sessions.append(session)

        if future_sessions:
            upcoming.append(
                {
                    **meeting,
                    "sessions": future_sessions,
                }
            )

    return upcoming
from datetime import datetime, timezone


def get_next_session():
    now = datetime.now(timezone.utc)

    upcoming = []

    for meeting in SCHEDULE:
        offset = meeting["gmtOffset"]

        for session in meeting["sessions"]:
            start = datetime.fromisoformat(
                session["startDate"] + offset
            )

            if start.astimezone(timezone.utc) > now:
                upcoming.append({
                    "meetingKey": meeting["meetingKey"],
                    "meetingName": meeting["name"],
                    "country": meeting["country"],
                    "countryCode": meeting["countryCode"],
                    "circuit": meeting["circuit"],
                    "session": session["name"],
                    "type": session["type"],
                    "startDate": start.isoformat(),
                    "endDate": datetime.fromisoformat(
                        session["endDate"] + offset
                    ).isoformat(),
                })

    upcoming.sort(key=lambda item: item["startDate"])

    return upcoming[0] if upcoming else None