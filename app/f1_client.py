import asyncio
import json
import logging
import urllib.parse
from typing import Callable

import requests
from websockets.asyncio.client import connect

logger = logging.getLogger(__name__)

NEGOTIATE_URL = (
    "https://livetiming.formula1.com/signalrcore/negotiate"
)
CONNECTION_URL = (
    "wss://livetiming.formula1.com/signalrcore"
)

RECORD_SEPARATOR = "\x1e"

F1_TOPICS = [
    "Heartbeat",
    "DriverList",
    "ExtrapolatedClock",
    "RaceControlMessages",
    "SessionInfo",
    "SessionStatus",
    "TimingAppData",
    "TrackStatus",
    "WeatherData",
    "SessionData",
    "TimingData",
    "TopThree",
    "LapCount",
]


class F1LiveClient:
    def __init__(self, on_message: Callable[[dict], None]):
        self.on_message = on_message
        self._stop_event = asyncio.Event()

    def stop(self):
        self._stop_event.set()

    async def _negotiate(self):
        headers = {
            "User-agent": "BestHTTP",
            "Accept-Encoding": "gzip, identity",
        }

        session = requests.Session()

        # Get the AWS load-balancer cookie.
        options = session.options(
            NEGOTIATE_URL,
            headers=headers,
            timeout=15,
        )

        cookie = options.cookies.get("AWSALBCORS")

        if not cookie:
            raise RuntimeError(
                "AWSALBCORS cookie was not returned"
            )

        headers["Cookie"] = f"AWSALBCORS={cookie}"

        # Get the SignalR connection token.
        response = session.post(
            NEGOTIATE_URL,
            params={"negotiateVersion": "1"},
            headers=headers,
            timeout=15,
        )

        response.raise_for_status()

        token = response.json()["connectionToken"]

        return token, headers

    async def run(self):
        logger.info("Starting F1 live timing client")

        while not self._stop_event.is_set():
            try:
                await self._run_connection()

            except asyncio.CancelledError:
                raise

            except Exception:
                logger.exception(
                    "F1 connection failed"
                )

                if not self._stop_event.is_set():
                    logger.info(
                        "Reconnecting in 5 seconds..."
                    )
                    await asyncio.sleep(5)

    async def _run_connection(self):
        token, headers = await self._negotiate()

        url = (
            f"{CONNECTION_URL}?"
            f"{urllib.parse.urlencode({'id': token})}"
        )

        logger.info("Connecting to F1 SignalR")

        async with connect(
            url,
            additional_headers=headers,
            max_size=None,
        ) as websocket:

            logger.info("F1 WebSocket connected")

            # SignalR handshake
            await websocket.send(
                '{"protocol":"json","version":1}'
                + RECORD_SEPARATOR
            )

            handshake = await websocket.recv()

            logger.debug(
                "SignalR handshake response: %s",
                handshake,
            )

            # Subscribe
            await websocket.send(
                json.dumps(
                    {
                        "type": 1,
                        "invocationId": "0",
                        "target": "Subscribe",
                        "arguments": [F1_TOPICS],
                    }
                )
                + RECORD_SEPARATOR
            )

            logger.info(
                "Subscribed to %d F1 topics",
                len(F1_TOPICS),
            )

            while not self._stop_event.is_set():
                message = await websocket.recv()
                logger.info("Received F1 WebSocket frame")
                await self._process_message(message)

    async def _process_message(self, message):
        if not message:
            return

        # SignalR uses ASCII record separator between messages.
        messages = message.split(RECORD_SEPARATOR)

        for raw in messages:
            if not raw:
                continue

            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                logger.warning(
                    "Could not decode F1 message: %s",
                    raw[:500],
                )
                continue

            message_type = data.get("type")

            # 6 = SignalR keepalive ping
            if message_type == 6:
                logger.debug("F1 heartbeat")
                continue

            logger.info(
                "F1 message type=%s",
                message_type,
            )

            self.on_message(data)