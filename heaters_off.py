#!/usr/bin/env python3
import aiohttp
import asyncio
import pysmartthings

tokenfile=open("token")
token = tokenfile.read().strip()

async def print_devices():
    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, token)
        devices = await api.devices()
        for device in devices:
            if "heater" in device.label:
                await device.switch_off()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_devices())
    loop.close()

if __name__ == '__main__':
    main()

