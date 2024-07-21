import asyncio
import logging
import websockets
import internal.status
from internal.ocpp_v16 import ChargePoint16
from app import cli


async def on_connect(websocket, path):
    try:
        requested_protocols = \
            websocket.request_headers["Sec-WebSocket-Protocol"]
    except KeyError:
        logging.error("Client hasn't requested any Subprotocol."
                      " Closing Connection")
        return await websocket.close()
    if websocket.subprotocol:
        logging.info("Protocols Matched: %s", websocket.subprotocol)
    else:
        logging.warning(
            "Protocols Mismatched | Expected Subprotocols: %s,"
            " but client supports  %s | Closing connection",
            websocket.available_subprotocols,
            requested_protocols,
        )
        return await websocket.close()

    if (websocket.subprotocol == "ocpp1.6"):
        charge_point_id = path.strip("/")
        logging.info(f"{charge_point_id} connected using OCPP1.6")
        cp = ChargePoint16(charge_point_id, websocket)
    else:
        """TODO: Support OCPP2.0.1"""
        return

    logging.debug(websocket.local_address)
    logging.debug(websocket.remote_address)

    if cp:
        internal.status.register(cp, websocket)
        await cp.start()


async def run_server():
    server = await websockets.serve(
        on_connect, "0.0.0.0", 9000, subprotocols=["ocpp1.6", "ocpp2.0.1"],
        ping_interval=None
    )

    logging.info("Server Started listening to new connections.")
    await server.wait_closed()


async def main():
    logging.getLogger().setLevel(logging.DEBUG)
    tasks = [run_server(), cli.process()]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
