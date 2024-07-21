import websockets
import time
import logging
from internal.ocpp_v16 import ChargePoint16
from internal.model import Charger

chargers = []


def register(cp: ChargePoint16, ws: websockets.WebSocketServerProtocol):
    item = Charger(cp, ws, time.time())
    chargers.append(item)


def unregister(cp: ChargePoint16):
    for charger in chargers:
        if charger.cp == cp:
            chargers.remove(charger)
            return


def get_by_cp(cp: ChargePoint16):
    for charger in chargers:
        if charger.cp == cp:
            return charger
    return None


def get_all():
    return chargers


def info():
    for charger in chargers:
        logging.info(charger.ws.local_address)
        logging.info(charger.ws.remote_address)
        logging.info(charger.ws.open)
        logging.info(charger.ws.closed)
        logging.info(charger.ws.close_code)
        logging.info(charger.ws.close_reason)


def delete_all():
    for charger in chargers:
        logging.debug(f"Delete {charger}")
        del charger
