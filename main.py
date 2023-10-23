from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, HTTPException, Depends
from fastapi.openapi.utils import get_openapi
from typing import Dict
import json
import asyncio
import aiohttp
import mail
from secrets import compare_digest
from decouple import config

app = FastAPI(docs_url='/')

security = HTTPBasic()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Misconfiguration Scanner",
        version="1.0.0",
        description="This is the API for the Misconfiguration Scanner",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


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
        # mail.send_email_alerts(ip, port)
        return {ip: port, "open": True}
    else:
        print(f"Port {port} is not open on {ip}")
        return {ip: port, "open": False}

def authenticate_user(credentials: HTTPBasicCredentials):
    username = config('API_USERNAME')
    password = config('API_PASSWORD')
    correct_username = compare_digest(credentials.username, username)
    correct_password = compare_digest(credentials.password, password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )
    return credentials.username

@app.get("/start_scan")
async def start_scan(credentials: HTTPBasicCredentials = Depends(security)):
    authenticate_user(credentials)
    # Lists of IPs and ports to check
    with open('ips.json', 'r') as file:
        data = json.load(file)
        ips = data['ips']
    ports = [80, 443, 22, 21, 10000, 2195, 2196, 25, 514, 5223, 541, 853, 8888, 8890, 9582, 53]

    tasks = [check_ip_and_port(ip, port) for ip in ips for port in ports]
    results = await asyncio.gather(*tasks)
    return {"results": results}