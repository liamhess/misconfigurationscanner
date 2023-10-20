from fastapi import FastAPI
from typing import Dict
import json
import asyncio
import aiohttp
import mail

app = FastAPI()

async def check_port(ip, port):
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(ip, port), timeout=1)
        writer.close()
        await writer.wait_closed()
        return True
    except (asyncio.TimeoutError, OSError):
        return False

async def check_admin_interface(ip, port):
    async with aiohttp.ClientSession() as session:
        try:
            url = f"https://{ip}:{port}/login"
            async with session.get(url, timeout=1, ssl=False) as response:
                if response.status == 200:
                    return True
        except aiohttp.ClientError:
            pass
        return False

async def check_ip_and_port(ip, port):
    if await check_port(ip, port):
        print(f"Port {port} is open on {ip}")
        if port == 10000 and await check_admin_interface(ip, port):
            mail.send_email_alerts(ip, port)
        return {ip: port, "open": True}
    else:
        print(f"Port {port} is not open on {ip}")
        return {ip: port, "open": False}

@app.get("/start_scan")
async def start_scan():
    # Lists of IPs and ports to check
    with open('test.json', 'r') as file:
        data = json.load(file)
        ips = data['ips']
    ports = [80, 443, 22, 21, 10000]

    tasks = [check_ip_and_port(ip, port) for ip in ips for port in ports]
    results = await asyncio.gather(*tasks)
    return {"results": results}