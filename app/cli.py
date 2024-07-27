import asyncio
import logging
import internal.status

logging.basicConfig(level=logging.INFO)


async def ainput(prompt: str = ""):
    return await asyncio.to_thread(input, prompt)


async def process():
    while True:
        line = await ainput()
        if line == "reset":
            for charger in internal.status.get_all():
                logging.debug(f"Request reset {charger.ws.remote_address}")
                await charger.cp.request_reset()
        elif line == "info":
            internal.status.info()
        elif line == "dall":
            internal.status.delete_all()
        elif line == "disconnect all":
            for charger in internal.status.get_all():
                logging.debug(f"Closing {charger.ws.remote_address}")
                await charger.ws.close()
        elif line == "keco":
            for charger in internal.status.get_all():
                await charger.cp.request_keco(vendor_id="kr.or.keco",
                                              message_id="BatteryInfoConfiguration",
                                              data="{\"configCnt\":\"1\"}")
