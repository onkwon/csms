import time
from dataclasses import dataclass
from internal.ocpp_v16 import ChargePoint16
import websockets


@dataclass
class Charger:
    cp: ChargePoint16
    ws: websockets.WebSocketServerProtocol
    time_registered: time
