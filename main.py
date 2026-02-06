import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import eth
import btc

app = FastAPI()

# Ensure Render finds the static folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=STATIC_DIR)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    address = data.get("address", "").strip()
    coin_type = data.get("coin_type", "eth")
    
    if coin_type == "btc":
        return btc.get_wallet_verdict(address)
    return eth.get_wallet_verdict(address)
