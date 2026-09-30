from __future__ import annotations

from copy import deepcopy
from threading import Lock


class F1State:
    def __init__(self):
        self._lock = Lock()

        self.session = {
            "name": None,
            "type": None,
            "status": None,
            "trackStatus": None,
            "lap": None,
            "totalLaps": None,
            "meetingKey": None,
            "meetingName": None,
            "officialName": None,
            "location": None,
            "country": None,
            "countryCode": None,
            "circuit": None,
            "sessionKey": None,
            "startDate": None,
            "endDate": None,
            "gmtOffset": None,
        }

        self.drivers = {}
        self.race_control = []

    def update(self, message: dict):
        if message.get("type") == 3:
            result = message.get("result", {})
            self._process_snapshot(result)
            return

        if message.get("type") != 1:
            return

        arguments = message.get("arguments", [])

        if len(arguments) < 2:
            return

        topic = arguments[0]
        data = arguments[1]

        self._process_topic(topic, data)

    def _process_snapshot(self, snapshot: dict):
        if "DriverList" in snapshot:
            self._process_driver_list(snapshot["DriverList"])

        if "SessionInfo" in snapshot:
            self._process_session_info(snapshot["SessionInfo"])
        
        if "SessionStatus" in snapshot:
            self._process_session_status(snapshot["SessionStatus"])

        if "TrackStatus" in snapshot:
            self._process_track_status(snapshot["TrackStatus"])

        if "LapCount" in snapshot:
            self._process_lap_count(snapshot["LapCount"])

        if "TimingData" in snapshot:
            self._process_timing_data(snapshot["TimingData"])

        if "TimingAppData" in snapshot:
            self._process_timing_app_data(
                snapshot["TimingAppData"]
            )

        if "RaceControlMessages" in snapshot:
            self._process_race_control(
                snapshot["RaceControlMessages"]
            )

    def _process_topic(self, topic: str, data):
        if topic == "DriverList":
            self._process_driver_list(data)

        elif topic == "SessionInfo":
            self._process_session_info(data)

        elif topic == "SessionStatus":
            self._process_session_status(data)

        elif topic == "LapCount":
            self._process_lap_count(data)

        elif topic == "TimingData":
            self._process_timing_data(data)

        elif topic == "TimingAppData":
            self._process_timing_app_data(data)
        
        elif topic == "TrackStatus":
            self._process_track_status(data)

        elif topic == "RaceControlMessages":
            self._process_race_control(data)

    def _process_driver_list(self, data: dict):
        with self._lock:
            for number, driver in data.items():
                if not str(number).isdigit():
                    continue

                self.drivers[number] = {
                    "number": int(number),
                    "abbreviation": driver.get("Tla"),
                    "name": driver.get("FullName"),
                    "team": driver.get("TeamName"),
                    "teamColour": driver.get("TeamColour"),
                    "position": None,
                    "gap": None,
                    "lastLap": None,
                    "bestLap": None,
                    "tyre": None,
                    "pit": None,
                    "pitStops": 0,
                    "sectors": [],
                }

    def _process_session_info(self, data: dict):
        with self._lock:
            meeting = data.get("Meeting", {})
            country = meeting.get("Country", {})
            circuit = meeting.get("Circuit", {})

            self.session["name"] = (
                meeting.get("Name")
                or data.get("MeetingName")
                or data.get("Name")
            )

            self.session["type"] = (
                data.get("Name")
                or data.get("Type")
            )

            self.session["meetingKey"] = meeting.get("Key")
            self.session["meetingName"] = meeting.get("Name")
            self.session["officialName"] = meeting.get("OfficialName")
            self.session["location"] = meeting.get("Location")

            self.session["country"] = country.get("Name")
            self.session["countryCode"] = country.get("Code")

            self.session["circuit"] = circuit.get("ShortName")

            self.session["sessionKey"] = data.get("Key")
            self.session["startDate"] = data.get("StartDate")
            self.session["endDate"] = data.get("EndDate")
            self.session["gmtOffset"] = data.get("GmtOffset")

    def _process_session_status(self, data: dict):
        with self._lock:
            self.session["status"] = (
                data.get("Status")
                or data.get("Message")
                or data.get("TrackStatus")
            )

    def _process_track_status(self, data: dict):
        status = (
            data.get("Status")
            or data.get("TrackStatus")
            or data.get("Message")
        )

        status_map = {
            "1": "AllClear",
            "2": "Yellow",
            "4": "SafetyCar",
            "5": "Red",
            "6": "VSCDeployed",
            "7": "VSCEnding",
        }

        status = status_map.get(str(status), status)

        with self._lock:
            self.session["trackStatus"] = status

    def _process_lap_count(self, data: dict):
        with self._lock:
            self.session["lap"] = self._number(
                data.get("CurrentLap")
            )

            self.session["totalLaps"] = self._number(
                data.get("TotalLaps")
            )

    def _process_timing_data(self, data: dict):
        lines = data.get("Lines", {})

        with self._lock:
            for number, timing in lines.items():
                if not str(number).isdigit():
                    continue

                if number not in self.drivers:
                    self.drivers[number] = {
                        "number": int(number),
                        "abbreviation": None,
                        "name": None,
                        "team": None,
                        "teamColour": None,
                        "position": None,
                        "gap": None,
                        "lastLap": None,
                        "bestLap": None,
                        "tyre": None,
                        "pit": None,
                        "pitStops": 0,
                        "sectors": [],
                    }

                driver = self.drivers[number]

                driver["position"] = self._number(
                    timing.get("Position")
                )

                if timing.get("InPit"):
                    driver["pit"] = "IN"
                elif timing.get("PitOut"):
                    driver["pit"] = "OUT"
                elif timing.get("Stopped"):
                    driver["pit"] = "STOPPED"
                else:
                    driver["pit"] = None

                driver["pitStops"] = (
                    self._number(timing.get("NumberOfPitStops"))
                    or 0
                )

                gap = (
                    timing.get("GapToLeader")
                    or timing.get("IntervalToPositionAhead")
                )

                if isinstance(gap, dict):
                    gap = gap.get("Value")

                driver["gap"] = gap or (
                    "Leader"
                    if driver["position"] == 1
                    else None
                )

                driver["lastLap"] = self._extract_lap_time(
                    timing.get("LastLapTime")
                )

                driver["bestLap"] = self._extract_lap_time(
                    timing.get("BestLapTime")
                )

                if any(
                    sector.get("OverallFastest")
                    for sector in timing.get("Sectors", [])
                    if isinstance(sector, dict)
                ):
                    print(
                        "OVERALL FASTEST SECTOR:",
                        timing.get("RacingNumber"),
                        timing.get("Sectors"),
                    )
                
                sectors = timing.get("Sectors", [])

                driver["sectors"] = [
                    {
                        "number": index + 1,
                        "time": self._extract_lap_time(sector),
                        "status": sector.get("Status"),
                        "personalFastest": sector.get(
                            "PersonalFastest",
                            False,
                        ),
                        "overallFastest": sector.get(
                            "OverallFastest",
                            False,
                        ),
                    }
                    for index, sector in enumerate(sectors)
                    if isinstance(sector, dict)
                ]

            # Calculate overall fastest sector times
            fastest_sector_times = [None, None, None]

            for current_driver in self.drivers.values():
                for index, sector in enumerate(
                    current_driver.get("sectors", [])
                ):
                    if index >= 3:
                        continue

                    value = sector.get("time")

                    if not value:
                        continue

                    try:
                        seconds = float(value)
                    except (TypeError, ValueError):
                        continue

                    current_fastest = fastest_sector_times[index]

                    if (
                        current_fastest is None
                        or seconds < current_fastest
                    ):
                        fastest_sector_times[index] = seconds

            # Mark the driver(s) with the overall fastest sector
            for current_driver in self.drivers.values():
                for index, sector in enumerate(
                    current_driver.get("sectors", [])
                ):
                    if index >= 3:
                        continue

                    value = sector.get("time")

                    if not value:
                        sector["overallFastest"] = False
                        continue

                    try:
                        seconds = float(value)
                    except (TypeError, ValueError):
                        sector["overallFastest"] = False
                        continue

                    sector["overallFastest"] = (
                        fastest_sector_times[index] is not None
                        and seconds == fastest_sector_times[index]
                    )

    def _process_timing_app_data(self, data: dict):
        lines = data.get("Lines", {})

        with self._lock:
            for number, timing in lines.items():
                if number not in self.drivers:
                    continue

                stints = timing.get("Stints", [])

                if not isinstance(stints, list) or not stints:
                    continue

                latest_stint = stints[-1]

                self.drivers[number]["tyre"] = (
                    latest_stint.get("Compound")
                )

    def _process_race_control(self, data: dict):
        messages = data.get("Messages", {})

        if isinstance(messages, dict):
            items = messages.items()

        elif isinstance(messages, list):
            items = enumerate(messages)

        else:
            return

        with self._lock:
            for message_id, message in items:
                if not isinstance(message, dict):
                    continue

                category = message.get("Category")
                text = message.get("Message")
                flag = message.get("Flag")
                status = message.get("Status")
                mode = message.get("Mode")

                severity = self._race_control_severity(
                    category=category,
                    message=text,
                    flag=flag,
                    status=status,
                    mode=mode,
                )

                item = {
                    "id": str(message_id),
                    "category": category,
                    "message": text,
                    "flag": flag,
                    "scope": message.get("Scope"),
                    "sector": message.get("Sector"),
                    "racingNumber": message.get(
                        "RacingNumber"
                    ),
                    "status": status,
                    "mode": mode,
                    "severity": severity,
                    "lap": self._number(
                        message.get("Lap")
                    ),
                    "timestamp": message.get("Utc"),
                }

                message_key = (
                    item["message"],
                    item["timestamp"],
                    item["lap"],
                    item["racingNumber"],
                )

                existing_index = next(
                    (
                        index
                        for index, existing in enumerate(
                            self.race_control
                        )
                        if (
                            existing.get("id") == item["id"]
                            or (
                                existing.get("message"),
                                existing.get("timestamp"),
                                existing.get("lap"),
                                existing.get("racingNumber"),
                            )
                            == message_key
                        )
                    ),
                    None,
                )

                if existing_index is not None:
                    self.race_control[
                        existing_index
                    ] = item
                else:
                    self.race_control.append(item)

            self.race_control = self.race_control[-100:]


    @staticmethod
    def _race_control_severity(
        category=None,
        message=None,
        flag=None,
        status=None,
        mode=None,
    ):
        category_text = str(category or "").lower()
        message_text = str(message or "").lower()
        flag_text = str(flag or "").lower()
        status_text = str(status or "").lower()
        mode_text = str(mode or "").lower()

        values = " ".join(
            [
                category_text,
                message_text,
                flag_text,
                status_text,
                mode_text,
            ]
        )
        # Session Complete / Finished
        if (
            flag_text in {"chequered", "checkered"}
            or "chequered flag" in message_text
            or "checkered flag" in message_text
        ):
            return "info"

        # Red flag / session stopped
        if (
            flag_text == "red"
            or "red flag" in values
            or "session stopped" in values
            or "race stopped" in values
        ):
            return "red"

        # Safety Car / Virtual Safety Car
        if any(
            keyword in values
            for keyword in [
                "safety car",
                "safetycar",
                "virtual safety car",
                "vsc deployed",
                "vsc ending",
            ]
        ):
            return "safety-car"

        # Yellow flags
        if (
            "yellow" in flag_text
            or "yellow flag" in values
            or "double yellow" in values
        ):
            return "yellow"

        # Blue flags
        if (
            "blue" in flag_text
            or "blue flag" in values
        ):
            return "blue"

        # Black flags
        if (
            "black" in flag_text
            or "black flag" in values
        ):
            return "red"

        # Penalties / steward activity
        if any(
            keyword in values
            for keyword in [
                "penalty",
                "penalised",
                "penalized",
                "investigation",
                "summoned",
                "decision",
                "stewards",
            ]
        ):
            return "penalty"

        # Track limits / deleted lap times
        if any(
            keyword in values
            for keyword in [
                "track limits",
                "time deleted",
                "lap deleted",
                "deleted -",
            ]
        ):
            return "track-limits"

        # DRS
        if "drs" in values:
            return "drs"

        # Track clear
        if any(
            keyword in values
            for keyword in [
                "track clear",
                "all clear",
                "allclear",
            ]
        ):
            return "clear"

        return "info"
    def snapshot(self) -> dict:
        with self._lock:
            drivers = list(self.drivers.values())

            drivers.sort(
                key=lambda driver: (
                    driver["position"]
                    if driver["position"] is not None
                    else 999
                )
            )

            return {
                "session": deepcopy(self.session),
                "drivers": deepcopy(drivers),
                "raceControl": deepcopy(self.race_control),
            }

    @staticmethod
    def _number(value):
        if value is None:
            return None

        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _extract_lap_time(value):
        if isinstance(value, dict):
            return (
                value.get("Value")
                or value.get("DisplayName")
            )

        return value