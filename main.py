import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# Import both logic files
import eth
import btc 

app = FastAPI()

# FIX: Absolute paths for Render
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
    address = data.get("address")
    
    # Logic to detect if it's a BTC address or ETH address
    # Simple check: BTC addresses often start with '1', '3', or 'bc1'
    if address.startswith("0x"):
        result = eth.get_wallet_verdict(address)
    else:
        result = btc.get_wallet_verdict(address)
        
    return result
