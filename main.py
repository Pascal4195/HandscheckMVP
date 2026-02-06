from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from eth import get_eth_transactions
from btc import get_btc_transactions
from verdict import get_verdict

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/check/{coin}/{address}")
async def check_wallet(coin: str, address: str):
    if coin.lower() == "eth":
        txs = get_eth_transactions(address)
    else:
        txs = get_btc_transactions(address)
    
    label, desc, color = get_verdict(txs)
    
    return {
        "verdict": label,
        "details": desc,
        "color": color
    }
