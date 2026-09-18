from __future__ import annotations

from pydantic import BaseModel, Field


class Session(BaseModel):
    name: str | None = None
    type: str | None = None
    status: str | None = None
    trackStatus: str | None = None
    lap: int | None = None
    totalLaps: int | None = None

    meetingKey: int | None = None
    meetingName: str | None = None
    officialName: str | None = None
    location: str | None = None
    country: str | None = None
    countryCode: str | None = None
    circuit: str | None = None
    sessionKey: int | None = None
    startDate: str | None = None
    endDate: str | None = None
    gmtOffset: str | None = None

class ScheduleSession(BaseModel):
    name: str
    type: str
    startDate: str
    endDate: str


class ScheduleMeeting(BaseModel):
    meetingKey: int
    name: str
    officialName: str | None = None
    location: str | None = None
    country: str | None = None
    countryCode: str | None = None
    round: int | None = None
    gmtOffset: str | None = None
    circuit: str | None = None
    sessions: list[ScheduleSession] = Field(
        default_factory=list
    )


class Sector(BaseModel):
    number: int
    time: str | None = None
    status: int | str | None = None
    personalFastest: bool = False
    overallFastest: bool = False


class Driver(BaseModel):
    number: int
    abbreviation: str | None = None
    name: str | None = None
    team: str | None = None
    teamColour: str | None = None
    position: int | None = None
    gap: str | None = None
    lastLap: str | None = None
    bestLap: str | None = None
    tyre: str | None = None
    pit: str | None = None
    pitStops: int = 0
    sectors: list[Sector] = Field(default_factory=list)


class RaceControlMessage(BaseModel):
    id: str
    category: str | None = None
    message: str | None = None
    flag: str | None = None
    scope: str | None = None
    sector: int | None = None
    racingNumber: str | int | None = None
    status: str | None = None
    mode: str | None = None
    lap: int | None = None
    timestamp: str | None = None


class F1Snapshot(BaseModel):
    session: Session
    drivers: list[Driver] = Field(default_factory=list)
    raceControl: list[RaceControlMessage] = Field(
        default_factory=list
    )

class ScheduleResponse(BaseModel):
    meetings: list[ScheduleMeeting] = Field(
        default_factory=list
    )