from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
from typing import Dict
from typing import List
import json
import asyncio
import aiohttp
import mail
from secrets import compare_digest
from decouple import config

app = FastAPI(docs_url='/')

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows CORS for all get, post, etc. requests from the origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

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

with open('ips.json', 'r') as file:
    data = json.load(file)
    ips = data['ips']
with open('ports.json', 'r') as file:
    data = json.load(file)
    ports = data['ports']

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
        # mail.send_email_alerts(ip, port)
        return {ip: port, "open": True}
    else:
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

@app.get("/get_ports",
    tags=["Getting Data"],
    summary="Getting a JSON of all open ports for all IPs",
    description="This endpoint checks the given IPs and ports and returns the results.",
    response_description="JSON of open and closed ports")
async def get_ports(credentials: HTTPBasicCredentials = Depends(security)):
    authenticate_user(credentials)

    tasks = [check_ip_and_port(ip, port) for ip in ips for port in ports]
    results = await asyncio.gather(*tasks)
    return {"results": results}

@app.post("/send_email",
    tags=["Notifying"],
    summary="Notify user via E-Mail",
    description="This endpoint sends an E-Mail to the user with all open and closed ports for all IPs that are declared",
    response_description="Status of the E-Mail sending")
def send_email(credentials: HTTPBasicCredentials = Depends(security)):
    authenticate_user(credentials)
    try:
        success = mail.send_email_alerts(ips, ports)
        if not success:
            raise HTTPException(status_code=400, detail="Email sending failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Email sent successfully"}


